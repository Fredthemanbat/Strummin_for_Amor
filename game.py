import arcade
import arcade.gui
from queue import Queue
import random
import time

SCREEN_HEIGHT = 650
SCREEN_WIDTH = 1000

BLACK_GUITAR = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Guitar_Cactus_Black.png"
BLACK_TRUMPET = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Trumpet_Cactus_Black.png"
BLACK_VIOLIN = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Violin_cactus_Black.png"

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/MONKE.png", 
                         0.15
                        )

        self.center_x = 120
        self.center_y = 400

class Senorita_monke(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Senorita_MONKE.png",
                         0.65
                        )
        
        self.center_x = 1000
        self.center_y = 900

class Guitar_Cactus(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Guitar_Cactus.png", 1)

        self.center_x = 1500
        self.center_y = 300

class Trumpet_Cactus(arcade.Sprite):
    def __init__(self):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Trumpet_Cactus.png", 0.25)

        self.center_x = 2500
        self.center_y = 700

class Violin_Cactus(arcade.Sprite):
    def __init__(self, scale):
        super().__init__("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Violin_cactus.png", scale)

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
   
class GameView(arcade.Window):
    def __init__(self):
        super().__init__(1000, 650, "Chur")
        arcade.set_background_color(arcade.csscolor.DARK_GRAY)

        self.scene = None
        self.player = None
        self.senorita = None
        self.tile_map = None
        self.camera = None
        self.complete = 0
        self.gui_camera = None
        self.items_order = None

        self.taco_timer = 0.0 
        self.taco_spawn_interval = 10
        self.taco_list = arcade.SpriteList()
        self.llama_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    
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

        self.collect_coin_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Part 1.wav")
        self.trumpet_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Part 2.wav")
        self.violin_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Part 3.wav")
        self.full_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/La Bamba Full.wav")
        self.taco_sound = arcade.load_sound("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/audio/Taco_song.wav")

        black_items = {"Guitar": (BLACK_GUITAR, 0.5),
                       "Violin" : (BLACK_VIOLIN, 0.18),
                        "Trumpet" : (BLACK_TRUMPET, 0.25)
                    }
        items = ["Guitar", "Violin", "Trumpet"]
        random.shuffle(items)  
        self.items_order = items

        for item in self.items_order:
            file_path, scale = black_items[item]
            self.show_queue(file_path, scale)

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

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            queue.add_to_queue(item="Guitar")
            arcade.play_sound(self.collect_coin_sound)
            self.show_queue("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Guitar_Cactus.png", 0.5)
            self.complete += 1

        for trumpet in trumpet_hit:
            trumpet.remove_from_sprite_lists()
            queue.add_to_queue(item="Trupmet")
            arcade.play_sound(self.trumpet_sound)
            self.show_queue("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Trumpet_Cactus.png", 0.25)
            self.complete += 1

        for violin in violin_hit:
            violin.remove_from_sprite_lists()
            queue.add_to_queue(item="Violin")
            self.violins = arcade.play_sound(self.violin_sound)
            self.show_queue("/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Violin_cactus.png", 0.18)
            self.complete += 1

        for taco in taco_hit:
            taco.remove_from_sprite_lists()
            self.player.center_x = 120
            self.player.center_y = 400

        if self.complete == 3:
            for senorita in senorita_hit:
                self.queue = queue.get_queue()
                queue.check_order(self.queue, self.items_order)
                senorita.remove_from_sprite_lists()
                arcade.play_sound(self.full_sound)

        for taco in self.taco_list:
            taco.center_y -= random.randint(1, 3)

    def spawn_taco(self):
        for i in range(20):
            taco_type = random.choice(["Flamin_Taco", "Taco"])
            if taco_type == "Flamin_Taco":
                file = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Flamin_Taco.png"
            else:
                file = "/Users/braedenleung/Documents/Hello World/Strummin' for Amor/Strummin_for_Amor/Taco.png"

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
        self.manager.draw()


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
