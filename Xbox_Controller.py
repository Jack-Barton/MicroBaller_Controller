import pygame
import time

# initialize pygame
pygame.init()

# get the first connected joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# print some information about the joystick
print("Joystick name:", joystick.get_name())
print("Number of axes:", joystick.get_numaxes())
print("Number of buttons:", joystick.get_numbuttons())

# continuously read and print the joystick inputs

while True:
    pygame.event.pump() # pump the event queue
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    print("Axes:", axes)
    print("Buttons:", buttons)
    time.sleep(2)


#def controllerMessage():
#    pygame.event.pump()  # pump the event queue
#    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
#    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
#    return [axes, buttons]

