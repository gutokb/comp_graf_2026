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

bunker = Object.Object(loader, 'objetos/bunker/bunker.obj', ['objetos/bunker/bunker.jpg'], program)
bunker.set_model(0.0, 0, 0, 1, 0, 0, -20, 2.5, 2.5, 2.5)

mesa = Object.Object(loader, 'objetos/mesa/Table.obj', ['objetos/mesa/Table_Mt.png'], program)
mesa.set_model(0.0, 0, 0, 1, 3.2, 0.173, -20, 0.012, 0.012, 0.012)

cadeira = Object.Object(loader, 'objetos/cadeira/cadeira.obj', ['objetos/cadeira/cadeira.png'], program)
cadeira.set_model(90.0, 0, 1, 0, 2.3, -0.5, -20, 0.02, 0.02, 0.02)

sacodormir = Object.Object(loader, 'objetos/sleepingbag/Sleeping_bag.obj', ['objetos/sleepingbag/sleepbag.png'], program)
sacodormir.set_model(90.0, 0, 1, 0, -1.75, -0.35, -23, 0.014, 0.014, 0.014)

cacto = Object.Object(loader, 'objetos/cactus/Cactus.obj', ['objetos/cactus/material_0.png'], program)
cacto.set_model(0.0, 0, 0, 1, 12, -0.5, -14, 0.3, 0.3, 0.3)

bomba = Object.Object(loader, 'objetos/bomba/Nuclear_Bomb.obj', ['objetos/bomba/Nuclear_Bomb.png'], program)
bomba.set_model(90.0, 1, 0, 0, 45, 20.0, -23, 0.01, 0.01, 0.01)

explosao = Object.Object(loader, 'objetos/explosao/Explosion.obj', ['objetos/explosao/Explosion.png'], program)
explosao.set_model(0.0, 0, 0, 1, 40, 0, -23, 0.2, 0.2, 0.2)

arma = Object.Object(loader, 'objetos/arma/AK-47.obj', ['objetos/arma/Material_44.png'], program)
arma.set_model(90.0, -1, 0.0, 0, 3.2, 0.885, -20.7, 0.006, 0.006, 0.006)

comida1 = Object.Object(loader, 'objetos/comida/Canned_Food.obj', ['objetos/comida/Can3.png'], program)
comida1.set_model(0.0, 1, 0.0, 0, 3.3, 0.885, -19, 0.015, 0.015, 0.015)

comida2 = Object.Object(loader, 'objetos/comida/Canned_Food.obj', ['objetos/comida/Can3.png'], program)
comida2.set_model(0.0, 1, 0.0, 0, 3.3, 0.885, -19.2, 0.015, 0.015, 0.015)

jornal = Object.Object(loader, 'objetos/jornal/old_newspaper.obj', ['objetos/jornal/standardSurface1.png'], program)
jornal.set_model(270.0, 0, 1.0, 0, 3.3, 0.885, -20, 0.0005, 0.0005, 0.0005)

telefone = Object.Object(loader, 'objetos/telefone/Antique_Old_Telephone.obj', ['objetos/telefone/AntiquePhone.png'], program)
telefone.set_model(180.0, 0, 1, 0, -1.6, 1.2, -16.08, 0.005, 0.005, 0.005)

sky = Object.Object(loader, 'objetos/skybox/skybox.obj', ['objetos/skybox/skybox2.webp'], program)
sky.set_model(0.0, 0, 0, 0, 0, 6.0, 0, 100.0, 100.0,100.0)

plane = Object.Object(loader, 'objetos/plane/plane.obj', ['objetos/plane/plane.png'], program)
plane.set_model(0.0, 0, 0, 0, 45, 22.0, -23, 1.0, 1.0,1.0)

floor = Object.Object(loader, 'objetos/floor/floor.obj', ['objetos/floor/floor.jpg'], program)
floor.set_model(0.0, 0, 0, 0, 0, -0.51, 0, 100.0, 0,100.0)


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
    bunker.draw()
    mesa.draw()
    cadeira.draw( )
    sacodormir.draw( )
    cacto.draw()
    bomba.draw()
    explosao.draw()
    arma.draw()
    comida1.draw()
    comida2.draw()
    jornal.draw()
    telefone.draw()
    sky.draw()
    floor.draw()
    glfw.swap_buffers(window)

glfw.terminate()