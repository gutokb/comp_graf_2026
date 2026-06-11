#version 330 core
layout(location = 0) in vec3 position;
uniform mat4 model;
uniform mat4 mat_transformation;

void main(){
    gl_Position = mat_transformation * model * vec4(position, 1.0);
}