from ..components.position import PositionComponent

class MovementSystem:
    def update(self, entity):
        if entity.has_component(PositionComponent):
            position = entity.get_component(PositionComponent)
            # Update position logic here
            print(f"Updating position for entity with position: ({position.x}, {position.y})")
