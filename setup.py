import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

include_files = [
    ("assets", "lib/assets")  # copy the whole assets folder
]

build_options = {
    "include_files": include_files,
}

setup(
    name="PixelWheel: Thessaloniki Edition",
    version="v0.2.0.alpha",
    description="PixelWheel: Thessaloniki Edition, a racing game made in current day Thessaloniki",
    options={"build_exe": build_options},
    executables=[Executable("main.py", base=base, target_name="PixelWheel.exe", icon=os.path.join("assets", "logo", "pixel_wheel_whole_logo.ico"))],
)
