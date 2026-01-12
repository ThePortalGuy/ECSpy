from .Entity import Entity

class World:
    def __init__(self):
        # {component : [EntitieIDs]}
        self.components = {}
        # {entityID : [components]}
        self.entities = {}
        # {entityID : Entity()}
        self.entityData = {}

    def addEntity(self, entity : Entity):
        self.entityData.update({entity.ID: entity})

        for component,data in entity.components.items():
            if not (component in self.components.keys()):
                self.components.update({component: []})
            
            self.components[component].append(entity.ID)
        
        self.entities.update({entity.ID : list(entity.components.values())})
