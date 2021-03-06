#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2020-05-06 19:49:30 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

cd covid-19-data/scripts/scripts/
echo "Updating COVID-19 dataset"
# python3 ecdc.py

cd ../../../src/
echo "Plotting dataset"
python3 plot_covid.py

cd ../OUTPUTS/
convert us_cd.png cd_all.png cd_all_capita.png cd_all_w_hc_capita.png cd_all_ratio.png cd_all_w_tests_capita.png cd_all_w_hc_tests_capita.png covid_plots.pdf
rm -rf *.png
