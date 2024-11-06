### initial build to submit crab jobs
```
cmssw-el7 # or equivilant on hexcms
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
git clone git@github.com:bchiarito/cmssw_CustomPFNanoTwoProng.git .
scram b -j 20 # less than 5 minutes
source /cvmfs/cms.cern.ch/common/crab-setup.sh
cd test
```

### to submit crab jobs
```
./submit_crab.py --help
```

### subsequent logins to check jobs only
```
cd CMSSW_10_6_27/src/test
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh
cd test
```

### to check on crab jobs
```
crab status -d <crab_dir> # specific job
crab tasks # list all jobs
```

### subsequent logins to submit new jobs
```
cmssw-el7 # or equivilant on hexcms
cd CMSSW_10_6_27/src/test
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh
cd test
```

### build instructions from scratch
```
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
# begin commands for photon scale factor code
git cms-init
git cms-addpkg RecoEgamma/EgammaTools  ### essentially just checkout the package from CMSSW
git clone https://github.com/cms-egamma/EgammaPostRecoTools.git
mv EgammaPostRecoTools/python/EgammaPostRecoTools.py RecoEgamma/EgammaTools/python/.
git clone -b ULSSfiles_correctScaleSysMC https://github.com/jainshilpi/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data/
git cms-addpkg EgammaAnalysis/ElectronTools
scram b -j 8
# end photon scale factor code
git cms-rebase-topic andrzejnovak:614nosort
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git cms-addpkg PhysicsTools/NanoAOD
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
mkdir temp
cd temp
git init
git remote add -f origin https://github.com/bchiarito/cmssw_CustomPFNanoTwoProng.git
git config core.sparseCheckout true
echo "tweaks" >> .git/info/sparse-checkout
git pull origin master
cd ..
mkdir -p PhysicsTools/NanoAODTools/test
cp temp/tweaks/pfnano_hacks/addPFCands_cff.py PhysicsTools/PFNano/python
cp temp/tweaks/pfnano_hacks/pfnano_cff.py PhysicsTools/PFNano/python
cp temp/tweaks/pfnano_hacks/photons_cff.py PhysicsTools/NanoAOD/python
cp temp/tweaks/pfnano_hacks/genparticles_cff.py PhysicsTools/NanoAOD/python
cp temp/tweaks/pfnano_hacks/LHETablesProducer.cc PhysicsTools/NanoAOD/plugins
cp temp/tweaks/pfnano_cfgs/NANOAOD*_cfg.py PhysicsTools/PFNano/test/
cp temp/tweaks/pfnano_cfgs/Cert_* PhysicsTools/PFNano/test/
cp temp/tweaks/nanoaodtools_modules/* PhysicsTools/NanoAODTools/python/postprocessing/modules/
cp temp/tweaks/nanoaodtools_running/* PhysicsTools/NanoAODTools/test
rm -rf temp/
scram b -j 10
```

### extra block inserted in cmsRun config file needed for Photon scale factors
```
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runEnergyCorrections=True,
                       runVID=True, #saves CPU time by not needlessly re-running VID, if you want the Fall17V2 IDs, set this to True or remove (default is True)
                       era='2018-UL')    
#a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)
```

### running PFNano step interactively
```
cp <miniaod_file.root> ./MiniAOD.root
echo "file:MiniAOD.root 1 1" >> infile.txt
cmsRun PhysicsTools/PFNano/test/NANOAOD_<XX>_UL<YY>_cfg.py inputFilesFile=infile.txt maxEvents=10
```

### running NanoAODTools step interactively
```
python PhysicsTools/NanoAODTools/scripts/nano_postproc.py . NanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.main twoprongConstr_optionalTrack_addLoose,photonConstr_default --bo PhysicsTools/NanoAODTools/test/dropPF.txt
python PhysicsTools/NanoAODTools/test/copy_tree.py NanoAOD_Skim.root
```

