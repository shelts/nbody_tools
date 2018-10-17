#!/bin/bash          
#/* Copyright (c) 2018 Siddhartha Shelton */

git add create_data_hist/*.py create_data_hist/*.dat

git add special_plot_scripts/*.py 
git add special_plot_scripts/*.sh

git add special_plot_scripts/fturnoff_plots/*.py 
git add special_plot_scripts/fturnoff_plots/*.sh
git add *.py *.dat *.sh

git commit -m "update"
git push