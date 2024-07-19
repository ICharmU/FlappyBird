import arcade, random

#initialize game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Flappy Bird"

RECT_WIDTH = 100
RECT_HEIGHT = 300
RECT_COLOR = arcade.color.BLUE

BACKGROUND_COLOR = arcade.color.RED

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT * (1 + 8*random.random()) / 10
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        if self.x <= 0:
            self.refill()

    def refill(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT * (1 + 8*random.random()) / 10

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, RECT_WIDTH, RECT_HEIGHT, RECT_COLOR)

        
            
class Bird:
    pass

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.pipe = Pipe()
        self.background_color = BACKGROUND_COLOR

    def on_update(self, delta_time):
        self.pipe.update()

    def on_draw(self):
        self.clear()
        self.pipe.draw()

def main():
    Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
    print('Game started')

if __name__ == '__main__':
    main()