import Setter
import glfw
import Lights
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import random
import Loader
import Object
import Camera
from ShadowMap import CubeShadowMap, SpotShadowMap

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

ambient = Lights.AmbientLight(program, strength=0.1, color=(1,1,1))

manager = Lights.LightManager(program, shininess=32.0)

# spot[0]: luz do avião (exterior)
plane_light = Lights.SpotLight(pos=(0, 20.50, 0), direction=(2,-1,0), color=(1,1,1), linear=0.014, quadratic=0.007)
manager.add_spot_light(plane_light)
# point[0]: luz do bunker (laranja)
manager.add_point_light(Lights.PointLight(pos=(-1.45, 2.50, 0.11), color=(1,0.5,0.2)))
# spot[1]: lanterna
manager.add_spot_light(Lights.SpotLight(pos=(1.45, -0.15, -2.45), direction=(0,0,1)))

free = False
detonate = False
collapse = False
angle_limit = 90
ambient_enabled = True
ambient_st = 0.1

plane_t = [-70.0, 0.0, 0.0]

bomb_t  = [-70.0, 0.0, 0.0]
bomb_r1 = [0.0, 0.0, 0.0, 1.0]
bomb_s  = [1.0, 1.0, 1.0]

explode_t = [0.0, 0.0, 0.0]
explode_s = [0.0, 0.0, 0.0]

rubble    = [1.0, 1.0, 1.0]
destroyed = [0.0, 0.0, 0.0]

entulho = Object.Object(loader, 'objetos/entulho/entulho.obj', ['objetos/entulho/entulho.png'], program)
entulho.set_model(0.0, 0, 0, 1, 0, 0, 0, 4.0, 4.0, 4.0)
entulho.set_transformations(['s'])

holo = Object.Object(loader, 'objetos/holo/holo.obj', ['objetos/holo/holo.jpg'], program)
holo.set_model(-90.0, 0, 1, 0, 2.5, 20.15, 0.2, 3.0, 3.0, 3.0)
holo.set_transformations(['t'])

bunker = Object.Object(loader, 'objetos/bunker/bunker.obj', ['objetos/bunker/bunker.jpg'], program)
bunker.set_model(0.0, 0, 0, 1, 0, 0, 0, 2.5, 2.5, 2.5)
bunker.set_transformations(['s'])

lampada = Object.Object(loader, 'objetos/lampada/lamp.obj', ['objetos/lampada/lamp.png'], program)
lampada.set_model(90.0, 1, 0, 0, -1.40, 2.65, 0.11, 0.001, 0.001, 0.001)
lampada.set_transformations(['s', 't', 'r', 't'])

lanterna = Object.Object(loader, 'objetos/lanterna/lanterna.obj', ['objetos/lanterna/lanterna.png'], program)
lanterna.set_model(-90.0, 0, 1, 0, 1.32, -0.25, -1.6, 0.0011, 0.0011, 0.0011)
lanterna.set_transformations(['s'])

porta = Object.Object(loader, 'objetos/porta/porta.obj', ['objetos/porta/porta.png'], program)
porta.set_model(90.0, 0, 1, 0, -3.20, -0.6, 0.18, 0.0099, 0.0094, 0.0090)
porta.set_transformations(['s','t','r','t'])

janela1 = Object.Object(loader, 'objetos/janela/janela.obj', ['objetos/janela/janela.png'], program)
janela1.set_model(90.0, 0, 0, 1, 1.40, 1.0, -2.45, 0.0057, 0.0057, 0.0057)
janela1.set_transformations(['s'])

janela2 = Object.Object(loader, 'objetos/janela/janela.obj', ['objetos/janela/janela.png'], program)
janela2.set_model(90.0, 0, 0, 1, 1.71, 1.1, 5.38, 0.0062, 0.0062, 0.0062)
janela2.set_transformations(['s'])

janela3 = Object.Object(loader, 'objetos/janela/janela.obj', ['objetos/janela/janela.png'], program)
janela3.set_model(90.0, 0, 1, 0, 5.935, 1.1, 1.7, 0.0074, 0.0074, 0.0074)
janela3.set_transformations(['s'])

janela4 = Object.Object(loader, 'objetos/janela/janela.obj', ['objetos/janela/janela.png'], program)
janela4.set_model(90.0, 0, 1, 0, 5.88, 0.9, -1.38, 0.0074, 0.0074, 0.0074)
janela4.set_transformations(['s'])

