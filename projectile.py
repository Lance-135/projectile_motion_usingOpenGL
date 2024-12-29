import glfw
from OpenGL.GL import *
import math


u = 50
angle = 45
rad_angle = math.radians(angle)
g = 9.81
dt = 0.01
t = 0

def calculatePoints(u, rad_angle):
    x = 0
    y = 0
    points= []
    while y>=0: 
        x += u*math.cos(rad_angle)*dt
        y += u*math.sin(rad_angle)*dt
        points.append((x,y))



def simulateProjectileMotion():
    points = calculatePoints()
    
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

    # Constants for simulation
    initial_velocity = 50.0  # m/s
    launch_angle = 45.0  # degrees

    # Initialize GLFW window
    window = init_window(window_width, window_height, "Projectile Motion Simulation")

    # Simulation parameters
    g = 9.8  # Gravitational acceleration (m/s^2)
    dt = 0.01  # Time step

    # Scale factor to fit the simulation in the window
    scale_x = window_width / 100.0  # Assume max horizontal distance is 100m
    scale_y = window_height / 50.0  # Assume max vertical height is 50m

    # Create a generator for projectile motion
    projectile_motion = simulateProjectileMotion()

    # Main rendering loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
