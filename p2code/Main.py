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

free = False
detonate = False
collapse = False
angle_limit = 90

plane_t = [-70.0, 0.0, 0.0]


bomb_t = [-70.0, 0.0, 0.0]
bomb_r1 = [0.0, 0.0, 0.0, 1.0]
bomb_s = [1.0, 1.0, 1.0]


explode_t = [0.0, 0.0, 0.0]
explode_s = [0.0, 0.0, 0.0]

rubble = [1.0, 1.0, 1.0]

bunker = Object.Object(loader, 'objetos/bunker/bunker.obj', ['objetos/bunker/bunker.jpg'], program)
bunker.set_model(0.0, 0, 0, 1, 0, 0, 0, 2.5, 2.5, 2.5)
bunker.set_transformations(['s'])

mesa = Object.Object(loader, 'objetos/mesa/Table.obj', ['objetos/mesa/Table_Mt.png'], program)
mesa.set_model(0.0, 0, 0, 1, 3.2, 0.173, 0, 0.012, 0.012, 0.012)
mesa.set_transformations(['s'])

cadeira = Object.Object(loader, 'objetos/cadeira/cadeira.obj', ['objetos/cadeira/cadeira.png'], program)
cadeira.set_model(90.0, 0, 1, 0, 2.3, -0.5, 0, 0.02, 0.02, 0.02)
cadeira.set_transformations(['s'])

sacodormir = Object.Object(loader, 'objetos/sleepingbag/Sleeping_bag.obj', ['objetos/sleepingbag/sleepbag.png'], program)
sacodormir.set_model(90.0, 0, 1, 0, -1.75, -0.35, -3, 0.014, 0.014, 0.014)
sacodormir.set_transformations(['s'])

cacto = Object.Object(loader, 'objetos/cactus/Cactus.obj', ['objetos/cactus/material_0.png'], program)
cacto.set_model(0.0, 0, 0, 1, 12, -0.5, -14, 0.3, 0.3, 0.3)

bomba = Object.Object(loader, 'objetos/bomba/Nuclear_Bomb.obj', ['objetos/bomba/Nuclear_Bomb.png'], program)
bomba.set_model(90.0, 0, 1, 0, 0, 20.0, 0.2, 0.004, 0.004, 0.004)
bomba.set_transformations(['r','t','s'])

explosao = Object.Object(loader, 'objetos/explosao/Explosion.obj', ['objetos/explosao/Explosion.png'], program)
explosao.set_model(0.0, 0, 0, 1, 0, 0, 0, 0.2, 0.2, 0.2)
explosao.set_transformations(['s','t'])

arma = Object.Object(loader, 'objetos/arma/AK-47.obj', ['objetos/arma/Material_44.png'], program)
arma.set_model(90.0, -1, 0.0, 0, 3.2, 0.885, -0.7, 0.006, 0.006, 0.006)
arma.set_transformations(['s'])

comida1 = Object.Object(loader, 'objetos/comida/Canned_Food.obj', ['objetos/comida/Can3.png'], program)
comida1.set_model(0.0, 1, 0.0, 0, 3.3, 0.885, 1.0, 0.015, 0.015, 0.015)
comida1.set_transformations(['s'])

comida2 = Object.Object(loader, 'objetos/comida/Canned_Food.obj', ['objetos/comida/Can3.png'], program)
comida2.set_model(0.0, 1, 0.0, 0, 3.3, 0.885, 0.8, 0.015, 0.015, 0.015)
comida2.set_transformations(['s'])

jornal = Object.Object(loader, 'objetos/jornal/old_newspaper.obj', ['objetos/jornal/standardSurface1.png'], program)
jornal.set_model(270.0, 0, 1.0, 0, 3.3, 0.885, 0, 0.0005, 0.0005, 0.0005)
jornal.set_transformations(['s'])

telefone = Object.Object(loader, 'objetos/telefone/Antique_Old_Telephone.obj', ['objetos/telefone/AntiquePhone.png'], program)
telefone.set_model(180.0, 0, 1, 0, -1.6, 1.2, 3.92, 0.005, 0.005, 0.005)
telefone.set_transformations(['s'])

