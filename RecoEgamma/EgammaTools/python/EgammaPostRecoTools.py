import FWCore.ParameterSet.Config as cms
import pkgutil
import os 

def _getCMSSWVersion():
    return os.environ['CMSSW_VERSION'].split("_")[1:]

def _validRelease():
    """this function defines all releases this file is currently valid for"""
    cmsswVersion =_getCMSSWVersion()
    majorVersion = int(cmsswVersion[0])
    minorVersion = int(cmsswVersion[1])
    allowedVersions = { 8 : [0],
                        9 : [4],
                        10 : [2,6],
                        11 : [0,1,2,3],
                        12 : [0,1,4,6]
                        }
                
    if majorVersion not in allowedVersions:
        allowedStr = ', '.join(str(x) for x in allowedVersions.keys())
        raise Exception("EgammaPostRecoTools: CMSSW major version {} is not supported; allowed versions: {}.\nPlease contact E/gamma POG to see if this version should be supported".format(majorVersion,allowedStr))
    elif minorVersion not in allowedVersions[majorVersion]:
        allowedStr = ', '.join(str(x) for x in allowedVersions[majorVersion])
        raise Exception("EgammaPostRecoTools: CMSSW major version {} is supported, but minor version {} is not, allowed versions: {}.\nPlease contact E/gamma POG to see if this version should be supported".format(majorVersion,minorVersion,allowedStr))

def _isULDataformat():
    cmsswVersion =_getCMSSWVersion()
    isUL = (int(cmsswVersion[0]) >= 10 and int(cmsswVersion[1]) >= 5) or (int(cmsswVersion[0]) >=11)
    return isUL


def _CMSSWGT11():
    cmsswVersion =_getCMSSWVersion()
    return int(cmsswVersion[0]) >=11


#define the default IDs to produce in VID
_defaultEleIDModules =  [ 'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff',
                        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff', 
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_iso_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_noIso_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Winter22_122X_V1_cff'
                        ]
_defaultPhoIDModules =  [ 'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V1_TrueVtx_cff',
                        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V1p1_cff', 
                        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff',
                        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Spring16_nonTrig_V1_cff',
                        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_RunIIIWinter22_122X_V1_cff',
                        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Winter22_122X_V1_cff'  
                        ]
if not _isULDataformat:
    #was depreciated due to the new e/gamma dataformat for UL
    _defaultPhoIDModules.insert(1,'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V1_cff')


#the new Fall17V2 modules are loaded as default if they exist in the release
#we do it this way as we can use the same script for all releases and people who
#dont want V2 can still use this script
_fall17V2PhoMVAIDModules = [
    'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff'
    ]
_fall17V2PhoCutIDModules = [
    'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff'
    ]
_fall17V2EleIDModules = [
    'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff'
    ]

if pkgutil.find_loader(_fall17V2EleIDModules[0]) != None:
    _defaultEleIDModules.extend(_fall17V2EleIDModules)
else:
    print ("EgammaPostRecoTools: Fall17V2 electron modules not found, running ID without them. If you want Fall17V2 IDs, please merge the approprate PR\n  94X:  git cms-merge-topic cms-egamma/EgammaID_949")

if pkgutil.find_loader(_fall17V2PhoMVAIDModules[0]) != None:
    _defaultPhoIDModules.extend(_fall17V2PhoMVAIDModules)
else:
    print ("EgammaPostRecoTools: Fall17V2 MVA photon modules not found, running ID without them. If you want Fall17V2 MVA Photon IDs, please merge the approprate PR\n  94X:  git cms-merge-topic cms-egamma/EgammaID_949\n  102X: git cms-merge-topic cms-egamma/EgammaID_1023")

if pkgutil.find_loader(_fall17V2PhoCutIDModules[0]) != None:
    _defaultPhoIDModules.extend(_fall17V2PhoCutIDModules)
