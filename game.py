import arcade
import arcade.gui
from queue import Queue
import random
import time

SCREEN_HEIGHT = 650
SCREEN_WIDTH = 1000

BLACK_GUITAR = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Guitar_Cactus_Black.png"
BLACK_TRUMPET = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Trumpet_Cactus_Black.png"
BLACK_VIOLIN = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Violin_cactus_Black.png"

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/MONKE.png", 
                         0.15
                        )

        self.center_x = 120
        self.center_y = 400

class Llama(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/llama.png", 0.1)

        self.center_x = center_x
        self.center_y = center_y

class Water(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Water.png")

        self.center_x = center_x
        self.center_y = center_y

class Senorita_monke(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Senorita_MONKE.png",
                         0.65
                        )
        
        self.center_x = 1000
        self.center_y = 900

class Guitar_Cactus(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Guitar_Cactus.png", 1)

        self.center_x = 1500
        self.center_y = 300

class Trumpet_Cactus(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Trumpet_Cactus.png", 0.25)

        self.center_x = 2500
        self.center_y = 700

class Violin_Cactus(arcade.Sprite):
    def __init__(self, scale):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Violin_cactus.png", scale)

        self.center_x = 3000
        self.center_y = 500

class queue_stuff():
    def __init__(self) -> None:
        self.q = []

    def add_to_queue(self, item):
        i = item
        return self.q.append(i)
    
    def remove_from_queue(self):
        return self.q.pop()

    def get_queue(self):
        return self.q
    
    def check_order(self, queue, correct_order):
        # for i in queue:
        #     print(i)
        if list(correct_order) == queue:
            print(True)
        else: 
            print(correct_order)
            print(queue)

queue = queue_stuff()

class IndicatorBar():
    def __init__(self, sprite_list):
        border_size = 4
        self.box_width = 150
        self.box_height = 40
        self.fullness= 1.0  

        self.background_box = arcade.SpriteSolidColor(
            self.box_width + border_size,
            self.box_height + border_size,
            arcade.color.BLACK,
        )
        self.full_box= arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            arcade.color.BLUE,
        )

        self.background_box.position = (self.box_width // 2 + 10, self.box_height // 2 + 10)
        self.full_box.position = (self.box_width // 2 + 10, self.box_height // 2 + 10)

        sprite_list.append(self.background_box)
        sprite_list.append(self.full_box)

    def get_fullness(self):
        return self.fullness

    def set_fullness(self, new_fullness):
        self.fullness= new_fullness
        self.full_box.width = self.box_width * new_fullness
        self.full_box.left = 10
   
class GameView(arcade.Window):
    def __init__(self):
        super().__init__(1000, 650, "Chur")
        arcade.set_background_color(arcade.csscolor.DARK_GRAY)

        self.scene = None
        self.player = None
        self.senorita = None
        self.tile_map = None
        self.camera = None
        self.gui_camera = None
        self.items_order = None
        self.black_items = None

        self.taco_timer = 0.0 
        self.taco_spawn_interval = 30
        self.taco_list = arcade.SpriteList()
        self.llama_list = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.hint_list = arcade.SpriteList()
        self.water_list = arcade.SpriteList()

        self.decrease_rate = 0.01
        self.health_bar = IndicatorBar(sprite_list=self.bar_list)

    
    def setup(self):
        layer_options = {
            "Platform" : {"use_spatial_hash" : True}
        }

        self.camera = arcade.Camera(1000, 650)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.wall_list = arcade.SpriteList()

        self.tile_map =  arcade.load_tilemap("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Map.tmx",
                                             scaling=0.5,
                                             layer_options=layer_options
                                            )
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player = Player()
        self.scene.add_sprite("Player", self.player)

        self.senorita = Senorita_monke()
        self.scene.add_sprite('Senorita', self.senorita)

        self.guitar = Guitar_Cactus()
        self.scene.add_sprite('Guitar', self.guitar)

        self.trumpet = Trumpet_Cactus()
        self.scene.add_sprite('Trumpet', self.trumpet)

        self.violin = Violin_Cactus(scale = 0.25)
        self.scene.add_sprite("Violin", self.violin)

        self.water = Water(center_x= 300, center_y= 600)
        self.scene.add_sprite("Water", self.water)
        
        for y in range(550, 560, 10):
            for x in range(600, 1200, 200):
                self.llama = Llama(center_x= x, center_y= y)
                self.scene.add_sprite("Llama", self.llama)

        self.collect_coin_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Part 1.wav")
        self.trumpet_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Part 2.wav")
        self.violin_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Part 3.wav")
        self.full_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Full.wav")
        self.taco_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/Taco_song.wav")

        self.black_items = {"Guitar": (BLACK_GUITAR, 0.5),
                       "Violin" : (BLACK_VIOLIN, 0.18),
                        "Trumpet" : (BLACK_TRUMPET, 0.25)
                    }
        items = ["Guitar", "Violin", "Trumpet"]
        random.shuffle(items)  
        self.items_order = items

        self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player,
        platforms=self.scene["Senorita"],
        gravity_constant=1,
        walls=self.scene["Platform"]
        )
    
    def show_queue(self, image, scale):
        health = arcade.Sprite(image, scale)
        gap_between_sprites = 70 
        health.center_x = 90 + len(self.health_list) * gap_between_sprites
        health.center_y =  580
        self.health_list.append(health)

    def show_hint(self, image, scale):
        health = arcade.Sprite(image, scale)
        gap_between_sprites = 70 
        health.center_x = 800 + len(self.hint_list) * gap_between_sprites
        health.center_y =  580
        self.hint_list.append(health)

    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.scene.update()
        self.center_camera_to_player()

        self.taco_timer += delta_time
        if self.taco_timer > self.taco_spawn_interval:
            self.spawn_llama()
            self.spawn_taco()
            self.taco_timer = 0

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene["Guitar"]
        )
        trumpet_hit = arcade.check_for_collision_with_list(self.player, self.scene["Trumpet"])
        violin_hit = arcade.check_for_collision_with_list(self.player, self.scene["Violin"])
        senorita_hit = arcade.check_for_collision_with_list(self.player, self.scene["Senorita"])
        taco_hit = arcade.check_for_collision_with_list(self.player, self.taco_list)
        water_hit = arcade.check_for_collision_with_list(self.player, self.scene["Water"])
        llama_hit = arcade.check_for_collision_with_list(self.player, self.scene["Llama"])

        for llama in llama_hit:
            llama.remove_from_sprite_lists()
            if self.items_order:
                instrument = self.items_order.pop(0)
                file_path, scale = self.black_items[instrument]
                self.show_hint(file_path, scale)

        for water in water_hit:
            water.remove_from_sprite_lists()
            new_fullness = self.health_bar.get_fullness() + 0.50
            self.health_bar.set_fullness(max(0.0, new_fullness))

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            queue.add_to_queue(item="Guitar")
            arcade.play_sound(self.collect_coin_sound)
            self.show_queue("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Guitar_Cactus.png", 0.5)

        for trumpet in trumpet_hit:
            trumpet.remove_from_sprite_lists()
            queue.add_to_queue(item="Trumpet")
            arcade.play_sound(self.trumpet_sound)
            self.show_queue("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Trumpet_Cactus.png", 0.25)

        for violin in violin_hit:
            violin.remove_from_sprite_lists()
            queue.add_to_queue(item="Violin")
            self.violins = arcade.play_sound(self.violin_sound)
            self.show_queue("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Violin_cactus.png", 0.18)

        for taco in taco_hit:
            taco.remove_from_sprite_lists()
            new_fullness = self.health_bar.get_fullness() - 0.10
            self.health_bar.set_fullness(max(0.0, new_fullness))
            self.player.center_x = 120
            self.player.center_y = 430

        for senorita in senorita_hit:
            self.queue = queue.get_queue()
            queue.check_order(self.queue, self.items_order)
            senorita.remove_from_sprite_lists()
            arcade.play_sound(self.full_sound)

        for taco in self.taco_list:
            taco.center_y -= random.randint(1, 3)
        
        new_fullness = self.health_bar.get_fullness() - self.decrease_rate * delta_time
        self.health_bar.set_fullness(max(0.0, new_fullness))

        if self.health_bar.get_fullness() <= 0:
            self.player.center_x = 120

    def spawn_taco(self):
        for i in range(20):
            taco_type = random.choice(["Flamin_Taco", "Taco"])
            if taco_type == "Flamin_Taco":
                file = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Flamin_Taco.png"
            else:
                file = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Assets/Taco.png"

            taco = arcade.Sprite(file, 1)
            taco.center_x = self.player.center_x + random.randint(-550, 550)
            taco.center_y = random.randint(1000, 2000)

            self.taco_list.append(taco)
    
    def spawn_llama(self):
        arcade.play_sound(self.taco_sound)


    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.wall_list.draw()
        self.taco_list.draw()
        self.gui_camera.use()
        self.health_list.draw()
        self.hint_list.draw()
        self.bar_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.player.change_x =  5 
        elif symbol == arcade.key.A:
            self.player.change_x = - 5 
        elif symbol == arcade.key.W:
            self.player.change_y = 15

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.player.change_x =  0
        elif symbol == arcade.key.A:
            self.player.change_x = 0
        elif symbol == arcade.key.W:
            self.player.change_y = 0
    
    def center_camera_to_player(self):
        camera_x = self.player.center_x - 1000 / 2
        camera_y = self.player.center_y - 650 / 2
        if camera_x < 0:
            camera_x = 0
        if camera_y < 15:
            camera_y = 15
        self.camera.move_to((camera_x, camera_y))


def main():
    window = GameView()
    queue = queue_stuff()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
