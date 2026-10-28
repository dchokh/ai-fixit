BASE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FixIt - See the problem. Get the solution.</title>
<style>
  :root {
    --blue: #1a56f0; --blue-soft: #e8f0ff; --ink: #111827; --muted: #6b7280;
    --text: #4b5563; --line: #e8ecf3; --panel: #f4f7fd;
  }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: Inter, "Segoe UI", system-ui, sans-serif; color: var(--ink); background: #fff; }

  /* Top header */
  .topbar { position: fixed; inset: 0 0 auto 0; height: 72px; background: #fff; z-index: 20;
            border-bottom: 1px solid var(--line); display: flex; align-items: center; padding: 0 32px; }
  .logo { display: flex; align-items: center; gap: 10px; font-size: 26px; font-weight: 800; color: var(--ink); }
  .logo svg { color: var(--blue); }
  .tagline { margin-left: 22px; padding-left: 22px; border-left: 1px solid #d9dee8; color: var(--text); font-size: 14px; }

  /* Sidebar */
  .sidebar { position: fixed; top: 72px; bottom: 0; left: 0; width: 220px; background: #fff;
             border-right: 1px solid var(--line); padding: 20px 16px; }
  .sidebar a { display: flex; align-items: center; gap: 14px; padding: 11px 14px; margin-bottom: 8px;
               border-radius: 10px; color: #374151; text-decoration: none; font-size: 15px; font-weight: 500; }
  .sidebar a:hover { background: #f3f6fc; }
  .sidebar a.active { background: var(--blue-soft); color: var(--blue); font-weight: 600; }

  /* Main */
  main { margin: 72px 0 0 220px; padding: 32px 32px 0; background: #fbfcff; min-height: calc(100vh - 72px); }
  .hero { display: grid; grid-template-columns: 1fr 1.15fr; gap: 40px; align-items: center;
          background: #f6f9ff; border-radius: 18px; padding: 32px 36px; }
  .pill { display: inline-flex; align-items: center; gap: 8px; background: var(--blue-soft); color: var(--blue);
          font-size: 13px; padding: 7px 14px; border-radius: 999px; margin-bottom: 18px; }
  h1 { font-size: 46px; line-height: 1.1; margin: 0 0 18px; font-weight: 800; letter-spacing: -.5px; }
  .lead { font-size: 18px; color: var(--text); line-height: 1.6; max-width: 500px; margin: 0 0 26px; }
  .btn-row { display: flex; gap: 16px; }
  .btn { display: inline-flex; align-items: center; gap: 10px; padding: 15px 26px; border-radius: 12px;
         font-size: 16px; font-weight: 600; cursor: pointer; border: 1px solid transparent; font-family: inherit; }
  .btn.primary { background: var(--blue); color: #fff; box-shadow: 0 6px 16px rgba(26,86,240,.3); }
  .btn.ghost { background: #fff; color: #1f2937; border-color: var(--line); }
  .btn.ghost svg { color: var(--blue); }
  .hint { color: var(--muted); font-size: 13px; margin-top: 14px; }

  /* Demo visual */
  .demo { position: relative; height: 340px; }
  .demo .photo { position: absolute; inset: 0 110px 0 0; border-radius: 14px; overflow: hidden;
                 background: linear-gradient(90deg, #cdb08a 0%, #e9dcc6 48%, #f1ebe0 52%, #d6bb94 100%); }
  .demo .photo::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 22%;
                        background: linear-gradient(#c58a45, #9b6a33); }
  .hinge { position: absolute; left: 50px; top: 100px; width: 140px; height: 160px; border: 2px solid var(--blue);
           background: rgba(255,255,255,.25); border-radius: 4px; display: flex; align-items: center; justify-content: center; }
  .hinge i { width: 80px; height: 100px; border-radius: 12px; background: linear-gradient(135deg,#f3f4f6,#9ca3af);
             box-shadow: 0 6px 14px rgba(0,0,0,.25); }
  .chip { position: absolute; left: 105px; top: 55px; background: var(--blue); color: #fff; font-size: 12px;
          font-weight: 600; padding: 7px 13px; border-radius: 10px; }
  .card { position: absolute; right: 0; top: 22px; width: 285px; background: #fff; border-radius: 16px;
          padding: 18px 20px; box-shadow: 0 14px 34px rgba(20,40,90,.16); }
  .card h4 { margin: 0 0 8px; font-size: 16px; display: flex; align-items: center; gap: 8px; }
  .card .desc { font-size: 13px; color: var(--muted); line-height: 1.5; padding-bottom: 14px; border-bottom: 1px solid #eef0f4; }
  .card .st { font-weight: 700; font-size: 14px; margin: 14px 0 10px; }
  .step { display: flex; gap: 10px; align-items: flex-start; font-size: 13px; color: #374151; margin-bottom: 10px; }
  .num { width: 20px; height: 20px; border-radius: 50%; background: var(--blue); color: #fff; font-size: 11px;
         font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .after { display: flex; align-items: center; gap: 10px; background: #f5f7fb; border-radius: 10px; padding: 8px 10px;
           font-size: 13px; margin-top: 4px; }
  .after .thumb { width: 44px; height: 34px; border-radius: 6px; background: linear-gradient(135deg,#d9c3a0,#b99567); }
  .after .ok { display: flex; align-items: center; gap: 6px; flex: 1; }

  /* Result panel (upload / demo) */
  #result { display: none; margin-top: 24px; background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 20px;
            grid-template-columns: 240px 1fr; gap: 24px; }
  #result.show { display: grid; }
  #result img { width: 100%; border-radius: 10px; object-fit: cover; }

  /* How it works */
  .how { margin-top: 28px; background: var(--panel); border-radius: 18px; padding: 26px 28px 30px; }
  .how h2 { margin: 0; font-size: 26px; }
  .how .sub { color: var(--text); margin: 6px 0 22px; }
  .steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 34px; }
  .scard { position: relative; background: #fff; border-radius: 14px; padding: 12px 12px 18px; }
  .scard:not(:last-child)::after { content: "\\2192"; position: absolute; right: -28px; top: 36%; color: #7ea2f8; font-size: 22px; }
  .simg { height: 128px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; position: relative; overflow: hidden; }
  .s1 { background: radial-gradient(circle at 50% 55%, #3a3a3a 0 28%, #1f1f1f 29% 55%, #4b4b4b 56%); }
  .s1::after { content: ""; position: absolute; width: 90px; height: 90px; border: 2px solid #f97362; background: rgba(249,115,98,.15); }
  .s2 { background: radial-gradient(circle at 50% 55%, #2a2a2a 0 55%, #4b4b4b 56%); }
  .s2 i { width: 70px; height: 70px; border-radius: 50%; background: #2f6bff; box-shadow: 0 0 22px #2f6bff; }
  .s3 { background: #f9fafb; border: 1px solid #eef0f4; color: #374151; }
  .s3 ol { margin: 0; padding-left: 16px; font-size: 10px; line-height: 1.9; color: #6b7280; }
  .s4 { background: radial-gradient(circle at 50% 55%, #3a3a3a 0 28%, #1f1f1f 29% 55%, #4b4b4b 56%); }
  .s4 .tick { position: absolute; top: 8px; right: 8px; width: 24px; height: 24px; border-radius: 50%; background: #16a34a;
              color: #fff; display: flex; align-items: center; justify-content: center; font-size: 14px; }
  .shead { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 16px; margin-bottom: 8px; }
  .shead .num { width: 26px; height: 26px; font-size: 13px; }
  .scard p { margin: 0 0 0 36px; font-size: 14px; color: var(--muted); line-height: 1.55; }

  /* Footer features */
  .feats { display: grid; grid-template-columns: repeat(4, 1fr); margin: 26px -32px 0; padding: 22px 32px 26px;
           border-top: 1px solid var(--line); background: #fff; }
  .feat { display: flex; gap: 14px; align-items: flex-start; padding: 0 20px; }
  .feat:not(:last-child) { border-right: 1px solid var(--line); }
  .feat .ic { color: var(--blue); }
  .feat .ic.green { color: #16a34a; }
  .feat b { font-size: 14px; display: block; margin-bottom: 4px; }
  .feat span { font-size: 12px; color: var(--muted); }

  .simple { padding: 60px 0; text-align: center; color: var(--text); }
  .simple h2 { color: var(--ink); }

  @media (max-width: 1100px) {
    .hero { grid-template-columns: 1fr; } .steps, .feats { grid-template-columns: 1fr 1fr; }
    .scard::after { display: none; }
  }
  @media (max-width: 800px) { .sidebar { display: none; } main { margin-left: 0; } .tagline { display: none; } }
</style>
</head>
<body>
  <header class="topbar">
    <div class="logo">{{ icons.wrench|safe }} FixIt</div>
    <div class="tagline">See the problem. Get the solution.</div>
  </header>

  <nav class="sidebar">
    <a href="/" class="{{ 'active' if active == 'home' }}">{{ icons.home|safe }} Home</a>
    <a href="/repairs" class="{{ 'active' if active == 'repairs' }}">{{ icons.clock|safe }} My Repairs</a>
    <a href="/favorites" class="{{ 'active' if active == 'favorites' }}">{{ icons.heart|safe }} Favorites</a>
    <a href="/settings" class="{{ 'active' if active == 'settings' }}">{{ icons.gear|safe }} Settings</a>
  </nav>

  <main>{{ content|safe }}</main>
</body>
</html>
"""

HOME = """
<section class="hero">
  <div>
    <div class="pill">{{ icons.sparkle_sm|safe }} AI-Powered Repair Assistant</div>
    <h1>Turn everyday problems<br>into easy fixes</h1>
    <p class="lead">Upload a photo of something broken or damaged, and let our AI identify the issue,
       show you what to do, and guide you step by step with clear visuals.</p>
    <div class="btn-row">
      <button class="btn primary" id="uploadBtn">{{ icons.camera|safe }} Upload a Photo</button>
      <button class="btn ghost" id="demoBtn">{{ icons.play|safe }} Try a Demo</button>
    </div>
    <input type="file" id="fileInput" accept=".jpg,.jpeg,.png" hidden>
    <div class="hint">JPG, PNG up to 10MB</div>
  </div>

  <div class="demo">
    <div class="photo">
      <div class="chip">Identified: Cabinet hinge</div>
      <div class="hinge"><i></i></div>
    </div>
    <div class="card">
      <h4>{{ icons.warn|safe }} Loose cabinet hinge</h4>
      <div class="desc">The hinge appears to be loose, which can cause the door to sag or not close properly.</div>
      <div class="st">Steps to fix:</div>
      <div class="step"><div class="num">1</div><div>Tighten the hinge screws<br>(top and bottom)</div></div>
      <div class="step"><div class="num">2</div><div>Check for stripped screw holes</div></div>
      <div class="step"><div class="num">3</div><div>Test the door movement</div></div>
      <div class="after"><div class="thumb"></div><div class="ok">{{ icons.check|safe }} After repair</div>{{ icons.chev|safe }}</div>
    </div>
  </div>
</section>

<section id="result">
  <div>
    <h3 id="original_photo" style="margin-top:0; text-align:center">Original photo</h3>
    <p id="resultText" style="color:#4b5563;line-height:1.6"></p>
    <img id="preview" alt="Your photo">
  </div>
  <div style="width:240px;">
    <h3 id="resultTitle" style="margin-top:0; text-align:center"></h3>
    <p id="resultText" style="color:#4b5563;line-height:1.6"></p>
    <img id="detected_hinge" alt="Result"></img>
  </div>
</section>

<section class="how">
  <h2>How It Works</h2>
  <p class="sub">From a simple photo to a clear repair plan — in just a few steps.</p>
  <div class="steps">
    <div class="scard"><div class="simg s1"></div>
      <div class="shead"><div class="num">1</div>Upload Your Photo</div>
      <p>Take or upload a photo of the broken or damaged item.</p></div>
    <div class="scard"><div class="simg s2"><i></i></div>
      <div class="shead"><div class="num">2</div>AI Identifies the Issue</div>
      <p>Our AI analyzes the image, segments the relevant parts, and explains what's wrong.</p></div>
    <div class="scard"><div class="simg s3"><ol><li>Remove the old derailleur</li><li>Install the new one</li><li>Adjust the gears</li><li>Test the shifting</li></ol></div>
      <div class="shead"><div class="num">3</div>Get Step-by-Step Instructions</div>
      <p>See clear, easy-to-follow steps with visual guidance.</p></div>
    <div class="scard"><div class="simg s4"><div class="tick">✓</div></div>
      <div class="shead"><div class="num">4</div>See the Result</div>
      <p>Get a visual of the final result and tips to keep it in good shape.</p></div>
  </div>
</section>

<section class="feats">
  <div class="feat"><div class="ic">{{ icons.sparkle|safe }}</div><div><b>Powered by Meta AI</b><span>Uses Muse Spark, SAM 3.1 and Muse Image</span></div></div>
  <div class="feat"><div class="ic green">{{ icons.shield|safe }}</div><div><b>Trusted Guidance</b><span>Clear, step-by-step instructions</span></div></div>
  <div class="feat"><div class="ic">{{ icons.bolt|safe }}</div><div><b>Save Time &amp; Money</b><span>Fix it yourself, whenever you want</span></div></div>
  <div class="feat"><div class="ic green">{{ icons.leaf|safe }}</div><div><b>More Sustainable</b><span>Keep items in use, reduce waste</span></div></div>
</section>

<script>
  const fileInput = document.getElementById("fileInput");
  const result = document.getElementById("result");
  const preview = document.getElementById("preview");
  const title = document.getElementById("resultTitle");
  const text = document.getElementById("resultText");

  document.getElementById("uploadBtn").onclick = () => fileInput.click();

  document.getElementById("demoBtn").onclick = () => {
    preview.style.display = "none";
    title.textContent = "Demo: Loose cabinet hinge";
    text.textContent = "Tighten the hinge screws (top and bottom), check for stripped screw holes, then test the door movement.";
    result.classList.add("show");
    result.style.gridTemplateColumns = "1fr";
  };

  fileInput.onchange = async () => {
    const file = fileInput.files[0];
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { alert("File is larger than 10MB."); return; }
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
    result.style.gridTemplateColumns = "240px 1fr";
    title.textContent = "Analyzing...";
    text.textContent = "";
    result.classList.add("show");

    const fd = new FormData();
    fd.append("photo", file);
    try {
    
      const data = await (await fetch("/api/analyze", {method: "POST", body: fd})).json();
      document.getElementById("detected_hinge").src = data.image;
  
      title.textContent = data.title || "Detected hinge";
      text.textContent = data.message || data.error;
    } catch (e) {
      console.log(e);
      title.textContent = "Error";
      text.textContent = "Could not reach the server.";
    }
  };
</script>
"""
