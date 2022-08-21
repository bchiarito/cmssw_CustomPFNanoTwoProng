from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math

from twoprong_constants import *

class twoprongModule(Module):
    def __init__(self, addLoose=False, optionalTrack=False):
        self.addLoose = addLoose
        self.optionalTrack = optionalTrack
        pass

    def mygetattr(self, my_obj, my_branch, default_bool):
        try: getattr(my_obj, my_branch)
        except RuntimeError: return default_bool
        else: return getattr(my_obj, my_branch)

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nTwoProng", "I")
        self.out.branch("TwoProng_pt", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_eta", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_phi", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_mass", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_massl", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_massPi0", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_massEta", "F", lenVar="nTwoProng")
        if self.addLoose:
          self.out.branch("TwoProng_chargedIso", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_neutralIso", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_egammaIso", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_trackSym", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_photonSym", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_passIso", "I", lenVar="nTwoProng")
          self.out.branch("TwoProng_passSym", "I", lenVar="nTwoProng")
          self.out.branch("TwoProng_isTight", "I", lenVar="nTwoProng")
        if self.optionalTrack:
          self.out.branch("TwoProng_nTracks", "F", lenVar="nTwoProng")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        pfcands = Collection(event, "PFCands")
        flags = Object(event, "Flag")

        # per event vectors
        TwoProng_pt = []
        TwoProng_eta = []
        TwoProng_phi = []
        TwoProng_mass = []
        TwoProng_massl = []
        TwoProng_massPi0 = []
        TwoProng_massEta = []
        TwoProng_nTracks = []
        if self.addLoose:
          TwoProng_chargedIso = []
          TwoProng_neutralIso = []
          TwoProng_egammaIso = []
          TwoProng_trackSym = []
          TwoProng_photonSym = []
          TwoProng_passIso = []
          TwoProng_passSym = []
          TwoProng_isTight = []

        # loop over pf cands
        for i in range(len(pfcands)):
          pfvec1 = pfcands[i].p4()
          pfvec1.SetPhi(pfcands[i].phiAtVtx)
          if (pfcands[i].fromPV <= 1) : continue
          if pfvec1.Pt() < const_minTrackPt : continue
          for j in range(len(pfcands)):
            if j <= i : continue
            # charged hadron pair
            pfvec2 = pfcands[j].p4()
            pfvec2.SetPhi(pfcands[j].phiAtVtx)
            if not ( (pfcands[i].pdgId == 211 and pfcands[j].pdgId == -211) or (pfcands[i].pdgId == -211 and pfcands[j].pdgId == 211) ) : continue
            if (pfcands[j].fromPV <= 1) : continue
            if pfvec2.Pt() < const_minTrackPt : continue
            if pfvec1.DeltaR(pfvec2) > const_minTrackDr : continue
            center = pfvec1 + pfvec2
            # photon from photon box
            photon = ROOT.TLorentzVector()
            photonPi0 = ROOT.TLorentzVector()
            photonEta = ROOT.TLorentzVector()
            leading_pf_photon = ROOT.TLorentzVector()
            for k in range(len(pfcands)):
              if not(pfcands[k].pdgId == 22 or abs(pfcands[k].pdgId == 11)) : continue
              pfvec3 = pfcands[k].p4()
              pfvec3.SetPhi(pfcands[k].phiAtVtx)
              if math.fabs(center.DeltaPhi(pfvec3)) > const_photonBoxPhi/2.0 : continue
              if math.fabs(center.Eta() - pfvec3.Eta()) > const_photonBoxEta/2.0 : continue
              photon += pfvec3
              if pfvec3.Pt() > leading_pf_photon.Pt() : leading_pf_photon = pfvec3
            photonPi0.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_pionMass)
            photonEta.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_etaMass)
            twoprong = center + photon
            # isolation
            chargedIso = 0
            neutralIso = 0
            egammaIso = 0
            for k in range(len(pfcands)):
              pfvec3 = pfcands[k].p4()
              pfvec3.SetPhi(pfcands[k].phiAtVtx)
              extraTrackIndex = -1
              if center.DeltaR(pfvec3) > const_isolationCone : continue
              if (pfcands[k].fromPV <= 1) : continue
              if (abs(pfcands[k].pdgId) == 211 or abs(pfcands[k].pdgId) == 13):
                if k == i or k == j : continue
                if not self.optionalTrack:
                  chargedIso += pfvec3.Pt()
                elif pfvec3.Pt() < const_minTrackPt:
                  chargedIso += pfvec3.Pt()
                else:
                  if extraTrackIndex == -1:
                    extraTrackIndex = k
                  else:
                    chargedIso += pfvec3.Pt()
              if pfcands[k].pdgId == 130:
                neutralIso += pfvec3.Pt()
              if (abs(pfcands[k].pdgId) == 11 or pfcands[k].pdgId == 22):
                if math.fabs(center.DeltaPhi(pfvec3)) <= const_photonBoxPhi/2.0 and math.fabs(center.Eta() - pfvec3.Eta()) <= const_photonBoxEta/2.0:
                  continue
                egammaIso += pfvec3.Pt()
            if self.optionalTrack and not extraTrackIndex == -1:
              # reform twoprong momentum with extra track
              extraTrack = pfcands[extraTrackIndex].p4()
              extraTrack.setPhi(pfcands[extraTrackIndex].PhiAtVtx)
              twoprong = center + photon + extraTrack
            passIso = True
            if chargedIso/twoprong.Pt() > const_chargedIsoCut : passIso = False
            if neutralIso/twoprong.Pt() > const_neutralIsoCut : passIso = False
            if egammaIso/twoprong.Pt() > const_egammaIsoCut : passIso = False
            # symmetry
            passSym = True
            track_symmetry = min(pfvec1.Pt(), pfvec2.Pt()) / max(pfvec1.Pt(), pfvec2.Pt())
            photon_symmetry = min(pfvec1.Pt()+pfvec2.Pt(), photon.Pt()) / max(pfvec1.Pt()+pfvec2.Pt(), photon.Pt())
            if track_symmetry < const_minTrackSymmetry : passSym = False
            if photon_symmetry < const_minPhotonSymmetry : passSym = False
            # apply cuts
            if photon.Pt() < const_photonMinPt : continue
            if twoprong.Pt() < const_minPt : continue
            if math.fabs(twoprong.Eta()) > const_maxEta : continue
            if not self.addLoose and not passIso: continue
            if not self.addLoose and not passSym: continue
            # finished, store
            TwoProng_pt.append(twoprong.Pt())            
            TwoProng_phi.append(twoprong.Phi())            
            TwoProng_eta.append(twoprong.Eta())
            TwoProng_mass.append(twoprong.M())            
            TwoProng_massl.append((center+leading_pf_photon).M())            
            TwoProng_massPi0.append((center+photonPi0).M())
            TwoProng_massEta.append((center+photonEta).M())            
            if self.addLoose:
              TwoProng_chargedIso.append(chargedIso/twoprong.Pt())
              TwoProng_neutralIso.append(neutralIso/twoprong.Pt())
              TwoProng_egammaIso.append(egammaIso/twoprong.Pt())
              TwoProng_trackSym.append(track_symmetry)
              TwoProng_photonSym.append(photon_symmetry)
              TwoProng_passIso.append(passIso)
              TwoProng_passSym.append(passSym)
              TwoProng_isTight.append(passIso and passSym)
            if self.optionalTrack:
              TwoProng_nTracks.append(2 if extraTrackIndex==-1 else 3)
        # loop over pfcands finished

        # fill branches
        nTwoProng = len(TwoProng_pt)
        self.out.fillBranch("nTwoProng", nTwoProng)
        self.out.fillBranch("TwoProng_pt", TwoProng_pt)
        self.out.fillBranch("TwoProng_eta", TwoProng_eta)
        self.out.fillBranch("TwoProng_phi", TwoProng_phi)
        self.out.fillBranch("TwoProng_mass", TwoProng_mass)
        self.out.fillBranch("TwoProng_massl", TwoProng_massl)
        self.out.fillBranch("TwoProng_massPi0", TwoProng_massPi0)
        self.out.fillBranch("TwoProng_massEta", TwoProng_massEta)
        if self.addLoose:
          self.out.fillBranch("TwoProng_chargedIso", TwoProng_chargedIso)
          self.out.fillBranch("TwoProng_neutralIso", TwoProng_neutralIso)
          self.out.fillBranch("TwoProng_egammaIso", TwoProng_egammaIso)
          self.out.fillBranch("TwoProng_trackSym", TwoProng_trackSym)
          self.out.fillBranch("TwoProng_photonSym", TwoProng_photonSym)
          self.out.fillBranch("TwoProng_passIso", TwoProng_passIso)
          self.out.fillBranch("TwoProng_passSym", TwoProng_passSym)
          self.out.fillBranch("TwoProng_isTight", TwoProng_isTight)
        if self.optionalTrack:
          self.out.fillBranch("TwoProng_nTracks", TwoProng_nTracks)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

twoprongConstr_default = lambda: twoprongModule()
twoprongConstr_addLoose = lambda: twoprongModule(addLoose=True)
twoprongConstr_optionalTrack = lambda: twoprongModule(optionalTrack=True)
twoprongConstr_optionalTrack_addLoose = lambda: twoprongModule(optionalTrack=True, addLoose=True)
