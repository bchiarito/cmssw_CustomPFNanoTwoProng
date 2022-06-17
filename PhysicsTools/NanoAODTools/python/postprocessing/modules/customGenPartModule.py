from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math

class customGenPartModule(Module):
    def __init__(self, signal):
        self.signal = signal
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if self.signal == 'res':
          self.out.branch("nGenPhi", "I")
          self.out.branch("GenPhi_pt", "F", lenVar="nGenPhi")
          self.out.branch("GenPhi_eta", "F", lenVar="nGenPhi")
          self.out.branch("GenPhi_phi", "F", lenVar="nGenPhi")
          self.out.branch("GenPhi_mass", "F", lenVar="nGenPhi")
          self.out.branch("GenPhi_status", "F", lenVar="nGenPhi")
          self.out.branch("GenPhi_index", "F", lenVar="nGenPhi")
        self.out.branch("nGenOmega", "I")
        self.out.branch("GenOmega_pt", "F", lenVar="nGenOmega")
        self.out.branch("GenOmega_eta", "F", lenVar="nGenOmega")
        self.out.branch("GenOmega_phi", "F", lenVar="nGenOmega")
        self.out.branch("GenOmega_mass", "F", lenVar="nGenOmega")
        self.out.branch("GenOmega_status", "F", lenVar="nGenOmega")
        self.out.branch("GenOmega_index", "F", lenVar="nGenOmega")
        self.out.branch("GenOmega_decaymode", "F", lenVar="nGenOmega")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def get_decaymode(self, genparticle):
        # FIXME
        return 0

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        genparticles = Collection(event, "GenPart")

        # per event vectors
        if self.signal == 'res':
          GenPhi_pt = []
          GenPhi_eta = []
          GenPhi_phi = []
          GenPhi_mass = []
          GenPhi_status = []
          GenPhi_index = []
        GenOmega_pt = []
        GenOmega_eta = []
        GenOmega_phi = []
        GenOmega_mass = []
        GenOmega_status = []
        GenOmega_index = []
        GenOmega_decaymode = []

        genis = []
        for i in range(len(genparticles)):
          genparticle = genparticles[i]
          if genparticle.pdgId == 54:
            genis.append(i)

        print genis
        last_part_index = -1
        if len(genis) == 1: last_part_index = genis[0]
        else:
          for i in genis:
            last_in_chain = True
            m = genparticles[i].genPartIdxMother
            m_id = genparticles[m].pdgId
            if not m_id == 54: last_in_chain = False # mother is not a Phi/Omega
            for j in genis:
              if i == genparticles[j].genPartIdxMother: last_in_chain = False # mother to a Phi/Omega
            if last_in_chain:
              last_part_index = i
        if last_part_index == -1: raise Exception("ERROR: Couldn't find last Phi/Omega in chain!")

        t = last_part_index
        if self.signal == 'res':
          GenPhi_pt.append(genparticles[t].pt)
          GenPhi_eta.append(genparticles[t].eta)
          GenPhi_phi.append(genparticles[t].phi)
          GenPhi_mass.append(genparticles[t].mass)
          GenPhi_status.append(genparticles[t].status)
          GenPhi_index.append(t)
        if self.signal == 'nonres':
          GenOmega_pt.append(genparticles[t].pt)
          GenOmega_eta.append(genparticles[t].eta)
          GenOmega_phi.append(genparticles[t].phi)
          GenOmega_mass.append(genparticles[t].mass)
          GenOmega_status.append(genparticles[t].status)
          GenOmega_index.append(t)
          decaymode = self.get_decaymode(genparticles[t])
          GenOmega_decaymode.append(decaymode)

        if self.signal == 'res':  
          for i in range(len(genparticles)):
            genparticle = genparticles[i]
            if genparticle.pdgId == 90000054 or genparticle.pdgId == 90000055:
              GenOmega_pt.append(genparticle.pt)
              GenOmega_eta.append(genparticle.eta)
              GenOmega_phi.append(genparticle.phi)
              GenOmega_mass.append(genparticle.mass)
              GenOmega_status.append(genparticle.status)
              GenOmega_index.append(i)
              decaymode = self.get_decaymode(genparticle)
              GenOmega_decaymode.append(decaymode)

        # fill branches
        if self.signal == 'res':
          nGenPhi = len(GenPhi_pt)
          self.out.fillBranch("nGenPhi", nGenPhi)
          self.out.fillBranch("GenPhi_pt", GenPhi_pt)
          self.out.fillBranch("GenPhi_eta", GenPhi_eta)
          self.out.fillBranch("GenPhi_phi", GenPhi_phi)
          self.out.fillBranch("GenPhi_mass", GenPhi_mass)
          self.out.fillBranch("GenPhi_status", GenPhi_status)
          self.out.fillBranch("GenPhi_index", GenPhi_index)
        nGenOmega = len(GenOmega_pt)
        self.out.fillBranch("nGenOmega", nGenOmega)
        self.out.fillBranch("GenOmega_pt", GenOmega_pt)
        self.out.fillBranch("GenOmega_eta", GenOmega_eta)
        self.out.fillBranch("GenOmega_phi", GenOmega_phi)
        self.out.fillBranch("GenOmega_mass", GenOmega_mass)
        self.out.fillBranch("GenOmega_status", GenOmega_status)
        self.out.fillBranch("GenOmega_index", GenOmega_index)
        self.out.fillBranch("GenOmega_decaymode", GenOmega_decaymode)
        return True

genpartConstr_res = lambda: customGenPartModule(signal='res') # resonant, Phi > omega omega
genpartConstr_nonres = lambda: customGenPartModule(signal='nonres') # non-resonant, t t omega
