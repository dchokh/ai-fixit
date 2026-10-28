import base64
from werkzeug.datastructures import FileStorage

from ai_models.meta.sam import Sam
from views.icons import ICONS
from views.html_templates import BASE, HOME
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB upload limit
ALLOWED = {"jpg", "jpeg", "png"}


def render(active, content):
    body = render_template_string(content, icons=ICONS)
    return render_template_string(BASE, icons=ICONS, active=active, content=body)


def placeholder(title):
    return (
        f'<div class="simple"><h2>{title}</h2>'
        "<p>This section is coming soon.</p></div>"
    )


@app.route("/")
def home():
    return render("home", HOME)


@app.route("/repairs")
def repairs():
    return render("repairs", placeholder("My Repairs"))


@app.route("/favorites")
def favorites():
    return render("favorites", placeholder("Favorites"))


@app.route("/settings")
def settings():
    return render("settings", placeholder("Settings"))


@app.route("/api/analyze", methods=["POST"])
def analyze():
    photo: FileStorage | None = request.files.get("photo")
    if not photo or not photo.filename:
        return jsonify(error="No file uploaded."), 400
    ext = photo.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED:
        return jsonify(error="Only JPG and PNG files are supported."), 400

    result = Sam(photo).ask("Broken hinge")

    return jsonify(
        image="data:image/png;base64," + base64.b64encode(result.image_png).decode(),
        objects=[{"id": o.object_id, "box": o.box, "pixels": int(o.mask.sum())}
                 for o in result.objects],
    )

    # TODO: send photo.read() to AI model and return its diagnosis + steps.
    return jsonify(
        title="Photo received",
        message="Connect your AI backend in the /api/analyze route to identify the issue "
                "and generate step-by-step repair instructions.",
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify(error="File is larger than 10MB."), 413


if __name__ == "__main__":
    app.run(debug=True)
