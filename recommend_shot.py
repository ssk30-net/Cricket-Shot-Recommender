def recommend_shot(orientation, trajectory):
    if not trajectory:
        return "Unable to detect ball trajectory."

    # Simplistic logic based on the direction of the ball
    # For example, if the ball is coming towards the leg side, recommend a pull or leg glance
    # This is highly simplified and should be replaced with a proper analysis

    # Calculate the direction based on the last point
    last_x, last_y = trajectory[-1]
    second_last_x, second_last_y = trajectory[-2] if len(trajectory) > 1 else (0, 0)
    dx = last_x - second_last_x
    dy = last_y - second_last_y

    if dx > 0:
        horizontal_direction = "Outside"
    else:
        horizontal_direction = "Inside"

    if dy > 0:
        vertical_direction = "Full Delivery"
    else:
        vertical_direction = "Short Delivery"

    # Example recommendations
    if orientation == "Right-Handed":
        if horizontal_direction == "Outside" and vertical_direction == "Full Delivery":
            return "Recommended Shot: Cover Drive"
        elif horizontal_direction == "Inside" and vertical_direction == "Short Delivery":
            return "Recommended Shot: Pull Shot"
        else:
            return "Recommended Shot: Defensive Shot"
    elif orientation == "Left-Handed":
        if horizontal_direction == "Outside" and vertical_direction == "Full Delivery":
            return "Recommended Shot: On Drive"
        elif horizontal_direction == "Inside" and vertical_direction == "Short Delivery":
            return "Recommended Shot: Hook Shot"
        else:
            return "Recommended Shot: Defensive Shot"
    else:
        return "Unable to determine orientation."
