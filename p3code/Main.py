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
manager.add_point_light(Lights.PointLight(pos=(10,10,10), color=(1,1,1)))
manager.add_point_light(Lights.PointLight(pos=(-10,5,0), color=(1,0.5,0.2)))  # warm light
manager.add_spot_light(Lights.SpotLight(pos=(0,10,0), direction=(0,-1,0)))






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

destroyed = [0.0, 0.0, 0.0]

'''entulho = Object.Object(loader, 'objetos/entulho/entulho.obj', ['objetos/entulho/entulho.png'], program)
entulho.set_model(0.0, 0, 0, 1, 0, 0, 0, 4.0, 4.0, 4.0)
entulho.set_transformations(['s'])'''


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

cactos = []
for i in range(40):
    x = random.uniform(-90.0, 90.0)
    z = random.uniform(-90.0, 90.0)
    while(abs(z) < 10):
        z = random.uniform(-90.0, 90.0)
    s_c = random.uniform(0.25, 0.6)
    cacto_t = [x,z]
    cacto = [s_c, cacto_t]
    cactos.append(cacto)
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
    tumble_t = [x,z]
    tumble = [s_t, tumble_t]
    tumbleweed.append(tumble)
tumbleweedtrue =Object.Object(loader, 'objetos/tumbleweed/Tumbleweed.obj', ['objetos/tumbleweed/Tumbleweed.png'], program)
tumbleweedtrue.set_model(0.0, 0, 0, 1, 0.0, -0.5, 0.0, 1.0, 1.0, 1.0)
tumbleweedtrue.set_transformations(['s','t'])
    
pedras = []
for i in range(50):
    x = random.uniform(-90.0, 90.0)
    z = random.uniform(-90.0, 90.0)
    while(abs(z) < 10):
        z = random.uniform(-90.0, 90.0)
    s_p = random.uniform(0.009, 0.05)
    pedra_t = [x, z]
    pedra = [s_p, pedra_t]
    pedras.append(pedra)
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
sky.set_model(0.0, 0, 0, 0, 0, 6.0, 0, 100.0, 100.0,100.0)

plane = Object.Object(loader, 'objetos/plane/plane.obj', ['objetos/plane/plane.png'], program)
plane.set_model(180.0, 0, 1, 0, 0, 21.15, 0, 0.6, 0.6,0.6)
plane.set_transformations(['t',])

floor = Object.Object(loader, 'objetos/floor/floor.obj', ['objetos/floor/floor.jpg'], program)
floor.set_model(0.0, 0, 0, 0, 0, -0.51, 0, 100.0, 0,100.0)


loader.upload()
print("VAO ID:", loader.vao)
print("vertices count:", len(loader.vertices_list))
print("normals count:", len(loader.normals_list))
print("textures count:", len(loader.textures_coord_list))

glEnable(GL_DEPTH_TEST)
polygonal_mode = False

# wrap key_event to also handle polygonal mode toggle
original_key_event = camera.key_event
def key_event(window, key, scancode, action, mods):
    global polygonal_mode, free, detonate, bomb_r1, bomb_s, bomb_t, explode_s, explode_t, rubble, angle_limit, collapse, destroyed
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
                    destroyed = [1.0, 1.0, 1.0]

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

depth_program      = Setter.make_depth_program()
spot_depth_program = Setter.make_spot_depth_program()

print("depth_program ID:", depth_program)
print("spot_depth_program ID:", spot_depth_program)
print("main program ID:", program)

far_plane          = 100.0

point_shadow_maps = [CubeShadowMap(1024) for _ in range(len(manager._point_lights))]
spot_shadow_maps  = [SpotShadowMap(1024) for _ in range(len(manager._spot_lights))]

all_objects = [bunker, plane, floor, bomba, mesa]
glfw.show_window(window)
while not glfw.window_should_close(window):
        # --- pass 1: point light cubemap depth ---
    glUseProgram(depth_program)
    for i, (pl, sm) in enumerate(zip(manager._point_lights, point_shadow_maps)):
        matrices = sm.get_shadow_matrices(pl.pos, far_plane)
        for j, mat in enumerate(matrices):
            loc = glGetUniformLocation(depth_program, f"shadow_matrices[{j}]")
            glUniformMatrix4fv(loc, 1, GL_FALSE, np.array(mat))
        glUniform3f(glGetUniformLocation(depth_program, "light_pos"), *pl.pos)
        glUniform1f(glGetUniformLocation(depth_program, "far_plane"), far_plane)
        sm.bind()
        for obj in all_objects:
            obj.draw(override_program=depth_program)
        sm.unbind(largura, altura)

    # --- pass 2: spot light 2D depth ---
    glUseProgram(spot_depth_program)
    for i, (sl, sm) in enumerate(zip(manager._spot_lights, spot_shadow_maps)):
        mat = sm.get_light_space_matrix(sl, far_plane)
        glUniformMatrix4fv(
            glGetUniformLocation(spot_depth_program, "light_space_matrix"),
            1, GL_FALSE, np.array(mat)
        )
        sm.bind()
        for obj in all_objects:
            obj.draw(override_program=spot_depth_program)
        sm.unbind(largura, altura)

    # --- pass 3: normal render ---
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(program)

    for i, sm in enumerate(point_shadow_maps):
        glActiveTexture(GL_TEXTURE0 + 8 + i)
        glBindTexture(GL_TEXTURE_CUBE_MAP, sm.cubemap)
        glUniform1i(glGetUniformLocation(program, f"shadow_cubemaps[{i}]"), 8 + i)

    offset = 8 + len(point_shadow_maps)
    for i, sm in enumerate(spot_shadow_maps):
        glActiveTexture(GL_TEXTURE0 + offset + i)
        glBindTexture(GL_TEXTURE_2D, sm.texture)
        glUniform1i(glGetUniformLocation(program, f"spot_shadow_maps[{i}]"), offset + i)

    glUniform1f(glGetUniformLocation(program, "far_plane"), far_plane)
    manager.upload(camera.get_position(), spot_shadow_maps=spot_shadow_maps)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if polygonal_mode else GL_FILL)

    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, camera.get_view())

    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, camera.get_projection())



    '''entulho.set_parameters(0,destroyed)
    entulho.draw()'''


    bunker.set_parameters(0,rubble)
    bunker.draw()
    

    mesa.set_parameters(0,rubble)
    mesa.draw()
    

    cadeira.set_parameters(0,rubble)
    cadeira.draw()
    

    sacodormir.set_parameters(0,rubble)
    sacodormir.draw()
    
    for cacto in cactos:
        cactotrue.set_parameters(0,[cacto[0],cacto[0],cacto[0]])
        cactotrue.set_parameters(1,[cacto[1][0],0.0,cacto[1][1]])
        cactotrue.draw()
        
    for t in tumbleweed:
        tumbleweedtrue.set_parameters(0,[t[0],t[0],t[0]])
        tumbleweedtrue.set_parameters(1,[t[1][0],0.0,t[1][1]])
        tumbleweedtrue.draw()
    
    for p in pedras:
        pedratrue.set_parameters(0,[p[0], p[0], p[0]])
        pedratrue.set_parameters(1,[p[1][0], 0.0, p[1][1]])
        pedratrue.draw()

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
    arma.set_parameters(1, [-3.2, -0.885, 0.7])
    arma.set_parameters(2, [45.0, 0.0, -1.0, 0.0])
    arma.set_parameters(3, [3.2, 0.885, -0.7])
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