mesa = Object.Object(loader, 'objetos/mesa/Table.obj', ['objetos/mesa/Table_Mt.png'], program)
mesa.set_model(0.0, 0, 0, 1, 3.2, 0.173, 0, 0.012, 0.012, 0.012)
mesa.set_transformations(['s'])

cadeira = Object.Object(loader, 'objetos/cadeira/cadeira.obj', ['objetos/cadeira/cadeira.png'], program)
cadeira.set_model(90.0, 0, 1, 0, 2.3, -0.5, 0, 0.02, 0.02, 0.02)
cadeira.set_transformations(['s'])

sacodormir = Object.Object(loader, 'objetos/sleepingbag/Sleeping_bag.obj', ['objetos/sleepingbag/sleepbag.png'], program)
sacodormir.set_model(90.0, 0, 1, 0, -1.75, -0.35, -3, 0.014, 0.014, 0.014)
sacodormir.set_transformations(['s'])

cactos = []
for i in range(40):
    x = random.uniform(-90.0, 90.0)
    z = random.uniform(-90.0, 90.0)
    while(abs(z) < 10):
        z = random.uniform(-90.0, 90.0)
    s_c = random.uniform(0.25, 0.6)
    cactos.append([s_c, [x, z]])
cactotrue = Object.Object(loader, 'objetos/cactus/Cactus.obj', ['objetos/cactus/material_0.png'], program)
cactotrue.set_model(0.0, 0, 0, 1, 0.0, -0.5, 0.0, 1.0, 1.0, 1.0)
cactotrue.set_transformations(['s','t'])

tumbleweed = []
for i in range(20):
    x = random.uniform(-90.0, 90.0)
    z = random.uniform(-90.0, 90.0)
    while(abs(z) < 10):
        z = random.uniform(-90.0, 90.0)
    s_t = random.uniform(0.002, 0.008)
    tumbleweed.append([s_t, [x, z]])
tumbleweedtrue = Object.Object(loader, 'objetos/tumbleweed/Tumbleweed.obj', ['objetos/tumbleweed/Tumbleweed.png'], program)
tumbleweedtrue.set_model(0.0, 0, 0, 1, 0.0, -0.5, 0.0, 1.0, 1.0, 1.0)
tumbleweedtrue.set_transformations(['s','t'])

pedras = []
for i in range(50):
    x = random.uniform(-90.0, 90.0)
    z = random.uniform(-90.0, 90.0)
    while(abs(z) < 10):
        z = random.uniform(-90.0, 90.0)
    s_p = random.uniform(0.009, 0.05)
    pedras.append([s_p, [x, z]])
pedratrue = Object.Object(loader, 'objetos/pedra/Desert_Rock_Base.obj', ['objetos/pedra/DefaultMaterial.png'], program)
pedratrue.set_model(0.0, 0, 0, 1, 0.0, -0.5, 0.0, 1, 1, 1)
pedratrue.set_transformations(['s', 't'])

bomba = Object.Object(loader, 'objetos/bomba/Nuclear_Bomb.obj', ['objetos/bomba/Nuclear_Bomb.png'], program)
bomba.set_model(90.0, 0, 1, 0, 0, 20.0, 0.2, 0.004, 0.004, 0.004)
bomba.set_transformations(['r','t','s'])

explosao = Object.Object(loader, 'objetos/explosao/Explosion.obj', ['objetos/explosao/Explosion.png'], program)
explosao.set_model(0.0, 0, 0, 1, 0, 0, 0, 0.2, 0.2, 0.2)
explosao.set_transformations(['s','t'])

arma = Object.Object(loader, 'objetos/arma/AK-47.obj', ['objetos/arma/Material_44.png'], program)
arma.set_model(90.0, -1, 0.0, 0, 3.2, 0.885, -0.7, 0.006, 0.006, 0.006)
arma.set_transformations(['s', 't','r', 't'])

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
sky.set_model(0.0, 0, 0, 0, 0, 6.0, 0, 100.0, 100.0, 100.0)

plane = Object.Object(loader, 'objetos/plane/plane.obj', ['objetos/plane/plane.png'], program)
plane.set_model(180.0, 0, 1, 0, 0, 21.15, 0, 0.6, 0.6, 0.6)
plane.set_transformations(['t'])

floor = Object.Object(loader, 'objetos/floor/floor.obj', ['objetos/floor/floor.jpg'], program)
floor.set_model(0.0, 0, 0, 0, 0, -0.51, 0, 100.0, 1.0, 100.0)

