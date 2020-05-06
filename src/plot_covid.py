#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2020-05-06 01:36:23 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

import numpy as np
import pandas as pd
from csv import DictReader
import matplotlib.pyplot as plt
import scipy.optimize as opt
import sys

sys.path.insert(0, '../../../../bin/python/')
import kaonlt as klt

c = klt.pyPlot(None)

# inp_f = "../covid-19-data/public/data/ecdc/full_data.csv"
inp_case = "../covid-19-data/public/data/ecdc/total_cases.csv"
inp_death = "../covid-19-data/public/data/ecdc/total_deaths.csv"

try:
    case_data = dict(pd.read_csv(inp_case))
    death_data = dict(pd.read_csv(inp_death))
except IOError:
    print("Error: %s or %s [plz]does not appear to exist." % (inp_death,case_data))

# Cases and deaths
us_c = np.array(case_data["United States"])
us_d = np.array(death_data["United States"])
china_c = np.array(case_data["China"])
china_d = np.array(death_data["China"])
de_c = np.array(case_data["Germany"])
de_d = np.array(death_data["Germany"])
sk_c = np.array(case_data["South Korea"])
sk_d = np.array(death_data["South Korea"])
itl_c = np.array(case_data["Italy"])
itl_d = np.array(death_data["Italy"])
uk_c = np.array(case_data["United Kingdom"])
uk_d = np.array(death_data["United Kingdom"])

# Ratio of cases to deaths
us_dc = us_d/us_c
china_dc = china_d/china_c
de_dc = de_d/de_c
sk_dc = sk_d/sk_c
itl_dc = itl_d/itl_c
uk_dc = uk_d/uk_c

# Populations
us_pop = 328.2e6
china_pop = 1.393e9
de_pop = 83.02e6
sk_pop = 51.64e6
itl_pop = 60.36e6
uk_pop = 66.65e6

# Health care ranks normalized to 100 (source: https://www.who.int/healthinfo/paper30.pdf and https://worldpopulationreview.com/countries/best-healthcare-in-the-world/)
us_hcr = 37/100
china_hcr = 144/100 
de_hcr = 25/100
sk_hcr = 58/100
itl_hcr = 2/100
uk_hcr = 18/100

days = np.array(range(np.int64(len(us_c))))

# This is the function we are trying to fit to the data.
def fit(x, a, b, c):
     return a * np.exp(-b * x) + c
 
f = plt.figure(figsize=(11.69,8.27))
plt.style.use('default')

plt.scatter(days,us_c, label='cases')
plt.scatter(days,us_d, label='death')
plt.legend(loc=0)
# plt.xscale('log')
plt.yscale('log')
plt.xlabel('Days', fontsize =16)
plt.ylabel('Events', fontsize =16)
plt.title('US Covid vs Days', fontsize =20)

f.savefig('../OUTPUTS/us_cd.png')

f = plt.figure(figsize=(11.69,8.27))
plt.style.use('default')

plt.scatter(us_c, us_d, label="US data #37")
plt.scatter(china_c, china_d, label="China data #144")
plt.scatter(de_c, de_d, label="Germany data #58")
plt.scatter(sk_c, sk_d, label="South Korea data #2")
plt.scatter(itl_c, itl_d, label="Italy data")
plt.scatter(uk_c, uk_d, label="UK data #18")

# The actual curve fitting happens here
optimizedParameters, pcov = opt.curve_fit(fit, us_c, us_d,maxfev=10000)

# Use the optimized parameters to plot the best fit
plt.plot(us_c, fit(us_c, *optimizedParameters), label="fit [$a*e^{-bx}+c$]");

plt.legend(loc=0)
plt.xscale('log')
# plt.yscale('log')
plt.xlabel('log(Cases)', fontsize =16)
plt.ylabel('Deaths', fontsize =16)
plt.title('US Death vs Case', fontsize =20)

f.savefig('../OUTPUTS/cd_all.png')

f = plt.figure(figsize=(11.69,8.27))
plt.style.use('default')

plt.scatter(us_c/us_pop, us_d/us_pop, label="US data")
plt.scatter(china_c/china_pop, china_d/china_pop, label="China data")
plt.scatter(de_c/de_pop, de_d/de_pop, label="Germany data")
plt.scatter(sk_c/sk_pop, sk_d/sk_pop, label="South Korea data")
plt.scatter(itl_c/itl_pop, itl_d/itl_pop, label="Italy data")
plt.scatter(uk_c/uk_pop, uk_d/uk_pop, label="UK data")

# The actual curve fitting happens here
optimizedParameters, pcov = opt.curve_fit(fit, us_c/us_pop, us_d/us_pop,maxfev=10000)

# Use the optimized parameters to plot the best fit
plt.plot(us_c/us_pop, fit(us_c/us_pop, *optimizedParameters), label="fit [$a*e^{-bx}+c$]");

plt.legend(loc=0)
plt.xscale('log')
# plt.yscale('log')
plt.xlabel('log(Cases per capita)', fontsize =16)
plt.ylabel('Deaths per capita', fontsize =16)
plt.title('US Death vs Case (per capita)', fontsize =20)

f.savefig('../OUTPUTS/cd_all_capita.png')

f = plt.figure(figsize=(11.69,8.27))
plt.style.use('default')

plt.scatter((us_c*us_hcr)/us_pop, (us_d*us_hcr)/us_pop, label="US data #37")
plt.scatter((china_c*china_hcr)/china_pop, (china_d*china_hcr)/china_pop, label="China data #144")
plt.scatter((de_c*de_hcr)/de_pop, (de_d*de_hcr)/de_pop, label="Germany data #25")
plt.scatter((sk_c*sk_hcr)/sk_pop, (sk_d*sk_hcr)/sk_pop, label="South Korea data #58")
plt.scatter((itl_c*itl_hcr)/itl_pop, (itl_d*itl_hcr)/itl_pop, label="Italy data #2")
plt.scatter((uk_c*uk_hcr)/uk_pop, (uk_d*uk_hcr)/uk_pop, label="UK data #18")

# The actual curve fitting happens here
optimizedParameters, pcov = opt.curve_fit(fit, (us_c*us_hcr)/us_pop, (us_d*us_hcr)/us_pop,maxfev=10000)

# Use the optimized parameters to plot the best fit
plt.plot((us_c*us_hcr)/us_pop, fit((us_c*us_hcr)/us_pop, *optimizedParameters), label="fit [$a*e^{-bx}+c$]");

plt.legend(loc=0)
plt.xscale('log')
# plt.yscale('log')
plt.xlabel('log(Cases per capita, weighted by health care rank)', fontsize =16)
plt.ylabel('Deaths per capita, weighted by health care rank', fontsize =16)
plt.title('US Death vs Case (per capita, weighted by health care rank)', fontsize =20)

f.savefig('../OUTPUTS/cd_all_wcapita.png')

f = plt.figure(figsize=(11.69,8.27))
plt.style.use('default')

plt.plot(days,us_dc, label='US')
plt.plot(days,china_dc, label='China')
plt.plot(days,de_dc, label='Germany')
plt.plot(days,sk_dc, label='South Korea')
plt.plot(days,itl_dc, label='Italy')
plt.plot(days,uk_dc, label='UK')
plt.legend(loc=0)
plt.xlabel('Days', fontsize =16)
plt.ylabel('Ratio', fontsize =16)
plt.title('Death to Case Ratio', fontsize =20)

f.savefig('../OUTPUTS/cd_all_ratio.png')

plt.show()
