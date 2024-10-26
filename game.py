import arcade
import arcade.gui
from queue import Queue
import random
import time
import pathlib

SCREEN_HEIGHT = 650
SCREEN_WIDTH = 1000
HEALTH_DECREASE_RATE = 0.075

PARENT_DIR = pathlib.Path(__file__).parent

ASSETS = {
    "BLACK_GUITAR": (PARENT_DIR / "Assets/Guitar_Cactus_Black.png",0.5),
    "BLACK_TRUMPET":(PARENT_DIR / "Assets/Trumpet_Cactus_Black.png",0.25),
    "BLACK_VIOLIN": (PARENT_DIR / "Assets/Violin_cactus_Black.png",0.18),
    "MONKE": PARENT_DIR / "Assets/MONKE.png",
    "LLAMA": (PARENT_DIR / "Assets/llama.png",0.1),
    "SENORITA": (PARENT_DIR / "Assets/Senorita_MONKE.png",0.65),
    "Guitar": (PARENT_DIR / "Assets/Guitar_Cactus.png", 0.75),
    "Trumpet": (PARENT_DIR / "Assets/Trumpet_Cactus.png",0.25),
    "Violin": (PARENT_DIR / "Assets/Violin_cactus.png", 0.18),
    "FLAMIN_TACO": (PARENT_DIR / "Assets/Flamin_Taco.png",1),
    "TACO": (PARENT_DIR / "Assets/Taco.png",1),
    "AUDIO_1": PARENT_DIR / "audio/La Bamba Part 1.wav",
    "AUDIO_2": PARENT_DIR / "audio/La Bamba Part 2.wav",
    "AUDIO_3": PARENT_DIR / "audio/La Bamba Part 3.wav",
    "AUDIO_FULL": PARENT_DIR / "audio/La Bamba Full.wav",
    "TACO_SOUND": PARENT_DIR / "audio/Taco_song.wav"
}

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(PARENT_DIR / "./Assets/MONKE.png", 
                         0.15
                        )
        self.center_x = 120
        self.center_y = 400

class Sprites(arcade.Sprite):
    def __init__(self, asset, center_x, center_y):
        filepath, scale = asset
        super().__init__(filepath, scale)
        self.center_x = center_x
        self.center_y = center_y


class queue_stuff():
    def __init__(self) -> None:
        self.q = []

    def add_to_queue(self, item):
        return self.q.append(item)
    
    def remove_from_queue(self):
        return self.q.pop()

    def get_queue(self):
        return self.q
    
    def clear_queue(self):
        return self.q.clear()
    
    def check_order(self, queue, correct_order):
        if list(correct_order) == queue:
            return True
        else: 
            return False

queue = queue_stuff()

class IndicatorBar():
    def __init__(self, sprite_list):
        border_size = 4
        self.box_width = 978
        self.box_height = 30
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

