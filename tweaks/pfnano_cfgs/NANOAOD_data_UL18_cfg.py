# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: nanoaod -s NANO --nThreads 1 --data --era Run2_2018,run2_nanoAOD_106Xv1 --conditions 106X_dataRun2_v32 --eventcontent NANOAOD --datatier NANOAOD --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False))) --filein file:output_numEvent100.root -n 100 --python_filename=nano_Run2018.py --no_exec
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ("python")
options.register("inputFilesFile", "", VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.register("goodLumis", "", VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.register("numof", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "")
options.register("totalforfile", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "")
options.setDefault("maxEvents", -1)
options.parseArguments()

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv1_cff import run2_nanoAOD_106Xv1

process = cms.Process('NANO',Run2_2018,run2_nanoAOD_106Xv1)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Log Messages
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# process input
readFiles = []
if options.inputFilesFile == "":
  readFiles.extend(['file:miniAOD_numEvent10.root'])
else:
  with open(options.inputFilesFile) as fi:
    for line in fi:
      # take filename and add "file:" .dat
      if options.inputFilesFile[-4:] == '.dat':
        newline = line.strip()
        location, numof, totalforfile = newline.split()
        numof = int(numof)
        totalforfile = int(totalforfile)
        i = location.rfind('/')
        location = location[i+1:len(location)]
        readFiles.append('file:'+location)
      # leave as is for .txt
      if options.inputFilesFile[-4:] == '.txt':
        newline = line.strip()
        location, numof, totalforfile = newline.split()
        numof = int(numof)
        totalforfile = int(totalforfile)
        readFiles.append(location)

# compute skips
if numof==1 and totalforfile==1:
  maxevents = -1
  skipevents = 0
elif numof == totalforfile:
  maxevents = int(round(float(options.maxEvents) / float(totalforfile)))
  skipevents = int(maxevents * (numof - 1))
  maxevents = -1
else:
  maxevents = int(round(float(options.maxEvents) / float(totalforfile)))
  skipevents = int(maxevents * (numof - 1))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(maxevents) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( readFiles ),
    secondaryFileNames = cms.untracked.vstring(),
    duplicateCheckMode = cms.untracked.string("checkEachRealDataFile"),
    skipEvents = cms.untracked.uint32(skipevents)
)

if not options.goodLumis=="" and not options.goodLumis=="None":
  import FWCore.PythonUtilities.LumiList as LumiList
  process.source.lumisToProcess = LumiList.LumiList(filename = options.goodLumis).getVLuminosityBlockRange()

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('nanoaod nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('NanoAOD.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v32', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeData 

#call to customisation function nanoAOD_customizeData imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeData(process)

# Automatic addition of the customisation function from PhysicsTools.PFNano.pfnano_cff
from PhysicsTools.PFNano.pfnano_cff import PFnano_customizeData, PFnano_customizeData_allPF, PFnano_customizeData_AK4JetsOnly, PFnano_customizeData_AK8JetsOnly, PFnano_customizeData_noInputs

#call to customisation function PFnano_customizeData imported from PhysicsTools.PFNano.pfnano_cff
#process = PFnano_customizeData(process)
process = PFnano_customizeData_allPF(process)
#process = PFnano_customizeData_AK4JetsOnly(process)
#process = PFnano_customizeData_AK8JetsOnly(process)
#process = PFnano_customizeData_noInputs(process)

# End of customisation functions

# Customisation from command line

process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
