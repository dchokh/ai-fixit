import io
import json
import os
import re
from dataclasses import dataclass

import numpy as np
from meta_sam_parser import SegmentationMask, decode_mask_to_raster
from PIL import Image, ImageDraw, ImageOps
import requests
from werkzeug.datastructures import FileStorage

from ai_models.meta.meta_model import MetaModel

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MODEL_API_KEY")

API_BASE = "https://api.meta.ai/v1"
PALETTE = [(255, 59, 48), (0, 122, 255), (52, 199, 89), (255, 204, 0), (175, 82, 222)]

# <id><|box;x1=..;y1=..;x2=..;y2=..;w=..;h=..|><|mask;x=..;y=..;data=H,W,payload|>
RECORD_RE = re.compile(
    r"(?P<id>\d+)<\|box;x1=(?P<x1>-?[\d.]+);y1=(?P<y1>-?[\d.]+);"
    r"x2=(?P<x2>-?[\d.]+);y2=(?P<y2>-?[\d.]+);w=(?P<w>\d+);h=(?P<h>\d+)\|>"
    r"<\|mask;x=(?P<mx>\d+);y=(?P<my>\d+);data=(?P<mh>\d+),(?P<mw>\d+),(?P<payload>.*?)\|>",
    re.S,
)


@dataclass
class SamObject:
    object_id: str
    box: tuple[float, float, float, float]  # x1, y1, x2, y2 in image pixels
    mask: np.ndarray  # bool array, same size as the image


@dataclass
class SamResult:
    image_png: bytes  # original image with masks and boxes drawn on it
    objects: list[SamObject]
    raw_text: str  # raw model output, useful for debugging


class Sam(MetaModel):
    ''' Sam 3.1 model wrapper '''

    def __init__(self, photo: FileStorage):
        # Normalize once so the uploaded image and the overlay use identical pixels
        # (EXIF rotation applied, RGB only).
        super().__init__(photo)
        raw = photo.read()
        self.image = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def ask(self, prompt: str) -> SamResult:
        file_id = self._upload()
        text = self._segment(file_id, prompt)
        objects = self._parse(text)
        return SamResult(self._render(objects), objects, text)

    def _upload(self) -> str:
        buf = io.BytesIO()
        self.image.save(buf, "JPEG", quality=95)
        resp = requests.post(
            f"{API_BASE}/files",
            headers=self.headers,
            data={"purpose": "user_data"},
            files={"file": ("upload.jpg", buf.getvalue(), "image/jpeg")},
            timeout=60,
        )
        resp.raise_for_status()
        file_id = resp.json().get("id")
        if not isinstance(file_id, str) or not file_id:
            raise RuntimeError("File upload completed without a file id.")
        return file_id

    def _segment(self, file_id: str, prompt: str) -> str:
        payload = {
            "model": "sam-3.1",
            "input": [{
                "type": "message",
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "file_id": file_id},
                ],
            }],
            "stream": True,
            "metadata": {"mask_encoding": "lossless"},
        }
        deltas, final = [], None
        with requests.post(
                f"{API_BASE}/responses",
                headers={**self.headers, "Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json",
                         "Accept": "text/event-stream"},
                json=payload,
                stream=True,
                timeout=120,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line.startswith(b"data: "):
                    continue
                data = line[6:].decode("utf-8", errors="replace")
                if data == "[DONE]":
                    break
                event = json.loads(data)
                etype = event.get("type", "")
                if etype == "response.output_text.delta":
                    deltas.append(event.get("delta", ""))
                elif etype == "response.output_text.done":
                    final = event.get("text")
                elif etype in ("response.failed", "error"):
                    raise RuntimeError(f"SAM request failed: {event}")
        return final if final is not None else "".join(deltas)

    def _parse(self, text: str) -> list[SamObject]:
        W, H = self.image.size
        objects = []
        for m in RECORD_RE.finditer(text):
            mw, mh = int(m["mw"]), int(m["mh"])
            payload = m["payload"]
            encoding = "lossless" if payload.startswith("~") else "one_bit"
            raster = decode_mask_to_raster(
                SegmentationMask(encoding=encoding, payload=payload, width=mw, height=mh)
            )
            small = Image.fromarray(
                np.frombuffer(raster, dtype=np.uint8).reshape(mh, mw) * 255, mode="L"
            )
            mx, my = int(m["mx"]), int(m["my"])
            if (mw, mh) != (W, H) and mx == 0 and my == 0:
                full = small.resize((W, H), Image.NEAREST)  # mask covers whole frame
            else:
                full = Image.new("L", (W, H), 0)
                full.paste(small, (mx, my))  # mask is a placed crop

            sx, sy = W / int(m["w"]), H / int(m["h"])  # box frame size -> image size
            box = (float(m["x1"]) * sx, float(m["y1"]) * sy,
                   float(m["x2"]) * sx, float(m["y2"]) * sy)
            objects.append(SamObject(m["id"], box, np.array(full) > 127))
        return objects

    def _render(self, objects: list[SamObject]) -> bytes:
        image = self.image.copy()
        for i, obj in enumerate(objects):
            color = PALETTE[i % len(PALETTE)]
            mask = Image.fromarray(obj.mask.astype(np.uint8) * 255, mode="L")
            tint = Image.blend(image, Image.new("RGB", image.size, color), 0.5)
            image = Image.composite(tint, image, mask)
            draw = ImageDraw.Draw(image)
            draw.rectangle(obj.box, outline=color, width=3)
            draw.text((obj.box[0] + 4, obj.box[1] + 4), f"#{obj.object_id}", fill=color)
        out = io.BytesIO()
        image.save(out, "PNG")
        return out.getvalue()
