from OpenGL.GL import *
import numpy as np
import glm

class Object:
    def __init__(self, loader, obj, texture, program):
        self.loader = loader
        self.start, self.qt, self.textureId = loader.load_obj_and_texture(obj, texture)
        self.program = program
        self.mat_model = np.array(glm.mat4(1.0))
        self.transformations = []  # list of chars: 't', 'r', 's'
        self.parameters = []       # list of float lists, one per transformation
        self.mat_transform = np.eye(4,4)
        self.visible = True 

    def set_model(self, angle_deg, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
        m = glm.mat4(1.0)
        m = glm.translate(m, glm.vec3(t_x, t_y, t_z))
        if angle_deg != 0:
            m = glm.rotate(m, glm.radians(angle_deg), glm.vec3(r_x, r_y, r_z))
        m = glm.scale(m, glm.vec3(s_x, s_y, s_z))
        self.mat_model = np.array(m)

    def set_transformations(self, chars: list[str]):
        """Set the transformation sequence as a list of chars: 't', 'r', 's'.
        Parameters must be set afterwards with set_parameters().
        Example: obj.set_transformations(['t', 'r', 's'])
        """
        for c in chars:
            if c not in ('t', 'r', 's'):
                raise ValueError(f"Invalid transformation '{c}'. Use 't', 'r', or 's'.")
        self.transformations = chars
        self.parameters = [None] * len(chars)

    def set_parameters(self, index: int, params: list[float]):
        """Set the float parameters for the transformation at the given index.
        't' expects [t_x, t_y, t_z]
        'r' expects [angle_deg, r_x, r_y, r_z]
        's' expects [s_x, s_y, s_z]
        """
        expected = {'t': 3, 'r': 4, 's': 3}
        kind = self.transformations[index]
        if len(params) != expected[kind]:
            raise ValueError(
                f"Transformation '{kind}' at index {index} expects "
                f"{expected[kind]} parameters, got {len(params)}."
            )
        self.parameters[index] = list(params)

    def _build_matrix(self, kind, params):
        m = glm.mat4(1.0)
        if kind == 't':
            m = glm.translate(m, glm.vec3(*params))
        elif kind == 'r':
            m = glm.rotate(m, glm.radians(params[0]), glm.vec3(*params[1:]))
        elif kind == 's':
            m = glm.scale(m, glm.vec3(*params))
        return m

    def _combined_transform(self):
        combined = glm.mat4(1.0)
        for kind, params in zip(reversed(self.transformations), reversed(self.parameters)):
            if params is None:
                continue  # skip unset transformations instead of crashing
            combined = combined * self._build_matrix(kind, params)
        return np.array(combined)
    


    def clear_transformations(self):
        self.transformations = []
        self.parameters = []

    def draw(self, override_program=None):
        if not self.visible:
            return

        prog = override_program if override_program else self.program
        glUseProgram(prog)

        glBindVertexArray(self.loader.vao)   # add this

        loc_model = glGetUniformLocation(prog, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, self.mat_model)

        if self.transformations:
            self.mat_transform = self._combined_transform()
            loc = glGetUniformLocation(prog, "mat_transformation")
            glUniformMatrix4fv(loc, 1, GL_TRUE, self.mat_transform)

        if override_program is None:
            glBindTexture(GL_TEXTURE_2D, self.textureId)


        from OpenGL.GL import glGetIntegerv, GL_CURRENT_PROGRAM, GL_VERTEX_ARRAY_BINDING
        current_program = glGetIntegerv(GL_CURRENT_PROGRAM)
        current_vao = glGetIntegerv(GL_VERTEX_ARRAY_BINDING)
        print(f"pre-draw: program={current_program}, vao={current_vao}, start={self.start}, qt={self.qt}")

        # check each attribute
        for loc, name in [(0, 'position'), (1, 'texture_coord'), (2, 'normal')]:
            enabled = glGetVertexAttribiv(loc, GL_VERTEX_ATTRIB_ARRAY_ENABLED)
            print(f"  attrib {loc} ({name}): enabled={enabled}")


        glDrawArrays(GL_TRIANGLES, self.start, self.qt)
        glBindVertexArray(0)               # add this

