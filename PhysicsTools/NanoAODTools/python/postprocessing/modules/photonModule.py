from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math

class photonModule(Module):
    def __init__(self, addLooseIso=False):
        self.addLooseIso = addLooseIso
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nHighPtIdPhoton", "I")
        self.out.branch("HighPtIdPhoton_pt", "F", lenVar="nHighPtIdPhoton")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        photons = Collection(event, "Photon")

        # per event vectors
        Photon_pt = []

        nPhoton = len(Photon_pt)

        # fill branches
        self.out.fillBranch("nHighPtIdPhoton", nHighPtIdPhoton)
        self.out.fillBranch("HighPtIdPhoton_pt", HightPtIdPhoton_pt)
        return True


photonConstr_default = lambda: photonModule()
