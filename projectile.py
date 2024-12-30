import time
import glfw
from OpenGL.GL import *
import math


def calculatePoints(v_x, v_y, g, dt, x,y):
    
    while y>=0: 
        x += v_x * dt
        y += v_y * dt
        v_y = v_y - g*dt
        print(v_y)
        yield x, y


def simulateProjectileMotion(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    # now display these points
    
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
    window_width, window_height = 800, 600
    x, y = 0, 0
    vertices = [(0,5), (5,0), (5,5)] # for a triangular object 
    
    initial_velocity = 100
    angle = 50 
    rad_angle = math.radians(angle)
    g = 9.81
    dt = 0.01
    v_x = initial_velocity*math.cos(rad_angle)
    v_y = initial_velocity*math.sin(rad_angle)

    points_generator = calculatePoints(v_x, v_y, g, dt, vertices)
    # Initialize GLFW window
    window = init_window(window_width, window_height, "Projectile Motion Simulation")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        try: 
            x, y = next(points_generator)
            simulateProjectileMotion(x, y)
        except StopIteration:
            break
        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()

if __name__ == "__main__":
    main()
