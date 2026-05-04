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

botaostart, botaoqt, bototexture = loader.load_obj_and_texture('objetos/botao/botao.obj', ['objetos/botao/botao.png'])
botao = Object.Object(botaostart, botaoqt, bototexture, program)

mesastart, mesaqt, mesatexture = loader.load_obj_and_texture('objetos/mesa/Table.obj', ['objetos/mesa/Table_Mt.png'])
mesa = Object.Object(mesastart, mesaqt, mesatexture, program)

cadeirastart, cadeiraqt, cadeiratexture = loader.load_obj_and_texture('objetos/cadeira/cadeira.obj', ['objetos/cadeira/cadeira.png'])
cadeira = Object.Object(cadeirastart, cadeiraqt, cadeiratexture, program)

sacodormirstart, sacodormirqt, sacodormirtexture = loader.load_obj_and_texture('objetos/sleepingbag/Sleeping_bag.obj', ['objetos/sleepingbag/sleepbag.png'])
sacodormir = Object.Object(sacodormirstart, sacodormirqt, sacodormirtexture, program)

cactostart, cactoqt, cactotexture = loader.load_obj_and_texture('objetos/cactus/Cactus.obj', ['objetos/cactus/material_0.png'])
cacto = Object.Object(cactostart, cactoqt, cactotexture, program)

bombastart, bombaqt, bombatexture = loader.load_obj_and_texture('objetos/bomba/Nuclear_Bomb.obj', ['objetos/bomba/Nuclear_Bomb.png'])
bomba = Object.Object(bombastart, bombaqt, bombatexture, program)

explosaostart, explosaqt, explosatexture = loader.load_obj_and_texture('objetos/explosao/Explosion.obj', ['objetos/explosao/Explosion.png'])
explosao = Object.Object(explosaostart, explosaqt, explosatexture, program)

skystart, skyqt, skytexture = loader.load_obj_and_texture('objetos/skybox/skybox.obj', ['objetos/skybox/skybox2.webp'])
sky = Object.Object(skystart, skyqt, skytexture, program)

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

    # COISAS ESTAO COM ALTURA Y -0,5 PQ TAVA FLUTUANDO NO CHAO, SE ARRUMAR TROCAR
    caixa.draw(0.0, 0, 0, 1, 0, 0, -20, 2.5, 2.5, 2.5, np.eye(4, 4))
    botao.draw(0.0, 0, 0, 1, 3.4, 0.56, -20.3, 0.006, 0.006, 0.006, np.eye(4, 4))
    mesa.draw(0.0, 0, 0, 1, 3.3, 0, -20, 0.008, 0.008, 0.008, np.eye(4, 4))
    cadeira.draw(90.0, 0, 1, 0, 2.6, -0.5, -20, 0.014, 0.014, 0.014, np.eye(4, 4))
    sacodormir.draw(90.0, 0, 1, 0, -1.75, 0, -23, 0.014, 0.014, 0.014, np.eye(4, 4))
    cacto.draw(0.0, 0, 0, 1, 12, -0.5, -14, 0.3, 0.3, 0.3, np.eye(4, 4))
    bomba.draw(90.0, 1, 0, 0, 45, 20.0, -23, 0.01, 0.01, 0.01, np.eye(4, 4))
    explosao.draw(0.0, 0, 0, 1, 40, 0, -23, 0.2, 0.2, 0.2, np.eye(4, 4))
    sky.draw(0.0, 0, 0, 0, 0, 0, 0, 100.0, 100.0,100.0, np.eye(4, 4))
    glfw.swap_buffers(window)

glfw.terminate()