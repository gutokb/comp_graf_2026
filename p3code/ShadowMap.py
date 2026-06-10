from OpenGL.GL import *
import glm
import numpy as np


class CubeShadowMap:
    def __init__(self, resolution=1024):
        self.resolution = resolution
        self.fbo        = None
        self.cubemap    = None
        self._setup()

    def _setup(self):
        self.fbo = glGenFramebuffers(1)

        self.cubemap = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubemap)
        for i in range(6):
            glTexImage2D(
                GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0,
                GL_DEPTH_COMPONENT, self.resolution, self.resolution,
                0, GL_DEPTH_COMPONENT, GL_FLOAT, None
            )
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, self.cubemap, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)

        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError(f"Shadow FBO incomplete: {status}")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def get_shadow_matrices(self, light_pos, far_plane):
        pos = glm.vec3(*light_pos)
        proj = glm.perspective(glm.radians(90.0), 1.0, 0.1, far_plane)
        return [
            proj * glm.lookAt(pos, pos + glm.vec3( 1, 0, 0), glm.vec3(0,-1, 0)),
            proj * glm.lookAt(pos, pos + glm.vec3(-1, 0, 0), glm.vec3(0,-1, 0)),
            proj * glm.lookAt(pos, pos + glm.vec3( 0, 1, 0), glm.vec3(0, 0, 1)),
            proj * glm.lookAt(pos, pos + glm.vec3( 0,-1, 0), glm.vec3(0, 0,-1)),
            proj * glm.lookAt(pos, pos + glm.vec3( 0, 0, 1), glm.vec3(0,-1, 0)),
            proj * glm.lookAt(pos, pos + glm.vec3( 0, 0,-1), glm.vec3(0,-1, 0)),
        ]

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.resolution, self.resolution)
        glClear(GL_DEPTH_BUFFER_BIT)

    def unbind(self, viewport_w, viewport_h):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, viewport_w, viewport_h)


class SpotShadowMap:
    def __init__(self, resolution=1024):
        self.resolution = resolution
        self.fbo        = None
        self.texture    = None
        self._setup()

    def _setup(self):
        self.fbo = glGenFramebuffers(1)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT,
                     self.resolution, self.resolution,
                     0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        # areas outside the light frustum should not be shadowed
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR,
                         np.array([1,1,1,1], dtype=np.float32))

        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                               GL_TEXTURE_2D, self.texture, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)

        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError(f"Spot shadow FBO incomplete: {status}")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def get_light_space_matrix(self, light, far_plane):
        pos  = glm.vec3(*light.pos)
        dire = glm.vec3(*light.direction)
        proj = glm.perspective(
            glm.radians(light.outer_cut_off * 2.0), 1.0, 0.1, far_plane
        )
        # pick an up vector that isn't parallel to direction
        up = glm.vec3(0,1,0) if abs(dire.y) < 0.99 else glm.vec3(1,0,0)
        view = glm.lookAt(pos, pos + dire, up)
        return proj * view

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.resolution, self.resolution)
        glClear(GL_DEPTH_BUFFER_BIT)

    def unbind(self, viewport_w, viewport_h):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, viewport_w, viewport_h)