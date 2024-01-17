import pygame
import json


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


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
            self.image.fill((0, 0, 0))
            self.rect = pygame.Rect(x1, y1, 25, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 20])
            self.image.fill((0, 0, 0))
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


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, color="black"):
        super().__init__()
        # self.outer_instance = outer_instance
        self.image = pygame.Surface((width, height))
        self.image.fill((150, 150, 150))
        # x = self.outer_instance.x
        # y = self.outer_instance.y + 86
        self.rect = self.image.get_rect().move(x, y)

        self.font = pygame.font.Font(None, 25)
        self.text = text
        self.rendered_text = self.font.render(self.text, True, color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)
        # self.mini_image = load_image("other_images/coin.png")
        # self.mini_image_rect = self.mini_image.get_rect().move(self.rect.x + 4, self.rect.y + 2)
        self.handled = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.rendered_text, self.text_rect)
        # screen.blit(self.mini_image, self.mini_image_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if click and self.rect.collidepoint(mouse_pos):
            if not self.handled:
                self.handled = True
                return True
            return False
        else:
            self.handled = False
            return False
