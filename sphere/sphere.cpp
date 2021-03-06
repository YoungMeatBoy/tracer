#include "sphere.hpp"

Sphere::Sphere(const Vec3f    &center, 
			   const float     radius, 
			   const Material &material)
{
	this->center = center;
	this->radius = radius;
	this->material = material;
}

/*
Algotythm from
http://www.lighthouse3d.com/tutorials/maths/ray-sphere-intersection/
*/
bool Sphere::ray_intersect(const Vec3f &orig, 
						   const Vec3f &dir, 
						   float &t0) 
						   const
{
	Vec3f L = center - orig;
	float tca = L * dir;
	float d2  = L * L - tca * tca;
	if (d2 > radius * radius)
		return false;

	float thc = sqrtf(radius * radius - d2);
	t0 = tca - thc;
	float t1 = tca + thc;
	if (t0 < 0)
		t0 = t1;
	if (t0 < 0)
		return false;
	return true;
}
