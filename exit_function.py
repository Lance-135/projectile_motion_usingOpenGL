import glfw

def exit_program(window):
    """Gracefully closes the GLFW window."""
    glfw.set_window_should_close(window, True)
