import math

import pygame  # Using pygame library's joystick functionality

pygame.joystick.init()  # Initialize the joystick
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]  # Get the list of joysticks

run = True

pygame.init()

while run:  # While the code is running
    for event in pygame.event.get():  # If something happened
        if event.type == pygame.JOYBUTTONDOWN:  # If button is clicked
            if joysticks[0].get_button(0):  # If it is the stop button
                run = False  # Stop the program
                break
    speed = -joysticks[0].get_axis(1)  # Left joystick Y-axis controls the speed
    angle = joysticks[0].get_axis(2)  # Right joystick X-axis controls the angle
    print(angle)  # Test code