else:
    print ("EgammaPostRecoTools: Fall17V2 cut based Photons ID modules not found, running ID without them. If you want Fall17V2 CutBased Photon IDs, please merge the approprate PR\n  94X:  git cms-merge-topic cms-egamma/EgammaID_949\n  102X: git cms-merge-topic cms-egamma/EgammaID_1023")

def _check_valid_era(era):
    valid_eras = ['2022-Prompt', '2017-Nov17ReReco','2016-Legacy','2016-Feb17ReMiniAOD','2018-Prompt','2016preVFP-UL', '2016postVFP-UL', '2017-UL', '2018-UL']
    if era not in valid_eras:
        raise RuntimeError('error, era {} not in list of allowed eras {}'.format(value,str(valid_eras)))
    return True


def _getEnergyCorrectionFile(era):
    _check_valid_era(era)
    if era=="2017-Nov17ReReco":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2017_17Nov2017_v1_ele_unc"
    if era=="2016-Legacy":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Legacy2016_07Aug2017_FineEtaR9_v3_ele_unc"
    if era=="2016-Feb17ReMiniAOD":
        raise RuntimeError('Error in postRecoEgammaTools, era 2016-Feb17ReMiniAOD is not currently implimented')
    if era=="2018-Prompt":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2018_Step2Closure_CoarseEtaR9Gain_v2"
    if era=="2017-UL":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2017_24Feb2020_runEtaR9Gain_v2"
    if era=="2018-UL":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2018_29Sep2020_RunFineEtaR9Gain"
    if era=="2016preVFP-UL":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2016_UltraLegacy_preVFP_RunFineEtaR9Gain_v3"
    if era=="2016postVFP-UL":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2016_UltraLegacy_postVFP_RunFineEtaR9Gain_v1"
    if era=="2022-Prompt":
        return "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Step3_scale_step2_smearings/step4_Prompt2022FG_28_06_2023_v0"

    raise LogicError('Error in postRecoEgammaTools, era '+era+' not added to energy corrections function, please update this function')



def _isInputFrom80X(era):
    _check_valid_era(era)
    if era=="2016-Legacy" or era=="2016-Feb17ReMiniAOD": return True
    else: return False

def _isInputFrom94XTo102X(era):
    _check_valid_era(era)
    if era=="2017-Nov17ReReco" or era=="2018-Prompt": return True
    else: return False

def _getMVAsBeingRun(vidMod):
    mvasBeingRun = []
    for id_ in vidMod.physicsObjectIDs:
        for cut in id_.idDefinition.cutFlow:
            if cut.cutName.value().startswith("GsfEleMVA") or cut.cutName.value().startswith("PhoMVA"):
                mvaValueName = cut.mvaValueMapName.getProductInstanceLabel().replace("RawValues","Values")
                
                mvasBeingRun.append({'val' : {'prod' : cut.mvaValueMapName.getModuleLabel(),'name' : mvaValueName}, 'cat' : {'prod' : cut.mvaCategoriesMapName.getModuleLabel(),'name' : cut.mvaCategoriesMapName.getProductInstanceLabel() }})
    return mvasBeingRun
                
def _addMissingMVAValuesToUserData(process,egmod):

    if len(egmod)<2 or egmod[0].modifierName.value()!='EGExtraInfoModifierFromFloatValueMaps' or egmod[1].modifierName.value()!='EGExtraInfoModifierFromIntValueMaps':
        raise RuntimeError('dumping offending module {}\nError in postRecoEgammaTools._addMissingMVAValuesToUserData, we assume that the egamma_modifiers are setup so first its the float mod and then the int mod, this is currently not the case, the offending module dump is above'.format(egmod.dumpPython()))
    
    eleMVAs = _getMVAsBeingRun(process.egmGsfElectronIDs)
    phoMVAs = _getMVAsBeingRun(process.egmPhotonIDs)

    addVar = lambda modifier,var: setattr(modifier,var['name'],cms.InputTag(var['prod'],var['name']))
    
    for eleMVA in eleMVAs:
        if not hasattr(egmod[0].electron_config,eleMVA['val']['name']):
            addVar(egmod[0].electron_config,eleMVA['val'])
            addVar(egmod[1].electron_config,eleMVA['cat'])
    
    for phoMVA in phoMVAs:
        if not hasattr(egmod[0].photon_config,phoMVA['val']['name']):
            addVar(egmod[0].photon_config,phoMVA['val'])
            addVar(egmod[1].photon_config,phoMVA['cat'])
    
