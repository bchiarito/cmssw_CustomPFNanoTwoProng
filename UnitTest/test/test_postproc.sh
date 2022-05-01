#! /bin/bash
python ../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.twoprongModule twoprongConstr_default --bo ../../PhysicsTools/NanoAODTools/test/dropPF.txt
python ../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.twoprongModule twoprongConstr_addLooseIso --bo ../../PhysicsTools/NanoAODTools/test/dropPF.txt
python ../../PhysicsTools/NanoAODTools/test/copy_tree.py NanoAOD_Skim.root
python plot_test_twoprong.py NANOAOD_TwoProng.root
