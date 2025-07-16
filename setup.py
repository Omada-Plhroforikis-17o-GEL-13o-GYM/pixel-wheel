from cx_Freeze import setup, Executable

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
    executables=[Executable("main.py")],
)
