import random
import time
import turtle
import pygame

window = turtle.Screen()
window.tracer(0)
window.bgpic("space.gif")
window.setup(0.5, 0.75)
window.title("Space Invaders")


# Create laser cannon
cannon = turtle.Turtle()
cannon.penup()
window.addshape("PLAYER1.gif")
cannon.shape("PLAYER1.gif")
cannon.setposition(0, -200)  # Initial cannon position
cannon.cannon_movement = 0  # -1 for left, 1 for right, 0 for stationary

# Game state variables
GAME_RUNNING = 0
lasers = []
power_lasers = []
aliens = []
power_activated = 0
power_activated_time = None
FRAME_RATE = 30
TIME_FOR_1_FRAME = 1 / FRAME_RATE
CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.2
ALIEN_SPEED = 3.5
LIFE = 3
COINS= 0

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)  # Base
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)  # Next tier
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  # Tip of cannon
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    if power_activated == 1:
        if power_activated_time is not None and (time.time() - power_activated_time <4)  :
            return power_laser()
    laser = turtle.Turtle()
    laser.penup()
    window.addshape("LASER1.gif")
    laser.shape("LASER1.gif")
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor() + 10)
    laser.setheading(90)
    laser.pendown()
    laser.showturtle()
    laser.pensize(10)
    lasers.append(laser)

def activate_power1():
    global power_activated, power_activated_time,COINS
    power_activated_time = time.time()
    if COINS>10:
        if power_activated == 0:
            power_activated = 1
        elif power_activated == 1:
             power_activated = 0
        COINS-=10

def power_laser():
    laser = turtle.Turtle()
    laser.penup()
    window.addshape("POWERLASER1.gif")
    laser.shape("POWERLASER1.gif")  # Set the shape first
    laser.shapesize(stretch_wid=0.5, stretch_len=4)  # Adjust the size
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor() + 10)
    laser.setheading(90)
    # laser.pendown()
    laser.showturtle()  # Show the laser after positioning
    power_lasers.append(laser)


def life_gain():
    global COINS,LIFE
    if COINS >30:
        COINS-=30
        LIFE+=1

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    if laser.ycor() > TOP:
        if laser in lasers:
            remove_sprite(laser, lasers)
        elif lasers in power_lasers:
            remove_sprite(laser, power_lasers)

def create_alien(random_num):
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(random.randint(int(LEFT + GUTTER), int(RIGHT - GUTTER)), TOP)
    match random_num:
        case 0:
            window.addshape("BABIES.gif")
            alien.shape("BABIES.gif")
        case 1:
            window.addshape("BLACK1.gif")
            alien.shape("BLACK1.gif")
        case 2:
            window.addshape("SHORT.gif")
            alien.shape("SHORT.gif")
        case _:
            window.addshape("BLACK1.gif")
            alien.shape("BLACK1.gif")

    alien.pensize(10)
    alien.setheading(-90)
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)

