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
        if not self.optionalTrack:
          self.label = "TwoProng"
        else:
          self.label = "TwoProngModified"

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
        self.out.branch("n"+self.label+"", "I")
        self.out.branch(""+self.label+"_pt", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_eta", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_phi", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_mass", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_massl", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_massPi0", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_massEta", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHpos_pt", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHpos_eta", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHpos_phi", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHpos_mass", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHneg_pt", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHneg_eta", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHneg_phi", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_CHneg_mass", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_neutral_pt", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_neutral_eta", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_neutral_phi", "F", lenVar="n"+self.label+"")
        self.out.branch(""+self.label+"_neutral_mass", "F", lenVar="n"+self.label+"")
        if self.optionalTrack:
          self.out.branch(""+self.label+"Modified_nTracks", "I", lenVar="n"+self.label+"Modified")
          self.out.branch(""+self.label+"Modified_CHextra_pt", "F", lenVar="n"+self.label+"Modified")
          self.out.branch(""+self.label+"Modified_CHextra_eta", "F", lenVar="n"+self.label+"Modified")
          self.out.branch(""+self.label+"Modified_CHextra_phi", "F", lenVar="n"+self.label+"Modified")
          self.out.branch(""+self.label+"Modified_CHextra_mass", "F", lenVar="n"+self.label+"Modified")
          self.out.branch(""+self.label+"Modified_CHextra_charge", "F", lenVar="n"+self.label+"Modified")
        if self.addLoose:
          self.out.branch(""+self.label+"_chargedIso", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_neutralIso", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_egammaIso", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_trackSym", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_photonSym", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_passIso", "I", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_passSym", "I", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_isTight", "I", lenVar="n"+self.label+"")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        pfcands = Collection(event, "PFCands")

        # per event vectors
        TwoProng_pt = []
        TwoProng_eta = []
        TwoProng_phi = []
        TwoProng_mass = []
        TwoProng_massl = []
        TwoProng_massPi0 = []
        TwoProng_massEta = []
        TwoProng_CHpos_pt = []
        TwoProng_CHpos_eta = []
        TwoProng_CHpos_phi = []
        TwoProng_CHpos_mass = []
        TwoProng_CHneg_pt = []
        TwoProng_CHneg_eta = []
        TwoProng_CHneg_phi = []
        TwoProng_CHneg_mass = []
        TwoProng_neutral_pt = []
        TwoProng_neutral_eta = []
        TwoProng_neutral_phi = []
        TwoProng_neutral_mass = []
        if self.optionalTrack:
          TwoProng_nTracks = []
          TwoProng_CHextra_pt = []
          TwoProng_CHextra_eta = []
          TwoProng_CHextra_phi = []
          TwoProng_CHextra_mass = []
          TwoProng_CHextra_charge = []
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
            extraTrackIndex = -1
            for k in range(len(pfcands)):
              pfvec3 = pfcands[k].p4()
              pfvec3.SetPhi(pfcands[k].phiAtVtx)
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
              extraTrack.SetPhi(pfcands[extraTrackIndex].phiAtVtx)
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
            #
            pfvec2 = pfcands[j].p4()
            pfvec2.SetPhi(pfcands[j].phiAtVtx)
            if (pfcands[i].pdgId == 211):
              chpos = pfvec1
              chneg = pfvec2
            else:
              chpos = pfvec2
              chneg = pfvec1
            neutral = photon
            # finished, store
            TwoProng_pt.append(twoprong.Pt())
            TwoProng_phi.append(twoprong.Phi())
            TwoProng_eta.append(twoprong.Eta())
            TwoProng_mass.append(twoprong.M())
            TwoProng_massl.append((center+leading_pf_photon).M())
            TwoProng_massPi0.append((center+photonPi0).M())
            TwoProng_massEta.append((center+photonEta).M())
            TwoProng_CHpos_pt.append(chpos.Pt())
            TwoProng_CHpos_eta.append(chpos.Eta())
            TwoProng_CHpos_phi.append(chpos.Phi())
            TwoProng_CHpos_mass.append(chpos.M())
            TwoProng_CHneg_pt.append(chneg.Pt())
            TwoProng_CHneg_eta.append(chneg.Eta())
            TwoProng_CHneg_phi.append(chneg.Phi())
            TwoProng_CHneg_mass.append(chneg.M())
            TwoProng_neutral_pt.append(neutral.Pt())
            TwoProng_neutral_eta.append(neutral.Eta())
            TwoProng_neutral_phi.append(neutral.Phi())
            TwoProng_neutral_mass.append(neutral.M())
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
              if extraTrackIndex == -1:
                TwoProng_nTracks.append(2)
                TwoProng_CHextra_pt.append(-1000.0)
                TwoProng_CHextra_eta.append(-1000.0)
                TwoProng_CHextra_phi.append(-1000.0)
                TwoProng_CHextra_mass.append(-1000.0)
                TwoProng_CHextra_charge.append(1000.0)
              else:
                chextra = extraTrack
                TwoProng_nTracks.append(3)
                TwoProng_CHextra_pt.append(chextra.Pt())
                TwoProng_CHextra_eta.append(chextra.Eta())
                TwoProng_CHextra_phi.append(chextra.Phi())
                TwoProng_CHextra_mass.append(chextra.M())
                TwoProng_CHextra_charge.append(pfcands[extraTrackIndex].charge)
        # loop over pfcands finished

        # sort twoprong collections
        if len(TwoProng_pt)>1:
          twoprong_branches = [
            TwoProng_eta,
            TwoProng_phi,
            TwoProng_mass,
            TwoProng_massl,
            TwoProng_massPi0,
            TwoProng_massEta,
            TwoProng_CHpos_pt,
            TwoProng_CHpos_eta,
            TwoProng_CHpos_phi,
            TwoProng_CHpos_mass,
            TwoProng_CHneg_pt,
            TwoProng_CHneg_eta,
            TwoProng_CHneg_phi,
            TwoProng_CHneg_mass,
            TwoProng_neutral_pt,
            TwoProng_neutral_eta,
            TwoProng_neutral_phi,
            TwoProng_neutral_mass,
          ]
          if self.addLoose: twoprong_branches.extend([
            TwoProng_chargedIso,
            TwoProng_neutralIso,
            TwoProng_egammaIso,
            TwoProng_trackSym,
            TwoProng_photonSym,
            TwoProng_passIso,
            TwoProng_passSym,
            TwoProng_isTight,
          ])
          if self.optionalTrack: twoprong_branches.extend([
            TwoProng_nTracks,
            TwoProng_CHextra_pt,
            TwoProng_CHextra_eta,
            TwoProng_CHextra_phi,
            TwoProng_CHextra_mass,
            TwoProng_CHextra_charge,
          ])
          for branch in twoprong_branches:
              lookup = dict(( (el, TwoProng_pt[branch.index(el)]) for el in branch))
              branch.sort(key = lookup.__getitem__, reverse=True)
          TwoProng_pt.sort(reverse=True)

        # fill branches
        nTwoProng = len(TwoProng_pt)
        self.out.fillBranch("n"+self.label+"", nTwoProng)
        self.out.fillBranch(""+self.label+"_pt", TwoProng_pt)
        self.out.fillBranch(""+self.label+"_eta", TwoProng_eta)
        self.out.fillBranch(""+self.label+"_phi", TwoProng_phi)
        self.out.fillBranch(""+self.label+"_mass", TwoProng_mass)
        self.out.fillBranch(""+self.label+"_massl", TwoProng_massl)
        self.out.fillBranch(""+self.label+"_massPi0", TwoProng_massPi0)
        self.out.fillBranch(""+self.label+"_massEta", TwoProng_massEta)
        self.out.fillBranch(""+self.label+"_CHpos_pt", TwoProng_CHpos_pt)
        self.out.fillBranch(""+self.label+"_CHpos_eta", TwoProng_CHpos_eta)
        self.out.fillBranch(""+self.label+"_CHpos_phi", TwoProng_CHpos_phi)
        self.out.fillBranch(""+self.label+"_CHpos_mass", TwoProng_CHpos_mass)
        self.out.fillBranch(""+self.label+"_CHneg_pt", TwoProng_CHneg_pt)
        self.out.fillBranch(""+self.label+"_CHneg_eta", TwoProng_CHneg_eta)
        self.out.fillBranch(""+self.label+"_CHneg_phi", TwoProng_CHneg_phi)
        self.out.fillBranch(""+self.label+"_CHneg_mass", TwoProng_CHneg_mass)
        self.out.fillBranch(""+self.label+"_neutral_pt", TwoProng_neutral_pt)
        self.out.fillBranch(""+self.label+"_neutral_eta", TwoProng_neutral_eta)
        self.out.fillBranch(""+self.label+"_neutral_phi", TwoProng_neutral_phi)
        self.out.fillBranch(""+self.label+"_neutral_mass", TwoProng_neutral_mass)
        if self.optionalTrack:
          self.out.fillBranch(""+self.label+"_nTracks", TwoProng_nTracks)
          self.out.fillBranch(""+self.label+"_CHextra_pt", TwoProng_CHextra_pt)
          self.out.fillBranch(""+self.label+"_CHextra_eta", TwoProng_CHextra_eta)
          self.out.fillBranch(""+self.label+"_CHextra_phi", TwoProng_CHextra_phi)
          self.out.fillBranch(""+self.label+"_CHextra_mass", TwoProng_CHextra_mass)
          self.out.fillBranch(""+self.label+"_CHextra_charge", TwoProng_CHextra_charge)
        if self.addLoose:
          self.out.fillBranch(""+self.label+"_chargedIso", TwoProng_chargedIso)
          self.out.fillBranch(""+self.label+"_neutralIso", TwoProng_neutralIso)
          self.out.fillBranch(""+self.label+"_egammaIso", TwoProng_egammaIso)
          self.out.fillBranch(""+self.label+"_trackSym", TwoProng_trackSym)
          self.out.fillBranch(""+self.label+"_photonSym", TwoProng_photonSym)
          self.out.fillBranch(""+self.label+"_passIso", TwoProng_passIso)
          self.out.fillBranch(""+self.label+"_passSym", TwoProng_passSym)
          self.out.fillBranch(""+self.label+"_isTight", TwoProng_isTight)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

twoprongConstr_default = lambda: twoprongModule()
twoprongConstr_addLoose = lambda: twoprongModule(addLoose=True)
twoprongConstr_optionalTrack = lambda: twoprongModule(optionalTrack=True)
twoprongConstr_optionalTrack_addLoose = lambda: twoprongModule(optionalTrack=True, addLoose=True)
