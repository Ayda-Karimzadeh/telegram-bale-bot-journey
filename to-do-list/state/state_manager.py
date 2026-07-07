user_state = {}

def set_state(user_id, state):
    user_state[user_id] = state

def get_state(user_id):
    return user_state.get(user_id, "none")

def clear_state(user_id):
    user_state.pop(user_id, None)

