import time
import glfw
from OpenGL.GL import *
import math
from advProjectile import draw_ground, draw_trail
import pygame


# Initializing pygame mixer 
pygame.mixer.init()
bounce_sound = pygame.mixer.Sound("bounce.wav") # the bounce sound effect file

# Globals for mouse interaction
mouse_pressed = False
start_point = [50, 50]  # Starting point of the projectile
end_point = [50, 50]  # Dragging point or  initial dragging point which determines the angle and velocity
launch_projectile = False

# For tracking the projectile
projectile_generator = None
projectile_active = False

# Window dimensions
window_width, window_height = 900, 800


def calculate_points(v_x, v_y, g, dt, point, restitution, trail):
    while point[1] >= 0:
        point[0] += v_x * dt
        point[1] += v_y * dt
        v_y -= g * dt
        if point[1] <= 10:  # Ground level
            point[1] = 10  # Reset to ground level
            bounce_sound.play()
            v_y = -v_y * restitution[1]
            v_x = v_x* restitution[0]   # Reverse velocity with damping
            if abs(v_y) < 10  and abs(v_x)< 1:  # Stop bouncing when energy is negligible
                trail.clear() # Deleting the trail after the position of the projectile is reset to initial point
                break
        if point[0]>1000 or point[1] > 1500: 
            trail.clear()
            break
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
    mouse_pressed = False
    g = 9.81  # Gravity
    dt = 0.01  # Time step
    trail = [] # list to store the points in trail

    window = init_window(window_width, window_height, "Projectile Motion Simulation")
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        draw_ground(window_width, window_height) # function to draw ground
        draw_trail(trail)

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
            # dx = start_point[0] - end_point[0]   # for back pull
            # dy = start_point[1] - end_point[1]
            velocity = math.sqrt(dx**2 + dy**2) * 0.4  # Scale velocity
            angle = math.atan2(dy, dx)
            v_x = velocity * math.cos(angle)
            v_y = velocity * math.sin(angle)
            # basically the fraction of initial velocity remaining after each bounce 
            restitution = (0.3, 0.7)
            projectile_generator = calculate_points(v_x, v_y, g, dt, start_point[:], restitution, trail)
            projectile_active = True
            launch_projectile = False

        # Simulate projectile if active
        if projectile_active:
            try:
                point = next(projectile_generator)
                trail.append(list(point)) # adding the point to the trail
                if len(trail) >500:  # so limiting the length of trail 
                    trail.pop(0) 
                glColor3f(1, 0.25, 0.45)  # Green color for the projectile
                simulate_projectile_motion(point)
            except StopIteration:
                projectile_active = False  # Reset when the projectile hits the ground

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.001)

    glfw.terminate()


if __name__ == "__main__":
    main()
