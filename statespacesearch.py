import json
from random import shuffle

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

## action meets all preconditions, and would make some change to the current state
def actionValid(action, state):
  return state >= action[0] and state.isdisjoint(action[1]) and (len(action[2] - state) > 0 or not state.isdisjoint(action[3]))

## action could have set a value in the current state
## and that value previously would have matched the initial state
def actionRelevant(action, currentState, initialState):
  return len((currentState & action[2]) - initialState) > 0 or len((action[3] - currentState) & initialState) > 0

def planForward(i, g, limit):
  plan = []
  state = i.copy()
  c = limit
  while True:
    print("stepping with state {0}".format(state))
    if state >= g[0] and state.isdisjoint(g[1]):
      return (True, "Generated {0} steps.".format(limit - c), plan)
    if c <= 0:
      return (False, "No solution found after {0} steps.".format(limit), plan)
    c = c - 1
    shuffle(actions)
    acted = False
    for action in actions:
      if actionValid(action, state):
        plan.append(action[4])
        state = (state | action[2]) - action[3]
        acted = True
        break
    if not acted:
      return (False, "No valid actions.", plan)

def planBackward(i, g, limit):
  plan = []
  state = (i | g[0]) - g[1]
  c = limit
  while True:
    print("stepping with state {0}".format(state))
    if state == i:
      return (True, "Generated {0} steps.".format(limit - c), plan)
    if c <= 0:
      return (False, "No solution found after {0} steps.".format(limit), plan)
    c = c - 1
    shuffle(actions)
    acted = False
    for action in actions:
      if actionRelevant(action, state, initialState):
        plan.insert(0, action[4])
        state = (state - action[2]) | action[3]
        state = (state | action[0]) - action[1]
        acted = True
        break
    if not acted:
      return (False, "No relevant actions.", plan)


source_fname = 'actions.json'

actions = loadActions(source_fname)

initialState = set(['hole', 'field'])
goals = [set(['water']), set()]

# res = planForward(initialState, goals, 20)
res = planBackward(initialState, goals, 20)

print("{0}: {1}\nPlan: {2}".format("Success" if res[0] else "Failure", res[1], " -> ".join(res[2])))

# a = set(['straw', 'water'])
# b = set(['mud', 'straw', 'water'])

# print(b - a)
