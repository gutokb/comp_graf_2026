#version 330 core
#extension GL_ARB_shading_language_420pack : require

#define MAX_POINT_LIGHTS 16
#define MAX_SPOT_LIGHTS  8

struct PointLight {
    vec3  pos;
    vec3  color;
    float constant;
    float linear;
    float quadratic;
};

struct SpotLight {
    vec3  pos;
    vec3  direction;
    vec3  color;
    float cut_off;
    float outer_cut_off;
    float constant;
    float linear;
    float quadratic;
};

uniform float      ambient_strength;
uniform vec3       ambient_color;
uniform float      shininess;
uniform float      kd;
uniform float      ks;
uniform vec3       view_pos;
uniform int        num_point_lights;
uniform int        num_spot_lights;
uniform PointLight point_lights[MAX_POINT_LIGHTS];
uniform SpotLight  spot_lights[MAX_SPOT_LIGHTS];
uniform float      far_plane;
uniform mat4       spot_light_space_matrices[MAX_SPOT_LIGHTS];

layout(binding = 0) uniform sampler2D   imagem;
layout(binding = 1) uniform samplerCube shadow_cubemaps[MAX_POINT_LIGHTS];
layout(binding = 5) uniform sampler2D   spot_shadow_maps[MAX_SPOT_LIGHTS];

varying vec2 out_texture;
varying vec3 out_normal;
varying vec3 out_frag_pos;

float attenuation(float dist, float constant, float linear, float quadratic) {
    return 1.0 / (constant + linear * dist + quadratic * (dist * dist));
}

float sample_point_shadow(int i, vec3 frag_to_light) {
    if (i == 0) return texture(shadow_cubemaps[0], frag_to_light).r;
    if (i == 1) return texture(shadow_cubemaps[1], frag_to_light).r;
    if (i == 2) return texture(shadow_cubemaps[2], frag_to_light).r;
    return 1.0;
}

float sample_spot_shadow(int i, vec2 coords) {
    if (i == 0) return texture(spot_shadow_maps[0], coords).r;
    if (i == 1) return texture(spot_shadow_maps[1], coords).r;
    if (i == 2) return texture(spot_shadow_maps[2], coords).r;
    return 1.0;
}

float calc_point_shadow(int i, vec3 frag_pos, vec3 light_pos){
    vec3  frag_to_light = frag_pos - light_pos;
    float closest_depth = sample_point_shadow(i, frag_to_light) * far_plane;
    float current_depth = length(frag_to_light);
    float bias          = 0.05;
    return current_depth - bias > closest_depth ? 1.0 : 0.0;
}

float calc_spot_shadow(int i, vec3 frag_pos){
    vec4  frag_in_light = spot_light_space_matrices[i] * vec4(frag_pos, 1.0);
    vec3  proj_coords   = frag_in_light.xyz / frag_in_light.w;
    proj_coords         = proj_coords * 0.5 + 0.5;
    if(proj_coords.z > 1.0) return 0.0;
    float closest_depth = sample_spot_shadow(i, proj_coords.xy);
    float current_depth = proj_coords.z;
    float bias          = 0.001;
    return current_depth - bias > closest_depth ? 1.0 : 0.0;
}

vec3 calc_point_light(int i, PointLight light, vec3 norm, vec3 view_dir){
    vec3  light_dir   = normalize(light.pos - out_frag_pos);
    float diff        = max(dot(norm, light_dir), 0.0);
    vec3  reflect_dir = reflect(-light_dir, norm);
    float spec        = pow(max(dot(view_dir, reflect_dir), 0.0), shininess);
    float att         = attenuation(length(light.pos - out_frag_pos),
                                    light.constant, light.linear, light.quadratic);
    float shadow      = calc_point_shadow(i, out_frag_pos, light.pos);
    return light.color * (kd * diff + ks * spec) * att * (1.0 - shadow);
}

vec3 calc_spot_light(int i, SpotLight light, vec3 norm, vec3 view_dir){
    vec3  light_dir   = normalize(light.pos - out_frag_pos);
    float theta       = dot(light_dir, normalize(-light.direction));
    float epsilon     = light.cut_off - light.outer_cut_off;
    float intensity   = clamp((theta - light.outer_cut_off) / epsilon, 0.0, 1.0);
    float diff        = max(dot(norm, light_dir), 0.0);
    vec3  reflect_dir = reflect(-light_dir, norm);
    float spec        = pow(max(dot(view_dir, reflect_dir), 0.0), shininess);
    float att         = attenuation(length(light.pos - out_frag_pos),
                                    light.constant, light.linear, light.quadratic);
    float shadow      = calc_spot_shadow(i, out_frag_pos);
    return light.color * (kd * diff + ks * spec) * att * intensity * (1.0 - shadow);
}

void main(){
    vec3 norm     = normalize(out_normal);
    vec3 view_dir = normalize(view_pos - out_frag_pos);

    vec3 result = ambient_color * ambient_strength;

    for (int i = 0; i < num_point_lights; i++)
        result += calc_point_light(i, point_lights[i], norm, view_dir);

    for (int i = 0; i < num_spot_lights; i++)
        result += calc_spot_light(i, spot_lights[i], norm, view_dir);

    vec4 tex = texture2D(imagem, out_texture);
    gl_FragColor = tex * vec4(result, 1.0);
}