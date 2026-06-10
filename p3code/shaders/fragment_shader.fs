#version 330 core

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
uniform vec3       view_pos;
uniform int        num_point_lights;
uniform int        num_spot_lights;
uniform PointLight point_lights[MAX_POINT_LIGHTS];
uniform SpotLight  spot_lights[MAX_SPOT_LIGHTS];

varying vec2 out_texture;
varying vec3 out_normal;
varying vec3 out_frag_pos;

uniform sampler2D imagem;

float attenuation(float dist, float constant, float linear, float quadratic) {
    return 1.0 / (constant + linear * dist + quadratic * (dist * dist));
}

vec3 calc_point_light(PointLight light, vec3 norm, vec3 view_dir) {
    vec3  light_dir  = normalize(light.pos - out_frag_pos);
    float diff       = max(dot(norm, light_dir), 0.0);
    vec3  reflect_dir = reflect(-light_dir, norm);
    float spec       = pow(max(dot(view_dir, reflect_dir), 0.0), shininess);
    float att        = attenuation(length(light.pos - out_frag_pos),
                                   light.constant, light.linear, light.quadratic);
    return light.color * (diff + spec) * att;
}

vec3 calc_spot_light(SpotLight light, vec3 norm, vec3 view_dir) {
    vec3  light_dir   = normalize(light.pos - out_frag_pos);
    float theta       = dot(light_dir, normalize(-light.direction));
    float epsilon     = light.cut_off - light.outer_cut_off;
    float intensity   = clamp((theta - light.outer_cut_off) / epsilon, 0.0, 1.0);

    float diff        = max(dot(norm, light_dir), 0.0);
    vec3  reflect_dir = reflect(-light_dir, norm);
    float spec        = pow(max(dot(view_dir, reflect_dir), 0.0), shininess);
    float att         = attenuation(length(light.pos - out_frag_pos),
                                    light.constant, light.linear, light.quadratic);
    return light.color * (diff + spec) * att * intensity;
}

void main(){
    vec3 norm     = normalize(out_normal);
    vec3 view_dir = normalize(view_pos - out_frag_pos);

    vec3 result = ambient_color * ambient_strength;

    for (int i = 0; i < num_point_lights; i++)
        result += calc_point_light(point_lights[i], norm, view_dir);

    for (int i = 0; i < num_spot_lights; i++)
        result += calc_spot_light(spot_lights[i], norm, view_dir);

    vec4 tex = texture2D(imagem, out_texture);
    gl_FragColor = tex * vec4(result, 1.0);
}