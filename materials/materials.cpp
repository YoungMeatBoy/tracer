#include "materials.hpp"

Material::Material(const float refractive_index,
				   const Vec4f &albedo, 
				   const Vec3f &diffuse_color, 
				   const float specular_exponent)
{
	this->refractive_index  = refractive_index;
	this->albedo            = albedo;
	this->diffuse_color     = diffuse_color;
	this->specular_exponent = specular_exponent;
}

Material::Material()
{
	this->refractive_index  = 1;
	this->albedo            = {1, 0, 0, 0};
	this->diffuse_color     = {};
	this->specular_exponent = {};
}
