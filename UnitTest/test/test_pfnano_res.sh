#! /bin/bash
printf "\n\n################################## TESTING UL18 MC ##################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_mc_UL18_cfg.py inputFilesFile=mc_res.txt maxEvents=10
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL18 MC ###################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL18 MC ################################\n"
