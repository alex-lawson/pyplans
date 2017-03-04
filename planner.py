from random import shuffle

## action meets all preconditions, and would make some change to the current state
def actionValid(action, state):
  return state >= action[0] and state.isdisjoint(action[1]) and (len(action[2] - state) > 0 or not state.isdisjoint(action[3]))

## action achieves one or more conditions contained in the subgoals
def actionRelevant(action, sg):
  return not sg[0].isdisjoint(action[2]) or not sg[1].isdisjoint(action[3])

def applyAction(state, action):
  return (state | action[2]) - action[3]

def planForward(actions, i, g):
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
        plan.append(action)
        state = (state | action[2]) - action[3]
        if state in pastStates:
          return (False, "Repeat of previously visited state")
        pastStates.append(state.copy())
        acted = True
        break
    if not acted:
      return (False, "No valid actions")

def planBackward(actions, i, g):
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
        plan.insert(0, action)
        sg[0] = (sg[0] - action[2]) | action[0]
        sg[1] = (sg[1] - action[3]) | action[1]
        if sg in pastSgs:
          return (False, "Repeat of previously visited subgoal set")
        pastSgs.append([sg[0].copy(), sg[1].copy()])
        acted = True
        break
    if not acted:
      return (False, "No relevant actions")

def planSTRIPS(actions, i, g):
  plan = []
  s = i.copy()
  while True:
    if s >= g[0] and s.isdisjoint(g[1]):
      return (True, plan)
    shuffle(actions)
    acted = False
    for a in actions:
      if actionRelevant(a, g):
        recRes = planSTRIPS(actions, s, a)
        if not recRes[0]:
          return recRes
        for pa in recRes[1]:
          s = applyAction(s, pa)
        s = applyAction(s, a)
        plan = plan + recRes[1] + [a]
        acted = True
        break
    if not acted:
      return (False, "No relevant actions")

def createPlan(actions, i, g, planFunction, tries):
  t = 0
  failures = []
  while t < tries:
    t += 1
    res = planFunction(actions, i, g)
    if res[0]:
      print("Success after {0} tries".format(t))
      return (res[0], res[1], failures)
    else:
      failures.append(res[1])
  return (False, "No plan found after {0} tries".format(tries), failures)