class CfgData:
    
    def __init__(self,args,kwargs):      
        self.defaults = {
            'applyEnergyCorrections' : False,
            'applyVIDOnCorrectedEgamma' : False,
            'isMiniAOD' : True,
            'era' : '2017-Nov17ReReco',
            'eleIDModules' : _defaultEleIDModules,
            'phoIDModules' : _defaultPhoIDModules,
            'runVID' : True,
            'runEnergyCorrections' : True,
            'applyEPCombBug' : False,
            'autoAdjustParams' : True,
            'computeHeepTrkPtIso' : True,
            'process' : None
        }
        #I hate this hack but easiest way to communicate that the preVID updator is running
        #gets set when we know we are going to run it or not
        self.runningPreVIDUpdator = False       

        if len(args)>1: 
            raise Exception('error multiple unnamed parameters pass to EgammaPostRecoTools')
        
        for k,v in self.defaults.items():
            setattr(self,k,v)
        
        for k,v in kwargs.items():
            if k not in self.defaults:
                raise Exception('error parameter {} not recognised'.format(k))
            setattr(self,k,v)
        
        if self.process == None:
            try:
                self.process = args[0]
            except IndexError:
                raise Exception('error, no "process" arguement passed')

##end utility functions

def _setupEgammaPreVIDUpdator(eleSrc,phoSrc,cfg):
    """
    This function updates the electrons and photons to form the basis for VID/energy correction
    Examples are updates to new dataformats and applications of the energy regression
    it only runs the updator if there is something to update
    
    defines a task egammaUpdatorTask which may or may not be empty
    
    """
    process = cfg.process
    process.egammaUpdatorTask = cms.Task()

    modifiers = cms.VPSet()
    from RecoEgamma.EgammaTools.egammaObjectModificationsInMiniAOD_cff import egamma8XObjectUpdateModifier
    if _isULDataformat():
        from RecoEgamma.EgammaTools.egammaObjectModificationsInMiniAOD_cff import egamma9X105XUpdateModifier
        if _isInputFrom80X(cfg.era):
            egamma9X105XUpdateModifier.allowGsfTrackForConvs = True

    if _isInputFrom80X(cfg.era): 
        if not cfg.isMiniAOD:
            #this is here as a reminder when we fix this bug
            egamma8XObjectUpdateModifier.ecalRecHitsEB = cms.InputTag("reducedEcalRecHitsEB","")
            egamma8XObjectUpdateModifier.ecalRecHitsEE = cms.InputTag("reducedEcalRecHitsEE","")
            print ("EgammaPostRecoTools: begin warning:")
            print ("   when running in 80X AOD, currenly do not fill 94X new data members ")
            print ("   members not filled: ")
            print ("      eles: e2x5Left, e2x5Right, e2x5Top, e2x5Bottom, nSaturatedXtals, isSeedSaturated")
            print ("      phos: nStaturatedXtals, isSeedSaturated")
            print ("   these are needed for the 80X energy regression if you are running it (if you dont know if  you are, you are not)")
            print ("   the miniAOD method fills them correctly")
            print ("   if you have a use case for AOD and need those members, contact e/gamma pog and we can find a solution")
            print ("EgammaPostRecoTools: end warning")
        else:
            modifiers.append(egamma8XObjectUpdateModifier)
    if (_isInputFrom80X(cfg.era) or _isInputFrom94XTo102X(cfg.era)) and _isULDataformat(): 
        #we have to add the modules to produce the variables needed to update the to new dataformat to the task
        process.load('RecoEgamma.ElectronIdentification.heepIdVarValueMapProducer_cfi')
        process.load('RecoEgamma.PhotonIdentification.photonIDValueMapProducer_cff')

        if cfg.isMiniAOD:
            process.load('RecoEgamma.EgammaIsolationAlgos.egmPhotonIsolationMiniAOD_cff')
            phoIsoTask = process.egmPhotonIsolationMiniAODTask 
            process.heepIDVarValueMaps.elesMiniAOD = eleSrc
            if not _CMSSWGT11(): 
                process.photonIDValueMapProducer.srcMiniAOD = phoSrc
                process.photonIDValueMapProducer.src = cms.InputTag("") 
            else:
                process.photonIDValueMapProducer.src = phoSrc 
            #now disabling miniAOD/AOD auto detection...
            process.heepIDVarValueMaps.dataFormat = 2 
            
            
            
        else:
            raise Exception("EgammaPostRecoTools: It is currently not possible to read AOD produced pre 106X in 106X+, please email e/gamma pog to get a resolution") 
            process.load('RecoEgamma.EgammaIsolationAlgos.egmPhotonIsolationAOD_cff')
            phoIsoTask = process.egmPhotonIsolationAODTask 
            process.heepIDVarValueMaps.elesAOD = eleSrc
            process.photonIDValueMapProducer.src = phoSrc
            #now disabling miniAOD/AOD auto detection...
            process.heepIDVarValueMaps.dataFormat = 1
            process.photonIDValueMapProducer.srcMiniAOD = cms.InputTag("") 
            
        process.egmPhotonIsolation.srcToIsolate = phoSrc
    

        process.egammaUpdatorTask.add(process.heepIDVarValueMaps,phoIsoTask,process.photonIDValueMapProducer)
        modifiers.append(egamma9X105XUpdateModifier)

    if modifiers != cms.VPSet():
        cfg.runningPreVIDUpdator = True
        if cfg.isMiniAOD:        
            modifiedEleProdName = "ModifiedElectronProducer"
            modifiedPhoProdName = "ModifiedPhotonProducer"
            updatedEleName = "updatedElectrons"
            updatedPhoName = "updatedPhotons"
        else:
            modifiedEleProdName = "ModifiedGsfElectronProducer"
            modifiedPhoProdName = "ModifiedRecoPhotonProducer"
            updatedEleName = "gedGsfElectrons"
            updatedPhoName = "gedPhotons"
            
            
        setattr(process,updatedEleName,cms.EDProducer(modifiedEleProdName,
                                                      src=eleSrc,
                                                      modifierConfig = cms.PSet(
                                                          modifications = modifiers
                                                      )
                                                  )
        )
        setattr(process,updatedPhoName,cms.EDProducer(modifiedPhoProdName,
                                                     src=phoSrc,
                                                     modifierConfig = cms.PSet(
                                                         modifications = modifiers
                                                     )
                                                 )
        )
        process.egammaUpdatorTask.add(getattr(process,updatedEleName))
        process.egammaUpdatorTask.add(getattr(process,updatedPhoName))
        return cms.InputTag(updatedEleName),cms.InputTag(updatedPhoName)
    else:
        return cms.InputTag(eleSrc.value()),cms.InputTag(phoSrc.value())

                                          
