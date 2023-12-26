### build instructions
```
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
git clone git@github.com:bchiarito/cmssw_CustomPFNanoTwoProng.git .
scram b -j 10
```

### unit testing
```
UnitTest/test/
```

### running by hand
```
cd <base>/PhysicsTools/PFNano/test/
cmsRun NANOAOD_$4_$5_cfg.py inputFilesFile=cmssw_infiles_$3.dat goodLumis=$6 maxEvents=-1
python ../../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.twoprongModule myModuleConstr
```

### build instructions from scratch
```
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
git cms-rebase-topic andrzejnovak:614nosort
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

cp UnitTest/test/PFNano_tweaks/addPFCands_cff.py PhysicsTools/PFNano/python
cp UnitTest/test/PFNano_tweaks/pfnano_cff.py PhysicsTools/PFNano/python
cp UnitTest/test/PFNano_tweaks/photons_cff.py PhysicsTools/NanoAOD/python
cp UnitTest/test/PFNano_tweaks/genparticles_cff.py PhysicsTools/NanoAOD/python
cp UnitTest/test/PFNano_tweaks/LHETablesProducer.cc PhysicsTools/NanoAOD/plugins
scram b -j 10
```

### all module constructors
genpartConstr   res, nonres
filtersConstr   UL18
photonConstr    default, addLoose
recoPhiConstr   cutBased, HPID
selectionConstr default, muon, photon
twoprongConstr  default, addLoose, optionalTrack, optionalTrack_addLoose

