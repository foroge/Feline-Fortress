import pygame
import json

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def update_card(cards, screen):
    for card in cards:
        card.button.update()
    for card in cards:
        card.all_draw(screen)


def update_rect(groups, screen):
    if type(groups) == list:
        for sprites in groups:
            for sprite in sprites:
                sprite.self_draw(screen)
    else:
        for sprite in groups:
            sprite.self_draw(screen)


def change_size_sprites(sprites, camera):
    scale = camera.scale
    for sprite in sprites:
        sprite.change_size(scale)
    cols = [False, False, False, False]
    for sprite in sprites:
        check = sprite.check(horizontal_borders, vertical_borders)
        if not cols[0] and check[0][0]:
            cols[0] = True
        if not cols[1] and check[0][1]:
            cols[1] = True
        if not cols[2] and check[1][0]:
            cols[2] = True
        if not cols[3] and check[1][1]:
            cols[3] = True
    if not all(cols):
        camera.scale += camera.step
        for sprite in sprites:
            sprite.change_size(camera.scale)


def sprites_move(sprites, vx, vy, hor_borders, ver_borders):
    for sprite in sprites:
        sprite.update(vx, vy)
    check = check_collision(sprites, vx, vy, hor_borders, ver_borders)
    if check[0] or check[1]:
        for sprite in sprites:
            sprite.update(check[0], check[1])
        # sptires_move(sprites, check[0], 0, hor_borders, ver_borders)
        # sptires_move(sprites, 0, check[1], hor_borders, ver_borders)


def enem_move(sprites, level_map, camera_scale, king):
    for sprite in sprites:
        sprite.move(level_map, camera_scale, king)


def cats_attack(sprites, enemy_group):
    for sprite in sprites:
        sprite.try_attack(enemy_group)


def move_projectiles(sprites):
    for sprite in sprites:
        sprite.go_to_enemy()


def check_collision(sprites, vx, vy, horizontal_borders, vertical_borders):
    new_vx = 0
    new_vy = 0
    col_h = [False, False]
    col_v = [False, False]
    for sprite in sprites:
        check = sprite.check(horizontal_borders, vertical_borders)
        if not col_h[0] and check[0][0]:
            col_h[0] = True
        if not col_h[1] and check[0][1]:
            col_h[1] = True
        if not col_v[0] and check[1][0]:
            col_v[0] = True
        if not col_v[1] and check[1][1]:
            col_v[1] = True
    if not all(col_h):
        new_vy = -vy
    if not all(col_v):
        new_vx = -vx
    return new_vx, new_vy


def move(sprites, level_map, camera_scale):
    for sprite in sprites:
        sprite.move(level_map, camera_scale)


def set_def_position(sprites, x, y, size):
    for sprite in sprites:
        sprite.set_default_value(x, y, size)


def get_json(filename):
    with open(filename) as file:
        data = json.load(file)
    return data


def set_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2 - 20:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([20, y2 - y1])
            self.image.fill((109, 86, 80))
            self.rect = pygame.Rect(x1, y1, 25, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 20])
            self.image.fill((109, 86, 80))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 25)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.scale = 0.8
        self.step = 0.02
        self.old_scale = 0.8

    def change_scale(self, flag):
        if flag and self.scale <= 1.2:
            self.old_scale = self.scale
            self.scale += self.step
        elif not flag and self.scale > 0.8:
            self.old_scale = self.scale
            self.scale -= self.step
