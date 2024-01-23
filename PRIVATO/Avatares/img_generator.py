from PIL import Image


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)

    return tuple(rgb)


def crearImg(array_colores, color_base, path):

    try:

        im = Image.new(mode="RGB", size=(110, 110),
                       color=color_base)

        x, y = 0, 0
        x_base, y_base = 0, 0

        for color in array_colores:

            for i in range(100):

                if y == 9 and x == 10:
                    break

                else:

                    if x > 9:
                        x = 0
                        y += 1

                    rgb_color = hex_to_rgb(color)
                    im.putpixel((x_base + x, y_base + y), rgb_color)

                    x += 1

            if x_base == 100:
                x_base = 0
                y_base += 10
                x = 0
                y = 0

            else:
                x_base += 10
                x = 0
                y = 0

        print(path)

        im.save(path)

        return True

    except:
        return False


def formatColores(string_colores):

    lista_colores = []

    color = ""

    for i in range(len(string_colores)):

        if string_colores[i] == "-":
            continue

        elif string_colores[i] == "x":
            lista_colores.append("e9e7e7")

        else:

            caracter = string_colores[i]
            color += caracter
            if len(color) == 6:
                lista_colores.append(color)
                color = ""

    return lista_colores
