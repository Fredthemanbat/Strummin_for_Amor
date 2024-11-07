import random
import pathlib
import arcade
import arcade.gui

SCREEN_HEIGHT = 650
SCREEN_WIDTH = 1000
HEALTH_DECREASE_RATE = 0.02  # speed at which health decreases
TACO_SPAWN_INTERVAL = 40  # the time between taco spawns

PARENT_DIR = pathlib.Path(__file__).parent

# dictionary of all the assets
# sprites have the scale included in a tuple
ASSETS = {
    "PLAYER": (PARENT_DIR / "./Assets/MONKE.png", 0.15),
    "MONKE": PARENT_DIR / "Assets/MONKE.png",
    "LLAMA": (PARENT_DIR / "Assets/llama.png", 0.1),
    "SENORITA": (PARENT_DIR / "Assets/Senorita_MONKE.png", 0.65),
    "Guitar": (PARENT_DIR / "Assets/Guitar_Cactus.png", 0.75),
    "Trumpet": (PARENT_DIR / "Assets/Trumpet_Cactus.png", 0.25),
    "Violin": (PARENT_DIR / "Assets/Violin_cactus.png", 0.18),
    "FLAMIN_TACO": (PARENT_DIR / "Assets/Flamin_Taco.png", 1),
    "TACO": (PARENT_DIR / "Assets/Taco.png", 1),
    "AUDIO_1": PARENT_DIR / "audio/La Bamba Part 1.wav",
    "AUDIO_2": PARENT_DIR / "audio/La Bamba Part 2.wav",
    "AUDIO_3": PARENT_DIR / "audio/La Bamba Part 3.wav",
    "AUDIO_FULL": PARENT_DIR / "audio/La Bamba Full.wav",
}


class Sprites(arcade.Sprite):
    """A function that creates the sprites"""

    def __init__(self, asset, center_x, center_y):
        filepath, scale = asset  # seperates the values in the tuple
        super().__init__(filepath, scale)
        self.center_x = center_x
        self.center_y = center_y


class QueueStuff:
    def __init__(self) -> None:
        """Sets up the queue"""
        self.q = []

    def add_to_queue(self, item):
        """Ends the item to the end of the queue and returns the new one"""
        return self.q.append(item)

    def remove_from_queue(self):
        """Returns the queue with the first item removed"""
        return self.q.pop()

    def get_queue(self):
        """Returns the full queue"""
        return self.q

    def clear_queue(self):
        """Clears the queue"""
        return self.q.clear()

    def check_order(self, queue, correct_order):
        """Checks the order of the queue against the correct order list"""
        if list(correct_order) == queue:
            return True
        else:
            return False


# creates a queue instance
queue = QueueStuff()


