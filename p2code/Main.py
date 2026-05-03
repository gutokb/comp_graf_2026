import Setter
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import Loader
import Object
import Camera

altura = 700
largura = 700

program, window = Setter.set(altura, largura)

camera = Camera.Camera(largura, altura)

glfw.set_key_callback(window, camera.key_event)
glfw.set_framebuffer_size_callback(window, camera.framebuffer_size_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)
glfw.set_scroll_callback(window, camera.scroll_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

loader = Loader.Loader(program)
caixastart, caixaqt, caixatexture = loader.load_obj_and_texture('objetos/bunker/bunker.obj', ['objetos/bunker/bunker.jpg'])
caixa = Object.Object(caixastart, caixaqt, caixatexture, program)
loader.upload()

glEnable(GL_DEPTH_TEST)
polygonal_mode = False

# wrap key_event to also handle polygonal mode toggle
original_key_event = camera.key_event
def key_event(window, key, scancode, action, mods):
    global polygonal_mode
    original_key_event(window, key, scancode, action, mods)
    if key == glfw.KEY_P and action == glfw.PRESS:
        polygonal_mode = not polygonal_mode
glfw.set_key_callback(window, key_event)

glfw.show_window(window)
while not glfw.window_should_close(window):
    camera.tick(glfw.get_time())
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if polygonal_mode else GL_FILL)

    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, camera.get_view())

    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, camera.get_projection())

    caixa.draw(0.0, 0, 0, 1, 0, 0, -20, 1.5, 1.5, 1.5, np.eye(4, 4))

    glfw.swap_buffers(window)

glfw.terminate()