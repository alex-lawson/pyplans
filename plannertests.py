from planner import *
import json

def loadActions(source_fname):
  af = open(source_fname)
  afJson = json.load(af)
  af.close()

  al = []
  for aConfig in afJson:
    newAction = [set(), set(), set(), set(), aConfig['name']]
    for k, v in aConfig['pre'].iteritems():
      newAction[0 if v else 1].add(k)
    for k, v in aConfig['post'].iteritems():
      newAction[2 if v else 3].add(k)
    al.append(newAction)

  return al

source_fname = 'actions.json'

actions = loadActions(source_fname)

initialState = set(['hole', 'field'])
goals = [set(['water']), set(['knife'])]

res = tryPlan(actions, initialState, goals, planForward, 10)

if res[0]:
  print("Success! \nCreated plan: {0}{1}{2}".format(" -> ".join(res[1]),"\nReasons for plan failure:\n" if len(res[2]) > 0 else "", "\n".join(res[2])))
else:
  print("Failure: {0}\nReasons for plan failure:\n{1}".format(res[1], "\n".join(res[2])))

# a = set(['straw', 'water'])
# b = set(['mud', 'straw', 'water'])

# print(b - a)
