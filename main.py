# -------imports-------
import turtle as trtl
import random as ran
import time as times
import os
from PIL import Image


# -------High Score Logic-------
def get_high_score(mode):
    filename = f"highscore_{mode}.txt"
    if not os.path.exists(filename):
        return 0
    with open(filename, "r") as f:
        try:
            return int(f.read())
        except:
            return 0


def save_high_score(new_score, mode):
    high_score = get_high_score(mode)
    if new_score > high_score:
        filename = f"highscore_{mode}.txt"
        with open(filename, "w") as f:
            f.write(str(new_score))
        return True
    return False


# -------Screen Setup & Dynamic Background-------
wn = trtl.Screen()
wn.tracer(False)
wn.setup(width=1.0, height=1.0)

try:
    wn._root().state('zoomed')
except:
    pass

screen_width = wn.window_width()
screen_height = wn.window_height()

try:
    original_bg = Image.open("background.gif")
    stretched_bg = original_bg.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    stretched_bg.save("temp_bg.gif")
    wn.bgpic("temp_bg.gif")
except:
    wn.bgpic("background.gif")

# Shapes
shapes = ["pipe.gif", "pipe2.gif", "redbird.gif", "bluebird.gif",
          "yellowbird.gif", "explosion.gif", "redbirdfall.gif", "yellowbirdfall.gif",
          "bluebirdfall.gif", "redbirdup.gif", "bluebirdup.gif", "yellowbirdup.gif"]
for s in shapes:
    wn.addshape(s)

# -------Turtles & UI-------
font_setup = ("Times New Roman", 35, "bold")
font_setup2 = ("Times New Roman", 70, "bold")
font_setup3 = ("Times New Roman", 40, "normal")
btn_font = ("Times New Roman", 20, "bold")

sc = trtl.Turtle(visible=False)
sc.pu()
sc.goto(0, 300)

bird = trtl.Turtle()
bird.pu()
bird.ht()  # Hide default black arrow
bird.speed(0)

easy_btn = trtl.Turtle(shape="square");
easy_btn.color("lightgreen");
easy_btn.shapesize(2, 6);
easy_btn.pu();
easy_btn.ht()
med_btn = trtl.Turtle(shape="square");
med_btn.color("gold");
med_btn.shapesize(2, 6);
med_btn.pu();
med_btn.ht()
hard_btn = trtl.Turtle(shape="square");
hard_btn.color("tomato");
hard_btn.shapesize(2, 6);
hard_btn.pu();
hard_btn.ht()

click = 0
score = 0
y_vel = 0
bird_type = "redbird.gif"
birdfall_type = "redbirdfall.gif"
game_active = False
pipeSpeed = 25
pipe_gap = 800
current_mode = "medium"

p_list = []
for i in range(3):
    tp = trtl.Turtle(shape="pipe2.gif")
    bp = trtl.Turtle(shape="pipe.gif")
    for p in [tp, bp]:
        p.pu()
        p.ht()
    p_list.append([tp, bp, 0, False])

b1, b2, b3 = trtl.Turtle(), trtl.Turtle(), trtl.Turtle()
for b in [b1, b2, b3]:
    b.pu()
    b.ht()


# -------Functions-------
def updateHeight(old_h=None):
    """Generates a height that is at least 150 pixels away from the previous one."""
    new_h = ran.randint(350, 720)
    if old_h is not None:
        # Keep picking a new height until the jump is significant enough
        while abs(new_h - old_h) < 150:
            new_h = ran.randint(350, 720)
    return new_h


def init_difficulty():
    bird.ht()
    sc.clear()
    sc.goto(0, 180)
    sc.write("Select Difficulty", align="center", font=font_setup)
    easy_btn.goto(-200, 50);
    easy_btn.st()
    sc.goto(-200, 0);
    sc.write("EASY", align="center", font=btn_font)
    med_btn.goto(0, 50);
    med_btn.st()
    sc.goto(0, 0);
    sc.write("MEDIUM", align="center", font=btn_font)
    hard_btn.goto(200, 50);
    hard_btn.st()
    sc.goto(200, 0);
    sc.write("HARD", align="center", font=btn_font)
    easy_btn.onclick(lambda x, y: set_difficulty(15, 1000, "easy"))
    med_btn.onclick(lambda x, y: set_difficulty(25, 800, "medium"))
    hard_btn.onclick(lambda x, y: set_difficulty(35, 650, "hard"))
    wn.update()


def set_difficulty(speed, gap, mode):
    global pipeSpeed, pipe_gap, current_mode
    pipeSpeed, pipe_gap, current_mode = speed, gap, mode
    for btn in [easy_btn, med_btn, hard_btn]:
        btn.ht()
        btn.onclick(None)
    init_selection()


