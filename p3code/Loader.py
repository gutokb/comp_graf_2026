from OpenGL.GL import *
from PIL import Image
import numpy as np
import os
import ctypes

class Loader:
    vertices_list = []    
    textures_coord_list = []
    numberTextures = 0
    program = 0

    def __init__(self,nprogram):
        glEnable(GL_TEXTURE_2D)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        glEnable(GL_LINE_SMOOTH)
        self.program = nprogram

    def load_model_from_file(self, filename):
        # Convert relative path to absolute path based on this script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, filename)
   
        objects = {}
        vertices = []
        texture_coords = []
        faces = []

        material = None

        # abre o arquivo obj para leitura
        for line in open(filename, "r"): ## para cada linha do arquivo .obj
            if line.startswith('#'): continue ## ignora comentarios
            values = line.split() # quebra a linha por espaço
            if not values: continue

            ### recuperando vertices
            if values[0] == 'v':
                vertices.append(values[1:4])

            ### recuperando coordenadas de textura
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            ### recuperando faces 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

        model = {}
        model['vertices'] = vertices
        model['texture'] = texture_coords
        model['faces'] = faces

        return model


    def load_texture_from_file(self, texture_id, img_textura):
        # Convert relative path to absolute path based on this script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_textura = os.path.join(script_dir, img_textura)
        
        print(texture_id)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        img = Image.open(img_textura)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)
        #image_data = np.array(list(img.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)



    '''
    É possível encontrar, na Internet, modelos .obj cujas faces não sejam triângulos. Nesses casos, precisamos gerar triângulos a partir dos vértices da face.
    A função abaixo retorna a sequência de vértices que permite isso. Créditos: Hélio Nogueira Cardoso e Danielle Modesti (SCC0650 - 2024/2).
    '''
    def circular_sliding_window_of_three(self, arr):
        if len(arr) == 3:
            return arr
        circular_arr = arr + [arr[0]]
        result = []
        for i in range(len(circular_arr) - 2):
            result.extend(circular_arr[i:i+3])
        return result
    
    def load_obj_and_texture(self,objFile, texturesList):
        print(objFile)
        modelo = self.load_model_from_file(objFile)
        
        ### inserindo vertices do modelo no vetor de vertices
        verticeInicial = len(self.vertices_list)
        print('Processando modelo {}. Vertice inicial: {}'.format(objFile, len(self.vertices_list)))
        faces_visited = []
        for face in modelo['faces']:
            if face[2] not in faces_visited:
                faces_visited.append(face[2])
            for vertice_id in self.circular_sliding_window_of_three(face[0]):
                self.vertices_list.append(modelo['vertices'][vertice_id - 1])
            for texture_id in self.circular_sliding_window_of_three(face[1]):
                self.textures_coord_list.append(modelo['texture'][texture_id - 1])
            
        verticeFinal = len(self.vertices_list)
        print('Processando modelo {}. Vertice final: {}'.format(objFile, len(self.vertices_list)))
        
        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        for i in range(len(texturesList)):
            self.load_texture_from_file(self.numberTextures,texturesList[i])
            self.numberTextures += 1
        
        return verticeInicial, verticeFinal - verticeInicial, self.numberTextures-1
    
    def upload(self):
        buffer_VBO = glGenBuffers(2)
        vertices = np.zeros(len(self.vertices_list), [("position", np.float32, 3)])
        vertices['position'] = self.vertices_list


        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

        textures = np.zeros(len(self.textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
        textures['position'] = self.textures_coord_list


        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self.program, "texture_coord")

        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)