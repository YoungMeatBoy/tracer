#ifndef __FILE_HPP__
#define __FILE_HPP__

#include <fstream>
#include <limits>
#include "../geometry.h"
#include "../sphere/sphere.hpp"
#include "../light/light.hpp"

void save_to(
			 const std::string &filename,
			 const size_t height,
			 const size_t width,
			 std::vector<Vec3f> framebuffer);

std::pair<std::vector<Sphere>, std::vector<Light>> load_from_file(const std::string &filename);

#endif