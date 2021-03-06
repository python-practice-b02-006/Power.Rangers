from obj import Object
import colors as cl


def read_obj(file_name):
    """Take characteristics for spacce objects from file and make objects.
    Parametrs:
    **file_name** — Input file name.
    """
    input_file_lines = open(file_name, 'r')
    objects = []
    for line in input_file_lines:
        if len(line.strip()) == 0 or line[0] == '#':
            continue  # пустые строки и строки-комментарии пропускаем
        objects.append(parse_obj_par(line))
    return objects


def parse_obj_par(line):
    """Take object characteristis from string.
    Input string format:
    X_coord Y_coord Velocity_X Velocity_Y Mass Radius Color
    Parametrs:
    **line** — string with object characteristics.
    """

    color = cl.Colors()
    obj = Object()
    obj.coords[0] = float(line.split()[0])
    obj.coords[1] = float(line.split()[1])
    obj.vel[0] = float(line.split()[2])
    obj.vel[1] = float(line.split()[3])
    obj.mass = float(line.split()[4])
    obj.rad = float(line.split()[5])
    obj.color = color.COLORS[int(line.split()[6])]
    return obj


if __name__ == "__main__":
    print("This module is not for direct call!")
