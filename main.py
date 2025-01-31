import time
import glfw
from OpenGL.GL import *
from start_function import draw_start_screen, handle_start_screen_click
from exit_function import exit_program
from Projectile import main as projectile_simulation  # Import Projectile.py's main function
from utils import init_window
from MIprojectile import main as mi_projectile

# Window settings
window_width, window_height = 900, 800
current_state = "start"

def mouse_button_callback(window, button, action, mods):
    """Handles mouse button interactions."""
    global current_state
    xpos, ypos = glfw.get_cursor_pos(window)
    
    if current_state == "start":
        current_state = handle_start_screen_click(xpos, ypos, window, current_state)
        if current_state == "simulation":
            glfw.destroy_window(window)  # Close menu window before opening simulation
            # projectile_simulation()  # Start the projectile simulation
            mi_projectile()

def main():
    global current_state

    window = init_window(window_width, window_height, "Projectile Motion Simulation")
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        if current_state == "start":
            draw_start_screen()

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    exit_program(window)

if __name__ == "__main__":
    main()
