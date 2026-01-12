# DOCS


## Basic use

First of all, in order to access the classes and functions inside a ECSpy file you'll need to import it like
```python
from ECSpy.File import thingFromtheFile
```

### Fundementals:
- In your main file musn't create an App() you need to import ECSglobals.mainApplication. This is your games App()

### Basic use:

To start off, import your main application
```python
from ECSpy.ECSglobals import mainApplication as app
```
This is just  nicer to work with.

Now ECS is split into 3 things

- Entities
- Components
- Systems

ECSpy has all these 3 things.

### Creating a system

Systems in ECSpy are just python functions that you pass to the app class.

They dont take any arguements.
For example:
```python
#Here you can see this is just a normal python function
def mySystem():
    pass
```

To add this to the application you must use .addSystem
```python
from ECSpy.ECSglobals import mainApplication as app

def mySystem():
    pass

app.addSystem("Setup",mySystem)
```

The "setup" is the sytem type you assign to the system when you add it

- "Update" systems are run everyframe (in the order they were added)

- "Setup" systems are run once at startup (again in the order they were added)

Now currently the system doesnt do anything

To make it do something we must talk about components

### Creating a component

Components are simple classes that inherit from the ECSpy.Component.Component class. They store only data.

The base component class has only one attribute, name.
the name is the string used to identify the component inside of entities.

An example would be

```python
from ECSpy.Component import Component

class myComponent(Component):
    def __init__(self,myDataProperty)
        #The name of the component must be assigned
        super().__init__("myComponent")
        
        self.myDataProperty = myDataProperty

```

Components can have methods attached to them, but the base Component class has only one method. That being mut()

Its use case is as such
```python
myComp = myComponent(myDataProperty = 0)
myComp.mut("myDataProperty",myComp.myDataProperty+1)
#This increases the myDataProperty of myComp by one
#This is very important to use consistently when mutating component properties.
```

### Creating entities:

Entities are objects that store a group of components alongside a unique ID

To make them you have to use app.world.addEntity()

```python
# -- import app up here
from ECSpy.Entity import Entity

app.world.addEntity(Entity())
```

This is fine but this creates an empty entity with no components. To add components use need to use the Entity's addComponent method.

```python
app.world.addEntity(Entity.addComponent(myComponent(0)))
```

this creates an entity with a myComponent component.

### Combining these together

To use these together lets talk about how to actually modify entities at runtime and such

```python
# -- imports up here

class Name(Component):
    def __init__(self,namestring):
        super().__init__("Name")
        self.namestring = namestring

def printNames()
    pass

person1 = Entity().addComponent(Name("Patricia"))

app.world.addEntity(person1)
app.addSystem("Startup",printNames)

```

this will be our base. If you run this you will get no output because we have left the printNames system blank.

In order to print the names you need to get all the entities with a Name component. To do this you'll need to use ECSpy.Query.callComponents()

```python
from ECSpy.Query import callComponents
from ECSpy.Query import Query

def printNames():
    # callComponents takes a (returns) and (dependencies)
    names = callComponents(Query(returns = ("Name",), dependencies = ()))
```
call components will return a dict of entities   and theyre attached components. The list of components will be only the entities components in the returns of the query. So in this case we will get
```
{
    (the id of an entity) : Name()
}
```
If we had put any dependecies we wouldve gotten
```
{
    (the ID of an entity with the dependency) : Name()
}
```
now we need to go through each entity in the dict

```python
def printNames():
    names = callComponents(Query(returns = ("Name",), dependencies = ()))

    for entity in names.keys():
        for name in names[entity]:
            print(name.namestring)
```

with these changes, when we run the program now we will get an output of

```
patricia
```

Yippee!! it works!!!

Now lets try to modify its value.

```python
    def changeNames():
        names = callComponents(Query(returns = ("Name",), dependencies = ()))

        for entity in names.keys():
            for name in names[entity]:
                #use mut to modify namestring
                name.mut("namestring", "Jimmy")

#addSystem can accept a tuple of systems aswell
app.addSystem("Startup",(printNames,changeNames))
```

Now heres a distinction. If you run this now you will still get the same output of patricia.

```
patricia
```

This is because we add

- printNames
- then changeNames

so the names get changed after we print the names.
This is because the systems get ran in the order they are added.

So for our code to work properly we need to change it to 
```python
app.addSystem("Startup", (changeNames,printNames))
```

and now we get out desired output!

```
Jimmy
```
---
## Other stuff

### Plugins:

Plugins are python functions that modify the app. These are usefull for not having to have all your setup in your main.py. They take the app as the only parameter. An example would be.

```python
def myPlugin(app: App()):
    app.addSystem("Startup",myStartupSystem)
    app.addSystem("Update",(myUpdateSystem1,myUpdateSystem2))
```

to use this you will have to import the function from whatever file its in. And then call app.addPlugin()

```python
from myfile import myPlugin

#This can also take a tuple of plugins to add aswell, just like addSystem
app.addPlugin(myPlugin)
```
---
### Resources:

Resources are globally accessable components that are stored as part of the App() class and can be used by any system, anywhere.

To create a resource you do.

```python
from ECSpy.Resource import Resource

class myResource(Resource):
    def __init__(self,myProperty : int):
        super().__init__("myResource")
        self.myProperty = myProperty
```

This is the same process as defining a componenet, but instead of inheriting from the base component class, you inherit from the base resource class.

In order to use your resource, you must add it to the application by doing:

```python
#-- import mainApplication as app up here
app.addResource(myResource)
```

To access your resource, you can then, inside of a system call

```python
#-- import mainApplication as app up here

def mySystem():
    x =app.getResource("myResource").myProperty
```

Like mutating component, to mutate a resource property you must also use the .mut() method:

```python
def mySystem():
    app.getResource("myResource").mut("myProperty",1)
```

## Boilerplate
### How to set up a basic window:

Now that you know all of this, we can start making an actual application. We're going make a basic empty window, that you can expand on later. This is also the program inside the main.py file of the project, as a base. Note that this uses pygame-ce as its api for input and output. If you dont know anything about pygame check out https://pyga.me/docs/#tutorials

---
In order to make a window, were going to use the prelude module inside of ECSpy. This module does some basic pygame setup for us. Like starting up a basic event handler and initializing pygame.

Lets start out with creating out games data. This data is what will be used by the prelude module, to create a window of your desired size.

GameData is a resource so you have to import it first.

```python
from ECSpy.Prelude import GameData
```

Then you have to add the resource to your app. GameData takes 2 parameters, being screenSize->(width,height) and caption->"caption". These will be the size of the window (and its resolution) and the window caption.

```python
# -- import mainApplication as app here
app.addResource(GameData(
    screenSize = (300,300),
    caption = "ECSpy"
))
```

Now we've defined out game data. We can add the preludPlugin to our application, this plugin will create a Screen resource and a basic handleEvents system to create a window.

```python
# --import app and add gamedata up here
from ECSpy.Prelude import preludePlugin

app.addPlugin(preludePlugin)
```

the final piece is to call app.run() at the end 

```python
app.run()
```

If you run this now you should get a 300*300 black window!

---
### Explaining what we just did.

What we now have is a Screen resource and an eventHandler system.

By the handleEvents system can be found in ECSpy.Events and is

```python
def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    app.getRescource("Clock").Clock.tick(60)
```

This both handles some basic events, add ticks the pygame clock.

You can change this to fit your own needs however.

The Screen resource has only one property, that being Screen.screen. screen being a the pygame Surface of our window.





