from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route("/generator")
def generator():
  return render_template("obrazec.html")

@app.route("/nalozi", methods=["POST"])
def nalozi():
  zgornji = request.form.get("zgornji")
  spodnji = request.form.get("spodnji")
  slika_file = request.files.get("slika")

  img = Image.open(slika_file).convert("RGB")
  draw = ImageDraw.Draw(img)

  font_size = img.width // 20
  font = ImageFont.truetype("OpenSans.ttf", font_size)

  text_width = draw.textlength(zgornji, font=font)
  x = (img.width-text_width) / 2
  y = 10
  draw.text((x, y), zgornji, font=font, fill="white")

  text_width = draw.textlength(spodnji, font=font)
  x = (img.width-text_width) / 2
  y = img.height - 120
  draw.text((x, y), spodnji, font=font, fill="white")

  img_io = io.BytesIO()
  img.save(img_io, "JPEG", quality=95)
  img_io.seek(0)

  return send_file(img_io, mimetype="image/jpeg")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)