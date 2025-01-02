import time
import glfw
from OpenGL.GL import *
import math


def calculatePoints(v_x, v_y, g, dt, point, restitution):
    while True:
        point[0] += v_x * dt
        point[1] += v_y * dt
        v_y -= g * dt

        # Check for ground collision
        if point[1] <= 10:  # Ground level
            point[1] = 10  # Reset to ground level
            v_y = -v_y * restitution  # Reverse velocity with damping
            if abs(v_y) < 1:  # Stop bouncing when energy is negligible
                break

        yield point, v_y


def draw_circle(point, r, num_segments, color):
    glColor3f(*color)  # Set the color
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(point[0], point[1])  # Center of the circle
    for i in range(num_segments + 1):
        theta = 2.0 * math.pi * i / num_segments  # Angle in radians
        x = r * math.cos(theta)  # X coordinate
        y = r * math.sin(theta)  # Y coordinate
        glVertex2f(x + point[0], y + point[1])
    glEnd()


def draw_ground(width, height):
    # Draw a shaded ground rectangle
    glColor3f(0.3, 0.8, 0.3)  # Green for ground
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, 20)
    glVertex2f(0, 20)
    glEnd()


def draw_trail(trail):
    glColor3f(0.5, 0.5, 1.0)  # Light blue for the trail
    glBegin(GL_LINE_STRIP)
    for point in trail:
        glVertex2f(point[0], point[1])
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


def main():
    # Window dimensions
    window_width, window_height = 900, 800
    center = [10, 10]  # Initial position of the projectile

    initial_velocity = 100
    angle = 65  # Launch angle in degrees
    rad_angle = math.radians(angle)
    g = 9.81
    dt = 0.01
    restitution = 0.7  # Energy retention coefficient (bounciness)

    v_x = initial_velocity * math.cos(rad_angle)
    v_y = initial_velocity * math.sin(rad_angle)
    points_generator = calculatePoints(v_x, v_y, g, dt, center, restitution)
    window = init_window(window_width, window_height, "Bouncing Projectile Simulation")

    trail = []  # To store the projectile's trail

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Draw ground
        draw_ground(window_width, window_height)

        try:
            # Get the next point in the projectile motion
            point, v_y = next(points_generator)
            trail.append(list(point))  # Add the current point to the trail

            # Limit the trail length for performance
            if len(trail) > 500:
                trail.pop(0)

            # Draw the trail
            draw_trail(trail)

            # Draw the projectile
            color = (1.0 - point[1] / window_height, 0.2, point[1] / window_height)  # Dynamic color
            draw_circle(point, 8, 20, color)
        except StopIteration:
            break

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()


if __name__ == "__main__":
    main()
