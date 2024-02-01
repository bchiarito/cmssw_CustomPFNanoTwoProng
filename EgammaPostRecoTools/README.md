# EgammaPostRecoTools

```
cmsrel CMSSW_13_3_0
cd CMSSW_13_3_0/src
cmsenv
git-cms-init
git-cms-addpkg RecoEgamma/PhotonIdentification
git-cms-addpkg RecoEgamma/ElectronIdentification
git-cms-addpkg RecoEgamma/EgammaTools
git-cms-addpkg EgammaAnalysis/ElectronTools
git clone git@github.com:cms-egamma/EgammaPostRecoTools.git
scram b -j8
```

**For Run3 Scales + smearing corrections** 

The Run3 Scale and smearing files should be available here : EgammaAnalysis/ElectronTools/data/ScalesSmearings

The path to the correction file should be added here : https://github.com/Prasant1993/EgammaPostRecoTools/blob/Update_Run3ID_electronNoIso_MiniAOD/python/EgammaPostRecoTools.py#L117


**For Run3 electron and photon IDs** 

The electron and photon ID config files must be changed in [1] and [2] for adding the new IDs:

[1] https://github.com/cms-sw/cmssw/tree/master/RecoEgamma/ElectronIdentification/python/Identification

[2] https://github.com/cms-sw/cmssw/tree/master/RecoEgamma/PhotonIdentification/python/Identification

**Changes to be made in the Analysis config file to add the IDs and corrections to MiniAOD** 

In the analysis config file for producing ntuple, the follwing code block needs to be added :

```
from EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runEnergyCorrections=True,
                       runVID=True,
                       era='2022-Prompt',
                       eleIDModules=['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_iso_V1_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_noIso_V1_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Winter22_122X_V1_cff'],
				     
                       phoIDModules=['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_RunIIIWinter22_122X_V1_cff',
                                     'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Winter22_122X_V1_cff']
                      )
```

In your cms path, you need to add "process.egammaPostRecoSeq" to add the IDs and corrections to the MiniAOD and produce a new collection of SlimmedElectron and SlimmedPhoton:

```
process.p = cms.Path (process.egammaPostRecoSeq * process.ggNtuplizer)
```