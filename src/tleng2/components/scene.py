from abc import ABC, abstractmethod
from ..engine.properties import RendererProperties


class SceneCatcher:
    scenes = {}

    def __init__(self, 
            scene_key:str, 
            sr_param_key: str
        ) -> None:
        self.scenes.update({scene_key: self})
        RendererProperties.scene_parameters.update({scene_key:sr_param_key})


class Scene(SceneCatcher, ABC):
    def __init__(self,
            scene_name, 
            sr_param_key: str = 'default'
        )-> None:

        SceneCatcher.__init__(self,
                              scene_key=scene_name, 
                              sr_param_key=sr_param_key),
        self.scene_name = scene_name


    @abstractmethod
    def event_handling(self) -> None:
        '''
        To handle the events of mouse and other.
        If you want to access Keys Pressed, you can do so, from 
        
        `EngineProperties._events` `EngineProperties._keys_pressed`
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        '''

    @abstractmethod
    def update(self) -> None:
        '''
        game logic
        '''

    @abstractmethod
    def render(self) -> None:
        '''
        what to render to the screen
        '''


class SubSceneManagerCatcher:
    """
    Useful for split-screen gameplay were multiple subscenemanagers might need to be used
    """
    ...


class SubSceneManager:
    ...
