import math

# These constants are the defaults in dgmAttributeTypes. They may change.
decay_factor = 0.012  # Dogma attribute 1683 for this pin typeID
noise_factor = 0.8  # Dogma attribute 1687 for this pin typeID

def calculateExtractorValues(total_cycles = 30, cycle_time = 30 * 60, qty_per_cycle = 6965):
    """
    :param int total_cycles: End time in seconds - start time in seconds / cycle_time
    :param int cycle_time: Cycle time, in seconds
    :returns Generator[int]: A generaotr that iterates over all values
    """
    bar_width = float(cycle_time) / 900.0
    
    for cycle in range(0, total_cycles):
        t = (cycle + 0.5) * bar_width
        decay_value = qty_per_cycle / (1 + t * decay_factor)
        phase_shift = pow(qty_per_cycle, 0.7)

        sin_a = math.cos(phase_shift + t * (1 / 12))
        sin_b = math.cos(phase_shift / 2 + t * 0.2)
        sin_c = math.cos(t * 0.5)

        sin_stuff = max((sin_a + sin_b + sin_c) / 3, 0)

        bar_height = decay_value * (1 + noise_factor * sin_stuff)

        yield bar_width * bar_height
