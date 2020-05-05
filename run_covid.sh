#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2020-05-05 13:30:22 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

cd src/
python3 plot_covid.py

cd ../OUTPUTS/
convert us_cd.png cd_all.png cd_all_capita.png cd_all_wcapita.png cd_all_ratio.png covid_plots.pdf
rm -rf *.png
