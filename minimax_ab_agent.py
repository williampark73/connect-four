import random

cache = {}
temp_cache = {}
calls = 0
non_cache_calls = 0
end_state_evals = 0
depth_out_evals = 0
same_turn_evals = 0
other_turn_evals = 0

def minimax_ab_agent_first(game, state):
	return minimax_ab_agent(game, state, 1, 3)

def minimax_ab_agent_second(game, state):
	return minimax_ab_agent(game, state, 2, 3)

def minimax_ab_agent(game, state, agent_index, depth):
	global calls, non_cache_calls, end_state_evals, depth_out_evals, same_turn_evals, other_turn_evals, cache, temp_cache

	calls = 0
	non_cache_calls = 0
	end_state_evals = 0
	depth_out_evals = 0
	same_turn_evals = 0
	other_turn_evals = 0

	temp_cache = {}
	actions = game.actions(state)
	assert len(actions) > 0

	states = [game.successor(state, action) for action in actions]
	winning_indices = [index for index in range(len(states)) if game.is_end(states[index])[0]]
	if len(winning_indices) != 0:
		return random.choice(winning_indices)

	scores = [minimax_ab_value(game, game.successor(state, action), agent_index, 3 - agent_index, depth) for action in actions]
	print(scores)
	best_score = max(scores)
	print("Best score: " + str(best_score))
	best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
	chosen_index = random.choice(best_indices)

	print("Calls: " + str(calls))
	print("Non-Cache Calls " + str(non_cache_calls))
	print("End State Evals: " + str(end_state_evals))
	print("Depth Out Evals: " + str(depth_out_evals))
	print("Same Turn Evals: " + str(same_turn_evals))
	print("Other Turn Evals: " + str(other_turn_evals))
	print("Cache Size: " + str(len(cache)))
	print("Temp Cache Size: " + str(len(temp_cache)))

	return actions[chosen_index]

def minimax_ab_value(game, state, max_index, agent_index, depth):
	global calls, non_cache_calls, end_state_evals, depth_out_evals, same_turn_evals, other_turn_evals, cache, temp_cache

	calls += 1
	if str(state) in cache:
		return cache[str(state)]
	if str(state) in temp_cache:
		return temp_cache[str(state)]
	non_cache_calls += 1

	if game.is_end(state)[0]:
		end_state_evals += 1
		winner = game.is_end(state)[1]
		if winner == 0:
			cache[str(state)] = 0
			return 0
		elif winner == max_index:
			cache[str(state)] = float('inf')
			return float('inf')
		else:
			cache[str(state)] = -float('inf')
			return -float('inf')

	if depth == 0:
		depth_out_evals += 1
		temp_cache[str(state)] = 0
		return 0 # No evaluation function

	actions = game.actions(state)
	if state[-1] == max_index:
		same_turn_evals += 1
		values = []
		for action in actions:
			value = minimax_ab_value(game, game.successor(state, action), max_index, 3 - agent_index, depth)
			if value == float('inf'):
				cache[str(state)] = value
				return value
			values.append(value)
		if max(values) != 0:
			cache[str(state)] = max(values)
		else:
			temp_cache[str(state)] = 0
		return max(values)
	else:
		other_turn_evals += 1
		values = []
		for action in actions:
			value = minimax_ab_value(game, game.successor(state, action), max_index, 3 - agent_index, depth - 1)
			if value == -float('inf'):
				cache[str(state)] = value
				return value
			values.append(value)
		if min(values) != 0:
			cache[str(state)] = min(values)
		else:
			temp_cache[str(state)] = 0
		return min(values)
