# PixelWheel: Thessaloniki Edition

[![wakatime](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018df578-cfd3-4184-a4cc-c07e8a85718c.svg)](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018df578-cfd3-4184-a4cc-c07e8a85718c)

It's a 2D Racing game. The setting of the game is in current day Thessaloniki.

The game uses the Sprite-Stacking technique to create a pseudo 3d world. It also uses the [tleng](https://github.com/tl-ecosystem/tleng) game engine.

Work In Progress.

## Check the Releases!

Click here to get the newest Release of [PixelWheel: Thessaloniki Edition](https://github.com/Omada-Plhroforikis-17o-GEL-13o-GYM/pixel-wheel/releases)

## How to download:

Go to releases!

### Windows
 - Install the `.zip` file
 - Extract the `.zip` file to a folder of your liking
 - Double click the `.exe` file. 

### Linux
 - Using Wine:

    - Follow Windows How-To.

 - From Source: 
    - Clone the repository locally.

        ``` bash
        $ git clone https://www.github.com/Omada-Plhroforikis-17o-GEL-13o-GYM/pixel-wheel.git
        ```    

    - Change to the game directory

        ``` bash
        $ cd pixel-wheel
        ```

    - Download the requirements (delete if you have the pygame library and not pygame-ce)
    
        Using pip:
        ```
        $ pip install -r requirements.txt
        ```
        Using your package manager manually (apt, dnf, pacman ...):

        ``` bash
        $ sudo 'your-package-manager' install pygame3-'your-package'
        ```

    - Run the game.

        ``` bash
        $ python main.py
        ```

## Running reference.py
- You can move with `WASD` 
- You can turn on the debug mode, that shows the hitboxes with `B`
- You can toggle the clarity of the car model with `V` 

### TODO

MASSIVE TODO
- ECS re-write

- Redo the coordinate system, should be similar to pymunk, normal cartesian. Renderer will just convert the normal coordinates to the pygame-screen coordinates

- Abolishing display/window surfaces in RendererProperties 
- Update Renderable to hold a method for rendering complex objects (sprite stacking)
- Camera
- Renderer [the base part is complete]
