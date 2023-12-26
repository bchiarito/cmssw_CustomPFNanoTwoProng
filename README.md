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
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
git cms-rebase-topic andrzejnovak:614nosort
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
mkdir temp
cd temp
git init
git remote add -f origin origin https://github.com/bchiarito/cmssw_CustomPFNanoTwoProng.git
git config core.sparseCheckout true
echo "UnitTest/test/PFNano_tweaks" >> .git/info/sparse-checkout
git pull origin master
cd ..
cp temp/UnitTest/test/PFNano_tweaks/addPFCands_cff.py PhysicsTools/PFNano/python
cp temp/UnitTest/test/PFNano_tweaks/pfnano_cff.py PhysicsTools/PFNano/python
cp temp/UnitTest/test/PFNano_tweaks/photons_cff.py PhysicsTools/NanoAOD/python
cp temp/UnitTest/test/PFNano_tweaks/genparticles_cff.py PhysicsTools/NanoAOD/python
cp temp/UnitTest/test/PFNano_tweaks/LHETablesProducer.cc PhysicsTools/NanoAOD/plugins
rm -rf temp/
scram b -j 10
```
