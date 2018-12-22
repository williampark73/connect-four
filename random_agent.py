import random

def random_agent(game, state):
	actions = game.actions(state)
	action = random.choice(actions)
	print("Choosing action " + str(action))
	return action