class IndicatorBar:
    def __init__(self, sprite_list):
        """
        Sets up the outline rectangle
        and the blue inner rectangle that represents the health
        """
        border_size = 4
        self.box_width = 978
        self.box_height = 30
        self.fullness = 1.0

        self.background_box = arcade.SpriteSolidColor(
            self.box_width + border_size,
            self.box_height + border_size,
            arcade.color.BLACK,
        )
        self.full_box = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            arcade.color.BLUE,
        )
        self.background_box.position = (
            self.box_width // 2 + 10,
            self.box_height // 2 + 10,
        )
        self.full_box.position = (self.box_width // 2 + 10, self.box_height // 2 + 10)

        sprite_list.append(self.background_box)
        sprite_list.append(self.full_box)

    def get_fullness(self):
        """Returns the current fullness of the health bar"""
        return self.fullness

    def set_fullness(self, new_fullness):
        """Sets the new fullness for the health bar"""
        self.fullness = new_fullness
        self.full_box.width = self.box_width * new_fullness

        # anchors the health bar to the left of the screen
        # so that it only decreases from the right
        self.full_box.left = 10


class Introduction(arcade.View):
    def on_show_view(self):
        """Sets up the 'Introduction' view"""
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """Draws the instructions"""
        self.clear()
        arcade.draw_text(
            "Welcome!",
            self.window.width / 2,
            self.window.height / 2 + 25,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Collect the cacti in the right order to impress Senorita. "
            "Watch out though as falling foes and dehydration try to stop you. "
            "Use the WASD keys to move.",
            self.window.width / 2,
            self.window.height / 2 - 25,
            arcade.color.WHITE,
            multiline=True,
            width=700,
            font_size=20,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to advance",
            self.window.width / 2,
            self.window.height / 2 - 130,
            arcade.color.REDWOOD,
            font_size=20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Sets up the game when the window is clicked"""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameFinished(arcade.View):
    """Thic class handles the game over view"""

    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_show_view(self):
        """Sets up th view for the 'Game Finsished' screen"""
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """Draws the text"""
        self.clear()
        arcade.draw_text(
            "Game Finished!",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Score: {self.score}",
            self.window.width / 2,
            self.window.height / 2 - 45,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Made by Braeden",
            self.window.width / 2,
            self.window.height / 2 - 100,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )


class GameOver(arcade.View):
    def on_show_view(self):
        """Sets up the 'Game Over' view"""
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """Draws the view"""
        self.clear()
        arcade.draw_text(
            "Game Over",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Restarts the game when the screen is clicked"""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # sets the background
        arcade.set_background_color(arcade.csscolor.DARK_GRAY)
        self.scene = None
        self.player = None
        self.llama = None
        self.senorita = None
        self.tile_map = None
        self.camera = None
        self.gui_camera = None
        self.items_order = None
        self.correct_order = None
        self.current_sound = None
        self.health_bar = None
        self.button_centre_x = 0  # x location of the Reset button
        self.collected_items = []
        self.level = 1
        self.score = 0
        self.taco_timer = 0.0  # time since last taco drop

        # Sprite lists
        self.taco_list = arcade.SpriteList(use_spatial_hash=True)
        self.llama_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.bar_list = arcade.SpriteList()
        self.display_queue = arcade.SpriteList()
        self.hint_list = arcade.SpriteList()
        self.water_list = arcade.SpriteList(use_spatial_hash=True)

    def setup(self):
        """Sets up the main game logic"""

        # Loads in the Tiled Map
        layer_options = {
            "Platform": {"use_spatial_hash": True},
            "Roses": {"use_spatial_hash": True},
            "Water": {"use_spatial_hash": True},
            "Hidden": {"use_spatial_hash": True},
            "Ladders": {"use_spatial_hash": True},
        }

        self.tile_map = arcade.load_tilemap(
            PARENT_DIR / f"./Map{self.level}.tmx",
            scaling=0.5,
            layer_options=layer_options,
        )
        # sets up the scene with the correct level
        # Sprites will be added to the scene for simplicity
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # sets up the camera
        self.camera = arcade.Camera(1000, 650)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # PLAYER
        self.player = Sprites(ASSETS["PLAYER"], center_x=120, center_y=400)
        self.scene.add_sprite("Player", self.player)

        # sets up the health bar
        self.health_bar = IndicatorBar(sprite_list=self.bar_list)
        # takes the specified layers on the map and replaces them with the respective sprites
        # coordinates of sprite as specified on the map
        # Spawn in Senorita
        for sign in self.scene["Senoritas"]:
            senorita_position = sign.position
            self.senorita = Sprites(
                ASSETS["SENORITA"],
                center_x=senorita_position[0],
                center_y=senorita_position[1],
            )
            self.scene.add_sprite("Senorita", self.senorita)
        self.scene.remove_sprite_list_by_name("Senoritas")

        # Spawns in the Llamas
        for sign in self.scene["Llamas"]:
            llama_position = sign.position
            self.llama = Sprites(
                ASSETS["LLAMA"], center_x=llama_position[0], center_y=llama_position[1]
            )
            self.scene.add_sprite("Llama", self.llama)
        self.scene.remove_sprite_list_by_name("Llamas")

        # list of collected items cleared when game reset
        # makes sure it's empty
        self.collected_items.clear()
        # spawns in the cacti
        self.spawn_cacti()

        # loads in all the audio
        self.audio_1 = arcade.load_sound(ASSETS["AUDIO_1"])
        self.audio_2 = arcade.load_sound(ASSETS["AUDIO_2"])
        self.audio_3 = arcade.load_sound(ASSETS["AUDIO_3"])
        self.full_sound = arcade.load_sound(ASSETS["AUDIO_FULL"])

        # if items have been collected, reset them when moving to the next level
        if self.correct_order is not None:
            self.correct_order.clear()
            self.items_order.clear()
            self.display_queue.clear()
            self.hint_list.clear()
            queue.clear_queue()

        # Randomly shuffles the cacti and creates the correct order
        items = ["Guitar", "Violin", "Trumpet"]
        random.shuffle(items)
        songs = [self.audio_1, self.audio_2, self.audio_3]
        self.items_order = items  # list with the  order of the items
        # this list is for the as to not effect the correct order
        self.correct_order = items.copy()
        # creates a dictionary of items with their respective songs
        self.item_audio = dict(zip(items, songs))

        # creates a manager for the reset button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # the style for the reset button
        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.ORANGE_RED,
            "bg_color_pressed": arcade.color.GAINSBORO,
            "border_color_pressed": arcade.color.PICTON_BLUE,
            "font_color_pressed": arcade.color.BLACK,
        }
        # sets up the reset button
        self.v_box = arcade.gui.UIBoxLayout()
        self.reset_button = arcade.gui.UIFlatButton(
            text="Reset", width=80, style=default_style
        )
        self.v_box.add(self.reset_button)

        self.reset_button.on_click = self.reset

        # The physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.scene["Senorita"],
            gravity_constant=1,
            walls=self.scene["Platform"],
            ladders=self.scene["Ladders"],
        )

    def reset(self, event):
        """
        Called when the rest button is pressed
        Resets the queue
        """
        self.display_queue.clear()
        queue.clear_queue()
        self.respawn_cacti()
        if self.current_sound:
            arcade.stop_sound(self.current_sound)
        self.button_centre_x -= 1000
        self.button()

    def spawn_cacti(self):
        """Spawns the cacti in the fisrt time"""
        i = 0
        for cactus in self.scene["Cactus"]:
            cactus_position = cactus.position
            if i == 0:
                self.guitar = Sprites(
                    ASSETS["Guitar"],
                    center_x=cactus_position[0],
                    center_y=cactus_position[1],
                )
                self.scene.add_sprite("Guitar", self.guitar)
                self.guitar_pos = cactus_position
                i += 1
            elif i == 1:
                self.trumpet = Sprites(
                    ASSETS["Trumpet"],
                    center_x=cactus_position[0],
                    center_y=cactus_position[1],
                )
                self.scene.add_sprite("Trumpet", self.trumpet)
                self.trumpet_pos = cactus_position
                i += 1
            else:
                self.violin = Sprites(
                    ASSETS["Violin"],
                    center_x=cactus_position[0],
                    center_y=cactus_position[1],
                )
                self.scene.add_sprite("Violin", self.violin)
                self.violin_pos = cactus_position

    def respawn_cacti(self):
        """
        Respawns in the cacti
        Stores the location of each cacti in order to respawn in the correct place
        """
        for i in self.collected_items:
            if i == "Guitar":
                self.guitar = Sprites(
                    ASSETS["Guitar"],
                    center_x=self.guitar_pos[0], # self.guitar_pos is a tuple
                    center_y=self.guitar_pos[1],
                )
                self.scene.add_sprite("Guitar", self.guitar)

            elif i == "Trumpet":
                self.trumpet = Sprites(
                    ASSETS["Trumpet"],
                    center_x=self.trumpet_pos[0], # self.trumpet_pos is a tuple
                    center_y=self.trumpet_pos[1],
                )
                self.scene.add_sprite("Trumpet", self.trumpet)

            elif i == "Violin":
                self.violin = Sprites(
                    ASSETS["Violin"],
                    center_x=self.violin_pos[0], # self.violin_pos is a tuple
                    center_y=self.violin_pos[1],
                )
                self.scene.add_sprite("Violin", self.violin)

        # resets collect items as the queue is not cleared
        self.collected_items.clear()

    def button(self):
        """Adds the button to the button manager"""
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                align_x=self.button_centre_x + 45,
                align_y=-50,
                child=self.v_box,
            )
        )

    def show_queue(self, asset):
        """Shows the item that the player has collected in the order collected"""
        path, scale = asset
        health = arcade.Sprite(path, scale)
        gap_between_sprites = 70
        health.center_x = 90 + len(self.display_queue) * gap_between_sprites
        self.button_centre_x = health.center_x
        health.center_y = 580
        self.display_queue.append(health)

    def show_hint(self, image, scale):
        """Shows a hint of the correct order"""
        # creates the hint sprite
        # takes the file path adn converts it into string inorder to have the colour changed
        health = arcade.Sprite(str(image), scale)
        health.color = (
            arcade.csscolor.BLACK
        )  # Converts the sprite into a black silhouette
        gap_between_sprites = 70
        health.center_x = 800 + len(self.hint_list) * gap_between_sprites
        health.center_y = 580
        self.hint_list.append(health)

    def play_audio(self, item):
        """Play the correct audio for the collected item, stopping any currently playing audio."""
        # Stop the current sound if it is playing
        if self.current_sound:
            arcade.stop_sound(self.current_sound)

        # Get the new sound to play
        # Index the dicitonary to find the correct audio
        keys = list(self.item_audio.keys())
        values = list(self.item_audio.values())
        path = values[keys.index(item)]

        # Play the new sound and update the current sound tracker
        self.current_sound = arcade.play_sound(path)

    def on_update(self, delta_time: float):
        """Updates everything"""
        self.physics_engine.update()
        self.scene.update()
        self.center_camera_to_player()

        # spawns in the tacos after the spawn interval has passed
        self.taco_timer += delta_time
        if self.taco_timer > TACO_SPAWN_INTERVAL:
            self.spawn_taco()
            # reset the timer between drops
            self.taco_timer = 0

        # move the tacos down at different speeds
        for taco in self.taco_list:
            taco.center_y -= random.randint(1, 4)

        # decrease the health bar by the decrease rate and the time which has passed
        new_fullness = (
            self.health_bar.get_fullness() - HEALTH_DECREASE_RATE * delta_time
        )
        self.health_bar.set_fullness(max(0.0, new_fullness))

        # if the health bar has reached 0
        # player is reset to level 1 and game is finished
        if self.health_bar.get_fullness() == 0:
            self.level = 1
            end_view = GameOver()
            self.window.show_view(end_view)

        # checks all the collisions between the player and the sprite
        self.check_collisions()

    def check_collisions(self):
        """Check for collisions between player and sprite"""
        # cacti sprites
        for sprite_name in ["Guitar", "Trumpet", "Violin"]:
            hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene[sprite_name]
            )
            for item in hit_list:
                item.remove_from_sprite_lists()  # remove the collected sprite from the game
                queue.add_to_queue(
                    item=sprite_name
                )  # add the item collected to our queue
                self.collected_items.append(
                    sprite_name
                )  # add to the list of collected items
                self.play_audio(sprite_name)  # play the right sound
                self.show_queue(ASSETS[sprite_name])  # show the items in the queue
                self.button()  # spawn in the Reset button

        for taco in arcade.check_for_collision_with_list(self.player, self.taco_list):
            taco.remove_from_sprite_lists()
            # decrease the health bar by 0.25
            new_fullness = self.health_bar.get_fullness() - 0.25
            self.health_bar.set_fullness(max(0.0, new_fullness))
            # restarts the player back to the start
            self.player.center_x = 120
            self.player.center_y = 430

        for llama in arcade.check_for_collision_with_list(
            self.player, self.scene["Llama"]
        ):
            llama.remove_from_sprite_lists()
            if self.items_order:
                # remove the first item in the list of correct order
                # display this item as a hint
                instrument = self.items_order.pop(0)
                file_path, scale = ASSETS[instrument]
                self.show_hint(file_path, scale)

        # collisions between the water and the player
        for water in arcade.check_for_collision_with_list(
            self.player, self.scene["Water"]
        ):
            water.remove_from_sprite_lists()
            # increase the health bar by 0.5 when water collected
            new_fullness = self.health_bar.get_fullness() + 0.5
            self.health_bar.set_fullness(min(1.0, new_fullness))

        # collisions between the Roses and the player
        for rose in arcade.check_for_collision_with_list(
            self.player, self.scene["Roses"]
        ):
            # increases the score by 10
            rose.remove_from_sprite_lists()
            self.score += 10

        # logic around the senorita and/or changing levels
        for senorita in arcade.check_for_collision_with_list(
            self.player, self.scene["Senorita"]
        ):
            self.queue = queue.get_queue()

            if (
                self.level == 2
                and queue.check_order(self.queue, self.correct_order) is True
            ):
                # when the player is on the second level and has the correct order
                # the game is complete triggering the GameFinished view
                end_view = GameFinished(score=self.score)
                self.window.show_view(end_view)
                if self.current_sound:
                    arcade.stop_sound(self.current_sound)
                arcade.play_sound(self.full_sound)

            elif queue.check_order(self.queue, self.correct_order) is True:
                # if the player isn't on the second level but has the correct
                # order then when increase the level and set up the new level
                senorita.remove_from_sprite_lists()
                self.level += 1
                self.taco_timer = 0
                self.setup()
            else:
                # if the queue is not correct then everything is reset
                self.respawn_cacti()
                self.display_queue.clear()
                queue.clear_queue()
                self.button_centre_x -= 1000
                self.button()

    def spawn_taco(self):
        """Spawns in 20 tacos over the player"""
        for i in range(20):
            taco_type = random.choice(["FLAMIN_TACO", "TACO"])
            taco = Sprites(
                ASSETS[taco_type],
                center_x=self.player.center_x + random.randint(-550, 550),
                center_y=random.randint(1000, 2000),
            )
            self.taco_list.append(taco)

    def on_draw(self):
        """Draws everything"""
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.wall_list.draw()
        self.scene["Hidden"].draw()
        self.taco_list.draw()
        self.gui_camera.use()
        # everything drawn after the gui is relative to the screen
        self.display_queue.draw()
        self.hint_list.draw()
        self.bar_list.draw()  # health bar
        self.manager.draw()  # Reset button
        # draws the score
        arcade.draw_text(f"Score: {self.score} ", 50, 50, font_size=25)

    def on_key_press(self, symbol: int, modifiers: int):
        """Stuff to do when the button is pressed"""
        if symbol == arcade.key.D:
            self.player.change_x = 5
        elif symbol == arcade.key.A:
            self.player.change_x = -5
        elif symbol == arcade.key.W:
            if (
                self.physics_engine.can_jump()
            ):  # makes sures that the player is on the ground
                self.player.change_y = 15
            elif self.physics_engine.is_on_ladder():
                self.player.change_y = 5
        elif symbol == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -5

    def on_key_release(self, symbol: int, modifiers: int):
        """Reset everything when the key is released"""
        if symbol == arcade.key.D:
            self.player.change_x = 0
        elif symbol == arcade.key.A:
            self.player.change_x = 0
        elif symbol == arcade.key.W:
            self.player.change_y = 0

    def center_camera_to_player(self):
        """Moves the camera with the player"""
        camera_x = self.player.center_x - 1000 / 2
        camera_y = self.player.center_y - 650 / 2
        if camera_x < 0:
            camera_x = 0
        if camera_y < 15:
            camera_y = 15
        # keeps the camera centered over the player
        self.camera.move_to((camera_x, camera_y))


def main():
    """Set up the window and load up the game"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Strummin'n for amor")
    start_view = Introduction()
    window.show_view(start_view)
    arcade.run()

# runs the game
if __name__ == "__main__":
    main()
