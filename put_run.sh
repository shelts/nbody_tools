#!/bin/bash   
cd /boinc/milkyway/bin

sudo -u boinc ./nbody_start_search \
--min_simulation_time 2.0 \
--max_simulation_time 6.0 \
--min_orbit_time 1.0 \
--max_orbit_time 1.0 \
--min_radius_1 0.1  \
--max_radius_1 0.5 \
--min_radius_2 0.1 \
--max_radius_2 0.5 \
--min_mass_1 1.0 \
--max_mass_1 100.0 \
--min_mass_2 0.01 \
--max_mass_2 0.95 \
--inertia 0.75  \
--n_bodies 30000 \
--population_size 50 \
--differential_scaling_factor 0.8 \
--parent_selection random \
--crossover_rate 0.9 \
--parameters /boinc/src/milkyway_nbody_assimilator/data/EMD_v170.lua \
--histogram /boinc/src/milkyway_nbody_assimilator/data/hist_v170_3p95_0p2_0p2_11_0p2__7_2_18_diffSeed.hist \
--search_name de_nbody_7_2_2018_v170_20k__sim_3
