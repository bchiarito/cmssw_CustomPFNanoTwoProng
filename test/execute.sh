#!/bin/sh

export INITIAL_DIR=$(pwd)
echo "&&& Here there are all the input arguments &&&"
echo $@

echo "&&& contents &&&"
pwd
ls -lh
find . -maxdepth 7 -type d -not -path '*/\.*'
echo 'now CMSSW_BASE'
echo $CMSSW_BASE
ls -lh $CMSSW_BASE

echo "&&& cmsRun &&&"
/usr/bin/time -v cmsRun -j FrameworkJobReport.xml -p PSet.py

echo "&&& contents again &&"
pwd
ls -lh

echo '&&& Check inside nested CMSSW &&&'
pwd
ls -lh CMSSW_10_6_27/CMSSW_10_6_27/src/PhysicsTools/NanoAODTools/
pwd
echo '&&& Check if scripts/ location exists &&&'
pwd
ls -lh CMSSW_10_6_27/src/PhysicsTools/NanoAODTools/

echo '&&& Run NanoAODTools postprocessor &&&'
pwd
ls -lh *.root
/usr/bin/time -v python CMSSW_10_6_27/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.main twoprongDataMCConstr_default,photonConstr_default --bo dropPF.txt
pwd
ls -lh *.root

echo '&&& Run copy_tree.py &&&'
pwd
ls -lh *.root
cp CMSSW_10_6_27/src/PhysicsTools/NanoAODTools/test/copy_tree.py .
python copy_tree.py NanoAOD_Skim.root
pwd
ls -lh *.root

echo '&&& Finished &&&'
