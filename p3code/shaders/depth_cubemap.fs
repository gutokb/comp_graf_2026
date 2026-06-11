#version 330 core
in vec4 frag_pos;
uniform vec3  light_pos;
uniform float far_plane;

void main(){
    float dist = length(frag_pos.xyz - light_pos);
    gl_FragDepth = dist / far_plane;  // normalize to [0,1]
}