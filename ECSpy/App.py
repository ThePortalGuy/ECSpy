from .World import World

class App:
    def __init__(self):
        
        self.running = True
        self.systems = {
            "Update" : [],
            "Setup" : []
        }
        self.resources = {}
        self.world = World()

    def run(self):
        for system in self.systems["Setup"]:
            system()

        while self.running:
            for system in self.systems["Update"] :
                system()

    def addSystem(self,systype : str, system):
        if isinstance(system, tuple):
            for sys in system:
                self.systems[systype].append(sys)
        else:
            self.systems[systype].append(system)

    def addPlugin(self, plugin):
        if isinstance(plugin, tuple):
            for plug in plugin:
                plug(self)
        else:
            plugin(self)

    def addRescource(self, rescource):
        if isinstance(rescource, tuple):
            for re in rescource:
                self.resources.update({
                    re.name:re
                })
        else:
            self.resources.update({
                    rescource.name:rescource
                })
                
    def getRescource(self,name):
        return self.resources[name]
    
