#version 330 core
attribute vec3 position;
attribute vec2 texture_coord;
attribute vec3 normal;

varying vec2 out_texture;
varying vec3 out_normal;
varying vec3 out_frag_pos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 mat_transformation;

void main(){
    vec4 world_pos = mat_transformation * model * vec4(position, 1.0);
    gl_Position = projection * view * world_pos;
    out_texture  = vec2(texture_coord);
    out_frag_pos = vec3(world_pos);

    // Normal matrix corrects normals under non-uniform scaling
    out_normal = normalize(mat3(mat_transformation * model) * normal);
}