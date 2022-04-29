### build instructions
```
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
git clone git@github.com:bchiarito/cmssw_CustomPFNanoTwoProng.git
scram b -j 10
```

### unit testing
```
UnitTest/test/test_pfnano.sh
UnitTest/test/test_postproc.sh
```

### running by hand
```
python ../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.twoprongModule myModuleConstr
```

### build instructions from scratch
```
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
git cms-rebase-topic andrzejnovak:614nosort
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cp UnitTest/test/PFNano_tweaks/addPFCands_cff.py PhysicsTools/PFNano/python
cp UnitTest/test/PFNano_tweaks/pfnano_cff.py PhysicsTools/PFNano/python
scram b -j 10
```
