from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math

class simpleSelector(Module):
    def __init__(self, selection=''):
        self.sel = selection
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        twoprongs = Collection(event, "TwoProng")
        if self.sel == 'one muon':
          if len(muons) == 0 : return False
        if self.sel == 'one photon':
          if len(photons) == 0 : return False
        if self.sel == 'muon electron photon':
          if len(muons) > 0 and muons[0].pt > 15: return True
          if len(electrons) > 0 and electrons[0].pt > 15: return True
          if len(photons) > 0 and photons[0].pt > 15: return True
          return False
        return True

selectionConstr_default = lambda: simpleSelector()
selectionConstr_muon = lambda: simpleSelector('one muon')
selectionConstr_photon = lambda: simpleSelector('one photon')
selectionConstr_muonelectronphoton = lambda: simpleSelector('muon electron photon')
