# PixelWheel: Thessaloniki Edition

[![wakatime](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018df578-cfd3-4184-a4cc-c07e8a85718c.svg)](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018df578-cfd3-4184-a4cc-c07e8a85718c)

It's a 2D Racing game. The setting of the game is in current day Thessaloniki.

The game uses the Sprite-Stacking technique to create a pseudo 3d world. It also uses the [tleng](https://github.com/tl-ecosystem/tleng) game engine.

Work In Progress.

## Check the Releases!

Click here to get the newest Release of [PixelWheel: Thessaloniki Edition](https://github.com/Omada-Plhroforikis-17o-GEL-13o-GYM/pixel-wheel/releases)

## How to download:

Go to releases!
<details>
<summary><h3>Windows</h3></summary>
 
 - Install the `.zip` file
 - Extract the `.zip` file to a folder of your liking
 - Double click the `.exe` file. 
 
</details>


<details>
<summary><h3>Linux</h3></summary>

  - Using Wine:
    - Ensure that you have wine installed.
    - Follow Windows How-To.

 - Linux binaries:
    - Install the `pixel-wheel-linux.tar.gz` 
    - Extract the contents of `pixel-wheel-linux.tar.gz`
    - Double click on the `pixel-wheel` file
</details>

<details>
<summary><h3>From Source</h3></summary>
 
- Clone the games repository locally. And clone the Tleng Game engine Locally
    ``` bash
    $ git clone https://www.github.com/Omada-Plhroforikis-17o-GEL-13o-GYM/pixel-wheel.git
    $ git clone https://www.github.com/tl-ecosystem/tleng.git
    ```    
- Create a symbolic link inside pixel-wheel from the tleng repo:
    ```bash
    $ ln -r -s ./tleng/tleng2 ./pixel-wheel/src
    ```
- Change to the game directory
    ``` bash
    $ cd pixel-wheel
    ```
- Create a virtual python enviroment and then activate it:
    ```bash
    $ python -m venv venv
    ```
    - linux
    ```bash
    $ source ./venv/bin/activate
    ```
    - Windows
    ```bash
    $ .\venv\Scripts\Activate.ps1
    ```
- Download the requirements:

    Using pip:
    ```bash
    $ pip install -r requirements.txt
    ```
    Using your package manager manually (apt, dnf, pacman ...):
    ```bash
    $ sudo 'your-package-manager' install pygame3-'your-package'
    ```
- Run the game.
    ```bash
    $ python main.py
    ```
    
</details>

## Running Pixel Wheel (main.py) 
- When you boot up pixel wheel you are in the Menu
- You can click the buttons with `right click`
- If you press `Play` you free roam with `WASD`
- If you press `Credits` you can scroll with your `mouse-wheel`
- to go back to the `Menu` you need to press `esc` 

## Running reference.py
- You can move with `WASD` 
- You can turn on the debug mode, that shows the hitboxes with `B`
- You can toggle the clarity of the car model with `V` 

## TODO
- Redo the coordinate system, should be similar to pymunk, normal cartesian. Renderer will just convert the normal coordinates to the pygame-screen coordinates (mostly complete)

- Camera (almost complete)
- Renderer (mostly complete, even support y-sort)

MASSIVE TODO
- ECS re-write (for the v0.1.5-alpha update)
- Abolishing display/window surfaces in RendererProperties [being worked on for ecs] 
