all:  
	g++ -Wall -pedantic -std=c++11 -O3 trace.cpp ./files/files.cpp ./light/light.cpp ./materials/materials.cpp ./sphere/sphere.cpp
	./a
	python ./conversion/convert.py