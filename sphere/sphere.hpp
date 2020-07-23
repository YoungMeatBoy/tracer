#ifndef __SPHERES_HPP__
#define __SPHERES_HPP__

#include "../geometry.h"
#include "../materials/materials.hpp"

struct Sphere
{
	float radius;
	Vec3f center;
	Material material;

	Sphere(const Vec3f    &center, 
		   const float     radius, 
		   const Material &material);

	bool ray_intersect(const Vec3f &orig, 
					   const Vec3f &dir, 
					   float &t0)
					   const;
};

#endif