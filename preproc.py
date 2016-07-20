#---------------------------------------------------
# TRAJECTORY DATASETS from CRAWDAD
#---------------------------------------------------
# - http://www.crawdad.org/
# Taxi Cab Trajectories, Rome, Italy, 2014:
# - 370 taxi cabs during 30 days between 2/1/14 to 3/2/14
# - total more than 20 M trajectories (1.6 GB)
# - Coordinated Universal Time (UTC) +01:00
# Taxi Cab Trajectories, San Fransisco, CA, 2008:
# - 536 taxi cabs during 25 days between 5/17/08 to 6/10/08
# - total more than 10 M trajectories (0.4 GB)
# - Original Trajectory Format
#   - latitude, longitude, occupancy, UNIX epoch time
#   - in reverse chronological order
#   - e.g., Unix time 0 = UTC 1970/1/1 00:00:00
#   - e.g., Unix time 1429000000 = UTC 2015/4/14 08:26:40
#   - UTC-08:00, Summer Time UTC-07:00 in 3/13 through 11/16
#---------------------------------------------------
#!/usr/bin/env python



import numpy as np

import os # to create/delete a directory/file
import glob # to get a file path

import datetime # to use date time object
import pytz # to make time shift based on time zone

import pyproj # to calculate distance for (longitude, latitude)



class DatasetPreprocessing:
	"""This class is used for preprocessing data."""

	def __init__(self):
		return

	def create_contactlist(self, dataset, txrange):
		"""Create contact list from preprocessed dataset."""

		t_intvl = 30 # time interval (trajectory sampling rate)

		dates, nn, nodes = self.get_dates_nn_info(dataset)

		for date in dates:

			print date, nn[date]

			contactlist = [] # format: time u x_u y_u v x_v y_v
			edgelist = [] # format: u v times

			for u in nodes[date]:

				data_u = np.genfromtxt("file_%d.txt" % u, delimiter=",")
				data_u = data_u[~np.isnan(data_u).any(axis=1)] # remove nan

				for v in nodes[date]:

					if u >= v:
						continue

					data_v = np.genfromtxt("file_%d.txt" % v, delimiter=",")
					data_v = data_v[~np.isnan(data_v).any(axis=1)]

					# make them same time instances
					mask = np.in1d(data_u[:, 0], data_v[:, 0])
					data_u2 = data_u[mask]
					mask = np.in1d(data_v[:, 0], data_u2[:, 0])
					data_v = data_v[mask]

					contacts = self.calc_contacts(u, v, data_u2, data_v, txrange)

					contactlist += contacts
					contacts = np.asarray(contacts)
					times = list(contacts[:, 0])
					edge = [u, v, times]
					edgelist.append(edge)



	def calc_contacts(self, u, v, data_u, data_v, txrange):
		"""Calculate contacts between two nodes."""

		contacts = [] # contact data

		dists = self.calc_distance(data_u[:,1],data_u[:,2],data_v[:,1],data_v[:,2])

		mask = dists < txrange # compare distance with txrange

		t = data_u[mask][:, 0]
		u = np.ones(len(t))*u
		v = np.ones(len(t))*v

		data = np.c_[t, u, data_u[mask][:, 1:], v, data_v[mask][:, 1:]]
		contacts = data.tolist()

		return contacts



	def calc_distance(self, lat_u, lon_u, lat_v, lon_v):
		"""Calculate distance for two GPS coodinates in (lat, lon)."""

		q = pyproj.Geod(ellps="WGS84") # standard coordinate system in GPS
		fa, ba, d = q.inv(lon_u, lat_u, lon_v, lat_v)

		return d



	def get_dates_nn_info(dataset):
		"""Get dates and nodes information."""

		dates = []
		nn = {}
		nodes = {}

		dirpaths = glob.glob("Directory/*")
		for dirpath in dirpaths:
			date = dirpath.split("/")[-1]
			dates.append(date)
			filepaths = glob.glob("Directory/*")
			nodes_date = []
			for filepath in filepaths:
				filename = filepath.split("/")[-1]
				node_id = int(filename[-7: -4])
				nodes_date.append(node_id)
			nn[date] = len(nodes_date)
			nodes[date] = nodes_date

		return dates, nn, nodes


