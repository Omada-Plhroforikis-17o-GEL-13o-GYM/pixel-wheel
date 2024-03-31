# PixelWheel: Thessaloniki Edition

[![wakatime](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018df578-cfd3-4184-a4cc-c07e8a85718c.svg)](https://wakatime.com/badge/user/018c54ba-f9f5-426e-9733-6deb502d647d/project/018df578-cfd3-4184-a4cc-c07e8a85718c)

It's a 2D Racing game. 

Work In Progress.

- /assets/
    - Assets such as music and stuff
- /src/ 
    - other game related scripts
    - /tleng2/ 
        - game framework scripts
## Running reference.py
- You can move with `WASD` 
- You can turn on the debug mode, that shows the hitboxes with `B`
- You can toggle the clarity of the car model with `V` 

### TODO

MASSIVE TODO
- Redo the coordinate system, should be similar to pymunk, normal cartesian. Renderer will just convert the normal coordinates to the pygame-screen coordinates

- Abolishing display/window surfaces in RendererProperties 
- Update Renderable to hold a method for rendering complex objects (sprite stacking)
- Camera
- Renderer [the base part is complete]
