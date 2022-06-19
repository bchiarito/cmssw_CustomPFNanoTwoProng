import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ("python")
options.register("input", "", VarParsing.multiplicity.singleton, VarParsing.varType.string, "")

process = cms.Process("GENANA")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

# Source
readFiles = [
"file:new_signal_10ev.root"
]
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring( readFiles ),
#                            eventsToProcess = cms.untracked.VEventRange('1:206-1:206',)
)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

# Dumps list of gen particles 
process.printList = cms.EDAnalyzer("ParticleListDrawer",
                     src = cms.InputTag("prunedGenParticles"),
                     maxEventsToPrint  = cms.untracked.int32(-1),
                     printVertex = cms.untracked.bool(True)
)

# Draws gen particle decay chain
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("prunedGenParticles"),                                                                 
                                   printStatus = cms.untracked.bool(True),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(True),
                                   printVertex = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   #status = cms.untracked.vint32( 3 )
)

process.path = cms.Path(process.printTree)
