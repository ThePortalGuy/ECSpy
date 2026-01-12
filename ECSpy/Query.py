from .ECSglobals import mainApplication as app

class Query:
    def __init__(self, returns : tuple, dependencies : tuple):
        #tuple(strs) -> frozenset(str,str,str)
        #hopefully not frozenset('s','t','r','s')
        self.returns = frozenset(returns)
        self.dependencies = frozenset(dependencies) 

def callComponents(query : Query) -> dict:
    #Forgive me father i have sinned
    if len(query.returns) == 0:
        class NoQueryRequests(Exception):
            pass
        raise(NoQueryRequests("Requires atleast one query request"))
    
    request = []
    for item in query.returns:
        request.append(frozenset((app.world.components[item])))
    for item in query.dependencies:
        request.append(frozenset((app.world.components[item])))

    common_ids = frozenset.intersection(*sorted(request, key=len))

    neededReturns = {}

    for id in common_ids:
        for item in query.returns:
            data = []
            data.append(app.world.entityData.get(id).components.get(item)) #-> returns tuple i think :3
        neededReturns.update({id:data})

    return neededReturns