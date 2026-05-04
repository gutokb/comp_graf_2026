import glfw
import glm
import numpy as np


class Camera:
    # Limite de altura: chão está em Y = -0.5, altura mínima de câmera é 1.6 (altura de uma pessoa)
    MIN_HEIGHT = 1.55
    
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.pos   = glm.vec3(-3.0, 0.8, -20.0)
        self.front = glm.vec3(1.0, 0.0, 0.0)
        self.up    = glm.vec3(0.0, 1.0, 0.0)

        self.yaw   = -90.0
        self.pitch = 0.0
        self.lastX = largura / 2.0
        self.lastY = altura / 2.0
        self.fov   = 45.0

        self.firstMouse = True
        self.deltaTime  = 0.0
        self.lastFrame  = 0.0

    def camera_height(self):
        #Limita a câmera ao chão, impedindo que desça abaixo da altura mínima
        if self.pos.y < self.MIN_HEIGHT:
            self.pos.y = self.MIN_HEIGHT

    def key_event(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        cameraSpeed = 20 * self.deltaTime

        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.pos += cameraSpeed * self.front
            self.camera_height()

        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.pos -= cameraSpeed * self.front
            self.camera_height()

        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            self.pos -= glm.normalize(glm.cross(self.front, self.up)) * cameraSpeed
            self.camera_height()

        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            self.pos += glm.normalize(glm.cross(self.front, self.up)) * cameraSpeed
            self.camera_height()

    def mouse_callback(self, window, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = (xpos - self.lastX) * 0.05
        yoffset = (self.lastY - ypos) * 0.05
        self.lastX = xpos
        self.lastY = ypos

        self.yaw   += xoffset
        self.pitch += yoffset
        self.pitch  = max(-89.0, min(89.0, self.pitch))

        front = glm.vec3(
            glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        )
        self.front = glm.normalize(front)

    def scroll_callback(self, window, xoffset, yoffset):
        self.fov = max(1.0, min(45.0, self.fov - yoffset))

    def framebuffer_size_callback(self, window, largura, altura):
        self.largura = largura
        self.altura  = altura
        glViewport(0, 0, largura, altura)

    def tick(self, current_time):
        self.deltaTime = current_time - self.lastFrame
        self.lastFrame = current_time

    def get_view(self):
        return np.array(glm.lookAt(self.pos, self.pos + self.front, self.up))

    def get_projection(self):
        return np.array(glm.perspective(glm.radians(self.fov), self.largura / self.altura, 0.1, 200.0))