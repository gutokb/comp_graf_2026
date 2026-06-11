from OpenGL.GL import *
import math
import numpy as np

class AmbientLight:
    def __init__(self, program, strength=0.1, color=(1,1,1)):
        self._loc_strength = glGetUniformLocation(program, "ambient_strength")
        self._loc_color    = glGetUniformLocation(program, "ambient_color")
        self.set_strength(strength)
        self.set_color(color)

    def set_strength(self, v):
        glUniform1f(self._loc_strength, v)
    def set_color(self, c):
        glUniform3f(self._loc_color, *c)


class PointLight:
    def __init__(self, pos=(0,0,0), color=(1,1,1), constant=1.0, linear=0.09, quadratic=0.032):
        self.pos       = pos
        self.color     = color
        self.constant  = constant   # attenuation
        self.linear    = linear
        self.quadratic = quadratic


class SpotLight:
    def __init__(self, pos=(0,0,0), direction=(0,-1,0), color=(1,1,1),
                 cut_off=12.5, outer_cut_off=17.5,
                 constant=1.0, linear=0.09, quadratic=0.032):
        self.pos           = pos
        self.direction     = direction
        self.color         = color
        self.cut_off       = cut_off        # inner cone angle in degrees
        self.outer_cut_off = outer_cut_off  # outer cone angle in degrees
        self.constant      = constant
        self.linear        = linear
        self.quadratic     = quadratic


class LightManager:
    def __init__(self, program, shininess=32.0, far_plane=100.0):
        self._program    = program
        self._point_lights = []
        self._spot_lights  = []
        self._loc_shininess      = glGetUniformLocation(program, "shininess")
        self._loc_num_point      = glGetUniformLocation(program, "num_point_lights")
        self._loc_num_spot       = glGetUniformLocation(program, "num_spot_lights")
        self._loc_view_pos       = glGetUniformLocation(program, "view_pos")
        self._far_plane = far_plane
        self.set_shininess(shininess)

    def set_shininess(self, v):
        glUniform1f(self._loc_shininess, v)

    def add_point_light(self, light: PointLight):
        self._point_lights.append(light)

    def add_spot_light(self, light: SpotLight):
        self._spot_lights.append(light)

    def set_view_pos(self, pos):
        glUniform3f(self._loc_view_pos, *pos)
        self._view_pos = pos

    def upload(self, pos, spot_shadow_maps=None):
        from OpenGL.GL import glUniform1i, glUniform1f, glUniform3f
        glUniform1i(self._loc_num_point, len(self._point_lights))
        glUniform1i(self._loc_num_spot,  len(self._spot_lights))
        self.set_view_pos(pos)

        for i, pl in enumerate(self._point_lights):
            glUniform3f(glGetUniformLocation(self._program, f"point_lights[{i}].pos"),       *pl.pos)
            glUniform3f(glGetUniformLocation(self._program, f"point_lights[{i}].color"),     *pl.color)
            glUniform1f(glGetUniformLocation(self._program, f"point_lights[{i}].constant"),  pl.constant)
            glUniform1f(glGetUniformLocation(self._program, f"point_lights[{i}].linear"),    pl.linear)
            glUniform1f(glGetUniformLocation(self._program, f"point_lights[{i}].quadratic"), pl.quadratic)

        for i, sl in enumerate(self._spot_lights):
            glUniform3f(glGetUniformLocation(self._program, f"spot_lights[{i}].pos"),             *sl.pos)
            glUniform3f(glGetUniformLocation(self._program, f"spot_lights[{i}].direction"),       *sl.direction)
            glUniform3f(glGetUniformLocation(self._program, f"spot_lights[{i}].color"),           *sl.color)
            glUniform1f(glGetUniformLocation(self._program, f"spot_lights[{i}].cut_off"),         math.cos(math.radians(sl.cut_off)))
            glUniform1f(glGetUniformLocation(self._program, f"spot_lights[{i}].outer_cut_off"),   math.cos(math.radians(sl.outer_cut_off)))
            glUniform1f(glGetUniformLocation(self._program, f"spot_lights[{i}].constant"),        sl.constant)
            glUniform1f(glGetUniformLocation(self._program, f"spot_lights[{i}].linear"),          sl.linear)
            glUniform1f(glGetUniformLocation(self._program, f"spot_lights[{i}].quadratic"),       sl.quadratic)
            if spot_shadow_maps:
                mat = spot_shadow_maps[i].get_light_space_matrix(sl, self._far_plane)
                loc = glGetUniformLocation(self._program,
                                        f"spot_light_space_matrices[{i}]")
                glUniformMatrix4fv(loc, 1, GL_TRUE, np.array(mat))