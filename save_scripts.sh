#!/bin/bash          
#/* Copyright (c) 2018 Siddhartha Shelton */

cd create_data_hist
git add *.py *.dat *.sh
cd ..

cd special_plot_scripts/
git add *.py *.dat *.sh
cd ..

cd special_plot_scripts/fturnoff_plots/
git add *.py *.dat *.sh
cd ..
cd ..

git add *.py *.dat *.sh

git commit -m "update"
git push