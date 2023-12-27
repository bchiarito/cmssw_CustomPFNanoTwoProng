### build instructions
```
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
git clone git@github.com:bchiarito/cmssw_CustomPFNanoTwoProng.git .
scram b -j 10
```

### running PFNano step interactively
```
cp /cms/chiarito/rootfiles/framework_unittest/MiniAOD.root .
echo "file:MiniAOD.root" >> infile.txt
cmsRun PhysicsTools/PFNano/test/NANOAOD_XX_ULYY_cfg.py inputFilesFile=infile.txt maxEvents=10
```

### running NanoAODTools step interactively
```
python PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.main twoprongConstr_optionalTrack_addLoose,photonConstr_default,recoPhiConstr_HPID,recoPhiConstr_cutBased --bo ../../PhysicsTools/NanoAODTools/test/dropPF.txt
python PhysicsTools/NanoAODTools/test/copy_tree.py NanoAOD_Skim.root
```

### build instructions from scratch
```
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
git cms-rebase-topic andrzejnovak:614nosort
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/NanoAOD
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
mkdir temp
cd temp
git init
git remote add -f origin https://github.com/bchiarito/cmssw_CustomPFNanoTwoProng.git
git config core.sparseCheckout true
echo "UnitTest/test/PFNano_tweaks" >> .git/info/sparse-checkout
echo "PhysicsTools/NanoAODTools/python" >> .git/info/sparse-checkout
echo "PhysicsTools/NanoAODTools/test" >> .git/info/sparse-checkout
echo "PhysicsTools/PFNano/test/" >> .git/info/sparse-checkout
git pull origin master
cd ..
cp temp/UnitTest/test/PFNano_tweaks/addPFCands_cff.py PhysicsTools/PFNano/python
cp temp/UnitTest/test/PFNano_tweaks/pfnano_cff.py PhysicsTools/PFNano/python
cp temp/UnitTest/test/PFNano_tweaks/photons_cff.py PhysicsTools/NanoAOD/python
cp temp/UnitTest/test/PFNano_tweaks/genparticles_cff.py PhysicsTools/NanoAOD/python
cp temp/UnitTest/test/PFNano_tweaks/LHETablesProducer.cc PhysicsTools/NanoAOD/plugins
cp temp/PhysicsTools/PFNano/test/NANOAOD_* PhysicsTools/PFNano/test/
cp temp/PhysicsTools/PFNano/test/Cert_* PhysicsTools/PFNano/test/
cp temp/PhysicsTools/NanoAODTools/python/photons_cff.py PhysicsTools/NanoAODTools/python/
cp temp/PhysicsTools/NanoAODTools/python/genparticles_cff.py PhysicsTools/NanoAODTools/python/
cp temp/PhysicsTools/NanoAODTools/python/postprocessing/modules/*.py PhysicsTools/NanoAODTools/python/postprocessing/modules/
cp -r temp/PhysicsTools/NanoAODTools/test/ PhysicsTools/NanoAODTools
rm -rf temp/
scram b -j 10
```
