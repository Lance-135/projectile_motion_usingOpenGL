import time
import glfw
from OpenGL.GL import *
import math


def calculatePoints(v_x, v_y, g, dt, point):
    
    while point[1]>=0: 
        point[0] += v_x * dt
        point[1] += v_y * dt
        v_y = v_y - g*dt
        yield point



def simulateProjectileMotion(point):
    # For points
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


def main():
    # Window dimensions
    window_width, window_height = 900, 800
    x, y = 0, 0
    center = [10, 10]
    
    initial_velocity = 100
    angle = 90 
    rad_angle = math.radians(angle)
    g = 9.81
    dt = 0.01
    v_x = initial_velocity*math.cos(rad_angle)
    v_y = initial_velocity*math.sin(rad_angle)
    points_generator = calculatePoints(v_x, v_y, g, dt, center)
    window = init_window(window_width, window_height, "Projectile Motion Simulation")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        try: 
            # For point
            point = next(points_generator)
            simulateProjectileMotion(point)
        except StopIteration:
            break
        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()

if __name__ == "__main__":
    main()
