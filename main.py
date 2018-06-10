import argparse
from os import path
import json
import pygame
import sys


def convert_to_rgba(color):
    if color[0] == "#":
        return pygame.Color(color)
    elif color[0] == "(":
        color_list_in_rgba = [int(c) for c in color.strip("( )").split(',')]
        if len(color_list_in_rgba) == 3:
            color_list_in_rgba.append(255)
        return pygame.Color(color_list_in_rgba[0], color_list_in_rgba[1], color_list_in_rgba[2], color_list_in_rgba[3])
    else:
        raise Exception(str(color) + "is wrong color")


def main():
    try:
        arg_parser = argparse.ArgumentParser(description="process argv")
        arg_parser.add_argument("Input", help="Input file")
        arg_parser.add_argument("-o", "--Output", nargs="?", const="default_out", help="Output file")
        argv = arg_parser.parse_args()
        if not path.isfile(argv.Input):
            print("Input file does not exist")
            return
        with open(argv.Input, "r") as In:
            json_file = json.load(In)

        if not {"Figures", "Screen", "Palette"}.issubset(set(json_file.keys())):
            print("JSON file must include keys: Figures, Screen, Palette")
            return
        screen_data = json_file["Screen"]
        figures = json_file["Figures"]
        palette = json_file["Palette"]

        if not {"width", "height", "fg_color", "bg_color"}.issubset(set(screen_data.keys())):
            print("Screen must include: width, height, fg_color, bg_color")
            return

        pygame.init()
        screen = pygame.display.set_mode((screen_data["width"], screen_data["height"]))

        full_palette = {screen_data["bg_color"]: palette.get(screen_data["bg_color"]), screen_data["fg_color"]: palette.get(screen_data["fg_color"])}
        for fig in figures:
            if "color" in list(fig.keys()):
                if palette.get(fig["color"]) is not None:
                    full_palette.update({fig["color"]: palette.get(fig["color"])})
                else:
                    full_palette.update({fig["color"]: fig["color"]})
        #print(full_palette)
        for key in sorted(full_palette.keys()):
            full_palette.update({key: convert_to_rgba(full_palette.get(key))})
            #print(full_palette)

        screen.fill(full_palette.get(screen_data["bg_color"]))
        fg_color = full_palette.get(screen_data["fg_color"])

        for fig in figures:
            if "type" not in list(fig.keys()):
                raise Exception("No type of figure described")
            fig_type = fig["type"]

            if fig_type == "point":
                if not {"x", "y"}.issubset(set(fig.keys())):
                    raise Exception("Point coordinates")
                screen.set_at([fig["x"], fig["y"]], full_palette.get(fig.get("color"), fg_color))

            if fig_type == "circle":
                if not {"x", "y", "radius"}.issubset(set(fig.keys())):
                    raise Exception("Circle arguments")
                pygame.draw.circle(screen, full_palette.get(fig.get("color"), fg_color), [fig["x"], fig["y"]], fig["radius"])
            if fig_type == "polygon":
                if not {"points"}.issubset(set(fig.keys())):
                    raise Exception("Polygon arguments")
                pygame.draw.polygon(screen, full_palette.get(fig.get("color"), fg_color), fig["points"])
            if fig_type == "square":
                if not {"x", "y", "size"}.issubset(set(fig.keys())):
                    raise Exception("Square arguments")
                size = fig["size"]
                left = fig["x"] - (size/2)
                top = fig["y"] - (size/2)
                pygame.draw.rect(screen, full_palette.get(fig.get("color"), fg_color), pygame.Rect(left, top, size, size))
            if fig_type == "rectangle":
                if not {"x", "y", "width", "height"}.issubset(set(fig.keys())):
                    raise Exception("Rectangle arguments")
                size_x = fig["width"]
                size_y = fig["height"]
                left = fig["x"] - (size_x / 2)
                top = fig["y"] - (size_y / 2)
                pygame.draw.rect(screen, full_palette.get(fig.get("color"), fg_color),
                                 pygame.Rect(left, top, size_x, size_y))

        pygame.display.flip()
        if argv.Output is not None:
            pygame.image.save(screen,argv.Output+".jpg")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    except Exception as e:
        print(e.args[0])
        return


if __name__ == "__main__":
    main()