def _setupEgammaEnergyCorrections(eleSrc,phoSrc,cfg):
    """sets up the e/gamma energy corrections for miniAOD
    it will adjust eleSrc and phoSrc to the correct values

    it creates a task egammaScaleSmearTask with the modules to run
    """

    process = cfg.process

    process.egammaScaleSmearTask = cms.Task()  
    if cfg.runEnergyCorrections == False:
        return cms.InputTag(eleSrc.value()),cms.InputTag(phoSrc.value())
    
    if cfg.isMiniAOD:
        eleCalibName = "calibratedPatElectrons"
        phoCalibName = "calibratedPatPhotons"
    else:
        eleCalibName = "calibratedElectrons"
        phoCalibName = "calibratedPhotons"
        
    process.load('RecoEgamma.EgammaTools.calibratedEgammas_cff')

    eleCalibProd = getattr(process,eleCalibName)
    phoCalibProd = getattr(process,phoCalibName)

    eleCalibProd.src = eleSrc
    phoCalibProd.src = phoSrc
    
    energyCorrectionFile = _getEnergyCorrectionFile(cfg.era)
    eleCalibProd.correctionFile = energyCorrectionFile
    phoCalibProd.correctionFile = energyCorrectionFile


    if cfg.applyEPCombBug and hasattr(eleCalibProd,'useSmearCorrEcalEnergyErrInComb'):
        eleCalibProd.useSmearCorrEcalEnergyErrInComb=True
    elif hasattr(eleCalibProd,'useSmearCorrEcalEnergyErrInComb'):
        eleCalibProd.useSmearCorrEcalEnergyErrInComb=False
    elif cfg.applyEPCombBug:
        raise RuntimeError('Error in postRecoEgammaTools, the E/p combination bug can not be applied in >= 10_2_X (applyEPCombBug must be False) , it is only possible to emulate in 9_4_X')

    process.egammaScaleSmearTask.add(eleCalibProd)
    process.egammaScaleSmearTask.add(phoCalibProd)

    if cfg.applyEnergyCorrections or cfg.applyVIDOnCorrectedEgamma:
        eleCalibProd.produceCalibratedObjs = True
        phoCalibProd.produceCalibratedObjs = True
        return cms.InputTag(eleCalibName),cms.InputTag(phoCalibName)
    else:
        eleCalibProd.produceCalibratedObjs = False 
        phoCalibProd.produceCalibratedObjs = False 
        return cms.InputTag(eleSrc.value()),cms.InputTag(phoSrc.value())
    
        
