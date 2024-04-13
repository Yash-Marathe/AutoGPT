// Shader code for a sparkling water effect

// Constants
const float PI = 3.1415927410125732421875;
const float TWO_PI = 2.0 * PI;
const float HALF_PI = 0.5 * PI;
const float DEG_TO_RAD = PI / 180.0;
const float THRESHOLD_LOW = 0.05;
const float THRESHOLD_HIGH = 0.15;
const float THRESHOLD_MID = 0.20;
const float THRESHOLD_MID_HIGH = 0.30;
const float SPARKLE_SCALE = 0.55;
const float SPARKLE_INTENSITY = 0.3499999940395355224609375;
const float SPARKLE_PERIOD = 1.0499999523162841796875;
const float SPARKLE_FREQUENCY = 3.1415927410125732421875;
const float SOFT_RING_THICKNESS = 0.05;
const float SOFT_RING_BLUR = 0.10;
const float SOFT_CIRCLE_BLUR = 0.17;
const float TRIANGLE_NOISE_SCALE_X = 5.398700237274169921875;
const float TRIANGLE_NOISE_SCALE_Y = 5.442100048065185546875;
const float TRIANGLE_NOISE_OFFSET = 21.5351009368896484375;
const float TRIANGLE_NOISE_MULTIPLIER = 95.43070220947265625;
const float TRIANGLE_NOISE_ADDEND = 75.0496063232421875;
const float TRIANGLE_NOISE_THRESHOLD_LOW = 0.0;
const float TRIANGLE_NOISE_THRESHOLD_HIGH = 0.05;
const float TRIANGLE_NOISE_THRESHOLD_MID = 0.10;
const float TRIANGLE_NOISE_THRESHOLD_MID_HIGH = 0.20;
const float TRIANGLE_NOISE_THRESHOLD_HIGH_HIGH = 0.30;

// Flutter fragment shader
float4 flutter_FragCoord;

// Uniforms
uniform float4 u_color;
uniform float u_alpha;
uniform float4 u_sparkle_color;
uniform float u_sparkle_alpha;
uniform float u_blur;
uniform float2 u_center;
uniform float u_radius_scale;
uniform float u_max_radius;
uniform float2 u_resolution_scale;
uniform float2 u_noise_scale;
uniform float u_noise_phase;
uniform float2 u_circle1;
uniform float2 u_circle2;
uniform float2 u_circle3;
uniform float2 u_rotation1;
uniform float2 u_rotation2;
uniform float2 u_rotation3;

// Functions
float distance(float2 p1, float2 p2) {
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
}

float min(float a, float b) {
    return a < b ? a : b;
}

float max(float a, float b) {
    return a > b ? a : b;
}

// Main function
void FLT_main() {
    float2 p = flutter_FragCoord.xy;
    float2 uv_1 = p * u_resolution_scale;
    float2 density_uv = uv_1 - mod(p, u_noise_scale);
    float radius = u_max_radius * u_radius_scale;
    float2 param_13 = uv_1;
    float turbulence = turbulence_function(param_13);
    float2 param_14 = p;
    float2 param_15 = u_center;
    float param_16 = radius;
    float param_17 = SOFT_RING_THICKNESS * u_max_radius;
    float param_18 = u_blur;
    float ring = soft_ring_function(param_14, param_15, param_16, param_17, param_18);
    float2 param_19 = density_uv;
    float param_20 = u_noise_phase;
    float sparkle = sparkle_function(param_19, param_20) * ring * turbulence * u_sparkle_alpha;
    float2 param_21 = p;
    float2 param_22 = u_center;
    float param_23 = radius;
    float param_24 = u_blur;
    float wave_alpha = soft_circle_function(param_21, param_22, param_23, param_24) * u_alpha * u_color.w;
    float4 wave_color = float4(u_color.xyz * wave_alpha, wave_
