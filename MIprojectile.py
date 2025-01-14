import time
import glfw
from OpenGL.GL import *
import math

# Globals for mouse interaction
mouse_pressed = False
start_point = [50, 50]  # Starting point of the projectile
end_point = [50, 50]  # Dragging point
launch_projectile = False

# For tracking the projectile
projectile_generator = None
projectile_active = False

# Window dimensions
window_width, window_height = 900, 800


def calculate_points(v_x, v_y, g, dt, point):
    while point[1] >= 0:
        point[0] += v_x * dt
        point[1] += v_y * dt
        v_y -= g * dt
        yield point


def simulate_projectile_motion(point):
    num_segments = 10
    r = 5
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(point[0], point[1])  # Center of the circle
    for i in range(num_segments + 1):
        theta = 2.0 * math.pi * i / num_segments  # Angle in radians
        x = r * math.cos(theta)  # X coordinate
        y = r * math.sin(theta)  # Y coordinate
        glVertex2f(x + point[0], y + point[1])
    glEnd()


def init_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW initialization failed")

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window creation failed")

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)  # Set up orthographic projection

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return window


def mouse_button_callback(window, button, action, mods):
    global mouse_pressed, start_point, end_point, launch_projectile, projectile_active

    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            mouse_pressed = True
            end_point = list(start_point)  # Reset dragging endpoint
        elif action == glfw.RELEASE:
            mouse_pressed = False
            if not projectile_active:  # Only launch if no projectile is active
                launch_projectile = True


def cursor_position_callback(window, xpos, ypos):
    global end_point
    if mouse_pressed:
        end_point = [xpos, window_height - ypos]  # Flip Y-axis


def main():
    global launch_projectile, projectile_generator, projectile_active, start_point, end_point

    g = 9.81  # Gravity
    dt = 0.01  # Time step

    window = init_window(window_width, window_height, "Projectile Motion Simulation")
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Draw the dragging line and static projectile
        if mouse_pressed or not projectile_active:
            glColor3f(1, 0, 0)  # Red color for dragging line
            glBegin(GL_LINES)
            glVertex2f(start_point[0], start_point[1])  # Start point
            glVertex2f(end_point[0], end_point[1])  # Current drag point
            glEnd()

            # Draw the initial projectile
            glColor3f(0, 0, 1)  # Blue color for the static projectile
            simulate_projectile_motion(start_point)

        # Launch the projectile
        if launch_projectile and not projectile_active:
            dx = end_point[0] - start_point[0]
            dy = end_point[1] - start_point[1]
            velocity = math.sqrt(dx**2 + dy**2) * 0.2  # Scale velocity
            angle = math.atan2(dy, dx)
            v_x = velocity * math.cos(angle)
            v_y = velocity * math.sin(angle)
            projectile_generator = calculate_points(v_x, v_y, g, dt, start_point[:])
            projectile_active = True
            launch_projectile = False

        # Simulate projectile if active
        if projectile_active:
            try:
                point = next(projectile_generator)
                glColor3f(0, 1, 0)  # Green color for the projectile
                simulate_projectile_motion(point)
            except StopIteration:
                projectile_active = False  # Reset when the projectile hits the ground

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()


if __name__ == "__main__":
    main()
