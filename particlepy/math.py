# math.py

def get_correct_color(color: int or float or tuple or list):
    if isinstance(color, int):
        return [color, color, color, 255]
    elif isinstance(color, tuple) or isinstance(color, list):
        if len(color) == 3:
            return [color[0], color[1], color[2], 255]
        elif len(color) == 4:
            return list(color)
