from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math

from twoprong_constants import *
from simpleSelector import *
from photonModule import *

class twoprongModule(Module):
    def __init__(self, addLooseIso=False):
        self.addLooseIso = addLooseIso
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
        self.out.branch("TwoProng_passIso", "I", lenVar="nTwoProng")
        if self.addLooseIso:
          self.out.branch("TwoProng_chargedIso", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_neutralIso", "F", lenVar="nTwoProng")
          self.out.branch("TwoProng_egammaIso", "F", lenVar="nTwoProng")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        pfcands = Collection(event, "PFCands")
        flags = Object(event, "Flag")

        # baseline filtering
        pass_filter = (
        self.mygetattr(flags, 'goodVertices', True)
        and self.mygetattr(flags, 'HBHENoiseFilter', True)
        and self.mygetattr(flags, 'HBHENoiseIsoFilter', True)
        and self.mygetattr(flags, 'EcalDeadCellTriggerPrimitiveFilter', True)
        and self.mygetattr(flags, 'BadPFMuonFilter', True)
        and self.mygetattr(flags, 'BadChargedCandidateFilter', True)
        and self.mygetattr(flags, 'ecalBadCalibFilter', True)
        and self.mygetattr(flags, 'globalSuperTightHalo2016Filter', True)
        and self.mygetattr(flags, 'eeBadScFilter', True)
        )
        if not (pass_baseline): return False

        # per event vectors
        TwoProng_pt = []
        TwoProng_eta = []
        TwoProng_phi = []
        TwoProng_mass = []
        TwoProng_massl = []
        TwoProng_massPi0 = []
        TwoProng_massEta = []
        TwoProng_passIso = []
        if self.addLooseIso:
          TwoProng_chargedIso = []
          TwoProng_neutralIso = []
          TwoProng_egammaIso = []

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
            if photon.Pt() < const_photonMinPt : continue
            photonPi0.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_pionMass)
            photonEta.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_etaMass)
            twoprong = center + photon
            # overall kinematics
            if twoprong.Pt() < const_minPt : continue
            if math.fabs(twoprong.Eta()) > const_maxEta : continue
            # isolation
            chargedIso = 0
            neutralIso = 0
            egammaIso = 0
            for k in range(len(pfcands)):
              pfvec3 = pfcands[k].p4()
              pfvec3.SetPhi(pfcands[k].phiAtVtx)
              if center.DeltaR(pfvec3) > const_isolationCone : continue
              if (pfcands[k].fromPV <= 1) : continue
              if (abs(pfcands[k].pdgId) == 211 or abs(pfcands[k].pdgId) == 13):
                if k == i or k == j : continue
                chargedIso += pfvec3.Pt()
              if pfcands[k].pdgId == 130:
                neutralIso += pfvec3.Pt()
              if (abs(pfcands[k].pdgId) == 11 or pfcands[k].pdgId == 22):
                if math.fabs(center.DeltaPhi(pfvec3)) <= const_photonBoxPhi/2.0 and math.fabs(center.Eta() - pfvec3.Eta()) <= const_photonBoxEta/2.0:
                  continue
                egammaIso += pfvec3.Pt()
            passIso = True
            if chargedIso/twoprong.Pt() > const_chargedIsoCut : passIso = False
            if neutralIso/twoprong.Pt() > const_neutralIsoCut : passIso = False
            if egammaIso/twoprong.Pt() > const_egammaIsoCut : passIso = False
            if not self.addLooseIso and not passIso: continue
            # symmetry
            passSym = True
            track_symmetry = min(pfvec1.Pt(), pfvec2.Pt()) / max(pfvec1.Pt(), pfvec2.Pt())
            photon_symmetry = min(pfvec1.Pt()+pfvec2.Pt(), photon.Pt()) / max(pfvec1.Pt()+pfvec2.Pt(), photon.Pt())
            if track_symmetry < const_minTrackSymmetry : passSym = False
            if photon_symmetry < const_minPhotonSymmetry : passSym = False
            # finished, store
            TwoProng_pt.append(twoprong.Pt())            
            TwoProng_phi.append(twoprong.Phi())            
            TwoProng_eta.append(twoprong.Eta())
            TwoProng_mass.append(twoprong.M())            
            TwoProng_massl.append((center+leading_pf_photon).M())            
            TwoProng_massPi0.append((center+photonPi0).M())
            TwoProng_massEta.append((center+photonEta).M())            
            TwoProng_passIso.append(passIso)
            if self.addLooseIso:
              TwoProng_chargedIso.append(chargedIso/twoprong.Pt())
              TwoProng_neutralIso.append(neutralIso/twoprong.Pt())
              TwoProng_egammaIso.append(egammaIso/twoprong.Pt())
        # loop over pfcands finished
        nTwoProng = len(TwoProng_pt)

        # fill branches
        self.out.fillBranch("nTwoProng", nTwoProng)
        self.out.fillBranch("TwoProng_pt", TwoProng_pt)
        self.out.fillBranch("TwoProng_eta", TwoProng_eta)
        self.out.fillBranch("TwoProng_phi", TwoProng_phi)
        self.out.fillBranch("TwoProng_mass", TwoProng_mass)
        self.out.fillBranch("TwoProng_massl", TwoProng_massl)
        self.out.fillBranch("TwoProng_massPi0", TwoProng_massPi0)
        self.out.fillBranch("TwoProng_massEta", TwoProng_massEta)
        self.out.fillBranch("TwoProng_passIso", TwoProng_passIso)
        if self.addLooseIso:
          self.out.fillBranch("TwoProng_chargedIso", TwoProng_chargedIso)
          self.out.fillBranch("TwoProng_neutralIso", TwoProng_neutralIso)
          self.out.fillBranch("TwoProng_egammaIso", TwoProng_egammaIso)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

twoprongConstr_default = lambda: twoprongModule()
twoprongConstr_addLooseIso = lambda: twoprongModule(addLooseIso=True)
