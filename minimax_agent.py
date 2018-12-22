import random

def minimax_agent_first(game, state):
	return minimax_agent(game, state, 1, 2)

def minimax_agent_second(game, state):
	return minimax_agent(game, state, 2, 2)

def minimax_agent(game, state, agent_index, depth):
	actions = game.actions(state)
	assert len(actions) > 0
	scores = [minimax_value(game, game.successor(state, action), agent_index, 3 - agent_index, depth) for action in actions]
	print(scores)
	best_score = max(scores)
	print("Best score: " + str(best_score))
	best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
	chosen_index = random.choice(best_indices)
	return actions[chosen_index]

def minimax_value(game, state, max_index, agent_index, depth):
	if game.is_end(state)[0]:
		winner = game.is_end(state)[1]
		if winner == 0:
			return 0
		elif winner == max_index:
			return float('inf')
		else:
			return -float('inf')

	if depth == 0:
		return 0 # No evaluation function

	actions = game.actions(state)
	if state[1] == max_index:
		values = [minimax_value(game, game.successor(state, action), max_index, 3 - agent_index, depth) for action in actions]
		return max(values)
	else:
		values = [minimax_value(game, game.successor(state, action), max_index, 3 - agent_index, depth - 1) for action in actions]
		return min(values)
