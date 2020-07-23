#define _USE_MATH_DEFINES
#include <cmath>
#include <limits>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "geometry.h"
#include "./materials/materials.hpp"
#include "./light/light.hpp"
#include "./sphere/sphere.hpp"
#include "./files/files.hpp"

Vec3f reflect(const Vec3f &I, const Vec3f &N)
{
	return I - N * 2.f * (I * N);
}

Vec3f refract(const Vec3f &I, const Vec3f &N, const float eta_t, const float eta_i = 1.f)
{ // Snell's law
	float cosi = -std::max(-1.f, std::min(1.f, I * N));
	if (cosi < 0)
		return refract(I, -N, eta_i, eta_t); // if the ray comes from the inside the object, swap the air and the media
	float eta = eta_i / eta_t;
	float k = 1 - eta * eta * (1 - cosi * cosi);
	return k < 0 ? Vec3f(1, 0, 0) : I * eta + N * (eta * cosi - sqrtf(k)); // k<0 = total reflection, no ray to refract. I refract it anyways, this has no physical meaning
}

bool scene_intersect(const Vec3f &orig, const Vec3f &dir, const std::vector<Sphere> &spheres, Vec3f &hit, Vec3f &N, Material &material)
{
	float spheres_dist = std::numeric_limits<float>::max();
	for (size_t i = 0; i < spheres.size(); i++)
	{
		float dist_i;
		if (spheres[i].ray_intersect(orig, dir, dist_i) && dist_i < spheres_dist)
		{
			spheres_dist = dist_i;
			hit = orig + dir * dist_i;
			N = (hit - spheres[i].center).normalize();
			material = spheres[i].material;
		}
	}

	float checkerboard_dist = std::numeric_limits<float>::max();
	if (fabs(dir.y) > 1e-3)
	{
		// chenge orig.y + 4 on orig.y + 8
		float d = -(orig.y + 4) / dir.y; // the checkerboard plane has equation y = -4
		Vec3f pt = orig + dir * d;
		if (d > 0 && fabs(pt.x) < 10 && pt.z < -10 && pt.z > -30 && d < spheres_dist)
		{
			checkerboard_dist = d;
			hit = pt;
			N = Vec3f(0, 1, 0);
			Vec3f k = Vec3f(.4, .4, .4);
			material.diffuse_color = k;
			//material.diffuse_color = (int(.5 * hit.x + 1000) + int(.5 * hit.z)) & 1 ? Vec3f(.3, .3, .3) : Vec3f(.3, .2, .1);
		}
	}
	return std::min(spheres_dist, checkerboard_dist) < 1000;
}

Vec3f cast_ray(const Vec3f &orig, const Vec3f &dir, const std::vector<Sphere> &spheres, const std::vector<Light> &lights, size_t depth = 0)
{
	Vec3f point, N;
	Material material;

	if (depth > 6 || !scene_intersect(orig, dir, spheres, point, N, material))
	{
		return Vec3f(0.1, 0.1, 0.2); // background color
	}

	Vec3f reflect_dir = reflect(dir, N).normalize();
	Vec3f refract_dir = refract(dir, N, material.refractive_index).normalize();
	Vec3f reflect_orig = reflect_dir * N < 0 ? point - N * 1e-3 : point + N * 1e-3; // offset the original point to avoid occlusion by the object itself
	Vec3f refract_orig = refract_dir * N < 0 ? point - N * 1e-3 : point + N * 1e-3;
	Vec3f reflect_color = cast_ray(reflect_orig, reflect_dir, spheres, lights, depth + 1);
	Vec3f refract_color = cast_ray(refract_orig, refract_dir, spheres, lights, depth + 1);

	float diffuse_light_intensity = 0, specular_light_intensity = 0;
	for (size_t i = 0; i < lights.size(); i++)
	{
		Vec3f light_dir = (lights[i].position - point).normalize();
		float light_distance = (lights[i].position - point).norm();

		Vec3f shadow_orig = light_dir * N < 0 ? point - N * 1e-3 : point + N * 1e-3; // checking if the point lies in the shadow of the lights[i]
		Vec3f shadow_pt, shadow_N;
		Material tmpmaterial;
		if (scene_intersect(shadow_orig, light_dir, spheres, shadow_pt, shadow_N, tmpmaterial) && (shadow_pt - shadow_orig).norm() < light_distance)
			continue;

		diffuse_light_intensity += lights[i].intensity * std::max(0.f, light_dir * N);
		specular_light_intensity += powf(std::max(0.f, -reflect(-light_dir, N) * dir), material.specular_exponent) * lights[i].intensity;
	}
	return material.diffuse_color * diffuse_light_intensity * material.albedo[0] + Vec3f(1., 1., 1.) * specular_light_intensity * material.albedo[1] + reflect_color * material.albedo[2] + refract_color * material.albedo[3];
}

void render(const std::vector<Sphere> &spheres, const std::vector<Light> &lights)
{
	const int width = 1024;
	const int half_width = width / 2.;
	const int height = 768;
	const int half_height = height / 2.;
	// Угол зрения изи гуглица
	// было /3.
	const float fov = M_PI / 3.;
	std::vector<Vec3f> framebuffer(width * height);

	#pragma omp parallel for
	for (size_t j = 0; j < height; j++)
	{ // actual rendering loop
		for (size_t i = 0; i < width; i++)
		{
			float dir_x = (i + 0.5) - half_width;
			float dir_y = -(j + 0.5) + half_height; // this flips the image at the same time
			float dir_z = -height / (2. * tan(fov / 2.));
			framebuffer[i + j * width] = cast_ray(Vec3f(0, 0, 0), Vec3f(dir_x, dir_y, dir_z).normalize(), spheres, lights);
		}
	}

	save_to(std::string("./result/out.ppm"), height, width, framebuffer);
}



int main()
{
	std::string datafile("data.json");
	std::pair<std::vector<Sphere>, std::vector<Light>> data = load_from_file(datafile);
	std::vector<Sphere> spheres = data.first;
	/*
	spheres.push_back(Sphere(Vec3f(-3, 0, -16), 2, mirror));
	spheres.push_back(Sphere(Vec3f(-1.0, -1.5, -12), 2, ivory));
	spheres.push_back(Sphere(Vec3f(1.5, -0.5, -18), 3, glass));
	spheres.push_back(Sphere(Vec3f(7, 5, -18), 6, red_rubber));
	*/

	std::vector<Light> lights = data.second;
	std::cout << lights.size() << std::endl;
	/*
	lights.push_back(Light(Vec3f(-20, 20, 20), 1.5));
	lights.push_back(Light(Vec3f(30, 50, -25), 1.8));
	lights.push_back(Light(Vec3f(30, 20, 30), 1.7));
	*/
	render(spheres, lights);

	return 0;
}