def _setupEgammaVID(eleSrc,phoSrc,cfg):
    process = cfg.process
    process.egammaVIDTask = cms.Task()
    if cfg.runVID:
        #heep value map needs to be manually added to the task
        if not _isULDataformat()  and cfg.computeHeepTrkPtIso:
            import RecoEgamma.ElectronIdentification.Identification.heepElectronID_tools as heep_tools
            heep_tools.addHEEPProducersToSeq(process,cms.Sequence(),cfg.isMiniAOD,process.egammaVIDTask)
        process.egammaVIDTask.add(process.egmGsfElectronIDTask)
        process.egammaVIDTask.add(process.egmPhotonIDTask)
      
        
        process.egmGsfElectronIDs.physicsObjectSrc = eleSrc
        process.egmPhotonIDs.physicsObjectSrc = phoSrc

        if cfg.isMiniAOD:
            if not _CMSSWGT11():
                process.electronMVAValueMapProducer.srcMiniAOD = eleSrc
                process.photonMVAValueMapProducer.srcMiniAOD = phoSrc 
            #we need to also zero out the AOD srcs as otherwise it gets confused in two tier jobs
            #and bad things happen
                process.electronMVAValueMapProducer.src = cms.InputTag("")
                process.photonMVAValueMapProducer.src = cms.InputTag("") 
            else:
                process.electronMVAValueMapProducer.src = eleSrc
                process.photonMVAValueMapProducer.src = phoSrc

        else:
            process.electronMVAValueMapProducer.src = eleSrc
            process.photonMVAValueMapProducer.src = phoSrc 
            process.electronMVAValueMapProducer.srcMiniAOD = cms.InputTag("")
            process.photonMVAValueMapProducer.srcMiniAOD = cms.InputTag("")

            
        if hasattr(process,'electronMVAVariableHelper'):
            if cfg.isMiniAOD:
                if not _CMSSWGT11():
                    process.electronMVAVariableHelper.srcMiniAOD = eleSrc
                    process.electronMVAVariableHelper.src = cms.InputTag("")
                else:    
                    process.electronMVAVariableHelper.src = eleSrc
            else:
                process.electronMVAVariableHelper.src = eleSrc
                process.electronMVAVariableHelper.srcMiniAOD = cms.InputTag("")
                

        #pre UL dataformat, we have to run the egmPhotonIsolation and the like as part of vid
        #post UL dataformat its in the object, how if we are reading old data it will be running
        #as part of the updator sequence so even more important not to touch it
        if not _isULDataformat():
            process.egmPhotonIsolation.srcToIsolate = phoSrc
            if cfg.isMiniAOD:
                if not _CMSSWGT11():
                    process.photonIDValueMapProducer.srcMiniAOD = phoSrc
                    process.photonIDValueMapProducer.src = cms.InputTag("")
                else:
                    process.photonIDValueMapProducer.src = phoSrc
                if hasattr(process,'heepIDVarValueMaps'):
                    process.heepIDVarValueMaps.elesMiniAOD = eleSrc
                    process.heepIDVarValueMaps.dataFormat = 2
                    
            else:
                process.photonIDValueMapProducer.src = phoSrc
                process.photonIDValueMapProducer.srcMiniAOD = cms.InputTag("")
                if hasattr(process,'heepIDVarValueMaps'):
                    process.heepIDVarValueMaps.elesAOD = eleSrc
                    process.heepIDVarValueMaps.dataFormat = 1   
                if hasattr(process,'packedCandsForTkIso') and cfg.era.find("2016")!=-1:
                    process.packedCandsForTkIso.chargedHadronIsolation = ""          

    return eleSrc,phoSrc


