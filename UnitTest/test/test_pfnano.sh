#! /bin/bash
printf "\n\n################################## TESTING UL18 DATA ################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_data_UL18_cfg.py inputFilesFile=data.txt maxEvents=10 goodLumis=../../PhysicsTools/PFNano/test/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL18 DATA #################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL18 DATA ##############################\n"

printf "\n\n################################## TESTING UL17 DATA ################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_data_UL17_cfg.py inputFilesFile=data.txt maxEvents=10 goodLumis=../../PhysicsTools/PFNano/test/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL17 DATA #################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL17 DATA ##############################\n"

printf "\n\n################################## TESTING UL16 DATA ################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_data_UL16_cfg.py inputFilesFile=data.txt maxEvents=10 goodLumis=../../PhysicsTools/PFNano/test/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL16 DATA #################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL16 DATA ##############################\n"

printf "\n\n################################## TESTING UL18 MC ##################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_mc_UL18_cfg.py inputFilesFile=mc.txt maxEvents=10
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL18 MC ###################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL18 MC ################################\n"

printf "\n\n################################## TESTING UL18 MC ##################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_mc_UL17_cfg.py inputFilesFile=mc.txt maxEvents=10
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL17 MC ###################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL17 MC ################################\n"

printf "\n\n################################## TESTING UL16 MC ##################################\n\n\n"
cmsRun ../../PhysicsTools/PFNano/test/NANOAOD_mc_UL16_cfg.py inputFilesFile=mc.txt maxEvents=10
ret=$?
if [ ! $ret -eq 0 ]; then
  printf "\n\n################################## FAILED UL16 MC ###################################\n"
  exit 1
fi
printf "\n\n################################# SUCCESSFUL UL16 MC ################################\n"
