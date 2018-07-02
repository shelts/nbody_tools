#! /usr/bin/python
import os
from subprocess import call
import sys
args = sys.argv;

def __main__(arg):

    s = str( args[1] )
    pulled = "6_27_18"
    runs = "data_4_19_18"
    os.chdir("/boinc/milkyway/bin" )
    
    os.system("./tao_search_status --app milkyway_nbody --search_name " + s + " --print_best 49 >~/runs_" + runs + "_pulled_" + pulled + "/" + s)



__main__(args);
