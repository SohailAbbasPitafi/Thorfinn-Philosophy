from PIL import Image, ImageDraw

img = Image.open("static/img/thorfinn-original.png").convert("RGBA")
w, h = img.size

# make the white background transparent, starting from each corner
for point in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    ImageDraw.floodfill(img, point, (255, 255, 255, 0), thresh=30)

# shrink so the page loads fast
img.thumbnail((700, 700))
img.save("static/img/thorfinn.png")
print("Saved", img.size)