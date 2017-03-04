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

## action achieves one or more conditions contained in the subgoals
def actionRelevant(action, sg):
  return not sg[0].isdisjoint(action[2]) or not sg[1].isdisjoint(action[3])

def planForward(i, g):
  plan = []
  state = i.copy()
  pastStates = [state.copy()]
  while True:
    # print("stepping with state {0}".format(state))
    if state >= g[0] and state.isdisjoint(g[1]):
      return (True, plan)
    shuffle(actions)
    acted = False
    for action in actions:
      if actionValid(action, state):
        plan.append(action[4])
        state = (state | action[2]) - action[3]
        if state in pastStates:
          return (False, "Repeat of previously visited state")
        pastStates.append(state.copy())
        acted = True
        break
    if not acted:
      return (False, "No valid actions")

def planBackward(i, g):
  plan = []
  sg = [g[0].copy(), g[1].copy()]
  pastSgs = [[sg[0].copy(), sg[1].copy()]]
  while True:
    # print("stepping with subgoal {0}".format(sg))
    if i >= sg[0] and i.isdisjoint(sg[1]):
      return (True, plan)
    shuffle(actions)
    acted = False
    for action in actions:
      if actionRelevant(action, sg):
        plan.insert(0, action[4])
        sg[0] = (sg[0] - action[2]) | action[0]
        sg[1] = (sg[1] - action[3]) | action[1]
        if sg in pastSgs:
          return (False, "Repeat of previously visited subgoal set")
        pastSgs.append([sg[0].copy(), sg[1].copy()])
        acted = True
        break
    if not acted:
      return (False, "No relevant actions")

def planSTRIPS(i, g):
  plan = []
  while True:
    pass

def tryPlan(i, g, planFunction, tries):
  t = 0
  failures = []
  while t < tries:
    t += 1
    res = planFunction(i, g)
    if res[0]:
      print("Success after {0} tries".format(t))
      return (res[0], res[1], failures)
    else:
      failures.append(res[1])
  return (False, "No plan found after {0} tries".format(tries), failures)

source_fname = 'actions.json'

actions = loadActions(source_fname)

initialState = set(['hole', 'field'])
goals = [set(['water']), set()]

# res = planForward(initialState, goals, 20)
# res = planBackward(initialState, goals, 20)
# res = planSTRIPS(initialState, goals)

res = tryPlan(initialState, goals, planForward, 10)

if res[0]:
  print("Success! \nCreated plan: {0}{1}{2}".format(" -> ".join(res[1]),"\nReasons for plan failure:\n" if len(res[2]) > 0 else "", "\n".join(res[2])))
else:
  print("Failure: {0}\nReasons for plan failure:\n{1}".format(res[1], "\n".join(res[2])))

# a = set(['straw', 'water'])
# b = set(['mud', 'straw', 'water'])

# print(b - a)
