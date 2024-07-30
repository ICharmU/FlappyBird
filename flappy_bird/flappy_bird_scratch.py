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
        self.change_x = -3
        self.change_y = 0

    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        #return True for out of bounds, False for in bounds
        if self.x < -RECT_WIDTH/2:
            return True
        return False

    def refill(self):
        self.x = SCREEN_WIDTH+RECT_WIDTH/2
        self.y = SCREEN_HEIGHT * (-0.3 + 0.4 * random.random())

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, RECT_WIDTH, RECT_HEIGHT, RECT_COLOR)

    def get_coordinates(self):
        return (self.x, self.y)

#PipePair synchronizes each set of vertically aligned pipes
class PipePair(Pipe):
    def __init__(self, pipe_1, pipe_2):
        self.pipe_1 = pipe_1
        self.pipe_2 = pipe_2

    def update(self):
        self.pipe_1.update()
        self.pipe_2.update()
        if not (self.pipe_1.get_coordinates()[0] == self.pipe_2.get_coordinates()[0]):
            self.pipe_2.x = self.pipe_1.get_coordinates()[0]
        if (self.pipe_1.update()):
            self.refill()
    
    def refill(self):
        self.pipe_1.refill()
        self.pipe_2.refill()
        self.pipe_2.y = self.pipe_1.y + 1.2*SCREEN_HEIGHT

    def draw(self):
        self.pipe_1.draw()
        self.pipe_2.draw()



class Bird:
    pass

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        

        self.background_color = BACKGROUND_COLOR


    def on_update(self, delta_time):
        for pipe in pipepair_list:
            pipe.update() #update to match top pipe

    def on_draw(self):
        self.clear()
        for pipe in pipepair_list:
            pipe.draw()
        #arcade.draw_rectangle_filled(test.x, test.y, RECT_WIDTH, RECT_HEIGHT, arcade.color.PURPLE)
        #arcade.draw_rectangle_filled(test_2.x, test_2.y, RECT_WIDTH, RECT_HEIGHT, arcade.color.ORANGE)

    def on_key_press(self, key, modifiers):
        pass

#create all sets of pipes
def createPipePair():
    pipe_bottom = Pipe()
    pipe_top = copy.deepcopy(pipe_bottom)
    pipe_top.y = pipe_bottom.y+1.2*SCREEN_HEIGHT
    pipepair = PipePair(pipe_bottom, pipe_top)   
    return pipepair

pipepair_list = [createPipePair() for i in range(4)]

#initialize pipe locations so they are equally spaced and will never overlap, even after prolonged play time
for i in range(len(pipepair_list)):
    pipepair_list[i].pipe_1.x += i * SCREEN_WIDTH/3.5
    pipepair_list[i].pipe_2.x += i * SCREEN_WIDTH/3.5



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