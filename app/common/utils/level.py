def calculate_level_progress(xp: int, level: int) -> tuple[int, float]:
    """
    Calculate XP needed for next level and current level progress.

    Level progression formula:
    - Level 1: 0-99 XP
    - Level 2: 100-299 XP (200 XP needed)
    - Level 3: 300-599 XP (300 XP needed)
    - Level 4: 600-999 XP (400 XP needed)
    - And so on...

    Returns: (xp_to_next_level, level_progress_percentage)
    """
    if level == 1:
        xp_for_current_level = 0
        xp_for_next_level = 100
    else:
        # XP needed for current level: sum of (level * 100) for all previous levels
        xp_for_current_level = sum(i * 100 for i in range(1, level))
        # XP needed for next level: level * 100
        xp_for_next_level = xp_for_current_level + (level * 100)

    xp_in_current_level = xp - xp_for_current_level
    xp_needed_for_next_level = xp_for_next_level - xp

    # Calculate progress percentage (0-100)
    if level == 1:
        level_progress = min(100.0, (xp / 100.0) * 100.0)
    else:
        xp_needed_for_current_level = level * 100
        level_progress = min(100.0, (xp_in_current_level / xp_needed_for_current_level) * 100.0)

    return xp_needed_for_next_level, level_progress
