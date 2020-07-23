#include "light.hpp"

Light::Light(const Vec3f &position, const float intensity)
{
	this->position  = position;
	this->intensity = intensity;
}
