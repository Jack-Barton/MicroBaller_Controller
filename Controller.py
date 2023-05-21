import time
from math import trunc

import pygame


def controllerInit():
    """
    Initialises pygame and initialises the first controller it discovers.

    :return: The controller object discovered.
    """

    pygame.init()  # Initialize pygame
    controller = pygame.joystick.Joystick(0)  # Get the first connected controller
    controller.init()  # Initialize the controller
    return controller  # Return the controller object.


def controllerStream(controller):
    """
    Indefinitely reads then prints the axes and button values of controller respectively to the system out.

    :param controller: controller object.
    :return: N/A
    """

    while 1:
        pygame.event.pump()  # Get the most recent event
        axes = [controller.get_axis(i) for i in range(controller.get_numaxes())]  # Put axes values in an array
        buttons = [controller.get_button(i) for i in
                   range(controller.get_numbuttons())]  # Put button values in an array
        print("Axes:", axes)
        print("Buttons:", buttons)
        time.sleep(2)


def controllerMessage(controller):
    """
    Reads the current axis and buttons values of the given controller and returns an array of these values.

    :param controller: The controller to read from.
    :return: An array of axes and buttons with values normalized between (0 and 256) and (0 or 1) respectively.
    """

    pygame.event.pump()  # Get the most recent event
    axes = [(trunc(((controller.get_axis(i) + 1) / 2) * 256)) for i in
            range(controller.get_numaxes())]  # Normalise axis values (0 to 255) and add to array.
    buttons = [controller.get_button(i) for i in range(controller.get_numbuttons())]  # Add button values to array.
    return axes + buttons  # Return buttons array appended to axes array.


if __name__ == '__main__':
    """
    Prints the controller value array to system out every 2sec indefinitely.
    """

    activeController = controllerInit()  # Initialise the plugged in controller.
    while 1:
        print(controllerMessage(activeController))  # Print an array including axis and button values.
        time.sleep(2)  # Wait 2sec
