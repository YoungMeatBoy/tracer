#ifndef __MATERIALS_HPP__
#define __MATERIALS_HPP__

#include "../geometry.h"

struct Material
{
	Vec4f albedo;
	Vec3f diffuse_color;
	float refractive_index;
	float specular_exponent;
	Material();
	Material(const float refractive_index,
			 const Vec4f &albedo, 
			 const Vec3f &diffuse_color,
			 const float specular_exponent);
};


#endif // __MATERIALS_HPP__