import uuid
from .Component import Component

class Entity:
    def __init__(self):
        #{"component" : Component()}
        self.components = {}
        self.ID = uuid.uuid4()
        
    def addComponent(self, component : Component):
        if component.name in self.components.keys():
            class DuplicateComponents(Exception):
                pass
            raise DuplicateComponents("You can only have one component type per entity shitass")
        
        self.components.update({component.name : component})
        return self



        