loader.upload()

# materiais: (kd, ks, shininess)
bunker.kd,        bunker.ks,        bunker.shininess        = 0.80, 0.15,  16
entulho.kd,       entulho.ks,       entulho.shininess       = 0.80, 0.10,   8
floor.kd,         floor.ks,         floor.shininess         = 0.90, 0.05,   4
porta.kd,         porta.ks,         porta.shininess         = 0.70, 0.30,  32
janela1.kd,       janela1.ks,       janela1.shininess       = 0.20, 0.95, 256
janela2.kd,       janela2.ks,       janela2.shininess       = 0.20, 0.95, 256
janela3.kd,       janela3.ks,       janela3.shininess       = 0.20, 0.95, 256
janela4.kd,       janela4.ks,       janela4.shininess       = 0.20, 0.95, 256
mesa.kd,          mesa.ks,          mesa.shininess          = 0.75, 0.35,  32
cadeira.kd,       cadeira.ks,       cadeira.shininess       = 0.65, 0.50,  64
sacodormir.kd,    sacodormir.ks,    sacodormir.shininess    = 0.85, 0.05,   8
jornal.kd,        jornal.ks,        jornal.shininess        = 0.90, 0.02,   4
lampada.kd,       lampada.ks,       lampada.shininess       = 0.40, 0.90, 128
lanterna.kd,      lanterna.ks,      lanterna.shininess      = 0.50, 0.85, 128
bomba.kd,         bomba.ks,         bomba.shininess         = 0.45, 0.95, 256
arma.kd,          arma.ks,          arma.shininess          = 0.50, 0.85, 128
comida1.kd,       comida1.ks,       comida1.shininess       = 0.45, 0.90, 256
comida2.kd,       comida2.ks,       comida2.shininess       = 0.45, 0.90, 256
telefone.kd,      telefone.ks,      telefone.shininess      = 0.50, 0.60,  64
plane.kd,         plane.ks,         plane.shininess         = 0.55, 0.80, 128
cactotrue.kd,     cactotrue.ks,     cactotrue.shininess     = 0.80, 0.20,  16
tumbleweedtrue.kd, tumbleweedtrue.ks, tumbleweedtrue.shininess = 0.80, 0.05, 4
pedratrue.kd,     pedratrue.ks,     pedratrue.shininess     = 0.75, 0.15,  16
sky.kd,           sky.ks,           sky.shininess           = 1.00, 0.00,   1
explosao.kd,      explosao.ks,      explosao.shininess      = 1.00, 0.00,   1

# objetos que respondem ao ajuste de kd/ks pelo teclado (exclui skybox)
scene_objects = [
    bunker, entulho, floor, porta,
    janela1, janela2, janela3, janela4,
    mesa, cadeira, sacodormir, jornal,
    lampada, lanterna, bomba, arma, comida1, comida2, telefone, plane,
    cactotrue, tumbleweedtrue, pedratrue,
]

glEnable(GL_DEPTH_TEST)
polygonal_mode = False