class Introduction(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameFinished(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Game Finished!", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

class GameOver(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Game Over", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
   
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.DARK_GRAY)

        self.scene = None
        self.player = None
        self.senorita = None
        self.tile_map = None
        self.camera = None
        self.gui_camera = None
        self.items_order = None
        self.correct_order = None
        self.black_items = None
        self.centre_x = 0

        self.taco_timer = 0.0 
        self.taco_spawn_interval = 5
        self.taco_list = arcade.SpriteList()
        self.llama_list = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.hint_list = arcade.SpriteList()
        self.water_list = arcade.SpriteList()
        self.level = 1
        self.score= 0

        self.health_bar = IndicatorBar(sprite_list=self.bar_list)

    
    def setup(self):
        layer_options = {
            "Platform" : {"use_spatial_hash" : True}
        }

        self.camera = arcade.Camera(1000, 650)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.wall_list = arcade.SpriteList()

        self.tile_map =  arcade.load_tilemap(PARENT_DIR / f"./Map{self.level}.tmx",
                                             scaling=0.5,
                                             layer_options=layer_options
                                            )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player = Player()
        self.scene.add_sprite("Player", self.player)

        self.senorita = Sprites(ASSETS["SENORITA"],center_x=3200,center_y=500)
        self.scene.add_sprite('Senorita', self.senorita)

        self.guitar = Sprites(ASSETS["Guitar"], center_x=1500,center_y=500)
        self.scene.add_sprite('Guitar', self.guitar)

        self.trumpet = Sprites(ASSETS["Trumpet"],center_x=2500,center_y=500)
        self.scene.add_sprite('Trumpet', self.trumpet)

        self.violin = Sprites(ASSETS["Violin"], center_x=3000,center_y=500)
        self.scene.add_sprite("Violin", self.violin)

        for x in range(600, 1200, 200):
            self.llama = Sprites(ASSETS['LLAMA'], center_x= x, center_y= 560)
            self.scene.add_sprite("Llama", self.llama)

        self.audio_1 = arcade.load_sound(ASSETS['AUDIO_1'])
        self.audio_2 = arcade.load_sound(ASSETS['AUDIO_2'])
        self.audio_3 = arcade.load_sound(ASSETS['AUDIO_3'])
        
        self.full_sound = arcade.load_sound(ASSETS['AUDIO_FULL'])
        self.taco_sound = arcade.load_sound(ASSETS['TACO_SOUND'])

        if self.correct_order is not None:
            self.correct_order.clear()
            self.items_order.clear()
            self.health_list.clear()
            self.hint_list.clear()
            queue.clear_queue()

        self.black_items = {"Guitar": (ASSETS["BLACK_GUITAR"]),
                            "Violin" : (ASSETS["BLACK_VIOLIN"]),
                            "Trumpet" : (ASSETS["BLACK_TRUMPET"])
                            }
        items = ["Guitar", "Violin", "Trumpet"]

        random.shuffle(items)
        songs = [self.audio_1, self.audio_2, self.audio_3]
        self.items_order = items
        self.correct_order = items.copy()

        self.item_audio = dict(zip(items, songs))
 
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color":  arcade.color.ORANGE_RED,
            "bg_color_pressed": arcade.color.GAINSBORO,
            "border_color_pressed": arcade.color.PICTON_BLUE,
            "font_color_pressed": arcade.color.BLACK,
        }

        self.v_box = arcade.gui.UIBoxLayout()
        reset_button = arcade.gui.UIFlatButton(text="Reset", width=80, style=default_style)
        self.v_box.add(reset_button)

        reset_button.on_click = self.reset

        self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player,
        platforms=self.scene["Senorita"],
        gravity_constant=1,
        walls=self.scene["Platform"],
        ladders=self.scene["Ladders"]
        )

    def reset(self, event):
        self.health_list.clear()
        queue.clear_queue()
        self.respawn_cacti()
        self.centre_x -=1000
        self.button()

    def respawn_cacti(self):
        self.guitar = Sprites(ASSETS['Guitar'], center_x=1500,center_y=500)
        self.scene.add_sprite('Guitar', self.guitar)

        self.trumpet = Sprites(ASSETS["Trumpet"],center_x=2500,center_y=500)
        self.scene.add_sprite('Trumpet', self.trumpet)

        self.violin = Sprites(ASSETS["Violin"], center_x=3000,center_y=500)
        self.scene.add_sprite("Violin", self.violin)

    def button(self):
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                align_x= self.centre_x + 45,
                align_y= -50,
                child=self.v_box)
        )

    def show_queue(self, asset):
        path, scale = asset
        health = arcade.Sprite(path, scale)
        gap_between_sprites = 70 
        health.center_x = 90 + len(self.health_list) * gap_between_sprites
        self.centre_x = health.center_x
        health.center_y =  580
        self.health_list.append(health)

    def show_hint(self, image, scale):
        health = arcade.Sprite(image, scale)
        gap_between_sprites = 70 
        health.center_x = 800 + len(self.hint_list) * gap_between_sprites
        health.center_y =  580
        self.hint_list.append(health)
    
    def play_audio(self, item):
        keys=list(self.item_audio.keys())
        values=list(self.item_audio.values())
        path= values[keys.index(item)]
        arcade.play_sound(path)

    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.scene.update()
        self.center_camera_to_player()

        self.taco_timer += delta_time
        if self.taco_timer > self.taco_spawn_interval:
            self.spawn_taco()
            self.taco_timer = 0
       
        for senorita in arcade.check_for_collision_with_list(self.player, self.scene["Senorita"]):
            self.queue = queue.get_queue()

            if self.level == 2 and queue.check_order(self.queue, self.correct_order) is True:
                end_view = GameFinished()
                self.window.show_view(end_view)
                
            elif queue.check_order(self.queue, self.correct_order) is True:
                senorita.remove_from_sprite_lists()
                self.level += 1
                self.setup()
                # arcade.play_sound(self.full_sound)
            else:
                self.health_list.clear()
                queue.clear_queue()
                self.respawn_cacti()

        for taco in self.taco_list:
            taco.center_y -= random.randint(1, 3)

        new_fullness = self.health_bar.get_fullness() - HEALTH_DECREASE_RATE * delta_time
        self.health_bar.set_fullness(max(0.0,new_fullness))

        # if self.health_bar.get_fullness() == 0:
        #     end_view = GameOver()
        #     self.window.show_view(end_view)

        self.check_collisions()

    def check_collisions(self):
        for sprite_name in ["Guitar", "Trumpet", "Violin"]:
            hit_list = arcade.check_for_collision_with_list(self.player, self.scene[sprite_name])
            for item in hit_list:
                item.remove_from_sprite_lists()
                queue.add_to_queue(item=sprite_name)
                self.play_audio(sprite_name)
                self.show_queue(ASSETS[sprite_name])
                self.button()

        # for taco in arcade.check_for_collision_with_list(self.player, self.taco_list):
        #     taco.remove_from_sprite_lists()
        #     new_fullness = self.health_bar.get_fullness() - 0.10
        #     self.health_bar.set_fullness(max(0.0, new_fullness))
        #     self.player.center_x = 120
        #     self.player.center_y = 430

        for llama in arcade.check_for_collision_with_list(self.player, self.scene["Llama"]):
            llama.remove_from_sprite_lists()
            if self.items_order:
                instrument = self.items_order.pop(0)
                file_path, scale = self.black_items[instrument]
                self.show_hint(file_path, scale)

        for water in arcade.check_for_collision_with_list(self.player, self.scene["Water"]):
            water.remove_from_sprite_lists()
            new_fullness = self.health_bar.get_fullness() + 0.5
            self.health_bar.set_fullness(min(1.0, new_fullness)) 
        
        for rose in arcade.check_for_collision_with_list(self.player, self.scene["Roses"]):
            rose.remove_from_sprite_lists()
            self.score += 10
        


    def spawn_taco(self):
        for i in range(20):
            taco_type = random.choice(["FLAMIN_TACO", "TACO"])

            taco = Sprites(ASSETS[taco_type],
                           center_x=self.player.center_x + random.randint(-550, 550),
                           center_y=random.randint(1000, 2000))
            self.taco_list.append(taco)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.wall_list.draw()
        self.taco_list.draw()
        self.scene['Hidden'].draw()
        self.gui_camera.use()
        self.health_list.draw()
        self.hint_list.draw()
        self.bar_list.draw()
        self.manager.draw()

        arcade.draw_text(
            f"Score: {self.score} ", 
            50,
            50, 
            font_size=25
            )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.player.change_x =  5 
        elif symbol == arcade.key.A:
            self.player.change_x = - 5 
        elif symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = 15
            elif self.physics_engine.is_on_ladder():
                self.player.change_y = 5
        elif symbol == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -5

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
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Strummin'n for amor")
    start_view = Introduction()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
