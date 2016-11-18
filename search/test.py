import search


class MyProblem(search.SearchProblem):

    def __init__(self):
        print "init"

    def getStartState(self):
        return "A"

    def isGoalState(self, state):
        if state == "G":
            return True
        return False

    """
    def getSuccessors(self, state):
        actions = list()
        if state == "A":
            actions.append("B1")
            actions.append("C")
            actions.append("B2")
        elif state == "B1":
            actions.append("C")
        elif state == "C":
            actions.append("D")
        elif state == "B2":
            actions.append("C")
        elif state == "D":
            actions.append("E1")
            actions.append("F")
            actions.append("E2")
        elif state == "E1":
            actions.append("F")
        elif state == "F":
            actions.append("G")
        elif state == "E2":
            actions.append("F")

        action_triplets = list()
        for action in actions:
            action_triplets.append((action, action, 1))
        return action_triplets
    """
    """
    def getSuccessors(self, state):
        actions = list()
        if state == "A":
            actions.append("B")
            actions.append("G")
            actions.append("D")
        elif state == "B":
            actions.append("D")
        elif state == "D":
            actions.append("G")

        action_triplets = list()
        for action in actions:
            action_triplets.append((action, action, 1))
        return action_triplets
    """
    def getSuccessors(self, state):
        actions = list()
        costs = list()
        if state == "A":
            actions.append("B")
            costs.append(1)

            actions.append("G")
            costs.append(10)
        elif state == "B":
            actions.append("C")
            costs.append(1)
        elif state == "C":
            actions.append("G")
            costs.append(1)

        action_triplets = list()
        for i in range(0, len(actions)):
            action_triplets.append((actions[i], actions[i], costs[i]))
        return action_triplets


    def getCostOfActions(self, actions):
        cost = 0
        previous_action = None
        for action in actions:
            if action == "B":
                cost += 1
            elif action == "C":
                cost += 1
            elif action == "G":
                if previous_action is None:
                    cost += 10
                else:
                    cost += 1
            previous_action = action

        return cost


"""
problem = MyProblem()
solution = search.aStarSearch(problem)
print solution
"""


node1 = search.Node("A")
node2 = search.Node("A")

print "node1 == node2 ?"
print node1 == node2

