from PIL import Image

img = Image.open("pixel_wheel_whole_logo.png")
img.save("pixel_wheel_whole_logo.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