original_key_event = camera.key_event
def key_event(window, key, scancode, action, mods):
    global polygonal_mode, free, detonate, bomb_r1, bomb_s, bomb_t, explode_s, explode_t, rubble, angle_limit, collapse, destroyed, ambient_enabled, ambient_st
    original_key_event(window, key, scancode, action, mods)

    # luzes: 1=ambiente  2=bunker(point0)  3=avião(spot0)  4=lanterna(spot1)
    if key == glfw.KEY_1 and action == glfw.PRESS:
        ambient_enabled = not ambient_enabled
    if key == glfw.KEY_2 and action == glfw.PRESS:
        manager._point_lights[0].enabled = not manager._point_lights[0].enabled
    if key == glfw.KEY_3 and action == glfw.PRESS:
        manager._spot_lights[0].enabled = not manager._spot_lights[0].enabled
    if key == glfw.KEY_4 and action == glfw.PRESS:
        manager._spot_lights[1].enabled = not manager._spot_lights[1].enabled

    # difusa: 5=+ 6=−   especular: 7=+ 8=−
    if key == glfw.KEY_5 and (action == glfw.PRESS or action == glfw.REPEAT):
        for obj in scene_objects: obj.kd = min(1.0, obj.kd + 0.05)
    if key == glfw.KEY_6 and (action == glfw.PRESS or action == glfw.REPEAT):
        for obj in scene_objects: obj.kd = max(0.0, obj.kd - 0.05)
    if key == glfw.KEY_7 and (action == glfw.PRESS or action == glfw.REPEAT):
        for obj in scene_objects: obj.ks = min(1.0, obj.ks + 0.05)
    if key == glfw.KEY_8 and (action == glfw.PRESS or action == glfw.REPEAT):
        for obj in scene_objects: obj.ks = max(0.0, obj.ks - 0.05)

    # ambiente: seta cima=+ seta baixo=−
    if key == glfw.KEY_UP and (action == glfw.PRESS or action == glfw.REPEAT):
        if ambient_st < 1.0: ambient_st += 0.05
    if key == glfw.KEY_DOWN and (action == glfw.PRESS or action == glfw.REPEAT):
        if ambient_st > 0.0: ambient_st -= 0.05

    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if bomb_t[0] > -30 and bomb_t[0] < -10:
            angle_limit = 80
        free = True

    if key == glfw.KEY_P and action == glfw.PRESS:
        polygonal_mode = not polygonal_mode

    if key == glfw.KEY_RIGHT and (action == glfw.PRESS or action == glfw.REPEAT):
        plane_t[0] += 0.6
        if not free:
            bomb_t = plane_t.copy()
        else:
            if bomb_r1[0] >= -angle_limit:
                bomb_r1[0] -= 0.90
            elif not detonate:
                detonate = True
                explode_s = [0.03, 0.03, 0.03]
                bomb_s = [0.0, 0.0, 0.0]
                explode_t = bomb_t.copy()
                explode_t[0] += 20.0
                if angle_limit < 90:
                    explode_t[1] += 3.0
                if -15 < explode_t[0] < 15:
                    rubble    = [0.0, 0.0, 0.0]
                    destroyed = [1.0, 1.0, 1.0]

        if detonate and explode_s[0] < 1.5 and not collapse:
            explode_s[0] += 0.05
            explode_s[1] += 0.05
            explode_s[2] += 0.05
            explode_t[1] += 0.2
            if explode_s[0] > 1.5:
                collapse = True

        if collapse and explode_s[0] > 0:
            explode_s[0] -= 0.0125
            explode_s[1] -= 0.0125
            explode_s[2] -= 0.0125
            explode_t[1] -= 0.05
            if explode_s[0] < 0:
                explode_s = [0.0, 0.0, 0.0]

glfw.set_key_callback(window, key_event)

depth_program      = Setter.make_depth_program()
spot_depth_program = Setter.make_spot_depth_program()

far_plane = 100.0

point_shadow_maps = [CubeShadowMap(1024) for _ in range(len(manager._point_lights))]
spot_shadow_maps  = [SpotShadowMap(1024) for _ in range(len(manager._spot_lights))]

# objetos que projetam sombra
all_objects = [bunker, floor, mesa, porta, janela1, janela2, janela3, janela4, cadeira]