def init_selection():
    global click
    click = 0
    sc.clear()
    sc.goto(0, 180)
    sc.write("Pick A Bird", align="center", font=font_setup)
    b1.goto(-200, 50);
    b1.shape("yellowbird.gif");
    b1.st()
    b2.goto(0, 50);
    b2.shape("bluebird.gif");
    b2.st()
    b3.goto(200, 50);
    b3.shape("redbird.gif");
    b3.st()
    b1.onclick(lambda x, y: select_bird("yellowbirdup.gif", "yellowbirdfall.gif"))
    b2.onclick(lambda x, y: select_bird("bluebirdup.gif", "bluebirdfall.gif"))
    b3.onclick(lambda x, y: select_bird("redbirdup.gif", "redbirdfall.gif"))
    wn.update()


def select_bird(b_up, b_fall):
    global bird_type, birdfall_type, click
    bird_type, birdfall_type, click = b_up, b_fall, 1
    sc.clear()
    for b in [b1, b2, b3]: b.ht()
    b1.onclick(None);
    b2.onclick(None);
    b3.onclick(None)
    start_game_loop()


def flap(x=None, y=None):
    global y_vel, game_active
    if game_active: y_vel = 19


def handle_collision():
    global game_active
    if not game_active: return
    game_active = False
    bird.shape("explosion.gif")
    wn.update()
    times.sleep(0.5)
    game_over()


def game_over():
    is_new_high = save_high_score(score, current_mode)
    sc.clear()
    sc.goto(0, 150)
    sc.write("GAME OVER", align="center", font=font_setup2)
    sc.goto(0, 50)
    sc.write(f"Score: {score}", align="center", font=font_setup3)
    sc.goto(0, -10)
    sc.write(f"High Score ({current_mode.capitalize()}): {get_high_score(current_mode)}", align="center",
             font=font_setup3)
    if is_new_high:
        sc.goto(0, -70)
        sc.write("NEW RECORD!", align="center", font=("Times New Roman", 30, "bold"))
    sc.goto(0, -150)
    sc.write("Press 'R' to Play Again", align="center", font=font_setup)
    wn.onkeypress(reset_game, "r")
    wn.onkeypress(reset_game, "R")
    wn.update()


def reset_game():
    if not game_active:
        wn.onkeypress(None, "r")
        wn.onkeypress(None, "R")
        sc.clear()
        init_difficulty()


def game_tick():
    global y_vel, game_active, score
    if not game_active: return

    bird.goto(bird.xcor(), bird.ycor() + y_vel)
    y_vel -= 3
    bird.shape(birdfall_type if y_vel <= -15 else bird_type)

    if bird.ycor() <= -260:
        handle_collision()
        return

    for p_pair in p_list:
        top, bot, h, passed = p_pair
        top.bk(pipeSpeed)
        bot.bk(pipeSpeed)

        # Collision Check
        if abs(bird.xcor() - top.xcor()) < 55:
            if bird.ycor() + 12 >= h - 380 or bird.ycor() - 12 <= h - 510:
                handle_collision()
                return

        if bird.xcor() > top.xcor() and not passed:
            score += 1
            p_pair[3] = True
            sc.clear()
            sc.goto(0, 300)
            sc.write(score, align="center", font=font_setup)

        # Reset Pipe with New Randomized Logic
        if top.xcor() < -1200:
            old_h = p_pair[2]
            new_h = updateHeight(old_h)  # Pass the old height to ensure randomness
            p_pair[2], p_pair[3] = new_h, False
            new_x = top.xcor() + (pipe_gap * 3)
            top.goto(new_x, new_h)
            bot.goto(new_x, new_h - 950)

    wn.update()
    wn.ontimer(game_tick, 40)


def start_game_loop():
    global score, y_vel, game_active
    score, y_vel, game_active = 0, 0, True
    bird.goto(-300, 0);
    bird.st()

    # Initialize pipes with significant height differences
    last_h = 500
    for i, p_pair in enumerate(p_list):
        h = updateHeight(last_h)
        last_h = h
        p_pair[2], p_pair[3] = h, False
        p_pair[0].goto(800 + (i * pipe_gap), h)
        p_pair[1].goto(800 + (i * pipe_gap), h - 950)
        p_pair[0].st();
        p_pair[1].st()

    sc.goto(0, 300)
    sc.write(score, align="center", font=font_setup)
    game_tick()


wn.onkeypress(flap, "space")
wn.onscreenclick(flap)
wn.listen()
init_difficulty()
wn.mainloop()