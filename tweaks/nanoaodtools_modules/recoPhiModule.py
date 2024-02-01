from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math

const_PhotonCutBasedIDMin = 2

class recoPhiModule(Module):
    def __init__(self, photon):
        self.photon = photon

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if self.photon == "cutBased": self.cutbasedstr = "CutBased"
        if self.photon == "HPID": self.cutbasedstr = ""
        self.out.branch(self.cutbasedstr+"RecoPhi_pass", "B")
        self.out.branch(self.cutbasedstr+"RecoPhi_pt", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_eta", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_phi", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_mass", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_photonLeg_pt", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_photonLeg_eta", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_photonLeg_phi", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_photonLeg_mass", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_twoprongLeg_pt", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_twoprongLeg_eta", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_twoprongLeg_phi", "F")
        self.out.branch(self.cutbasedstr+"RecoPhi_twoprongLeg_mass", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        twoprongs = Collection(event, "TwoProng")
        if self.photon == "cutBased": photons = Collection(event, "Photon")
        if self.photon == "HPID": photons = Collection(event, "HighPtIdPhoton")

        # reconstruct phi
        recophi_vec = ROOT.Math.PtEtaPhiMVector()
        photon_vec = ROOT.Math.PtEtaPhiMVector()
        twoprong_vec = ROOT.Math.PtEtaPhiMVector()
        twoprong_i = []
        photon_i = []
        recophi_pass = False
        for i, twoprong in enumerate(twoprongs):
          if abs(twoprong.eta) > 2.5: continue
          for j, photon in enumerate(photons):
            if self.photon == "cutBased" and photon.cutBased < const_PhotonCutBasedIDMin: continue
            if abs(photon.eta) > 2.5: continue
            twoprong_vec = ROOT.Math.PtEtaPhiMVector(twoprong.pt, twoprong.eta, twoprong.phi, twoprong.mass)
            photon_vec = ROOT.Math.PtEtaPhiMVector(photon.pt, photon.eta, photon.phi, photon.mass)
            if ROOT.Math.VectorUtil.DeltaPhi(twoprong_vec, photon_vec) > 0.1:
              photon_i.append(j)
              twoprong_i.append(i)
        if len(twoprong_i)>0 and len(photon_i)>0:
          ii = min(twoprong_i)
          jj = min(photon_i)
          twoprong_cand = twoprongs[ii]
          photon_cand = photons[jj]
          twoprong_vec = ROOT.Math.PtEtaPhiMVector(twoprong_cand.pt, twoprong_cand.eta, twoprong_cand.phi, twoprong_cand.mass)
          photon_vec = ROOT.Math.PtEtaPhiMVector(photon_cand.pt, photon_cand.eta, photon_cand.phi, photon_cand.mass)
          recophi_vec = twoprong_vec + photon_vec
          recophi_pass = True
        
        # fill branches
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_pass", recophi_pass)
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_pt", recophi_vec.Pt())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_eta", recophi_vec.Eta())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_phi", recophi_vec.Phi())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_mass", recophi_vec.M())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_photonLeg_pt", photon_vec.Pt())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_photonLeg_eta", photon_vec.Eta())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_photonLeg_phi", photon_vec.Phi())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_photonLeg_mass", photon_vec.M())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_twoprongLeg_pt", twoprong_vec.Pt())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_twoprongLeg_eta", twoprong_vec.Eta())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_twoprongLeg_phi", twoprong_vec.Phi())
        self.out.fillBranch(self.cutbasedstr+"RecoPhi_twoprongLeg_mass", twoprong_vec.M())
        return True

recoPhiConstr_cutBased = lambda: recoPhiModule(photon='cutBased')
recoPhiConstr_HPID = lambda: recoPhiModule(photon='HPID')