glfw.show_window(window)
while not glfw.window_should_close(window):

    if destroyed[0] == 1.0:
        manager._point_lights[0].enabled = False
        manager._spot_lights[1].enabled = False

    glfw.poll_events()
    camera.tick(glfw.get_time())

    # pass 1: sombras de point lights (cubemap)
    glUseProgram(depth_program)
    for i, (pl, sm) in enumerate(zip(manager._point_lights, point_shadow_maps)):
        matrices = sm.get_shadow_matrices(pl.pos, far_plane)
        for j, mat in enumerate(matrices):
            glUniformMatrix4fv(glGetUniformLocation(depth_program, f"shadow_matrices[{j}]"), 1, GL_TRUE, np.array(mat))
        glUniform3f(glGetUniformLocation(depth_program, "light_pos"), *pl.pos)
        glUniform1f(glGetUniformLocation(depth_program, "far_plane"), far_plane)
        sm.bind()
        for obj in all_objects: obj.draw(override_program=depth_program)
        sm.unbind(largura, altura)

    # pass 2: sombras de spot lights (2D)
    glUseProgram(spot_depth_program)
    for i, (sl, sm) in enumerate(zip(manager._spot_lights, spot_shadow_maps)):
        mat = sm.get_light_space_matrix(sl, far_plane)
        glUniformMatrix4fv(glGetUniformLocation(spot_depth_program, "light_space_matrix"), 1, GL_TRUE, np.array(mat))
        sm.bind()
        for obj in all_objects: obj.draw(override_program=spot_depth_program)
        sm.unbind(largura, altura)

    # pass 3: render principal
    glFinish()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(program)
    glUniform1i(glGetUniformLocation(program, "imagem"), 0)
    ambient.set_strength(ambient_st if ambient_enabled else 0.0)

    for i, sm in enumerate(point_shadow_maps):
        glActiveTexture(GL_TEXTURE1 + i)
        glBindTexture(GL_TEXTURE_CUBE_MAP, sm.cubemap)
        glUniform1i(glGetUniformLocation(program, f"shadow_cubemaps[{i}]"), 1 + i)

    for i, sm in enumerate(spot_shadow_maps):
        glActiveTexture(GL_TEXTURE0 + 5 + i)  # binding = 5 no fragment shader
        glBindTexture(GL_TEXTURE_2D, sm.texture)
        glUniform1i(glGetUniformLocation(program, f"spot_shadow_maps[{i}]"), 5 + i)

    glUniform1f(glGetUniformLocation(program, "far_plane"), far_plane)
    manager.upload(camera.get_position(), spot_shadow_maps=spot_shadow_maps)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if polygonal_mode else GL_FILL)

    glUniformMatrix4fv(glGetUniformLocation(program, "view"),       1, GL_TRUE, camera.get_view())
    glUniformMatrix4fv(glGetUniformLocation(program, "projection"), 1, GL_TRUE, camera.get_projection())

    plane_light.pos = (plane_t[0], 21.15, plane_t[2])

    entulho.set_parameters(0, destroyed)
    entulho.draw()

    bunker.set_parameters(0, rubble)
    bunker.draw()

    lampada.set_parameters(0, rubble)
    lampada.set_parameters(1, [1.4, -2.65, -0.11])
    lampada.set_parameters(2, [90.0, 0.0, -1.0, 0.0])
    lampada.set_parameters(3, [-1.4, 2.65, 0.11])
    lampada.draw()

    lanterna.set_parameters(0, rubble)
    lanterna.draw()

    porta.set_parameters(0, rubble)
    #porta.set_parameters(1,[3.20, 0.6, -0.18])
    #porta.set_parameters(2,[90.0, 0, 0, 1])
    #porta.set_parameters(3,[-3.20, -0.5, 0.18])
    porta.draw()

    janela1.set_parameters(0, rubble)
    janela1.draw()

    janela2.set_parameters(0, rubble)
    janela2.draw()

    janela3.set_parameters(0, rubble)
    janela3.draw()

    janela4.set_parameters(0, rubble)
    janela4.draw()

    mesa.set_parameters(0, rubble)
    mesa.draw()

    cadeira.set_parameters(0, rubble)
    cadeira.draw()

    sacodormir.set_parameters(0, rubble)
    sacodormir.draw()

    for cacto in cactos:
        cactotrue.set_parameters(0, [cacto[0], cacto[0], cacto[0]])
        cactotrue.set_parameters(1, [cacto[1][0], 0.0, cacto[1][1]])
        cactotrue.draw()

    for t in tumbleweed:
        tumbleweedtrue.set_parameters(0, [t[0], t[0], t[0]])
        tumbleweedtrue.set_parameters(1, [t[1][0], 0.0, t[1][1]])
        tumbleweedtrue.draw()

    for p in pedras:
        pedratrue.set_parameters(0, [p[0], p[0], p[0]])
        pedratrue.set_parameters(1, [p[1][0], 0.0, p[1][1]])
        pedratrue.draw()

    plane.set_parameters(0, plane_t)
    plane.draw()

    holo.set_parameters(0, plane_t)
    holo.draw()

    bomba.set_parameters(0, bomb_r1)
    bomba.set_parameters(1, bomb_t)
    bomba.set_parameters(2, bomb_s)
    bomba.draw()

    explosao.set_parameters(0, explode_s)
    explosao.set_parameters(1, explode_t)
    explosao.draw()

    arma.set_parameters(0, rubble)
    arma.set_parameters(1, [-3.2, -0.885, 0.7])
    arma.set_parameters(2, [45.0, 0.0, -1.0, 0.0])
    arma.set_parameters(3, [3.2, 0.885, -0.7])
    arma.draw()

    comida1.set_parameters(0, rubble)
    comida1.draw()

    comida2.set_parameters(0, rubble)
    comida2.draw()

    jornal.set_parameters(0, rubble)
    jornal.draw()

    telefone.set_parameters(0, rubble)
    telefone.draw()

    sky.draw()
    floor.draw()

    glfw.swap_buffers(window)

glfw.terminate()
