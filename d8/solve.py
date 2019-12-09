from collections import Counter
from typing import List

import arcade


def solve():
    with open('input.txt') as f:
        _input: List = f.read()

    width = 25
    tall = 6
    layers = list()
    data = _input

    while data:
        layer = list()
        for y in range(tall):
            row, data = data[:width], data[width:]
            layer.append(row)
        layers.append(layer)

    # Check sum
    counts = []
    for layer in layers:
        print(layer)
        c = Counter(''.join(layer))
        counts.append((c['0'], c['1'] * c['2']))
    print(sorted(counts)[0][1])

    # pic
    # 0 is black, 1 is white, and 2 is transparent
    SIZE = 50
    PADDING = 50
    arcade.open_window(width * SIZE + PADDING, tall * SIZE + PADDING, 'Image')

    shapes = arcade.ShapeElementList()
    for layer in reversed(layers):
        for y, row in enumerate(reversed(layer)):
            for x, pixel in enumerate(row):
                px = x * SIZE + SIZE / 2 + PADDING / 2
                py = y * SIZE + SIZE / 2 + PADDING / 2

                if pixel == '0':
                    rect = arcade.create_rectangle(px, py, SIZE, SIZE, arcade.color.BLACK, filled=True)
                elif pixel == '1':
                    rect = arcade.create_rectangle(px, py, SIZE, SIZE, arcade.color.WHITE, filled=True)
                else:
                    continue
                shapes.append(rect)

    arcade.set_background_color(arcade.color.BLACK)
    arcade.start_render()
    shapes.draw()
    arcade.finish_render()
    arcade.run()


if __name__ == '__main__':
    solve()
