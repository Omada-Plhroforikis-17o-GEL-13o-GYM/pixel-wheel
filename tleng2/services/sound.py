from os import path 

class SoundService:
    def __init__(self, sound_path: str) -> None:
        self.sound = path.join(sound_path)