def _setupEgammaPostVIDUpdator(eleSrc,phoSrc,cfg):
    from RecoEgamma.EgammaTools.egammaObjectModificationsInMiniAOD_cff import egamma_modifications,egamma8XLegacyEtScaleSysModifier
    from RecoEgamma.EgammaTools.egammaObjectModifications_tools import makeVIDBitsModifier,makeVIDinPATIDsModifier,makeEnergyScaleAndSmearingSysModifier  
    process = cfg.process

    process.egammaPostRecoPatUpdatorTask = cms.Task()

    if not cfg.isMiniAOD:
        return cms.InputTag(eleSrc.value()),cms.InputTag(phoSrc.value())

    if cfg.runVID:
        egamma_modifications.append(makeVIDBitsModifier(process,"egmGsfElectronIDs","egmPhotonIDs"))
        egamma_modifications.append(makeVIDinPATIDsModifier(process,"egmGsfElectronIDs","egmPhotonIDs"))
    else:
        egamma_modifications = cms.VPSet() #reset all the modifications which so far are just VID

    if cfg.runEnergyCorrections:
        egamma_modifications.append(makeEnergyScaleAndSmearingSysModifier("calibratedPatElectrons","calibratedPatPhotons"))
        egamma_modifications.append(egamma8XLegacyEtScaleSysModifier)
        

    
    #add any missing variables to the slimmed electron 
    if cfg.runVID:
        #MVA V2 values may not be added by default due to data format consistency issues
        _addMissingMVAValuesToUserData(process,egamma_modifications)
        #now add HEEP trk isolation if old dataformat (new its in the object proper)
        if not _isULDataformat() and cfg.computeHeepTrkPtIso:
            for pset in egamma_modifications:
                if pset.hasParameter("modifierName") and pset.modifierName == cms.string('EGExtraInfoModifierFromFloatValueMaps'):
                    pset.electron_config.heepTrkPtIso = cms.InputTag("heepIDVarValueMaps","eleTrkPtIso")
                    break

    for pset in egamma_modifications:
        pset.overrideExistingValues = cms.bool(True)
        if hasattr(pset,"electron_config"): pset.electron_config.electronSrc = eleSrc
        if hasattr(pset,"photon_config"): pset.photon_config.photonSrc = phoSrc

    process.slimmedElectrons = cms.EDProducer("ModifiedElectronProducer",
                                              src=eleSrc,
                                              modifierConfig = cms.PSet(
                                                  modifications = egamma_modifications
                                                  )
                                              )
    process.slimmedPhotons = cms.EDProducer("ModifiedPhotonProducer",
                                            src=phoSrc,
                                            modifierConfig = cms.PSet(
                                                modifications = egamma_modifications
                                                )
                                            )

   
    #we only run if the modifications are going to do something
    if egamma_modifications != cms.VPSet() or cfg.runningPreVIDUpdator:
        process.egammaPostRecoPatUpdatorTask.add(process.slimmedElectrons)
        process.egammaPostRecoPatUpdatorTask.add(process.slimmedPhotons)
        return eleSrc,phoSrc
    else:
        return cms.InputTag(eleSrc.value()),cms.InputTag(phoSrc.value())

