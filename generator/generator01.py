import numpy as np
import random


def generate(i):
	maxConsec_base = 4
	maxPresence_base = 8
	maxHours_base  = 10
	minHours_base = 1
	nNurses = i 


	mu, sigma = 12, 12
	demand_samples = np.random.normal(mu, sigma, nNurses)



if __name__ == '__main__':

	generate(20)