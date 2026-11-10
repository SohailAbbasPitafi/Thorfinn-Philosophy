import os
from PIL import Image

RAW_DIR = "raw_images"
OUT_DIR = "static/img"
WIDTH, HEIGHT = 480, 600          # 4:5 portrait, matches the frame
TOP_BIAS = 0.2                    # 0 = keep the top, 0.5 = centered crop

os.makedirs(OUT_DIR, exist_ok=True)

for filename in sorted(os.listdir(RAW_DIR)):
    stem, ext = os.path.splitext(filename)
    if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue

    img = Image.open(os.path.join(RAW_DIR, filename)).convert("RGB")
    w, h = img.size
    target_ratio = WIDTH / HEIGHT

    if w / h > target_ratio:                      # too wide: trim the sides
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:                                         # too tall: trim the bottom
        new_h = int(w / target_ratio)
        top = int((h - new_h) * TOP_BIAS)
        img = img.crop((0, top, w, top + new_h))

    img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
    img.save(os.path.join(OUT_DIR, stem + ".jpg"), quality=85)
    print("Saved", stem + ".jpg")