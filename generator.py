#!/usr/bin/env python

import random
import time
import csv
import numpy as np
import pickle
import threading
import numpy as np
import pandas as pd
import requests


def fault(temp, hum, dec):
    # checks if the parameters are within reasonable limits
    if 20 <= temp <= 50 and 30 <= hum <= 70 and 60 <= dec <= 100:
        return False
    else:
        return True


# generates random values for temperature
def temp():
    rand = random.random()
    if rand < 0.9:
        return round(random.uniform(20, 50), 2)
    else:
        return round(random.uniform(-50, 200), 2)


# generates random values for humidity
def humidity():
    rand = random.random()
    if rand < 0.9:
        return random.randint(30, 70)
    else:
        return random.randint(0, 100)


# generate random values for loudness
def decibels():
    rand = random.random()
    if rand < 0.9:
        return random.randint(60, 100)
    else:
        return random.randint(0, 150)


# generates random values for a single unit
def simulate(fault=False):
    units = [temp(), humidity(), decibels()]
    if fault:
        pd.concat([units, fault(units[0], units[1], units[2])], axis=1)
    return units
