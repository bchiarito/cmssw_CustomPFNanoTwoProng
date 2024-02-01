
import FWCore.ParameterSet.Config as cms
import os
import sys
# set up process
process = cms.Process("EGAMMA")

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis') 
options.register('isMiniAOD',True,options.multiplicity.singleton,options.varType.bool," whether we are running on miniAOD or not")
options.register('runVID',True,options.multiplicity.singleton,options.varType.bool," ")
options.register('runEnergyCorrections',True,options.multiplicity.singleton,options.varType.bool," ")
options.register('applyEnergyCorrections',False,options.multiplicity.singleton,options.varType.bool," ")
options.register('applyVIDOnCorrectedEgamma',False,options.multiplicity.singleton,options.varType.bool," ")
options.register('applyEPCombBug',False,options.multiplicity.singleton,options.varType.bool," ")
options.register('era','2022-Prompt',options.multiplicity.singleton,options.varType.string," ")
options.register('isMC',False,options.multiplicity.singleton,options.varType.bool," ")
options.register('unscheduled',False,options.multiplicity.singleton,options.varType.bool," ")
options.register('nrThreads',1,options.multiplicity.singleton,options.varType.int," ")

options.parseArguments()

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(500),
    limit = cms.untracked.int32(10000000)
)
# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                #'/store/mc/Run3Summer22EEMiniAODv3/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/forPOG_124X_mcRun3_2022_realistic_postEE_v1-v3/2810000/014eb5f9-88c8-4620-a422-28a3fe114f1c.root',
                                #'/store/mc/Run3Summer22EEMiniAODv3/GluGluHtoGG_M-125_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/MINIAODSIM/124X_\
#mcRun3_2022_realistic_postEE_v1-v2/2560000/002bf121-178f-4113-b039-74014d1e8d22.root',
                              '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/390/00000/17c661a8-c901-41f6-9274-11f8ea2b8183.root'
                            ),  
                          )

process.options = cms.untracked.PSet(
    numberOfStreams = cms.untracked.uint32(options.nrThreads),
    numberOfThreads = cms.untracked.uint32(options.nrThreads),
    wantSummary = cms.untracked.bool(False)
)


def getGlobalTagName(isMC,era):
    if era=='2022-Prompt':
        if isMC: return '124X_mcRun3_2022_realistic_postEE_v1'
        else: return '124X_dataRun3_Prompt_v10'
    if era=='2018-Prompt':
        if isMC: return '102X_upgrade2018_realistic_v15'
        else: return '102X_dataRun2_Prompt_v11'
    elif era=='2017-Nov17ReReco':
        if isMC: return '94X_mc2017_realistic_v10'
        else: return '94X_dataRun2_ReReco_EOY17_v2'
    elif era=='2016-Legacy':
        if isMC: return '94X_mcRun2_asymptotic_v3'
        else: return '94X_dataRun2_v10'
    elif era=='2017-UL':
        if isMC: return '106X_mc2017_realistic_v6'
        else: return '106X_dataRun2_v20'
    else:
        raise RuntimeError('Error in runPostRecoEgammaTools, era {} not currently implimented. Allowed eras are 2018-Prompt 2017-Nov17ReReco 2016-Legacy 2017-UL'.format(era)) 
    

#process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")
#process.load("Configuration.StandardSequences.Services_cff")
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, getGlobalTagName(isMC=options.isMC,era=options.era), '')


from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       applyEnergyCorrections=False,
                       applyVIDOnCorrectedEgamma=False,
                       isMiniAOD=True,
                       era='2022-Prompt',                    
                       runVID=True,
                       runEnergyCorrections=True,
                       applyEPCombBug=False,
                       eleIDModules=['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_iso_V1_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_RunIIIWinter22_noIso_V1_cff',
                                     'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Winter22_122X_V1_cff'],
                       phoIDModules=['RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff',
                                     'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff',
                                     'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_RunIIIWinter22_122X_V1_cff',
                                     'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Winter22_122X_V1_cff']
                       )



#process.TFileService = cms.Service("TFileService", fileName = cms.string('ggtree_mc.root'))

process.p = cms.Path( process.egammaPostRecoSeq )

process.egammaOutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string(options.outputFile.replace(".root","_EDM.root")),
    outputCommands = cms.untracked.vstring('drop *',
                                           "keep *_*_*_RECO",
                                           "keep *_*_*_PAT",
                                           'keep *_*_*_HLT',
                                           'keep *_slimmedElectrons*_*_*',
                                           'keep *_slimmedPhotons*_*_*')
                                        )
if not options.isMiniAOD:
    process.egammaOutput.outputCommands = cms.untracked.vstring('drop *',
                                                                'keep *_gedGsfElectrons_*_*',
                                                                'keep *_gedPhotons_*_*',
                                                                'keep *_calibratedElectrons_*_*',
                                                                'keep *_calibratedPhotons_*_*',
                                                                'keep *_egmGsfElectronIDs_*_*',
                                                                'keep *_egmPhotonIDs_*_*')
    

process.outPath = cms.EndPath(process.egammaOutput)

residualCorrFileName = None
if options.isMiniAOD:
    try: 
        residualCorrFileName = process.calibratedPatElectrons.correctionFile.value()
    except AttributeError:
        pass
else:
    try:
        residualCorrFileName = process.calibratedElectrons.correctionFile.value()
    except AttributeError:
        pass

msgStr='''EgammaPostRecoTools:
  running with GT: {}
  running residual E corr: {}'''
print (msgStr.format(process.GlobalTag.globaltag.value(),residualCorrFileName))

if options.unscheduled:
    print ("  converting to unscheduled")
    from FWCore.ParameterSet.Utilities import convertToUnscheduled
    process=convertToUnscheduled(process)