def _setupEgammaPostRecoSeq(*args,**kwargs):
    """
    This function loads the calibrated producers calibratedPatElectrons,calibratedPatPhotons, 
    sets VID & other modules to the correct electron/photon source,
    loads up the modifiers and which then creates a new slimmedElectrons,slimmedPhotons collection
    with VID and scale and smearing all loaded in

    It runs internally in four steps

    1) update of the pre-vid object
    2) running E/gamma scale and smearing
    3) running VID
    4) update of the post-vid object

    Note the code has evolved (now dual miniAOD/AOD functions) so this function makes being seperate from 
    setupEgammaPostRecoSeq makes less sense than it used to
    """

    cfg = CfgData(args,kwargs)
    
    if cfg.applyEnergyCorrections != cfg.applyVIDOnCorrectedEgamma:
        raise RuntimeError('Error, applyEnergyCorrections {} and applyVIDOnCorrectedEgamma {} must be equal to each other for now,\n functionality for them to be different isnt yet availible'.format(applyEnergyCorrections,applyVIDOnCorrectedEgamma))

    if cfg.isMiniAOD:
        srcPhoLabel = 'slimmedPhotons'
        srcEleLabel = 'slimmedElectrons'
    else:
        srcPhoLabel = 'gedPhotons'
        srcEleLabel = 'gedGsfElectrons'

    phoSrc = cms.InputTag(srcPhoLabel,processName=cms.InputTag.skipCurrentProcess())
    eleSrc = cms.InputTag(srcEleLabel,processName=cms.InputTag.skipCurrentProcess())

    eleSrc,phoSrc = _setupEgammaPreVIDUpdator(eleSrc=eleSrc,phoSrc=phoSrc,cfg=cfg)
    eleSrc,phoSrc = _setupEgammaEnergyCorrections(eleSrc=eleSrc,phoSrc=phoSrc,cfg=cfg)
    eleSrc,phoSrc = _setupEgammaVID(eleSrc=eleSrc,phoSrc=phoSrc,cfg=cfg)
    eleSrc,phoSrc = _setupEgammaPostVIDUpdator(eleSrc=eleSrc,phoSrc=phoSrc,cfg=cfg)
    
    process = cfg.process
    
    process.egammaUpdatorSeq = cms.Sequence(process.egammaUpdatorTask)
    process.egammaScaleSmearSeq = cms.Sequence(process.egammaScaleSmearTask)
    process.egammaVIDSeq = cms.Sequence(process.egammaVIDTask)
    process.egammaPostRecoPatUpdatorSeq = cms.Sequence(process.egammaPostRecoPatUpdatorTask)


    process.egammaPostRecoSeq = cms.Sequence(
        process.egammaUpdatorSeq +
        process.egammaScaleSmearSeq +
        process.egammaVIDSeq + 
        process.egammaPostRecoPatUpdatorSeq
    )

