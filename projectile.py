import glfw
import pygame
from OpenGL.GL import *
import math
import time
import random

# Increased Window Dimensions
WIDTH, HEIGHT = 1900, 900
launch_started = False  # Flag for launch trigger
simulation_complete = False  # Flag to track when simulation ends

# Store user inputs
user_input = {"speed": "", "angle": "", "gravity": "9.81"}  # Default gravity
input_field = "speed"  # Track which field is being edited
launch_ready = False  # Start simulation only when inputs are complete

# Initialize Pygame and Pygame Mixer for Sound Effects
pygame.init()
pygame.mixer.init()
try:
    bounce_sound = pygame.mixer.Sound("bounce.wav")  # Load bouncing sound effect
    print("Sound loaded successfully.")
except pygame.error as e:
    print(f"Error loading sound: {e}")
    exit()

bounce_sound.set_volume(1.0)  # Set volume to maximum (valid range is 0.0 to 1.0)

def get_user_input():
    """Get user input for multiple projectiles."""
    num_projectiles = int(input("Enter the number of projectiles: "))
    projectiles = []

    for i in range(num_projectiles):
        print(f"\nProjectile {i + 1}:")
        speed = float(input("Enter initial speed (m/s): "))
        angle = float(input("Enter launch angle (degrees): "))
        gravity = float(input("Enter gravity (m/s^2, default 9.81): ") or 9.81)
        projectiles.append((speed, math.radians(angle), gravity))

    return projectiles

def calculate_trajectory(speed, angle, gravity, start_x=0, start_y=0, projectile_number=1):
    """Calculate projectile motion with realistic bouncing physics."""
    time_steps = 300  # Increased for smoother trajectory
    trajectories = []
    max_bounces = 3  # Number of bounces
    e = 0.7  # Coefficient of restitution
    previous_max_height = 0  # Track height reduction

    print(f"\nProjectile {projectile_number}: Initial Speed: {speed:.2f} m/s, Launch Angle: {math.degrees(angle):.2f}°")

    bounce_times = []  # Track the times of each bounce

    for bounce in range(max_bounces + 1):
        t_flight = (2 * speed * math.sin(angle)) / gravity
        dt = t_flight / time_steps
        points = []
        ground_hit = False  # Track if the projectile hit the ground
        max_height = 0  # Track max height of the current bounce

        for i in range(time_steps + 1):
            t = i * dt
            x = start_x + speed * math.cos(angle) * t
            y = start_y + (speed * math.sin(angle) * t) - (0.5 * gravity * t**2)

            if y < 0:  # Ground impact
                y = 0
                if not ground_hit:  # Ensure sound plays only once per bounce
                    print("Playing bounce sound...")
                    bounce_sound.play()
                    ground_hit = True
                    bounce_times.append(t)  # Record the time of the bounce
                break

            if y > max_height:
                max_height = y  # Update max height
        
            points.append((x, y))

        if bounce > 0:  # Print height reduction after the first bounce
            height_reduction = ((previous_max_height - max_height) / previous_max_height) * 100
            print(f"Bounce {bounce}: Max Height = {max_height:.2f} m, Reduction = {height_reduction:.2f}%")

        previous_max_height = max_height  # Store the current max height for next bounce
        trajectories.append((points, t_flight))

        if bounce < max_bounces and len(points) > 0:
            # Bounce physics
            vy_impact = -speed * math.sin(angle)
            vy_new = -e * vy_impact  # Reverse and reduce vertical component
            vx = speed * math.cos(angle)
            
            speed = math.sqrt(vx**2 + vy_new**2)
            angle = math.atan(vy_new / vx) if vx != 0 else 0
            start_x, start_y = points[-1]

    print(f"Final Speed after last bounce for Projectile {projectile_number}: {speed:.2f} m/s\n")
    return trajectories, speed, angle, start_x, start_y, bounce_times

def draw_circle(x, y, radius=3, segments=40):  # Enlarged moving ball
    """Draws a larger moving ball."""
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        dx = radius * math.cos(theta)
        dy = radius * math.sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()

def draw_trajectory(points, color):
    """Render the entire projectile trajectory at an enlarged scale."""
    glColor3f(*color)
    glBegin(GL_LINE_STRIP)
    for x, y in points:
        glVertex2f(x / 4, y / 4)  # Adjusted for better scaling
    glEnd()

def draw_axes():
    """Draw X and Y axes for reference."""
    glColor3f(1, 1, 1)  # White axes
    glLineWidth(2.0)

    glBegin(GL_LINES)
    # X-axis
    glVertex2f(-WIDTH / 4, 0)  
    glVertex2f(WIDTH / 4, 0)   
    # Y-axis
    glVertex2f(0, -HEIGHT / 4)  
    glVertex2f(0, HEIGHT / 4)   
    glEnd()

