from ECSpy.ECSglobals import mainApplication as app
from ECSpy.Prelude import preludePlugin
from ECSpy.Prelude import GameData

app.addRescource(GameData((300,300),"BIOLWIREL"))
app.addPlugin(preludePlugin)
app.run()