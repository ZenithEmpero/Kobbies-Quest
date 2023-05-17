import pygame

pygame.init()

# Set up the window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Continuous Image Rotation Example")

# Load the image
image = pygame.image.load("textures/duck.png")

# Set the initial rotation angle and rotation speed
rotation_angle = 0
rotation_speed = 2  # Adjust the speed of rotation

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Rotate the image
    rotated_image = pygame.transform.rotate(image, rotation_angle)

    # Get the rect of the rotated image
    rotated_rect = rotated_image.get_rect(center=(400, 300))

    # Update the rotation angle
    rotation_angle += rotation_speed

    # Wrap the angle to keep it within 0-359 degrees range
    rotation_angle %= 360

    # Calculate the centered position for drawing the rotated image
    rotated_pos = rotated_rect.center

    # Adjust the position to account for the rotation
    draw_pos = (rotated_pos[0] - rotated_rect.width / 2, rotated_pos[1] - rotated_rect.height / 2)

    # Draw the rotated image onto the screen
    screen.blit(rotated_image, draw_pos)

    pygame.display.flip()

pygame.quit()