def draw_input_screen():
    """Draws the user input fields and instructions."""
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Instruction text
    render_text("Enter values and press ENTER to launch:", 50, HEIGHT - 50)
    
    # Draw input fields
    render_text(f"Speed (m/s): {user_input['speed']}", 50, HEIGHT - 100)
    render_text(f"Angle (degrees): {user_input['angle']}", 50, HEIGHT - 150)
    render_text(f"Gravity (m/s^2): {user_input['gravity']}", 50, HEIGHT - 200)
    
    # Highlight active input field
    render_text(f">>> {input_field.upper()}", 50, HEIGHT - 250)

def key_callback(window, key, scancode, action, mods):
    """Handles keyboard input for user data entry."""
    global input_field, launch_ready

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_BACKSPACE:  # Remove last character
            user_input[input_field] = user_input[input_field][:-1]
        elif key == glfw.KEY_ENTER:  # Move to next field or start simulation
            if input_field == "speed":
                input_field = "angle"
            elif input_field == "angle":
                input_field = "gravity"
            else:
                launch_ready = True  # All inputs completed, start simulation
        elif glfw.KEY_0 <= key <= glfw.KEY_9 or key == glfw.KEY_PERIOD:  # Numeric input
            user_input[input_field] += chr(key)

def render_text(text, x, y, font_size=24):
    """Render text using Pygame and display it in OpenGL."""
    pygame.font.init()
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (255, 255, 255, 255))  # White text
    
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def display_report(speed, angle, elapsed_time):
    """Display projectile data dynamically on the screen using Pygame text."""
    text = f"Time: {elapsed_time:.2f}s | Speed: {speed:.2f} m/s | Angle: {math.degrees(angle):.2f}°"
    render_text(text, 10, HEIGHT - 40)

def mouse_button_callback(window, button, action, mods):
    """Trigger launch when the mouse is clicked."""
    global launch_started
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        launch_started = True

def main():
    global launch_started, simulation_complete, launch_ready
    if not glfw.init():
        return
    
    window = glfw.create_window(WIDTH, HEIGHT, "Projectile Simulation", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)  # Capture keyboard input
    
    # Adjust scale for better visibility
    glOrtho(0, WIDTH / 4, 0, HEIGHT / 4, -1, 1)

    glfw.set_mouse_button_callback(window, mouse_button_callback)

    projectiles = get_user_input()
    trajectories = []
    colors = []
    total_simulation_time = 0
    bounce_times_all_projectiles = []  # To store the bounce times for all projectiles
    
    for i, (speed, angle, gravity) in enumerate(projectiles, start=1):
        trajectory_bounces, speed, angle, start_x, start_y, bounce_times = calculate_trajectory(speed, angle, gravity, projectile_number=i)
        trajectories.append((trajectory_bounces, speed, angle, start_x, start_y))
        colors.append((random.random(), random.random(), random.random()))  # Generate random colors
        bounce_times_all_projectiles.append(bounce_times)

    start_time = None

    while not glfw.window_should_close(window):
        if simulation_complete:
            break  # Stop the simulation once all projectiles have finished

        glClear(GL_COLOR_BUFFER_BIT)
        draw_axes()

        if launch_started:
            if start_time is None:
                start_time = time.time()

            elapsed_time = time.time() - start_time
            total_time = 0
            all_done = True  # Track if all projectiles are done

            for i, (trajectory_bounces, speed, angle, start_x, start_y) in enumerate(trajectories):
                color = colors[i]
                total_time = 0

                for bounce_index, (points, t_flight) in enumerate(trajectory_bounces):
                    draw_trajectory(points, color)

                    if elapsed_time >= total_time and elapsed_time <= total_time + t_flight:
                        index = min(int(((elapsed_time - total_time) / t_flight) * len(points)), len(points) - 1)
                        x, y = points[index]
                        glColor3f(*color)
                        draw_circle(x / 4, y / 4, radius=3)
                        display_report(speed, angle, elapsed_time)
                        all_done = False
                    
                    total_time += t_flight
                
                # Check if the projectile has completed all its bounces
                for bounce_time in bounce_times_all_projectiles[i]:
                    if elapsed_time >= bounce_time and elapsed_time <= bounce_time + 0.1:  # Allow for small window of time
                        print("Playing bounce sound...")  # Debugging message
                        bounce_sound.play()

            if all_done:
                simulation_complete = True  # End simulation if all projectiles are done

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    print("Simulation complete!")

if __name__ == "__main__":
    main()
