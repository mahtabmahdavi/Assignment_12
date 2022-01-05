import math
import time
import random
import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class SpaceShip(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png")
        self.width = 48
        self.height = 48
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 32
        self.angle = 0
        self.change_angle = 0
        self.speed = 4
        self.score = 0
        self.life = 3
        self.life_image = arcade.load_texture("heart.png")
        self.bullet_list = []


    def rotate(self):
        self.angle += self.speed * self.change_angle


    def fire(self):
        self.bullet_list.append(Bullet(self))


    def sound_fire(self):
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/laser1.mp3"))



class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png")
        self.width = 48
        self.height = 48
        self.center_x = random.randint(self.width, SCREEN_WIDTH - self.width)
        self.center_y = SCREEN_HEIGHT + self.height // 2
        self.speed = 4
        
        
    def move(self, factor):
        self.center_y -= self.speed * factor


    def explosion_sound(self):
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/explosion1.wav"))



class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.angle = host.angle
        self.speed = 6


    def move(self):
        angle = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle)
        self.center_y += self.speed * math.cos(angle)



class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Intersteller Game 🚀")
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")

        self.me = SpaceShip()
        self.start_time = time.time()
        self.enemy_list = []
        self.next_enemy = 5


    def on_update(self, delta_time: float):
        self.end_time = time.time()

        if self.end_time - self.start_time > self.next_enemy:
            self.enemy_list.append(Enemy())
            self.next_enemy = random.randint(2, 6)
            self.start_time = time.time()

        self.me.rotate()
        factor = 1
        for enemy in self.enemy_list:
            enemy.move(factor)
            factor += 0.5

        for bullet in self.me.bullet_list:
            bullet.move()

        for enemy in self.enemy_list:
            if any (arcade.check_for_collision(enemy, bullet) for bullet in self.me.bullet_list):
                enemy.explosion_sound()
                self.enemy_list.remove(enemy)
                self.me.bullet_list.remove(bullet)
                self.me.score += 1

        if any (enemy.center_y <= 0 for enemy in self.enemy_list):
            self.enemy_list.remove(enemy)
            self.me.life -= 1

        if any (bullet.center_y >= SCREEN_HEIGHT or bullet.center_y <= 0 or bullet.center_x >= SCREEN_WIDTH or bullet.center_x <= 0 for bullet in self.me.bullet_list):
            self.me.bullet_list.remove(bullet)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.me.fire()
            self.me.sound_fire()
        elif symbol == arcade.key.RIGHT:
            self.me.change_angle = -1
        elif symbol == arcade.key.LEFT:
            self.me.change_angle = 1


    def on_key_release(self, symbol: int, modifiers: int):
        self.me.change_angle = 0


    def on_draw(self):
        arcade.start_render()

        if self.me.life <= 0:
            arcade.draw_text("GAME OVER!", (SCREEN_WIDTH // 4), SCREEN_HEIGHT // 2, arcade.color.ORANGE, width = 400, font_size = 40, align = "center")
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
            self.me.draw()

            for enemy in self.enemy_list:
                enemy.draw()

            for bullet in self.me.bullet_list:
                bullet.draw()

            arcade.draw_text(f"score : {self.me.score}", SCREEN_WIDTH - 105, 5, arcade.color.RED, width = 100, font_size = 15, align = "center")

            space = 0
            for life in range(self.me.life):
                arcade.draw_texture_rectangle(15 + space, 15, 20, 20, self.me.life_image)
                space += 25



game = Game()
game.run()