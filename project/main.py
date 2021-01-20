from tkinter import Tk, Canvas, Label
from pynput.keyboard import Key, Listener
from game_manager import GameManager


class App:

    def __init__(self):
        self.setup_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.key_listener()
        self.move_monsters()  # enable: monsters move periodically
        self.root.mainloop()

    def setup_gui(self):
        self.create_window()
        self.game_manager = GameManager()
        self.create_canvas()
        self.create_stat_bar()
        self.create_description()
        self.create_info_bar()

    def create_window(self):
        self.root = Tk()
        self.root.title("Wanderer by Mark Ambrus")

    def create_canvas(self):
        self.size = self.game_manager.area.size
        self.canvas = Canvas(self.root, width=self.size, height=self.size)
        self.canvas.pack()
        self.fill_canvas()

    def fill_canvas(self):
        self.game_manager.area.draw_map(self.canvas)
        self.game_manager.spawn_characters(self.canvas)

    def create_stat_bar(self):
        self.hero_stat_bar = Label(text=self.game_manager.hero.introduce())
        self.hero_stat_bar.pack()

    def create_description(self):
        self.game_description = Label(text='''Welcome to the Wanderer game!
            Let's play! Use the arrow keys or WASD to move the hero.
            Cross path with monsters to fight them.
            Collect the key and kill the boss to go to the next level.''')
        self.game_description.pack()

    def create_info_bar(self):
        self.progress_info = Label(text="Area: " +
                                   str(self.game_manager.area_number) +
                                   " | " +
                                   str(self.game_manager.kill_count) +
                                   " monsters slayed.")
        self.progress_info.pack()

    def key_listener(self):
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.focus_set()

    def on_key_press(self, e):
        # W or w or up arrow key
        if e.keycode == 87 or e.keycode == 119 or e.keycode == 8320768:
            direction = 'up'
        # S or s or down arrow key
        elif e.keycode == 83 or e.keycode == 115 or e.keycode == 8255233:
            direction = 'down'
        # A or a or left arrow key
        elif e.keycode == 65 or e.keycode == 97 or e.keycode == 8124162:
            direction = 'left'
        # D or d or right arrow key
        elif e.keycode == 68 or e.keycode == 100 or e.keycode == 8189699:
            direction = 'right'
        else:
            return
        self.game_turn(direction)

    def game_turn(self, direction):
        self.game_manager.set_hero_position(self.canvas, direction)
        self.after_move()

    def move_monsters(self):
        wait = self.calculate_wait()
        self.game_manager.move_monsters(self.canvas)
        self.after_move()
        self.root.after(wait, self.move_monsters)

    def calculate_wait(self):
        difficulty = (self.game_manager.area_number - 1) * 40
        wait = 1500 - difficulty  # max 1.5 sec wait
        min_wait = 300  # min 0.3 sec wait
        if wait < min_wait:
            return min_wait
        else:
            return wait

    def after_move(self):
        self.check_hero_death()
        self.game_manager.check_next_area(self.canvas)
        self.config_labels()

    def check_hero_death(self):
        if self.game_manager.hero.current_health <= 0:
            self.canvas.delete("all")
            self.game_manager = GameManager()
            self.fill_canvas()

    def config_labels(self):
        self.progress_info.config(text="Area: " +
                                  str(self.game_manager.area_number) +
                                  " | " +
                                  str(self.game_manager.kill_count) +
                                  " monsters slayed.")
        self.hero_stat_bar.config(text=self.game_manager.hero.introduce())

    def callback(self):
        self.root.quit()


app = App()
