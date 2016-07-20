#---------------------------------------------------
# Prediction Error Metrics
#---------------------------------------------------
# - http://scikit-learn.org/stable/modules/model_evaluation.html#
# - to evaluate the quality of predictions of a model
# - Most simple one is MAE. If large errors, RMSE is better.
#---------------------------------------------------
#!/usr/bin/env python



import numpy as np
import scipy as sp # to calculate confidence intervals



def mean_absolute_error(self, y1, y2):
	"""Mean Absolute Error (MAE)"""
	# - predicted value (y2), true value (y1)
	# - MAE(y1, y2) = 1/n Summation i = 1 to n |y1 - y2|

	e = np.absolute(y1 - y2)
	m, h = mean_confidence_interval(e)

	return m, h



def root_mean_squared_error(self, y1, y2):
	"""Root Mean Squared Error (RMSE)"""
	# - predicted value (y2), true value (y1)
	# - RMSE(y1, y2) = root(MSE)
	# - MSE(y1, y2) = 1/n Summation i = 1 to n square(y1 - y2)

	e = np.square(y1 - y2) # to amplify large errors
	m, h = mean_confidence_interval(e)
	m = np.sqrt(m)
	h = np.sqrt(h)

	return m, h



def relative_absolute_error(self, y1, y2):
	"""Relative Absolute Error (RAE)"""
	# - predicted value (y2), true value (y1)
	# - RAE(y1, y2) = Summation i = 1 to n |(y1 - y2)| /
	#                 Summation i = 1 to n |(mean(y1) - y2)|

	e1 = np.absolute(y1 - y2)
	e2 = np.absolute(np.mean(y1) - y2)
	m = np.sum(e1) / np.sum(e2)
	h = 0

	return m, h



def root_relative_squared_error(self, y1, y2):
	"""Root Relative Squared Error (RRSE)"""
	# - predicted value (y2), true value (y1)
	# - RRSE(y1, y2) = root(RSE)
	# - RSE(y1, y2) = Summation i = 1 to n (y1 - y2)**2 /
	#           Summation i = 1 to n (mean(y1) - y2)**2

	e1 = np.square(y1 - y2)
	e2 = np.square(np.mean(y1) - y2)
	m = np.sum(e1) / np.sum(e2)
	m = np.sqrt(m)
	h = 0

	return m, h



def mean_absolute_percentage_deviation(self, y1, y2):
	"""Mean Absolute Percentage deviation (MAPD)"""
	# - predicted value (y2), true value (y1)
	# - MAPD(y1, y2) = 1/n Summation i = 1 to n |(y1 - y2)/y1|

	e = np.absolute((y1 - y2)/y1)
	m, h = mean_confidence_interval(e)

	return m, h



def mean_confidence_interval(self, data):

	confidence = 0.95
	a = 1.0*np.array(data)
	n = len(a)
	m = np.mean(a)
	se = sp.stats.sem(a)
	h = se * sp.stats.t._ppf((1+confidence)/2., n-1)

	return m, h