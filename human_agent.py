#from connect_four import ConnectFourGame

def human_agent(game, state):
	actions = game.actions(state)
	print("Possible actions: " + str(actions))
	action = -1
	while action not in actions:
		action = int(input("Enter a valid action: "))
	return action