def game_play(x,y):
    global LIFE, GAME_RUNNING, lasers, aliens,COINS
    window.clear()
    window.tracer(0)
    window.bgpic("space.gif")
    LIFE = 3
    score = 0
    lasers.clear()
    aliens.clear()
    GAME_RUNNING = 0
    cannon.setposition(0, FLOOR_LEVEL)
    cannon.cannon_movement = 0

    # Create turtle for writing text
    text = turtle.Turtle()
    text.penup()
    text.hideturtle()
    text.setposition(LEFT * 0.8, TOP * 0.6)
    text.color(1, 1, 1)
    # Create instruction for superpowers
    life_icon = turtle.Turtle()
    life_icon.penup()
    life_icon.hideturtle()
    life_icon.goto(RIGHT*0.8,TOP *0.8)
    window.addshape('life+.gif')
    life_icon.shape("life+.gif")
    life_icon.showturtle()

    superpower_icon = turtle.Turtle()
    superpower_icon.penup()
    superpower_icon.hideturtle()
    superpower_icon.goto(RIGHT*0.5,TOP *0.8)
    window.addshape('superpower.gif')
    superpower_icon.shape("superpower.gif")
    superpower_icon.showturtle()

    # Key bindings
    window.onkeypress(move_left, "Left")
    window.onkeypress(move_right, "Right")
    window.onkeyrelease(stop_cannon_movement, "Left")
    window.onkeyrelease(stop_cannon_movement, "Right")
    window.onkeypress(create_laser, "space")
    window.onkeypress(activate_power1, "q")
    window.onkeypress(turtle.bye, "z")
    window.onkeypress(life_gain,'e')
    window.listen()

    draw_cannon()

    # Game loop
    alien_timer = 0
    game_timer = time.time()

    while LIFE > 0:
        window.update()
        time_elapsed = time.time() - game_timer
        text.clear()
        text.write(f"Time: {time_elapsed:5.1f}s\nScore: {score:5}\nLife: {LIFE}\nCoins: {COINS}", font=("Courier", 20, "bold"))

        # Move cannon
        new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
        if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
            cannon.setx(new_x)
            draw_cannon()

        # Move all lasers
        for laser in lasers.copy():
            move_laser(laser)

        # Spawn new aliens
        if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
            random_num = random.randint(0,3);
            create_alien(random_num)
            alien_timer = time.time()

        # Move all aliens
        # Move all aliens
        for alien in aliens.copy():
            alien.forward(ALIEN_SPEED)

            # Prepare to remove lasers
            lasers_to_remove = []
            power_lasers_to_remove = []

            # Check for collision with normal lasers
            for laser in lasers.copy():
                if laser.distance(alien) < 20:
                    lasers_to_remove.append(laser)
                    remove_sprite(alien, aliens)
                    score += 1
                    COINS+=1

            # Check for collision with power lasers
            for laser in power_lasers.copy():
                move_laser(laser)
                if laser.ycor() > TOP:
                    power_lasers_to_remove.append(laser)
                    continue  # Skip to the next laser

                # Check if they are on the same y level
                if abs(laser.ycor() - alien.ycor()) < 20:
                    if abs(laser.xcor() - alien.xcor()) < 50:  # Define your threshold
                        power_lasers_to_remove.append(laser)
                        remove_sprite(alien, aliens)
                        score += 1

            # Remove lasers after the loop to avoid modifying the list during iteration
            for laser in lasers_to_remove:
                remove_sprite(laser, lasers)

            for laser in power_lasers_to_remove:
                remove_sprite(laser, power_lasers)

            if alien.ycor() < FLOOR_LEVEL:
                LIFE -= 1
                remove_sprite(alien, aliens)

        time.sleep(TIME_FOR_1_FRAME)

    # Game Over
    GAME_RUNNING = 1
    game_over_screen()

def game_over_screen():
    global window
    window.clear()
    window.bgcolor(0.2, 0.2, 0.2)
    splash_text = turtle.Turtle()
    splash_text.penup()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    splash_text.setposition(LEFT * 0.38, TOP * 0.3)
    splash_text.write("GAME OVER", font=("Courier", 40, "bold"))

    shop_button=turtle.Turtle()
    shop_button.penup()
    shop_button.hideturtle()
    shop_button.goto( RIGHT*0.6,BOTTOM *0.3)
    shop_button.showturtle()
    window.addshape('shop.gif')
    shop_button.shape('shop.gif')
    shop_button.onclick(shop)

    play_again_button= turtle.Turtle()
    play_again_button.penup()
    play_again_button.hideturtle()
    play_again_button.goto(LEFT*0.6,BOTTOM * 0.3)
    play_again_button.showturtle()
    window.addshape('playagain.gif')
    play_again_button.shape("playagain.gif")
    play_again_button.onclick(play_again)

def play_again(x, y):
    game_play(x,y)

def exit_game(x,y):
    turtle.bye()

def main_menu():
    play_button= turtle.Turtle()
    play_button.penup()
    play_button.goto(0,0)
    window.addshape("PLAY.gif")
    play_button.shape("PLAY.gif")
    play_button.showturtle()
    play_button.onclick(game_play)

    exit_button= turtle.Turtle()
    exit_button.penup()
    exit_button.goto(0,-100)
    window.addshape("EXIT.gif")
    exit_button.shape("EXIT.gif")
    exit_button.showturtle()
    exit_button.onclick(exit_game)

    logo= turtle.Turtle()
    logo.penup()
    logo.goto(0,150)
    window.addshape("logo.gif")
    logo.shape("logo.gif")
    logo.showturtle()


    window.update()
def shop(x,y):
    global window
    window.clear()
    window.bgcolor(0.2, 0.2, 0.2)
    splash_text = turtle.Turtle()
    splash_text.penup()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    splash_text.setposition(LEFT * 0.38, TOP * 0.3)
    splash_text.write("SHOP", font=("Courier", 40, "bold"))

    shop_button=turtle.Turtle()
    shop_button.penup()
    shop_button.hideturtle()
    shop_button.goto( RIGHT*0.6,BOTTOM *0.3)
    shop_button.showturtle()
    window.addshape('LASER2.gif')
    shop_button.shape('LASER2.gif')
    shop_button.onclick(shop)

    play_again_button= turtle.Turtle()
    play_again_button.penup()
    play_again_button.hideturtle()
    play_again_button.goto(LEFT*0.6,BOTTOM * 0.3)
    play_again_button.showturtle()
    window.addshape('RED.gif')
    play_again_button.shape("RED.gif")
    play_again_button.onclick(play_again)


# Start the game
main_menu()

turtle.done()
