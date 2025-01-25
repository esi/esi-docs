import math

# Inputs - these are set from the API results.
# Note that all times are in seconds.
planet_dict = {}
planet_dict["total_cycles"] = (
    30  # End time in seconds - start time in seconds / cycle time
)
planet_dict["cycle_time"] = 30 * 60  # 30 minutes, value from API cycleTime * 60
planet_dict["qty_per_cycle"] = 6965

# These constants are the defaults in dgmAttributeTypes. They may change.
decay_factor = 0.012  # Dogma attribute 1683 for this pin typeID
noiseFactor = 0.8  # Dogma attribute 1687 for this pin typeID

# Populated by data from the PI ESI Endpoint

cycle_time = planet_dict["cycle_time"]
planet_dict["total_qty"] = 0
quantityPerCycle = planet_dict["qty_per_cycle"]
barWidth = cycle_time / 900
total_cycles = planet_dict["total_cycles"]
for cycle in range(0, int(total_cycles)):
    t = (cycle + 0.5) * barWidth
    decay_value = quantityPerCycle / (1 + t * decay_factor)
    phaseShift = pow(quantityPerCycle, 0.7)

    sinA = math.cos(phaseShift + t * (1 / 12))
    sinB = math.cos(phaseShift / 2 + t * 0.2)
    sinC = math.cos(t * 0.5)

    sinStuff = (sinA + sinB + sinC) / 3
    sinStuff = max(sinStuff, 0)

    barHeight = decay_value * (1 + noiseFactor * sinStuff)

    planet_dict["total_qty"] += barWidth * barHeight

planet_dict["average_qty"] = planet_dict["total_qty"] / planet_dict["total_cycles"]
