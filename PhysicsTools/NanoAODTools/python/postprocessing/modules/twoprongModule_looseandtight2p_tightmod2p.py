from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import numpy as np
import time

from twoprong_constants import *

#makes two collections:
#  TwoProng collection with tight 2p + loose sidebands
#  TwoProngModified collection with tight 3-pronged objects, if possible to construct them
class twoprongModule_looseandtight2p_tightmod2p(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nTwoProng",             "I")
        self.out.branch("TwoProng_pt",           "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_eta",          "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_phi",          "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_mass",         "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_massl",        "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_massPi0",      "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_massEta",      "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHpos_pt",     "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHpos_eta",    "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHpos_phi",    "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHpos_mass",   "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHneg_pt",     "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHneg_eta",    "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHneg_phi",    "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_CHneg_mass",   "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_neutral_pt",   "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_neutral_eta",  "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_neutral_phi",  "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_neutral_mass", "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_chargedIso",   "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_neutralIso",   "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_egammaIso",    "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_trackSym",     "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_photonSym",    "F", lenVar="nTwoProng")
        self.out.branch("TwoProng_passIso",      "I", lenVar="nTwoProng")
        self.out.branch("TwoProng_passSym",      "I", lenVar="nTwoProng")
        self.out.branch("TwoProng_isTight",      "I", lenVar="nTwoProng")

        self.out.branch("nTwoProngModified",               "I")
        self.out.branch("TwoProngModified_pt",             "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_eta",            "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_phi",            "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_mass",           "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_massl",          "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_massPi0",        "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_massEta",        "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHpos_pt",       "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHpos_eta",      "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHpos_phi",      "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHpos_mass",     "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHneg_pt",       "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHneg_eta",      "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHneg_phi",      "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHneg_mass",     "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_neutral_pt",     "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_neutral_eta",    "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_neutral_phi",    "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_neutral_mass",   "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_chargedIso",     "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_neutralIso",     "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_egammaIso",      "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_trackSym",       "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_photonSym",      "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_passIso",        "I", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_passSym",        "I", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_isTight",        "I", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_nTracks",        "I", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHextra_pt",     "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHextra_eta",    "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHextra_phi",    "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHextra_mass",   "F", lenVar="nTwoProngModified")
        self.out.branch("TwoProngModified_CHextra_charge", "F", lenVar="nTwoProngModified")
          
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        starttime=time.time()
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
        
        TwoProng_chargedIso = []
        TwoProng_neutralIso = []
        TwoProng_egammaIso = []
        TwoProng_trackSym = []
        TwoProng_photonSym = []
        TwoProng_passIso = []
        TwoProng_passSym = []
        TwoProng_isTight = []

        TwoProngModified_pt = []
        TwoProngModified_eta = []
        TwoProngModified_phi = []
        TwoProngModified_mass = []
        TwoProngModified_massl = []
        TwoProngModified_massPi0 = []
        TwoProngModified_massEta = []
        TwoProngModified_CHpos_pt = []
        TwoProngModified_CHpos_eta = []
        TwoProngModified_CHpos_phi = []
        TwoProngModified_CHpos_mass = []
        TwoProngModified_CHneg_pt = []
        TwoProngModified_CHneg_eta = []
        TwoProngModified_CHneg_phi = []
        TwoProngModified_CHneg_mass = []
        TwoProngModified_neutral_pt = []
        TwoProngModified_neutral_eta = []
        TwoProngModified_neutral_phi = []
        TwoProngModified_neutral_mass = []

        TwoProngModified_chargedIso = []
        TwoProngModified_neutralIso = []
        TwoProngModified_egammaIso = []
        TwoProngModified_trackSym = []
        TwoProngModified_photonSym = []
        TwoProngModified_passIso = []
        TwoProngModified_passSym = []
        TwoProngModified_isTight = []

        TwoProngModified_nTracks = []
        TwoProngModified_CHextra_pt = []
        TwoProngModified_CHextra_eta = []
        TwoProngModified_CHextra_phi = []
        TwoProngModified_CHextra_mass = []
        TwoProngModified_CHextra_charge = []

        filtered_pfcands = [ (i, pfcand) for i, pfcand in enumerate(pfcands) if (pfcand.fromPV > 1 and pfcand.pt >= const_minTrackPt and abs(pfcand.pdgId) == 211) ]
        filtered_photons = [ pfcand for pfcand in pfcands if (pfcand.pdgId == 22 or abs(pfcand.pdgId) == 11) ]
        photonPi0 = ROOT.TLorentzVector()
        photonEta = ROOT.TLorentzVector()
        
        # loop over pf cands
        for i, pfcand1 in filtered_pfcands:
          pfvec1 = pfcand1.p4()
          pfvec1.SetPhi(pfcand1.phiAtVtx)
          for j, pfcand2 in filtered_pfcands:
            if j <= i : continue
            # charged hadron pair
            if not ( (pfcands[i].pdgId == 211 and pfcands[j].pdgId == -211) or (pfcands[i].pdgId == -211 and pfcands[j].pdgId == 211) ) : continue
            pfvec2 = pfcand2.p4()
            pfvec2.SetPhi(pfcand2.phiAtVtx)
            if pfvec1.DeltaR(pfvec2) > const_maxTrackDr : continue
            center = pfvec1 + pfvec2

            # photons: photon box + e/gamma isolation
            photon = ROOT.TLorentzVector()
            leading_pf_photon = ROOT.TLorentzVector()
            egammaIso = 0
            for pfcand_photon in filtered_photons:
              pfvec3 = pfcand_photon.p4()
              pfvec3.SetPhi(pfcand_photon.phiAtVtx)
              if abs(center.DeltaPhi(pfvec3)) > const_photonBoxPhi/2.0 or abs(center.Eta() - pfvec3.Eta()) > const_photonBoxEta/2.0:
                #if e/gamma not in photon box, check if it contributes to the photon isolation
                if pfcand_photon.fromPV > 1 and center.DeltaR(pfvec3) <= const_isolationCone: #should pfcand_photon.fromPV >1 for everything in the photon box??-----------------------------------------
                  egammaIso += pfvec3.Pt()
                continue
              photon += pfvec3
              if pfvec3.Pt() > leading_pf_photon.Pt() : leading_pf_photon = pfvec3
            if photon.Pt() < const_photonMinPt : continue
            twoprong = center + photon
            photonPi0.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_pionMass)
            photonEta.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_etaMass)
            chpos, chneg = (pfvec1, pfvec2) if pfcands[i].pdgId == 211 else (pfvec2, pfvec1)
            neutral = photon

            # extra track search + isolation calc (except egamma iso which is calculated earlier)
            chargedIso = 0
            modifiedchargedIso = 0
            neutralIso = 0
            extraTrackIndex = -1
            filtered_iso_candidates = [ (k, pfcand) for k, pfcand in enumerate(pfcands) if (pfcand.fromPV > 1 and center.DeltaR(pfcand.p4()) <= const_isolationCone) ]
            for k, pfcand_iso in filtered_iso_candidates:
              pfvec3 = pfcand_iso.p4()
              pfvec3.SetPhi(pfcand_iso.phiAtVtx)
              if pfcands[k].pdgId == 130:
                neutralIso += pfvec3.Pt()
              elif abs(pfcand_iso.pdgId) in [211, 13]:
                if k == i or k == j : continue
                chargedIso += pfvec3.Pt()
                if extraTrackIndex == -1 and pfvec3.Pt() > const_minTrackPt:
                  extraTrackIndex = k
                  continue
                modifiedchargedIso+=pfvec3.Pt() #same as normal charged iso, except it doesn't include the extra track
            passIso =  (chargedIso / twoprong.Pt() < const_chargedIsoCut) and (neutralIso / twoprong.Pt() < const_neutralIsoCut) and (egammaIso / twoprong.Pt() < const_egammaIsoCut)
            
            # include extra track in modified twoprong; for these, cut on pt and eta, calc and cut on iso and sym, then save
            if extraTrackIndex != -1:
              extraTrack = pfcands[extraTrackIndex].p4()
              extraTrack.SetPhi(pfcands[extraTrackIndex].phiAtVtx)
              modifiedtwoprong = center + photon + extraTrack
              if (modifiedtwoprong.Pt() < const_minPt): continue #if modified 2p doesn't pass pt cut, normal 2p won't either; skip to next 2p candidate
              if abs(modifiedtwoprong.Eta()) < const_maxEta:
                modifiedpassIso = (modifiedchargedIso / modifiedtwoprong.Pt() < const_chargedIsoCut) and (neutralIso / modifiedtwoprong.Pt() < const_neutralIsoCut) and (egammaIso / modifiedtwoprong.Pt() < const_egammaIsoCut)
                if modifiedpassIso:
                  track_symmetry = min(pfvec1.Pt(), pfvec2.Pt()) / max(pfvec1.Pt(), pfvec2.Pt())
                  photon_symmetry = min(pfvec1.Pt()+pfvec2.Pt(), photon.Pt()) / max(pfvec1.Pt()+pfvec2.Pt(), photon.Pt())
                  passSym = (track_symmetry > const_minTrackSymmetry) and (photon_symmetry > const_minPhotonSymmetry)
                  if passSym:
                    TwoProngModified_pt.append(modifiedtwoprong.Pt())
                    TwoProngModified_phi.append(modifiedtwoprong.Phi())
                    TwoProngModified_eta.append(modifiedtwoprong.Eta())
                    TwoProngModified_mass.append(modifiedtwoprong.M())
                    TwoProngModified_massl.append((center+extraTrack+leading_pf_photon).M())
                    TwoProngModified_massPi0.append((center+extraTrack+photonPi0).M())
                    TwoProngModified_massEta.append((center+extraTrack+photonEta).M())
                    TwoProngModified_CHpos_pt.append(chpos.Pt())
                    TwoProngModified_CHpos_eta.append(chpos.Eta())
                    TwoProngModified_CHpos_phi.append(chpos.Phi())
                    TwoProngModified_CHpos_mass.append(chpos.M())
                    TwoProngModified_CHneg_pt.append(chneg.Pt())
                    TwoProngModified_CHneg_eta.append(chneg.Eta())
                    TwoProngModified_CHneg_phi.append(chneg.Phi())
                    TwoProngModified_CHneg_mass.append(chneg.M())
                    TwoProngModified_neutral_pt.append(neutral.Pt())
                    TwoProngModified_neutral_eta.append(neutral.Eta())
                    TwoProngModified_neutral_phi.append(neutral.Phi())
                    TwoProngModified_neutral_mass.append(neutral.M())
                    TwoProngModified_chargedIso.append(modifiedchargedIso/modifiedtwoprong.Pt())
                    TwoProngModified_neutralIso.append(neutralIso/modifiedtwoprong.Pt())
                    TwoProngModified_egammaIso.append(egammaIso/modifiedtwoprong.Pt())
                    TwoProngModified_trackSym.append(track_symmetry)
                    TwoProngModified_photonSym.append(photon_symmetry)
                    TwoProngModified_passIso.append(modifiedpassIso)
                    TwoProngModified_passSym.append(passSym)
                    TwoProngModified_isTight.append(modifiedpassIso and passSym)
                    chextra = extraTrack
                    TwoProngModified_nTracks.append(3)
                    TwoProngModified_CHextra_pt.append(chextra.Pt())
                    TwoProngModified_CHextra_eta.append(chextra.Eta())
                    TwoProngModified_CHextra_phi.append(chextra.Phi())
                    TwoProngModified_CHextra_mass.append(chextra.M())
                    TwoProngModified_CHextra_charge.append(pfcands[extraTrackIndex].charge)

            #proceed with operations for all (unmodified) 2p
            if (twoprong.Pt() < const_minPt) or (abs(twoprong.Eta()) > const_maxEta) : continue            

            # symmetry
            track_symmetry = min(pfvec1.Pt(), pfvec2.Pt()) / max(pfvec1.Pt(), pfvec2.Pt())
            photon_symmetry = min(pfvec1.Pt()+pfvec2.Pt(), photon.Pt()) / max(pfvec1.Pt()+pfvec2.Pt(), photon.Pt())
            passSym = (track_symmetry > const_minTrackSymmetry) and (photon_symmetry > const_minPhotonSymmetry)

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
            TwoProng_chargedIso.append(chargedIso/twoprong.Pt())
            TwoProng_neutralIso.append(neutralIso/twoprong.Pt())
            TwoProng_egammaIso.append(egammaIso/twoprong.Pt())
            TwoProng_trackSym.append(track_symmetry)
            TwoProng_photonSym.append(photon_symmetry)
            TwoProng_passIso.append(passIso)
            TwoProng_passSym.append(passSym)
            TwoProng_isTight.append(passIso and passSym)

            #fill twoprongmodified as well; implement iso, sym cuts
            if extraTrackIndex == -1 and passIso and passSym: 
              TwoProngModified_pt.append(twoprong.Pt())
              TwoProngModified_phi.append(twoprong.Phi())
              TwoProngModified_eta.append(twoprong.Eta())
              TwoProngModified_mass.append(twoprong.M())
              TwoProngModified_massl.append((center+leading_pf_photon).M())
              TwoProngModified_massPi0.append((center+photonPi0).M())
              TwoProngModified_massEta.append((center+photonEta).M())
              TwoProngModified_CHpos_pt.append(chpos.Pt())
              TwoProngModified_CHpos_eta.append(chpos.Eta())
              TwoProngModified_CHpos_phi.append(chpos.Phi())
              TwoProngModified_CHpos_mass.append(chpos.M())
              TwoProngModified_CHneg_pt.append(chneg.Pt())
              TwoProngModified_CHneg_eta.append(chneg.Eta())
              TwoProngModified_CHneg_phi.append(chneg.Phi())
              TwoProngModified_CHneg_mass.append(chneg.M())
              TwoProngModified_neutral_pt.append(neutral.Pt())
              TwoProngModified_neutral_eta.append(neutral.Eta())
              TwoProngModified_neutral_phi.append(neutral.Phi())
              TwoProngModified_neutral_mass.append(neutral.M())
              TwoProngModified_chargedIso.append(chargedIso/twoprong.Pt())
              TwoProngModified_neutralIso.append(neutralIso/twoprong.Pt())
              TwoProngModified_egammaIso.append(egammaIso/twoprong.Pt())
              TwoProngModified_trackSym.append(track_symmetry)
              TwoProngModified_photonSym.append(photon_symmetry)
              TwoProngModified_passIso.append(passIso)
              TwoProngModified_passSym.append(passSym)
              TwoProngModified_isTight.append(passIso and passSym)
              TwoProngModified_nTracks.append(2)
              TwoProngModified_CHextra_pt.append(-1000.0)
              TwoProngModified_CHextra_eta.append(-1000.0)
              TwoProngModified_CHextra_phi.append(-1000.0)
              TwoProngModified_CHextra_mass.append(-1000.0)
              TwoProngModified_CHextra_charge.append(1000.0)
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
            TwoProng_chargedIso,
            TwoProng_neutralIso,
            TwoProng_egammaIso,
            TwoProng_trackSym,
            TwoProng_photonSym,
            TwoProng_passIso,
            TwoProng_passSym,
            TwoProng_isTight,
          ]
          sorted_indices = np.argsort(TwoProng_pt)[::-1]
          #sorted_indices = sorted(range(len(TwoProng_pt)), key=lambda k: TwoProng_pt[k], reverse=True)
          # Apply the sorted indices to all branches
          for branch in twoprong_branches:
            branch[:] = np.array(branch)[sorted_indices]
            #branch[:] = [branch[i] for i in sorted_indices]


        if len(TwoProngModified_pt)>1:
          twoprong_branches = [
            TwoProngModified_eta,
            TwoProngModified_phi,
            TwoProngModified_mass,
            TwoProngModified_massl,
            TwoProngModified_massPi0,
            TwoProngModified_massEta,
            TwoProngModified_CHpos_pt,
            TwoProngModified_CHpos_eta,
            TwoProngModified_CHpos_phi,
            TwoProngModified_CHpos_mass,
            TwoProngModified_CHneg_pt,
            TwoProngModified_CHneg_eta,
            TwoProngModified_CHneg_phi,
            TwoProngModified_CHneg_mass,
            TwoProngModified_neutral_pt,
            TwoProngModified_neutral_eta,
            TwoProngModified_neutral_phi,
            TwoProngModified_neutral_mass,
            TwoProngModified_chargedIso,
            TwoProngModified_neutralIso,
            TwoProngModified_egammaIso,
            TwoProngModified_trackSym,
            TwoProngModified_photonSym,
            TwoProngModified_passIso,
            TwoProngModified_passSym,
            TwoProngModified_isTight,
            TwoProngModified_nTracks,
            TwoProngModified_CHextra_pt,
            TwoProngModified_CHextra_eta,
            TwoProngModified_CHextra_phi,
            TwoProngModified_CHextra_mass,
            TwoProngModified_CHextra_charge,
          ]
          sorted_indices_mod = np.argsort(TwoProngModified_pt)[::-1]
          #sorted_indices = sorted(range(len(TwoProngModified_pt)), key=lambda k: TwoProngModified_pt[k], reverse=True)
          for branch in twoprong_branches:
            branch[:] = np.array(branch)[sorted_indices_mod]
            #branch[:] = [branch[i] for i in sorted_indices]

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
        self.out.fillBranch("TwoProng_CHpos_pt", TwoProng_CHpos_pt)
        self.out.fillBranch("TwoProng_CHpos_eta", TwoProng_CHpos_eta)
        self.out.fillBranch("TwoProng_CHpos_phi", TwoProng_CHpos_phi)
        self.out.fillBranch("TwoProng_CHpos_mass", TwoProng_CHpos_mass)
        self.out.fillBranch("TwoProng_CHneg_pt", TwoProng_CHneg_pt)
        self.out.fillBranch("TwoProng_CHneg_eta", TwoProng_CHneg_eta)
        self.out.fillBranch("TwoProng_CHneg_phi", TwoProng_CHneg_phi)
        self.out.fillBranch("TwoProng_CHneg_mass", TwoProng_CHneg_mass)
        self.out.fillBranch("TwoProng_neutral_pt", TwoProng_neutral_pt)
        self.out.fillBranch("TwoProng_neutral_eta", TwoProng_neutral_eta)
        self.out.fillBranch("TwoProng_neutral_phi", TwoProng_neutral_phi)
        self.out.fillBranch("TwoProng_neutral_mass", TwoProng_neutral_mass)
        self.out.fillBranch("TwoProng_chargedIso", TwoProng_chargedIso)
        self.out.fillBranch("TwoProng_neutralIso", TwoProng_neutralIso)
        self.out.fillBranch("TwoProng_egammaIso", TwoProng_egammaIso)
        self.out.fillBranch("TwoProng_trackSym", TwoProng_trackSym)
        self.out.fillBranch("TwoProng_photonSym", TwoProng_photonSym)
        self.out.fillBranch("TwoProng_passIso", TwoProng_passIso)
        self.out.fillBranch("TwoProng_passSym", TwoProng_passSym)
        self.out.fillBranch("TwoProng_isTight", TwoProng_isTight)
        nTwoProngModified = len(TwoProngModified_pt)
        self.out.fillBranch("nTwoProngModified", nTwoProngModified)
        self.out.fillBranch("TwoProngModified_pt", TwoProngModified_pt)
        self.out.fillBranch("TwoProngModified_eta", TwoProngModified_eta)
        self.out.fillBranch("TwoProngModified_phi", TwoProngModified_phi)
        self.out.fillBranch("TwoProngModified_mass", TwoProngModified_mass)
        self.out.fillBranch("TwoProngModified_massl", TwoProngModified_massl)
        self.out.fillBranch("TwoProngModified_massPi0", TwoProngModified_massPi0)
        self.out.fillBranch("TwoProngModified_massEta", TwoProngModified_massEta)
        self.out.fillBranch("TwoProngModified_CHpos_pt", TwoProngModified_CHpos_pt)
        self.out.fillBranch("TwoProngModified_CHpos_eta", TwoProngModified_CHpos_eta)
        self.out.fillBranch("TwoProngModified_CHpos_phi", TwoProngModified_CHpos_phi)
        self.out.fillBranch("TwoProngModified_CHpos_mass", TwoProngModified_CHpos_mass)
        self.out.fillBranch("TwoProngModified_CHneg_pt", TwoProngModified_CHneg_pt)
        self.out.fillBranch("TwoProngModified_CHneg_eta", TwoProngModified_CHneg_eta)
        self.out.fillBranch("TwoProngModified_CHneg_phi", TwoProngModified_CHneg_phi)
        self.out.fillBranch("TwoProngModified_CHneg_mass", TwoProngModified_CHneg_mass)
        self.out.fillBranch("TwoProngModified_neutral_pt", TwoProngModified_neutral_pt)
        self.out.fillBranch("TwoProngModified_neutral_eta", TwoProngModified_neutral_eta)
        self.out.fillBranch("TwoProngModified_neutral_phi", TwoProngModified_neutral_phi)
        self.out.fillBranch("TwoProngModified_neutral_mass", TwoProngModified_neutral_mass)
        self.out.fillBranch("TwoProngModified_chargedIso", TwoProngModified_chargedIso)
        self.out.fillBranch("TwoProngModified_neutralIso", TwoProngModified_neutralIso)
        self.out.fillBranch("TwoProngModified_egammaIso", TwoProngModified_egammaIso)
        self.out.fillBranch("TwoProngModified_trackSym", TwoProngModified_trackSym)
        self.out.fillBranch("TwoProngModified_photonSym", TwoProngModified_photonSym)
        self.out.fillBranch("TwoProngModified_passIso", TwoProngModified_passIso)
        self.out.fillBranch("TwoProngModified_passSym", TwoProngModified_passSym)
        self.out.fillBranch("TwoProngModified_isTight", TwoProngModified_isTight)
        self.out.fillBranch("TwoProngModified_nTracks", TwoProngModified_nTracks)
        self.out.fillBranch("TwoProngModified_CHextra_pt", TwoProngModified_CHextra_pt)
        self.out.fillBranch("TwoProngModified_CHextra_eta", TwoProngModified_CHextra_eta)
        self.out.fillBranch("TwoProngModified_CHextra_phi", TwoProngModified_CHextra_phi)
        self.out.fillBranch("TwoProngModified_CHextra_mass", TwoProngModified_CHextra_mass)
        self.out.fillBranch("TwoProngModified_CHextra_charge", TwoProngModified_CHextra_charge)
        endtime=time.time()
        elapsed=endtime-starttime
        print("Time taken for this event (seconds): ",elapsed)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
twoprongDataMCConstr_default = lambda: twoprongModule_looseandtight2p_tightmod2p()
