#! /bin/bash
printf "### default: twoprong, photon, selector\n\n"
python ../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.main genpartConstr_res,filtersConstr_default,twoprongConstr_default,photonConstr_default,recoPhiConstr_HPID,recoPhiConstr_cutBased,selectionConstr_default --bo ../../PhysicsTools/NanoAODTools/test/dropPF.txt
printf "### finish: copy tree, histogram\n\n"
python ../../PhysicsTools/NanoAODTools/test/copy_tree.py NanoAOD_Skim.root
python plot_test_twoprong.py NANOAOD_TwoProng.root
