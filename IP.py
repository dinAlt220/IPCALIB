import sys
sys.path.insert(0,"../build")
import pycatima
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


class IP():
	def __init__(self):
		self.ip_type = None
		self.layer_thick = None
		self.layer_depth = None
		self.layers = pycatima.Layers()
		self.p = None
		self.Atom = 0.0
		self.Z = 0
		self.Q = 0
		self.range = None
		self.A = None
		self.B = None
		self.C = None
		self.L = None
		self.num = None
		self.ang = None
		self.GV_arr = []

	def set_type(self, type):
		if type == "TR":

			if self.layer_thick == None:
				print("Error! Set layer_thick first!")
				quit()

			if self.ang == None:
				print("Error! Set incident angle first!")
				quit()

			self.ip_type = type

			sensitive = pycatima.Material()
			#Ba
			sensitive.add_element(137.32, 56, (1.0 / 3.0))

			#F
			sensitive.add_element(18.99, 9, (1.0 / 3.0))

			#Br
			sensitive.add_element(79.90, 35, (0.85 / 3.0))

			#I
			sensitive.add_element(126.90, 53, (0.15 / 3.0))

			sensitive.density(2.85)

			sensitive.thickness_cm(self.layer_thick)
			self.num = int(50.0 * 1e-4 / self.layer_depth )

			for i in range(self.num):
				self.layers.add(sensitive)	

		else:
			print(str(type) + " is not implemented yet or not str type")

	def set_layer_thick(self, thick):
		self.layer_thick = thick * 1e-4
		self.layer_depth = thick * 1e-4

	def set_ion(self, A, Z, Q):
		self.Atom = A
		self.Z = Z
		self.Q = Q

	def set_energy_range(self, arr):
		self.range = arr

	def set_params(self, A, B, C, L):
		self.A = A
		self.B = B
		self.C = C
		self.L = L

	def set_theta_incident(self, ang):
		self.ang = ang
		if self.layer_thick == None:
			print("Error! Set layer_thick first!")
			quit()

		self.layer_thick = self.layer_thick / np.cos(self.ang * np.pi / 180.0)


	def run(self):

		print("ip_type is " + str(self.ip_type))
		print("layer_thick [um] is " + str(self.layer_depth * 1e4))
		print("Angle of incident [deg] is " + str(self.ang))
		print("Z of incident is " + str(self.Z))
		print("Atomic mass of incident is " + str(self.Atom))

		self.GV_arr = []

		for en in tqdm(self.range):

			GV = 0.0
			p = pycatima.Projectile(self.Atom, self.Z, self.Q, en / self.Atom)
			res = pycatima.calculate_layers(p, self.layers)

			for i in range(self.num):
				if res.results[i].Eloss == 0.0:
					break

				dE = res.results[i].Eloss

				z = self.layer_depth + self.layer_depth * i


				num = self.A * np.exp(-(z * 1e4) / self.L)
				denum = (1 + self.B * dE / (self.layer_depth * 1e4))
				GV += dE * (num / denum + self.C)

			if (en != 0 and GV == 0.0):

				dE = en

				z = self.layer_depth + self.layer_depth * i

				num = self.A * np.exp(-(z * 1e4) / self.L)

				denum = (1 + self.B * dE / (self.layer_depth * 1e4))
				GV += dE * (num / denum + self.C)

			self.GV_arr.append(GV)

		fig, (ax1) = plt.subplots(nrows=1, ncols=1)
		fig.set_figheight(20)
		fig.set_figwidth(20)
		ax1.set_xlabel("Energy [MeV]", fontsize = 30)
		ax1.set_ylabel("Sensitivity [GL/ion]", fontsize = 30)
		plt.xticks(fontsize=30)
		plt.yticks(fontsize=30)
		ax1.plot(self.range, self.GV_arr, color = 'blue', linewidth = 3)
		ax1.grid(which='minor', alpha=0.5)
		ax1.grid(which='major', alpha=1.0)
		plt.autoscale(tight=True)
		plt.show()


	def save_data(self):
		with open("data/GL_" + str(self.Z) + "_Z_" + str(self.Atom) + "_am_" + \
		str(self.ang) + "_deg_" + str("%.2f" % self.range[0]) + "-" + \
		str("%.2f" % self.range[-1]) + "_MeV" +  ".txt", "w") as file:

			for i in range(self.range.shape[0]):
				file.write("{}\t{}\n".format(self.range[i], self.GV_arr[i]))