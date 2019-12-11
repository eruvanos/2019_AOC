import math

from utils import Vector


def solve():
    with open('input.txt') as f:
        # with open('test_input_2.txt') as f:
        _input = f.read()

    field = _input.splitlines()
    asteroids = list()
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.append(Vector(x, y))

    max_visible = dict()
    station = None

    for center in asteroids:
        visible_asteroids = dict()
        for ast in asteroids:
            angle = math.atan2(ast.y - center.y, ast.x - center.x)  # atan pointing to the top
            angle = math.degrees(angle)

            angle += 90
            if angle < 0:
                # negative angles are shifted to positive value
                angle = 360 + angle
            # skip if there is already an nearer ast detected
            if angle in visible_asteroids:
                distance_to_old = center.distance(visible_asteroids[angle])
                distance_to_new = center.distance(ast)
                if distance_to_old < distance_to_new:
                    # print('skip')
                    continue

            visible_asteroids[angle] = ast

        if len(visible_asteroids) > len(max_visible):
            max_visible = visible_asteroids
            station = center

    # print(max_visible)
    print('Station:', station)
    print('Max visible:', len(max_visible))

    for i, angle in enumerate(sorted(max_visible.keys(), reverse=False), start=1):
        if i == 200:
            ast = max_visible[angle]
            print(f'{i}. {angle} -> {ast}')
            print('Solution', ast.x * 100 + ast.y)

    # import arcade
    # arcade.open_window(800, 800, 'Astroids', resizable=True)
    # # arcade.set_viewport(0, 800, 800, 0)
    #
    # SCALE = 30
    # arcade.start_render()
    #
    # arcade.draw_circle_filled(station.x * SCALE, 800 - station.y * SCALE, SCALE // 2, arcade.color.WHITE)
    # for i, angle in enumerate(sorted(max_visible.keys(), reverse=False), start=1):
    #     ast = max_visible[angle]
    #     arcade.draw_text(str(i), ast.x * SCALE, 800 - ast.y * SCALE, arcade.color.RED)
    #
    # arcade.finish_render()
    # arcade.run()


if __name__ == '__main__':
    solve()
