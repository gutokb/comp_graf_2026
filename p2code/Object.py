from OpenGL.GL import *
from PIL import Image
import numpy as np
import glm
import math
import Loader


def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
       
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    if angle!=0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

class Object:
    start = 0
    qt = 0
    textureId = 0
    program = 0
    mat_model = 0

    
    def __init__(self, loader, obj, texture ,nprogram):
        self.start, self.qt, self.textureId = loader.load_obj_and_texture(obj, texture)
        self.mat_model = model(0, 0 ,0, 0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.1)
        self.program = nprogram

    def setmodel(self, angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
        self.mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)

    def draw(self,  mat_transform):
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, self.mat_model)
        loc = glGetUniformLocation(self.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, self.textureId)
        
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, self.start, self.qt) ## renderizando