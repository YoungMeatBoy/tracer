#ifndef __LIGHT_HPP__
#define __LIGHT_HPP__

#include "../geometry.h"

struct Light
{
	Vec3f position;
	float intensity;
	Light(const Vec3f &position, 
		  const float intensity);
};

#endif