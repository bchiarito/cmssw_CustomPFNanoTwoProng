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
        self.out.branch(""+self.label+"_neutral_nPFpho", "I", lenVar="nTwoProng")
        self.out.branch(""+self.label+"_neutral_nPFele", "I", lenVar="nTwoProng")
        self.out.branch(""+self.label+"_neutral_nPFpos", "I", lenVar="nTwoProng")
        if self.optionalTrack:
          self.out.branch(""+self.label+"_nTracks", "I", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_CHextra_pt", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_CHextra_eta", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_CHextra_phi", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_CHextra_mass", "F", lenVar="n"+self.label+"")
          self.out.branch(""+self.label+"_CHextra_charge", "F", lenVar="n"+self.label+"")
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
        TwoProng_neutral_nPFpho = []
        TwoProng_neutral_nPFele = []
        TwoProng_neutral_nPFpos = []
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

        filtered_pfcands = [ (i, pfcands[i]) for i in range(len(pfcands)) if (pfcands[i].fromPV > 1 and pfcands[i].pt >= const_minTrackPt and abs(pfcands[i].pdgId) == 211) ]
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
            passIso = True
            egammaIso = 0
            PFpho = 0
            PFele = 0
            PFpos = 0            
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
              pdg = pfcand_photon.pdgId
              if pdg==22: PFpho+=1
              elif pdg==11: PFpos+=1
              elif pdg==-11: PFele+=1              
            if photon.Pt() < const_photonMinPt : continue
            twoprong = center + photon
            if not self.optionalTrack: #for normal 2p, can now do pt and eta cuts
              if (twoprong.Pt() < const_minPt) or (math.fabs(twoprong.Eta()) > const_maxEta) : continue            
            # symmetry
            passSym = True
            track_symmetry = min(pfvec1.Pt(), pfvec2.Pt()) / max(pfvec1.Pt(), pfvec2.Pt())
            photon_symmetry = min(pfvec1.Pt()+pfvec2.Pt(), photon.Pt()) / max(pfvec1.Pt()+pfvec2.Pt(), photon.Pt())
            if track_symmetry < const_minTrackSymmetry or photon_symmetry < const_minPhotonSymmetry : passSym = False
            if not self.addLoose and not passSym : continue #if no sidebands, and not passing sym, we're done
            # extra track addition + isolation calc (except egamma iso which is calculated earlier)
            chargedIso = 0
            neutralIso = 0
            extraTrackIndex = -1
            extraTrackPt=0
            filtered_iso_candidates = [ (k, pfcand) for k, pfcand in enumerate(pfcands) if pfcand.fromPV > 1 and center.DeltaR(pfcand.p4()) <= const_isolationCone ]
            for k, pfcand_iso in filtered_iso_candidates:
              pfvec3 = pfcand_iso.p4()
              pfvec3.SetPhi(pfcand_iso.phiAtVtx)
              pfvec3_pt = pfvec3.Pt()
              if abs(pfcand_iso.pdgId) in [211, 13] and (k not in (i,j)):
                chargedIso += pfvec3_pt
                if self.optionalTrack and pfvec3_pt > const_minTrackPt and pfvec3_pt >extraTrackPt:
                  extraTrackIndex = k
                  extraTrackPt = pfvec3_pt
              elif pfcands[k].pdgId == 130:
                neutralIso += pfvec3_pt
            chargedIso = chargedIso - extraTrackPt
            if self.optionalTrack and extraTrackIndex != -1:
              # reform twoprong momentum with extra track
              extraTrack = pfcands[extraTrackIndex].p4()
              extraTrack.SetPhi(pfcands[extraTrackIndex].phiAtVtx)
              twoprong = center + photon + extraTrack
            if (chargedIso / twoprong.Pt() > const_chargedIsoCut) or (neutralIso / twoprong.Pt() > const_neutralIsoCut) or (egammaIso / twoprong.Pt() > const_egammaIsoCut): passIso = False
            if not self.addLoose and not passIso: continue                
            if self.optionalTrack:
              if (twoprong.Pt() < const_minPt) or (math.fabs(twoprong.Eta())) > const_maxEta : continue            
            photonPi0.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_pionMass)
            photonEta.SetPtEtaPhiM(photon.Pt(), photon.Eta(), photon.Phi(), const_etaMass)

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
            TwoProng_neutral_nPFpho.append(PFpho)
            TwoProng_neutral_nPFele.append(PFele)
            TwoProng_neutral_nPFpos.append(PFpos)
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
            TwoProng_pt,
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
            TwoProng_neutral_nPFpho,
            TwoProng_neutral_nPFele,
            TwoProng_neutral_nPFpos,          
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
          # Get sorted indices based on TwoProng_pt once
          sorted_indices = sorted(range(len(TwoProng_pt)), key=lambda k: TwoProng_pt[k], reverse=True)
          # Apply the sorted indices to all branches
          for branch in twoprong_branches:
              branch[:] = [branch[i] for i in sorted_indices]

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
        self.out.fillBranch(""+self.label+"_neutral_nPFpho", TwoProng_neutral_nPFpho)
        self.out.fillBranch(""+self.label+"_neutral_nPFele", TwoProng_neutral_nPFele)
        self.out.fillBranch(""+self.label+"_neutral_nPFpos", TwoProng_neutral_nPFpos)
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
