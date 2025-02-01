import pygame
from OpenGL.GL import *
import glfw

# Button coordinates (x1, y1, x2, y2)
projectile_button = (350, 500, 550, 550)
mi_projectile_button = (350, 400, 550, 450)
exit_button = (350, 300, 550, 350)

# Initialize PyGame for font rendering
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)  # Default font, size 36

def render_text(text, x, y, background_color):
    """Renders text as a texture using PyGame and OpenGL."""
    text_surface = font.render(text, True, (255, 255, 255), background_color)  # White text on button-colored background
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glRasterPos2f(x, y)  # Position text
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_start_screen():
    """Draw the start menu with three buttons."""
    
    # Set background color
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw Projectile button
    glColor3f(0.2, 0.2, 0.8)  # Blue
    glBegin(GL_QUADS)
    glVertex2f(projectile_button[0], projectile_button[1])
    glVertex2f(projectile_button[2], projectile_button[1])
    glVertex2f(projectile_button[2], projectile_button[3])
    glVertex2f(projectile_button[0], projectile_button[3])
    glEnd()
    render_text("Projectile", 400, 515, (51, 51, 204))
    
    # Draw MI_projectile button
    glColor3f(0.2, 0.8, 0.2)  # Green
    glBegin(GL_QUADS)
    glVertex2f(mi_projectile_button[0], mi_projectile_button[1])
    glVertex2f(mi_projectile_button[2], mi_projectile_button[1])
    glVertex2f(mi_projectile_button[2], mi_projectile_button[3])
    glVertex2f(mi_projectile_button[0], mi_projectile_button[3])
    glEnd()
    render_text("MI_project", 400, 415, (51, 204, 51))
    
    # Draw Exit button
    glColor3f(0.8, 0.2, 0.2)  # Red
    glBegin(GL_QUADS)
    glVertex2f(exit_button[0], exit_button[1])
    glVertex2f(exit_button[2], exit_button[1])
    glVertex2f(exit_button[2], exit_button[3])
    glVertex2f(exit_button[0], exit_button[3])
    glEnd()
    render_text("Exit", 430, 315, (204, 51, 51))

def handle_start_screen_click(xpos, ypos, window, state):
    """Handles mouse clicks on the start screen buttons."""
    y_opengl = 800 - ypos  # Convert to OpenGL coordinates

    # Debugging prints (remove these later)
    print(f"Mouse Click at: ({xpos}, {y_opengl})")

    if projectile_button[0] <= xpos <= projectile_button[2] and projectile_button[1] <= y_opengl <= projectile_button[3]:
        print("Projectile Button Clicked!")
        return "projectile"  # Start projectile simulation
    
    elif mi_projectile_button[0] <= xpos <= mi_projectile_button[2] and mi_projectile_button[1] <= y_opengl <= mi_projectile_button[3]:
        print("MI_projectile Button Clicked!")
        return "mi_projectile"  # Start MI_projectile simulation

    elif exit_button[0] <= xpos <= exit_button[2] and exit_button[1] <= y_opengl <= exit_button[3]:
        print("Exit Button Clicked!")
        glfw.set_window_should_close(window, True)  # Close window
        return "exit"

    return state  # No change in state
