import json
import pathlib
import subprocess
from tkinter import (ACTIVE, BOTH, CENTER, FLAT, GROOVE, LEFT, RAISED, RIDGE,
					 RIGHT, SUNKEN, Button, Entry, Frame, IntVar, Label,
					 Listbox, OptionMenu, Radiobutton, StringVar, Tk,
					 messagebox)
from typing import *
from accessify import private
from PIL import Image


class Light():
	def __init__(self, x, y, z, intensity):
		self.x = x
		self.y = y
		self.z = z
		self.intensity = intensity

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z}), intensity = {self.intensity}"

	def as_dict(self):
		return {'x': self.x, 'y': self.y, 'z': self.z, 'intensity': self.intensity}


class Sphere():
	def __init__(self, x, y, z, radius, material):
		self.x = x
		self.y = y
		self.z = z
		self.radius = radius
		self.material = material

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z}), r = {self.radius} material = {self.material}"

	def as_dict(self):
		return {'x': self.x, 'y': self.y, 'z': self.z, 'radius': self.radius, 'material': self.material}


class CreateSphereInterface(Frame):
	def __init__(self, parent, size, spheres, spheres_text_area) -> None:
		Frame.__init__(self, parent, background='white')
		self.parent = parent
		self.spheres = spheres
		self.spheres_text_area = spheres_text_area
		self.parent.resizable(width=False, height=False)
		self.screen_width = self.parent.winfo_screenwidth()
		self.screen_height = self.parent.winfo_screenheight()
		geometry = self.__generate_geometry__(size)
		self.parent.geometry(geometry)
		self.pack_interface_items()

	def pack_interface_items(self) -> None:
		self.parent.title('Add sphere')
		self.pack(fill=BOTH, expand=1)
		self.pack_x_entry()
		self.pack_y_entry()
		self.pack_z_entry()
		self.pack_radius_entry()
		self.pack_material_listbox()
		self.pack_add_sphere_button()

	def pack_x_entry(self) -> None:
		x_lable, y_lable = 10, 0
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 5
		width_entry = 10

		lable = Label(self.parent, text='Enter x coordinate',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.x_entry = Entry(self.parent, width=width_entry)
		self.x_entry.place(x=x_entry, y=y_entry)

	def pack_y_entry(self) -> None:
		x_lable, y_lable = 10, 50
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 55
		width_entry = 10

		lable = Label(self.parent, text='Enter y coordinate',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.y_entry = Entry(self.parent, width=width_entry)
		self.y_entry.place(x=x_entry, y=y_entry)

	def pack_z_entry(self) -> None:
		x_lable, y_lable = 10, 100
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 105
		width_entry = 10

		lable = Label(self.parent, text='Enter z coordinate',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.z_entry = Entry(self.parent, width=width_entry)
		self.z_entry.place(x=x_entry, y=y_entry)

	def pack_radius_entry(self) -> None:
		x_lable, y_lable = 10, 150
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 155
		width_entry = 10

		lable = Label(self.parent, text='Enter sphere radius',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.radius_entry = Entry(self.parent, width=width_entry)
		self.radius_entry.place(x=x_entry, y=y_entry)

	def pack_material_listbox(self) -> None:
		choose_material_lable = Label(
			self.parent, text='Choose a material:', width=32, height=1, font="Courier 14")
		choose_material_lable.place(x=10, y=200)
		self.materials = ('red_rubber', 'glass', 'mirrow')
		self.material_index = IntVar()
		self.radiobuttons = list()
		y = 190
		for index, material in enumerate(self.materials):
			y += 50
			temp_button = Radiobutton(self.parent, text=material, value=index, variable=self.material_index,
									  padx=15, pady=10, width=27, justify=CENTER, font="Courier 14", state=ACTIVE)
			temp_button.place(x=10, y=y)
			self.radiobuttons.append(temp_button)

	def pack_add_sphere_button(self) -> None:
		button = Button(self.parent, text='add sphere', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.add_sphere_callback)
		button.place(x=100, y=400)

	def add_sphere_callback(self) -> None:
		succes = self.check_all_fields()
		if succes:
			data = self.get_data_from_fields()
			x, y, z, radius, material = data
			x = float(x)
			y = float(y)
			z = float(z)
			radius = float(radius)
			self.spheres.append(Sphere(x, y, z, radius, material))
			self.update_spheres_lable()
			self.parent.destroy()
		else:
			self.show_error_message("Check fields and material choosing!")

	def update_spheres_lable(self) -> None:
		self.spheres_text_area['text'] = ''
		for ind, sp in enumerate(self.spheres):
			self.spheres_text_area['text'] += f'Sphere {ind + 1} = ' + str(
				sp) + '\n'

	def show_error_message(self, error_message) -> None:
		_ = Tk()
		_.withdraw()
		messagebox.showerror("Error", error_message)

	def get_data_from_fields(self) -> Tuple[str, str, str, str, str]:
		x = self.x_entry.get()
		y = self.y_entry.get()
		z = self.z_entry.get()
		radius = self.radius_entry.get()
		material = self.materials[self.material_index.get()]
		return x, y, z, radius, material

	def check_all_fields(self):
		x, y, z, radius, material = self.get_data_from_fields()
		res = self.is_float(x)
		res = res and self.is_float(y)
		res = res and self.is_float(z)
		res = res and self.is_float(radius)
		return res

	@staticmethod
	def is_float(x) -> bool:
		try:
			float(x)
			return True
		except:
			return False

	@private
	def __generate_geometry__(self, size: Tuple[int, int]) -> str:
		width, height = size
		x = int((self.screen_width - width) / 2)
		y = int((self.screen_height - height) / 2)
		return f'{width}x{height}+{x}+{y}'

	def run(self):
		self.parent.mainloop()


class CreateLightInterface(Frame):
	def __init__(self, parent, size, lights, lights_text_area) -> None:
		Frame.__init__(self, parent, background='white')
		self.parent = parent
		self.lights = lights
		self.lights_text_area = lights_text_area
		self.parent.resizable(width=False, height=False)
		self.screen_width = self.parent.winfo_screenwidth()
		self.screen_height = self.parent.winfo_screenheight()
		geometry = self.__generate_geometry__(size)
		self.parent.geometry(geometry)
		self.pack_interface_items()

	def pack_interface_items(self) -> None:
		self.parent.title('Add sphere')
		self.pack(fill=BOTH, expand=1)
		self.pack_x_entry()
		self.pack_y_entry()
		self.pack_z_entry()
		self.pack_intensity_entry()
		self.pack_add_light_button()

	def pack_x_entry(self) -> None:
		x_lable, y_lable = 10, 0
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 5
		width_entry = 10

		lable = Label(self.parent, text='Enter x coordinate',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.x_entry = Entry(self.parent, width=width_entry)
		self.x_entry.place(x=x_entry, y=y_entry)

	def pack_y_entry(self) -> None:
		x_lable, y_lable = 10, 50
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 55
		width_entry = 10

		lable = Label(self.parent, text='Enter y coordinate',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.y_entry = Entry(self.parent, width=width_entry)
		self.y_entry.place(x=x_entry, y=y_entry)

	def pack_z_entry(self) -> None:
		x_lable, y_lable = 10, 100
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 105
		width_entry = 10

		lable = Label(self.parent, text='Enter z coordinate',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.z_entry = Entry(self.parent, width=width_entry)
		self.z_entry.place(x=x_entry, y=y_entry)

	def pack_intensity_entry(self) -> None:
		x_lable, y_lable = 10, 150
		width_lable, height_lable = 23, 1
		x_entry, y_entry = 290, 155
		width_entry = 10

		lable = Label(self.parent, text='Enter light intensity',
					  width=width_lable, height=height_lable, font="Courier 14")
		lable.place(x=x_lable, y=y_lable)

		self.intensity_entry = Entry(self.parent, width=width_entry)
		self.intensity_entry.place(x=x_entry, y=y_entry)

	def pack_add_light_button(self) -> None:
		button = Button(self.parent, text='add light', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.add_light_callback)
		button.place(x=100, y=400)

	def add_light_callback(self) -> None:
		succes = self.check_all_fields()
		if succes:
			data = self.get_data_from_fields()
			x, y, z, intensity = data
			x = float(x)
			y = float(y)
			z = float(z)
			intensity = float(intensity)
			self.lights.append(Light(x, y, z, intensity))
			self.update_lights_lable()
			self.parent.destroy()
		else:
			self.show_error_message("Check fields!")

	def update_lights_lable(self) -> None:
		self.lights_text_area['text'] = ''
		for ind, lig in enumerate(self.lights):
			self.lights_text_area['text'] += f'Light {ind + 1} = ' + str(
				lig) + '\n'

	def show_error_message(self, error_message) -> None:
		_ = Tk()
		_.withdraw()
		messagebox.showerror("Error", error_message)

	def get_data_from_fields(self) -> Tuple[str, str, str, str, str]:
		x = self.x_entry.get()
		y = self.y_entry.get()
		z = self.z_entry.get()
		intensity = self.intensity_entry.get()
		return x, y, z, intensity

	def check_all_fields(self):
		x, y, z, intensity = self.get_data_from_fields()
		res = self.is_float(x)
		res = res and self.is_float(y)
		res = res and self.is_float(z)
		res = res and self.is_float(intensity)
		return res

	@staticmethod
	def is_float(x) -> bool:
		try:
			float(x)
			return True
		except:
			return False

	@private
	def __generate_geometry__(self, size: Tuple[int, int]) -> str:
		width, height = size
		x = int((self.screen_width - width) / 2)
		y = int((self.screen_height - height) / 2)
		return f'{width}x{height}+{x}+{y}'

	def run(self):
		self.parent.mainloop()


class DestroyItem(Frame):
	def __init__(self, parent, size, items, text_area, name) -> None:
		Frame.__init__(self, parent, background='white')
		self.name = name
		self.parent = parent
		self.items = items
		self.text_area = text_area
		self.screen_width = self.parent.winfo_screenwidth()
		self.screen_height = self.parent.winfo_screenheight()
		self.parent.resizable(width=False, height=False)
		geometry = self.__generate_geometry__(size)
		self.parent.geometry(geometry)
		self.pack_interface_items()

	def pack_interface_items(self) -> None:
		self.parent.title('Destroy' + self.name)
		self.pack(fill=BOTH, expand=1)
		self.pack_remove_button()
		self.pack_info_lable()
		self.pack_index_entry()

	def pack_remove_button(self) -> None:
		x, y = 100, 400
		button = Button(self.parent, text='remove', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.remove)
		button.place(x=x, y=y)

	def pack_index_entry(self) -> None:
		x, y = 150, 200
		self.index_entry = Entry(self.parent, width=10)
		self.index_entry.place(x=x, y=y)

	def pack_info_lable(self) -> None:
		x, y = 50, 100
		lable = Label(
			self.parent, text=f"Enter number of the {self.name.lower()} \nto be removed", font="Courier 12", width=28, height=4)
		lable.place(x=x, y=y)

	def remove(self) -> None:
		data = self.index_entry.get()
		try:
			ind = int(data)
		except:
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "Please input correct number!")
		else:
			ind = ind - 1
			if ind < 0 or ind >= len(self.items):
				_ = Tk()
				_.withdraw()
				messagebox.showerror("Error", "Please input correct number!")
			else:
				self.items.remove(self.items[ind])
				self.update_lable()
				self.parent.destroy()

	def update_lable(self):
		self.text_area['text'] = ''
		for ind, item in enumerate(self.items):
			self.text_area['text'] += f'{self.name} {ind + 1} = ' + str(
				item) + '\n'

	@private
	def __generate_geometry__(self, size: Tuple[int, int]) -> str:
		width, height = size
		x = int((self.screen_width - width) / 2)
		y = int((self.screen_height - height) / 2)
		return f'{width}x{height}+{x}+{y}'

	def run(self) -> None:
		self.parent.mainloop()


class SpheresVisualizatorInterface(Frame):
	def __init__(self, parent, size, is_resizable=False):
		Frame.__init__(self, parent, background='white')
		self.parent = parent
		self.parent.resizable(width=is_resizable, height=is_resizable)
		self.screen_width = self.parent.winfo_screenwidth()
		self.screen_height = self.parent.winfo_screenheight()
		geometry = self.__generate_geometry__(size)
		self.parent.geometry(geometry)
		self.pack_interface_items()
		self.spheres = list()
		self.lights = list()
		self.visualizator = Visualizator()

	@private
	def pack_interface_items(self) -> None:
		self.parent.title('SpheresVisulator')
		self.pack(fill=BOTH, expand=1)
		self.pack_spheres_table()
		self.pack_lights_table()
		self.pack_create_sphere_button()
		self.pack_create_light_button()
		self.pack_remove_sphere_button()
		self.pack_remove_light_button()
		self.pack_render_button()
		self.pack_background_settings_button()
		self.pack_info_lable()

	def update_spheres_lable(self) -> None:
		self.spheres_text_area['text'] = ''
		for ind, sp in enumerate(self.spheres):
			self.spheres_text_area['text'] += f'Sphere {ind + 1} = ' + str(
				sp) + '\n'

	@private
	def __generate_geometry__(self, size: Tuple[int, int]) -> str:
		width, height = size
		x = int((self.screen_width - width) / 2)
		y = int((self.screen_height - height) / 2)
		return f'{width}x{height}+{x}+{y}'

	def update_lights_lable(self) -> None:
		self.lights_text_area['text'] = ''
		for ind, lig in enumerate(self.lights):
			self.lights_text_area['text'] += f'Light {ind + 1} = ' + str(
				lig) + '\n'

	@private
	def pack_spheres_table(self) -> None:
		x, y = (30, 30)
		text_size_width = 70
		text_size_height = 14
		self.spheres_text = Label(
			self.parent, height=text_size_height, width=text_size_width, font="Courier 10", justify=RIGHT)
		self.spheres_text.place(x=x, y=y)

	def pack_lights_table(self) -> None:
		x, y = (30, 300)
		text_size_width = 70
		text_size_height = 14
		self.lights_text = Label(
			self.parent, height=text_size_height, width=text_size_width, font="Courier 10", justify=RIGHT)
		self.lights_text.place(x=x, y=y)

	def pack_create_sphere_button(self) -> None:
		x, y = 650, 30
		button = Button(self.parent, text='add sphere', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.create_sphere_callback)
		button.place(x=x, y=y)

	def pack_create_light_button(self) -> None:
		x, y = 650, 300
		button = Button(self.parent, text='add light', width=17, height=3, bg='#F1E6C1 ',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.create_light_callback)
		button.place(x=x, y=y)

	def pack_remove_sphere_button(self) -> None:
		x, y = 650, 178
		button = Button(self.parent, text='remove sphere', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.remove_sphere_callback)
		button.place(x=x, y=y)

	def pack_remove_light_button(self) -> None:
		x, y = 650, 450
		button = Button(self.parent, text='remove light', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.remove_light_callback)
		button.place(x=x, y=y)

	def pack_render_button(self) -> None:
		x, y = 30, 570
		button = Button(self.parent, text='render image', width=17, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.render_callback)
		button.place(x=x, y=y)

	def pack_background_settings_button(self) -> None:
		x, y = 310, 570
		button = Button(self.parent, text='background settings', width=25, height=3, bg='#F1E6C1',
						fg='#3F6A8A', font="Courier 14", relief=FLAT, command=self.background_settings_callback)
		button.place(x=x, y=y)

	def pack_info_lable(self) -> None:
		x, y = 650, 570
		width, height = 17, 4
		info_lable = Label(self.parent, text='Miasnenko Dmitry\n2020\nBMSTU',
						   width=width, height=height, font="Courier 14", relief=FLAT)
		info_lable.place(x=x, y=y)

	def create_sphere_callback(self) -> None:
		if len(self.spheres) < 8:
			root_create_sphere = Tk()
			create_sphere_app = CreateSphereInterface(
				root_create_sphere, (380, 500), self.spheres, self.spheres_text)
			create_sphere_app.run()
		else:
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "To many spheres to be rendered!")

	def create_light_callback(self) -> None:
		if len(self.lights) < 8:
			root_create_light = Tk()
			create_light_app = CreateLightInterface(
				root_create_light, (380, 500), self.lights, self.lights_text)
			create_light_app.run()
		else:
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "To many lights to be rendered!")

	def remove_light_callback(self) -> None:
		if not len(self.lights):
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "No lights to be removed!")
		else:
			root_destroy_light = Tk()
			destroy_light_app = DestroyItem(
				root_destroy_light, (380, 500), self.lights, self.lights_text, 'Light')
			destroy_light_app.run()
			self.update_lights_lable()

	def remove_sphere_callback(self) -> None:
		if not len(self.spheres):
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "No spheres to be removed!")
		else:
			root_destroy_sphere = Tk()
			destroy_sphere_app = DestroyItem(
				root_destroy_sphere, (380, 500), self.spheres, self.spheres_text, 'Sphere')
			destroy_sphere_app.run()
			self.update_spheres_lable()

	def render_callback(self) -> None:
		if not len(self.lights):
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "No lights to be rendered!")
		elif not len(self.spheres):
			_ = Tk()
			_.withdraw()
			messagebox.showerror("Error", "To spheres to be rendered!")
		else:
			data = self.create_data()
			image_path = self.visualizator.render(data)
			self.visualizator.show(image_path)

	def create_data(self) -> dict:
		res = {'lights': list(), 'spheres': list()}
		for light in self.lights:
			res['lights'].append(light.as_dict())

		for sphere in self.spheres:
			res['spheres'].append(sphere.as_dict())
		return res

	def background_settings_callback(self) -> None:
		print(6)

	def run(self):
		self.parent.mainloop()


class Visualizator():
	def __init__(self):
		pass

	def render(self, data):
		data_file = pathlib.Path('./data.json')
		json.dump(data, open(data_file, 'w'))
		print(subprocess.call(['./a']))
		print(subprocess.call(['python', './conversion/convert.py']))
		return pathlib.Path('./result/out.jpg')

	def show(self, image):
		im = Image.open(image)
		im.show()


def main():
	root = Tk()
	app = SpheresVisualizatorInterface(root, (900, 685))
	app.run()


if __name__ == '__main__':
	main()
