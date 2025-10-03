import math

security_penalty = 50 # Value between 0 and 100. In-game uses a default value of 50.
sde_systems = {} # Implement this yourself. Load the systems from the SDE.

def cost_fn(from_system, to_system):
    system_security = sde_systems[to_system]["securityStatus"]
    penalty_cost = math.exp(0.15 * security_penalty)

    if system_security <= 0.0:
        return 2 * penalty_cost
    elif system_security < 0.45:
        return 0.90
    else:
        return penalty_cost