def setupEgammaPostRecoSeq(process,
                           applyEnergyCorrections=False,
                           applyVIDOnCorrectedEgamma=False,
                           isMiniAOD=True,
                           era="2017-Nov17ReReco",
                           eleIDModules=_defaultEleIDModules,
                           phoIDModules=_defaultPhoIDModules,
                           runVID=True,
                           runEnergyCorrections=True,
                           applyEPCombBug=False,
                           autoAdjustParams=True,
                           computeHeepTrkPtIso=True):
    """
    Note: computeHeepTrkPtIso can't be set to false if you want to run a HEEP ID.
    """
    #first check if we are running in a valid release, will throw if not
    _validRelease()

    from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDElectronIdProducer,switchOnVIDPhotonIdProducer,setupAllVIDIdsInModule,DataFormat,setupVIDElectronSelection,setupVIDPhotonSelection
    # turn on VID producer, indicate data format  to be
    # DataFormat.AOD or DataFormat.MiniAOD, as appropriate
    if runVID:
        if isMiniAOD:
            switchOnVIDElectronIdProducer(process,DataFormat.MiniAOD)
            switchOnVIDPhotonIdProducer(process,DataFormat.MiniAOD)
        else:
            switchOnVIDElectronIdProducer(process,DataFormat.AOD)
            switchOnVIDPhotonIdProducer(process,DataFormat.AOD)

        for idmod in eleIDModules:
            setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
        for idmod in phoIDModules:
            setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

    if autoAdjustParams:
        if ((era=="2016-UL") and runEnergyCorrections):
            print ("EgammaPostRecoTools:INFO auto adjusting runEnergyCorrections to False as they are not yet availible for 2016-UL, set autoAdjustParams = False to force them to run")
            runEnergyCorrections = False



    _setupEgammaPostRecoSeq(process,applyEnergyCorrections=applyEnergyCorrections,applyVIDOnCorrectedEgamma=applyVIDOnCorrectedEgamma,era=era,runVID=runVID,runEnergyCorrections=runEnergyCorrections,applyEPCombBug=applyEPCombBug,isMiniAOD=isMiniAOD, computeHeepTrkPtIso=computeHeepTrkPtIso)
    

    return process


def makeEgammaPATWithUserData(process,eleTag=None,phoTag=None,runVID=True,runEnergyCorrections=True,era="2017-Nov17ReReco",suffex="WithUserData"):
    """
    This function embeds the value maps into a pat::Electron,pat::Photon
    This function is not officially supported by e/gamma and is on a best effort bais
    eleTag and phoTag are type cms.InputTag
    outputs new collection with {eleTag/phoTag}.moduleLabel + suffex 
    """
    from RecoEgamma.EgammaTools.egammaObjectModificationsInMiniAOD_cff import egamma_modifications,egamma8XLegacyEtScaleSysModifier,egamma8XObjectUpdateModifier
    from RecoEgamma.EgammaTools.egammaObjectModifications_tools import makeVIDBitsModifier,makeVIDinPATIDsModifier,makeEnergyScaleAndSmearingSysModifier  
    if runVID:
        egamma_modifications.append(makeVIDBitsModifier(process,"egmGsfElectronIDs","egmPhotonIDs"))
        egamma_modifications.append(makeVIDinPATIDsModifier(process,"egmGsfElectronIDs","egmPhotonIDs"))
    else:
        egamma_modifications = cms.VPSet() #reset all the modifications which so far are just VID
    if _isInputFrom80X(era): 
        egamma_modifications.append(egamma8XObjectUpdateModifier) #if we were generated in 80X, we need fill in missing data members in 94X
    if runEnergyCorrections:
        egamma_modifications.append(makeEnergyScaleAndSmearingSysModifier("calibratedElectrons","calibratedPhotons"))
        egamma_modifications.append(egamma8XLegacyEtScaleSysModifier)
    
    process.egammaPostRecoPatUpdatorTask = cms.Task()

    if eleTag:
        modName = eleTag.moduleLabel+suffex
        setattr(process,modName,cms.EDProducer("ModifiedElectronProducer",
                                               src=eleTag,
                                               modifierConfig = cms.PSet(
                                                 modifications = egamma_modifications
                                                 )      
                                               ))
        process.egammaPostRecoPatUpdatorTask.add(getattr(process,modName))

    if phoTag:
        modName = phoTag.moduleLabel+suffex
        setattr(process,modName,cms.EDProducer("ModifiedPhotonProducer",
                                               src=phoTag,
                                               modifierConfig = cms.PSet(
                                                 modifications = egamma_modifications
                                                 )
                                               )) 
        process.egammaPostRecoPatUpdatorTask.add(getattr(process,modName))
        
    process.egammaPostRecoPatUpdatorSeq = cms.Sequence(process.egammaPostRecoPatUpdatorTask)
    return process
