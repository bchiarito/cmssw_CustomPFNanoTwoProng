from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math

from collections import Counter

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
        self.out.branch("GenOmega_prongs", "F", lenVar="nGenOmega")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def get_decaymode(self, index, genparticles):
        #print "finding daughters for", genparticles[index].pdgId
        daughters = []
        granddaughters = []
        for i, genparticle in enumerate(genparticles):
          if genparticle.genPartIdxMother == index: daughters.append(genparticle.pdgId)
          if genparticle.pdgId == 221 and genparticle.genPartIdxMother == index:
            for g in genparticles:
              if g.genPartIdxMother == i: granddaughters.append(g.pdgId)
        #for d in daughters:
        #  print "  ", d
        #for d in granddaughters:
        #  print "    ", d

        # eta modes
        if Counter(daughters) == Counter([22, 22]): return 1
        elif Counter(daughters) == Counter([111, 111, 111]): return 2
        elif Counter(daughters) == Counter([211, -211, 111]): return 3
        elif Counter(daughters) == Counter([211, -211, 22]): return 4

        # etaprime modes
        elif (Counter(daughters) == Counter([111, 111, 221])
             and Counter(granddaughters) == Counter([22, 22])): return 5
        elif (Counter(daughters) == Counter([111, 111, 221])
             and Counter(granddaughters) == Counter([111, 111, 111])): return 6
        elif (Counter(daughters) == Counter([22, 22])): return 7 # can never return
        elif (Counter(daughters) == Counter([211, -211, 221])
             and Counter(granddaughters) == Counter([22, 22])): return 8
        elif (Counter(daughters) == Counter([211, -211, 221])
             and Counter(granddaughters) == Counter([111, 111, 111])): return 9
        elif (Counter(daughters) == Counter([111, 111, 221])
             and Counter(granddaughters) == Counter([211, -211, 111])): return 10
        elif (Counter(daughters) == Counter([111, 111, 221])
             and Counter(granddaughters) == Counter([211, -211, 22])): return 11
        elif (Counter(daughters) == Counter([22, 113])
             and Counter(granddaughters) == Counter([211, -211])): return 12
        elif (Counter(daughters) == Counter([22, 223])
             and Counter(granddaughters) == Counter([211, -211, 111])): return 13
        elif (Counter(daughters) == Counter([211, -211, 221])
             and Counter(granddaughters) == Counter([211, -211, 111])): return 14
        elif (Counter(daughters) == Counter([211, -211, 221])
             and Counter(granddaughters) == Counter([211, -211, 22])): return 15

        # cannot determine
        else: return 0

    def get_prongs(self, decaymode):
        return {
          0: -1,
          1: 0,
          2: 0,
          3: 2,
          4: 2,
          5: 0,
          6: 0,
          7: 0,
          8: 2,
          9: 2,
          10: 2,
          11: 2,
          12: 2,
          13: 2,
          14: 4,
          15: 4
        }.get(decaymode, -1)

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
        GenOmega_prongs = []

        genis = []
        for i in range(len(genparticles)):
          genparticle = genparticles[i]
          if genparticle.pdgId == 54:
            genis.append(i)

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
          decaymode = self.get_decaymode(t, genparticles)
          GenOmega_decaymode.append(decaymode)
          GenOmega_prongs.append(self.get_prongs(decaymode))

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
              decaymode = self.get_decaymode(i, genparticles)
              GenOmega_decaymode.append(decaymode)
              GenOmega_prongs.append(self.get_prongs(decaymode))

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
        self.out.fillBranch("GenOmega_prongs", GenOmega_prongs)
        return True

genpartConstr_res = lambda: customGenPartModule(signal='res') # resonant, Phi > omega omega
genpartConstr_nonres = lambda: customGenPartModule(signal='nonres') # non-resonant, t t omega
