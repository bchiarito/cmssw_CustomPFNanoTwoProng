# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: nanoaod --filein file:output_numEvent100.root --fileout file:NanoAOD.root --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False))) --conditions 106X_mcRun2_asymptotic_v13 --step NANO --nThreads 1 --era Run2_2016 --python_filename NANOAOD_2016_cfg.py -n 10 --no_exec
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ("python")
options.register("inputFilesFile", "", VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.register("goodLumis", "", VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.setDefault("maxEvents", -1)
options.parseArguments()
from Configuration.Eras.Era_Run2_2016_cff import Run2_2016

process = cms.Process('NANO',Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Log Messages
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Input source
readFiles = []
if options.inputFilesFile == "":
  readFiles.extend(['file:miniAOD_numEvent10.root'])
else:
  with open(options.inputFilesFile) as fi:
    for line in fi:
      # process line if .dat
      if options.inputFilesFile[-4:] == '.dat':
        newline = line.strip()
        i = newline.rfind('/')
        newline = newline[i+1:len(line)]
        readFiles.append('file:'+newline)
      # dont process for .txt
      if options.inputFilesFile[-4:] == '.txt':
        readFiles.append(line.strip())
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( readFiles ),
    secondaryFileNames = cms.untracked.vstring(),
    duplicateCheckMode = cms.untracked.string("checkEachRealDataFile")
)
if not options.goodLumis=="" and not options.goodLumis=="None":
  import FWCore.PythonUtilities.LumiList as LumiList
  process.source.lumisToProcess = LumiList.LumiList(filename = options.goodLumis).getVLuminosityBlockRange()

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('nanoaod nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:NanoAOD.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v13', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

from PhysicsTools.PFNano.pfnano_cff import PFnano_customizeMC, PFnano_customizeMC_allPF, PFnano_customizeMC_AK4JetsOnly, PFnano_customizeMC_AK8JetsOnly, PFnano_customizeMC_noInputs
#process = PFnano_customizeMC(process)
process = PFnano_customizeMC_allPF(process)
#process = PFnano_customizeMC_AK4JetsOnly(process)
#process = PFnano_customizeMC_AK8JetsOnly(process)
#process = PFnano_customizeMC_noInputs(process)

# End of customisation functions

# Customisation from command line

process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
