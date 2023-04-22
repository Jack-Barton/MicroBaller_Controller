from math import trunc

import pygame
import time

async def joystickInit():
    # initialize pygame
    pygame.init()

    # get the first connected joystick
    joystick = pygame.joystick.Joystick(0)
    # initialize the joystick
    joystick.init()

    return joystick

# continuously read and print the joystick inputs
def controllerStream(joystick):
    i = 0
    while i < 2:
        pygame.event.pump() # pump the event queue
        axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
        buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        print("Axes:", axes)
        print("Buttons:", buttons)
        time.sleep(2)


# takes the controller and returns the joystick with values normalized between 0 and 256 and buttons (0 or 1) in an array
def controllerMessage(joystick):
    pygame.event.pump()  # pump the event queue
    axes = [(trunc(((joystick.get_axis(i) + 1) / 2) * 256)) for i in range(joystick.get_numaxes())]
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    return axes + buttons
