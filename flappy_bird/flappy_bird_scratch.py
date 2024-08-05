import arcade, random, copy, time
import arcade.gui

#initialize game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Flappy Bird"

RECT_WIDTH = 100
RECT_HEIGHT = SCREEN_HEIGHT
RECT_COLOR = arcade.color.BLUE #bottom
RECT_COLOR_2 = arcade.color.BLACK #top

BIRD_RADIUS = 12
BIRD_COLOR = arcade.color.CYBER_YELLOW

START_X = SCREEN_WIDTH/2
START_Y = SCREEN_HEIGHT/2
START_WIDTH = 0.75*SCREEN_WIDTH
START_HEIGHT = 0.3*SCREEN_HEIGHT
START_COLOR = arcade.color.ORANGE_RED

BACKGROUND_COLOR = arcade.color.RED

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT * (-0.3 + 0.4 * random.random())
        self.change_x = -1.5
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
class PipePair:
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
            pipepair_list.append(pipepair_list.pop(0))
    
    def refill(self):
        self.pipe_1.refill()
        self.pipe_2.refill()
        self.pipe_2.y = self.pipe_1.y + 1.2*SCREEN_HEIGHT

    def draw(self):
        self.pipe_1.draw()
        self.pipe_2.draw()



class Bird:
    def __init__(self):
        self.x = RECT_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.change_x = 0
        self.change_y = SCREEN_HEIGHT/20
        self.time = 0
        self.g_constant = 2
        self.score = 0
        self.HIGH_SCORE = 0

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, BIRD_RADIUS , BIRD_COLOR)
        self.draw_score()

    def update_pos(self, up=False):
        #give room for error above/below pipe when moving
        l = 2*16
        if up:
            for i in range(1,l+1):
                self.y += 3 * (self.change_y * (l-i)**2)/(l**3)

            self.time = 0
    
    def gravity(self):
        self.y -= self.g_constant * self.time**2
        self.time += 0.04

    def get_coordinates(self):
        return (self.x, self.y)
    
    def set_score(self, value):
        self.score = value

    def draw_score(self):
        PLAYER_SCORE = player_bird.score
        SCORE_SIZE = 60
        SCORE_X = SCREEN_WIDTH/2 - SCORE_SIZE/2
        SCORE_Y = SCREEN_HEIGHT * (0.85)
        SCORE_COLOR = arcade.color.WHITE
        SCORE_FONT = "Arial"
        arcade.draw_text(PLAYER_SCORE, SCORE_X, SCORE_Y, SCORE_COLOR, SCORE_SIZE, font_name = SCORE_FONT) 


class Start(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_color = arcade.color.ORANGE_RED
        arcade.set_background_color(self.background_color)

        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        start_button = arcade.gui.UIFlatButton(text="Start", width=SCREEN_WIDTH/3)
        start_button.on_click = self.on_buttonclick

        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=start_button))

    def on_buttonclick(self, event):
        arcade.close_window()
        Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        time.sleep(1)
        arcade.run()
        
    def on_draw(self):
        arcade.start_render()
        self.uimanager.draw()


class End(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_color = arcade.color.ORANGE_RED
        arcade.set_background_color(self.background_color)

        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        end_button = arcade.gui.UIFlatButton(text="Play Again", width=SCREEN_WIDTH/3)
        end_button.on_click = self.on_buttonclick

        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=end_button))

    def on_buttonclick(self, event):
        arcade.close_window()
        player_bird.y = START_Y
        player_bird.time = 0
        initialize_pipes()
        Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        player_bird.set_score(0)
        time.sleep(1)
        arcade.run()

    def on_draw(self):
        arcade.start_render()
        self.uimanager.draw()
        
        PLAYER_SCORE = player_bird.score
        SCORE_SIZE = 30
        SCORE_X = SCREEN_WIDTH/4
        SCORE_Y = SCREEN_HEIGHT * (0.7)
        SCORE_COLOR = arcade.color.MAROON
        SCORE_FONT = "Arial"
        arcade.draw_text(f"Your Score: {PLAYER_SCORE}\n\nHigh Score: {player_bird.HIGH_SCORE}", SCORE_X, SCORE_Y, SCORE_COLOR, SCORE_SIZE, width = SCREEN_WIDTH/2, align = "center", font_name = SCORE_FONT, bold=True) 


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_color = BACKGROUND_COLOR
        arcade.set_background_color(self.background_color)

    def on_update(self, delta_time):
        for pipe in pipepair_list:
            pipe.update() #update to match top pipe
        if -5/3 < pipepair_list[0].pipe_1.get_coordinates()[0] - RECT_WIDTH/2 < 5/3:
            player_bird.set_score(player_bird.score + 1)

    def on_draw(self):
        self.clear()
        for pipe in pipepair_list:
            pipe.draw()
        player_bird.gravity()
        player_bird.draw()
        if player_bird.get_coordinates()[1] < BIRD_RADIUS:
            arcade.close_window()
            if player_bird.score > player_bird.HIGH_SCORE:
                player_bird.HIGH_SCORE = player_bird.score
            End(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            arcade.run()
        elif player_bird.get_coordinates()[1] > SCREEN_HEIGHT - BIRD_RADIUS:
            player_bird.y = SCREEN_HEIGHT - BIRD_RADIUS  

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            player_bird.update_pos(True)
        else:
            player_bird.update_pos()

    def on_mouse_press(self, x, y, button, modifiers):
        player_bird.update_pos(True)


#create all sets of pipes
def createPipePair():
    pipe_bottom = Pipe()
    pipe_top = copy.deepcopy(pipe_bottom)
    pipe_top.y = pipe_bottom.y+1.2*SCREEN_HEIGHT
    pipepair = PipePair(pipe_bottom, pipe_top)   
    return pipepair



#initialize pipe locations so they are equally spaced and will never overlap
def initialize_pipes():
    global pipepair_list
    pipepair_list = [createPipePair() for i in range(4)]
    for i in range(len(pipepair_list)):
        pipepair_list[i].pipe_1.x += i * SCREEN_WIDTH/3.5
        pipepair_list[i].pipe_2.x += i * SCREEN_WIDTH/3.5

player_bird = Bird()

def main():
    initialize_pipes()
    Start(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
    
    print('Game started')

if __name__ == '__main__':
    main()