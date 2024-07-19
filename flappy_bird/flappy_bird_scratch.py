import arcade, random, copy

#initialize game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Flappy Bird"

RECT_WIDTH = 100
RECT_HEIGHT = SCREEN_HEIGHT
RECT_COLOR = arcade.color.BLUE #bottom
RECT_COLOR_2 = arcade.color.BLACK #top

BACKGROUND_COLOR = arcade.color.RED

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT * (-0.3 + 0.4 * random.random())
        self.change_x = 0
        self.change_y = 0
        self.i = 1

    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        if self.x <= 0:
            self.refill()

    def refill(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT * (-0.3 + 0.4 * random.random())

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, RECT_WIDTH, RECT_HEIGHT, RECT_COLOR)

class Bird:
    pass

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.pipe_bottom = Pipe()
        self.pipe_top = copy.deepcopy(self.pipe_bottom)
        self.pipe_top.y = self.pipe_bottom.y+1.2*SCREEN_HEIGHT

        self.background_color = BACKGROUND_COLOR

    def on_update(self, delta_time):
        self.pipe_top.update()
        self.pipe_bottom.update() #update to match top pipe

    def on_draw(self):
        self.clear()
        self.pipe_bottom.draw()
        self.pipe_top.draw()
        #arcade.draw_rectangle_filled(test.x, test.y, RECT_WIDTH, RECT_HEIGHT, arcade.color.PURPLE)
        #arcade.draw_rectangle_filled(test_2.x, test_2.y, RECT_WIDTH, RECT_HEIGHT, arcade.color.ORANGE)

#test pipe height for placement        
'''
test = Pipe()
test.y = -0.3*SCREEN_HEIGHT
test_2 = copy.deepcopy(test)
test_2.y = 1.3*SCREEN_HEIGHT

'''

def main():
    Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
    
    print('Game started')

if __name__ == '__main__':
    main()