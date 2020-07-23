#include "files.hpp"
#include <fstream>
#include "json.hpp"
#include "../materials/materials.hpp"

void save_to(
	const std::string &filename,
	const size_t height,
	const size_t width,
	std::vector<Vec3f> framebuffer)
{
	std::cout << "Saving to: " << filename << std::endl;

	std::ofstream ofs;
	ofs.open(filename.c_str(), std::ios::binary);

	// Format of this file requires
	//  format
	//  width
	//  height
	ofs << "P6\n"
		<< width << " " << height << "\n255\n";

	for (size_t i = 0; i < height * width; ++i)
	{
		Vec3f &c = framebuffer[i];
		float max = std::max(c[0], std::max(c[1], c[2]));
		if (max > 1)
			c = c * (1. / max);
		for (size_t j = 0; j < 3; j++)
		{
			ofs << (char)(255 * std::max(0.f, std::min(1.f, framebuffer[i][j])));
		}
	}
	std::cout << "Saving was successful!" << std::endl;
	ofs.close();
}

std::pair<std::vector<Sphere>, std::vector<Light>> load_from_file(const std::string &filename)
{
	Material ivory(1.0, Vec4f(0.6, 0.3, 0.1, 0.0), Vec3f(0.01, 0.01, 0.01), 50.);
	Material glass(1.5, Vec4f(0.0, 0.5, 0.1, 0.8), Vec3f(0.6, 0.7, 0.8), 125.);
	Material red_rubber(1.0, Vec4f(0.9, 0.1, 0.0, 0.0), Vec3f(0.3, 0.1, 0.1), 10.);
	Material mirror(1.0, Vec4f(0.0, 10.0, 0.8, 0.0), Vec3f(1.0, 1.0, 1.0), 1425.);
	std::vector<Sphere> spheres;
	std::vector<Light> lights;
	using json = nlohmann::json;
	std::ifstream i(filename.c_str());
	json data;
	i >> data;
	json ligths_json = data["lights"];
	json spheres_json = data["spheres"];
	std::map<std::string, Material> materials = {{"ivory"     , ivory}, 
												 {"glass"     , glass}, 
												 {"red_rubber", red_rubber}, 
												 {"mirrow"    , mirror}};
	for (auto light: ligths_json)
	{
		float x         = light["x"];
		float y         = light["y"];
		float z         = light["z"];
		float intensity = light["intensity"];

		lights.push_back(Light(Vec3f(x, y, z), intensity));
	}
	for(auto sphere: spheres_json)
	{
		float x      = sphere["x"];
		float y      = sphere["y"];
		float z      = sphere["z"];
		int   radius = sphere["radius"];
		std::string material = sphere["material"];
		spheres.push_back(Sphere(Vec3f(x, y, z), radius, materials[material]));
	}
	return std::make_pair(spheres, lights);
}