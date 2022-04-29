#! /bin/bash
#python ../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.twoprongModule twoprongConstr_default --bo dropPF.txt
python ../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.twoprongModule twoprongConstr_addLooseIso --bo dropPF.txt
python copy_tree.py NanoAOD_Skim.root
python plot_test_twoprong.py NANOAOD_TwoProng.root