sky = Object.Object(loader, 'objetos/skybox/skybox.obj', ['objetos/skybox/skybox2.webp'], program)
sky.set_model(0.0, 0, 0, 0, 0, 6.0, 0, 100.0, 100.0,100.0)

plane = Object.Object(loader, 'objetos/plane/plane.obj', ['objetos/plane/plane.png'], program)
plane.set_model(180.0, 0, 1, 0, 0, 21.15, 0, 0.6, 0.6,0.6)
plane.set_transformations(['t',])

floor = Object.Object(loader, 'objetos/floor/floor.obj', ['objetos/floor/floor.jpg'], program)
floor.set_model(0.0, 0, 0, 0, 0, -0.51, 0, 100.0, 0,100.0)


loader.upload()

glEnable(GL_DEPTH_TEST)
polygonal_mode = False

# wrap key_event to also handle polygonal mode toggle
original_key_event = camera.key_event
def key_event(window, key, scancode, action, mods):
    global polygonal_mode, free, detonate, bomb_r1, bomb_s, bomb_t, explode_s, explode_t, rubble, angle_limit, collapse
    original_key_event(window, key, scancode, action, mods)

    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if bomb_t[0]> -30 and bomb_t[0] < -10:
            angle_limit = 80

        free = True

    if key == glfw.KEY_P and action == glfw.PRESS:
        polygonal_mode = not polygonal_mode

    if key == glfw.KEY_RIGHT and (action == glfw.PRESS or action == glfw.REPEAT):
        plane_t[0] += 0.6
        if (free == False):
            bomb_t = plane_t.copy()
        else:
            if bomb_r1[0] >= - angle_limit:
                bomb_r1[0] -= 0.90

            elif detonate == False:
                detonate = True
                explode_s = [0.03, 0.03, 0.03]
                bomb_s = [0.0, 0.0, 0.0]
                explode_t = bomb_t.copy()
                explode_t[0] += 20.0
                if angle_limit < 90:
                    explode_t[1] += 3.0
                if explode_t[0] > -15 and explode_t[0] < 15:
                    rubble = [0.0, 0.0, 0.0]

        if (detonate == True) and (explode_s[0] < 1.5) and (collapse == False):
            explode_s[0] += 0.05
            explode_s[1] += 0.05
            explode_s[2] += 0.05
            explode_t[1] += 0.2
            if explode_s[0] > 1.5:
                collapse = True

        if (collapse == True) and explode_s[0] > 0:
            explode_s[0] -= 0.0125
            explode_s[1] -= 0.0125
            explode_s[2] -= 0.0125
            explode_t[1] -= 0.05
            if explode_s[0] < 0:
                explode_s = [0.0, 0.0, 0.0]

    
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
    bunker.set_parameters(0,rubble)
    bunker.draw()
    

    mesa.set_parameters(0,rubble)
    mesa.draw()
    

    cadeira.set_parameters(0,rubble)
    cadeira.draw()
    

    sacodormir.set_parameters(0,rubble)
    sacodormir.draw()
    


    cacto.draw()

    plane.set_parameters(0,plane_t)
    plane.draw()

    bomba.set_parameters(0,bomb_r1)
    bomba.set_parameters(1,bomb_t)
    bomba.set_parameters(2,bomb_s)
    bomba.draw()

    explosao.set_parameters(0, explode_s)
    explosao.set_parameters(1, explode_t)
    explosao.draw()

    arma.set_parameters(0,rubble)
    arma.draw()
    

    comida1.set_parameters(0,rubble)
    comida1.draw()
    

    comida2.set_parameters(0,rubble)
    comida2.draw()
    

    jornal.set_parameters(0,rubble)
    jornal.draw()
    

    telefone.set_parameters(0,rubble)
    telefone.draw()
    


    sky.draw()


    floor.draw()


    glfw.swap_buffers(window)

glfw.terminate()