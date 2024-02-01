#!/usr/bin/env python

import ROOT
import os
import glob
import argparse
import hashlib
from DataFormats.FWLite import Events, Handle
 
class DiffSummary(object):
    def __init__(self):
        self.min_diff_value = 0.0001
        self.vars_ = {}
        self.user_floats = {}
        self.user_ints = {}
        self.ids = {}
        self.nrtot = 0
        self.nrdiff = 0
        self.nrnotfound = 0
        self.interactive = False

    def create_hist(self,var,diff_data,nrbins=100,xmin=None,xmax=None):
        diff_vals = [x['diff'] for x in diff_data]
        if xmin==None:
            xmin = min(diff_vals)
        if xmax==None:
            xmax = max(diff_vals)+0.0001
        hist = ROOT.TH1D("{}DiffHist".format(var),";#Delta{}".format(var),nrbins,xmin,xmax)
        for val in diff_vals:
            hist.Fill(val)
        return hist

    def _make_varsdiff_summary(self,vars_data,out_dir,out_tag):
        diff_strs = []
        for var,diff_data in vars_data.iteritems():
            
            canvas = ROOT.TCanvas()
            canvas.SetLogy()
            hist = self.create_hist(var,diff_data)
            hist.Draw()
            out_name = "{}_{}.png".format(out_tag,var)
            canvas.Print("{}/{}".format(out_dir,out_name))
            diff_strs.append("   var {} has {} differences<br>".format(var,len(diff_data)))
            diff_strs.append("<a href={pngfile}><img class=\"image\" width=\"500\" src={pngfile} ALIGH=TOP></a><br>".format(pngfile=out_name))
            if self.interactive:
                raw_input("press any key to continue...")
        return diff_strs

    def create_summary(self,out_dir,out_tag=""):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        diff_strs = []

        diff_strs.append("#total {s.nrtot}, not found {s.nrnotfound}, diff {s.nrdiff}".format(s=self))
        diff_strs.extend(self._make_varsdiff_summary(self.vars_,out_dir,out_tag))
        diff_strs.extend(self._make_varsdiff_summary(self.user_floats,out_dir,out_tag))
        diff_strs.extend(self._make_varsdiff_summary(self.user_ints,out_dir,out_tag))
        diff_strs.extend(self._make_varsdiff_summary(self.ids,out_dir,out_tag))

        return "\n".join(diff_strs)

class EleDiffSummary(DiffSummary):
    _vars_to_check = ["et","eta","phi","pfIsolationVariables.sumChargedHadronPt","pfIsolationVariables.sumNeutralHadronEt","pfIsolationVariables.sumPhotonEt","pfIsolationVariables.sumChargedParticlePt","pfIsolationVariables.sumNeutralHadronEtHighThreshold","pfIsolationVariables.sumPhotonEtHighThreshold","pfIsolationVariables.sumPUPt","scPixCharge","isGsfCtfScPixChargeConsistent","isGsfScPixChargeConsistent","isGsfCtfChargeConsistent","isElectron","ctfGsfOverlap","ecalDrivenSeed","trackerDrivenSeed","shFracInnerHits","eSuperClusterOverP","eSeedClusterOverP","eSeedClusterOverPout","eEleClusterOverPout","deltaEtaSuperClusterTrackAtVtx","deltaEtaSeedClusterTrackAtCalo","deltaEtaEleClusterTrackAtCalo","deltaPhiSuperClusterTrackAtVtx","deltaPhiSeedClusterTrackAtCalo","deltaPhiEleClusterTrackAtCalo","deltaEtaSeedClusterTrackAtVtx","basicClustersSize","isEB","isEE","isGap","isEBEEGap","isEBGap","isEBEtaGap","isEBPhiGap","isEEGap","isEEDeeGap","isEERingGap","sigmaEtaEta","sigmaIetaIeta","sigmaIphiIphi","e1x5","e2x5Max","e5x5","r9","hcalDepth1OverEcal","hcalDepth2OverEcal","hcalOverEcal","hcalDepth1OverEcalBc","hcalDepth2OverEcalBc","hcalOverEcalBc","eLeft","eRight","eTop","eBottom","full5x5_sigmaEtaEta","full5x5_sigmaIetaIeta","full5x5_sigmaIphiIphi","full5x5_e1x5","full5x5_e2x5Max","full5x5_e5x5","full5x5_r9","full5x5_hcalDepth1OverEcal","full5x5_hcalDepth2OverEcal","full5x5_hcalOverEcal","full5x5_hcalDepth1OverEcalBc","full5x5_hcalDepth2OverEcalBc","full5x5_hcalOverEcalBc","full5x5_eLeft","full5x5_eRight","full5x5_eTop","full5x5_eBottom","scSigmaEtaEta","scSigmaIEtaIEta","scE1x5","scE2x5Max","scE5x5","hadronicOverEm","hadronicOverEm1","hadronicOverEm2","nSaturatedXtals","isSeedSaturated","dr03TkSumPt","dr03EcalRecHitSumEt","dr03HcalDepth1TowerSumEt","dr03HcalDepth2TowerSumEt","dr03HcalTowerSumEt","dr03HcalDepth1TowerSumEtBc","dr03HcalDepth2TowerSumEtBc","dr03HcalTowerSumEtBc","dr04TkSumPt","dr04EcalRecHitSumEt","dr04HcalDepth1TowerSumEt","dr04HcalDepth2TowerSumEt","dr04HcalTowerSumEt","dr04HcalDepth1TowerSumEtBc","dr04HcalDepth2TowerSumEtBc","dr04HcalTowerSumEtBc","convFlags","convDist","convDcot","convRadius","mva_Isolated","mva_e_pi","ecalDriven","passingCutBasedPreselection","passingPflowPreselection","ambiguous","passingMvaPreselection","trackFbrem","superClusterFbrem","numberOfBrems","fbrem","isEcalEnergyCorrected","correctedEcalEnergy","correctedEcalEnergyError","trackMomentumError","ecalEnergy","ecalEnergyError","caloEnergy","isEnergyScaleCorrected","pixelMatchSubdetector1","pixelMatchSubdetector2","pixelMatchDPhi1","pixelMatchDPhi2","pixelMatchDRz1","pixelMatchDRz2","full5x5_e2x5Left","full5x5_e2x5Right","full5x5_e2x5Top","full5x5_e2x5Bottom"]


    def add_diff(self,diffs,name,ele,val,diff_val):
        if name not in diffs: 
            diffs[name]=[]    
        diffs[name].append({'et' : ele.et(), 'eta' : ele.eta(), 'phi' : ele.phi() , 'val' : val,'diff' : diff_val})

    def fill(self,ele1,ele2):   
        self.nrtot +=1
        if ele2 == None:
            print "ele ",ele.et(),ele.eta(),ele.phi(),"not found"
            self.nrnotfound +=1
            return True

        diff = False
        for name in ele1.userFloatNames():
            vars_to_skip = ["ecalTrkEnergyErrPostCorr","ecalTrkEnergyPostCorr","energyScaleDown","energyScaleGainDown","energyScaleGainUp","energyScaleStatDown","energyScaleStatUp","energyScaleSystDown","energyScaleSystUp","energyScaleUp","energySigmaDown","energySigmaPhiDown","energySigmaPhiUp","energySigmaRhoDown","energySigmaRhoUp","energySigmaUp"]
            vars_to_skip =[]
            if name in vars_to_skip: continue
        
            if name not in ele2.userFloatNames(): continue
            diff_val = ele1.userFloat(name)-ele2.userFloat(name)
            if abs(diff_val)>self.min_diff_value:
                self.add_diff(self.user_floats,name,ele1,ele1.userFloat(name),diff_val)
                diff = True
        
        for name in ele1.userIntNames():
            if name not in ele2.userIntNames(): continue
            if ele1.userInt(name)!=ele2.userInt(name):               
                self.add_diff(self.user_ints,name,ele1,ele1.userInt(name),ele1.userInt(name)-ele2.userInt(name))
                diff = True

        for var in EleDiffSummary._vars_to_check:
            if var.find(".")==-1:
                val1 = getattr(ele1,var)()
                val2 = getattr(ele2,var)()
            else:
                var_split = var.split(".")
                if len(var_split)>2:
                    raise Exception("EgammaPostRecoTools:warning var {} has more than two layers, only a single . is supported".format(var))
                val1 = getattr(getattr(ele1,var_split[0])(),var_split[1])
                val2 = getattr(getattr(ele2,var_split[0])(),var_split[1])
                
            diff_val = val1-val2
            if abs(diff_val)>self.min_diff_value:
                self.add_diff(self.vars_,var,ele1,val1,diff_val)
                diff = True

        for ele_id in ele1.electronIDs():
            if ele2.isElectronIDAvailable(ele_id.first)==False: continue
            if ele_id.second != ele2.electronID(ele_id.first):
                self.add_diff(self.ids,ele_id.first,ele1,ele_id.second,ele_id.second-ele2.electronID(ele_id.first))
                diff = True

        if diff:
            self.nrdiff +=1
        return diff
        

class PhoDiffSummary(DiffSummary):
    _vars_to_check = ["et","energy","eta","phi"]

    def add_diff(self,diffs,name,pho,val,diff_val):
        if name not in diffs: 
            diffs[name]=[]    
        diffs[name].append({'et' : pho.et(), 'eta' : pho.eta(), 'phi' : pho.phi() , 'val' : val,'diff' : diff_val})

    def fill(self,pho1,pho2):   
        self.nrtot +=1
        if pho2 == None:
            print "pho ",pho.et(),pho.eta(),pho.phi(),"not found"
            self.nrnotfound +=1
            return True

        diff = False
        for name in pho1.userFloatNames():
            vars_to_skip =[]
            if name in vars_to_skip: continue
        
            if name not in pho2.userFloatNames(): continue
            diff_val = pho1.userFloat(name)-pho2.userFloat(name)
            if abs(diff_val)>self.min_diff_value:
                self.add_diff(self.user_floats,name,pho1,pho1.userFloat(name),diff_val)
                diff = True
        
        for name in pho1.userIntNames():
            if name not in pho2.userIntNames(): continue
            if pho1.userInt(name)!=pho2.userInt(name):               
                self.add_diff(self.user_ints,name,pho1,pho1.userInt(name),pho1.userInt(name)-pho2.userInt(name))
                diff = True


        for var in PhoDiffSummary._vars_to_check:         
            if var.find(".")==-1:
                val1 = getattr(pho1,var)()
                val2 = getattr(pho2,var)()
            else:
                var_split = var.split(".")
                if len(var_split)>2:
                    raise Exception("EgammaPostRecoTools:warning var {} has more than two layers, only a single . is supported".format(var))
                val1 = getattr(getattr(pho1,var_split[0])(),var_split[1])
                val2 = getattr(getattr(pho2,var_split[0])(),var_split[1])

            diff_val = val1 - val2
            if abs(diff_val)>self.min_diff_value:
                self.add_diff(self.vars_,var,pho1,val1,diff_val)
                diff = True

        for pho_id in pho1.photonIDs():
            if pho2.isPhotonIDAvailable(pho_id.first)==False: continue
            if pho_id.second != pho2.photonID(pho_id.first):
                print "diff pho {:.1f}, {:.2f}, {:.2f} : ID".format(pho1.et(),pho1.eta(),pho1.phi()),pho_id.first,pho_id.second,pho2.photonID(pho_id.first)
                self.add_diff(self.ids,pho_id.first,pho1,pho_id.second,pho_id.second-pho2.photonID(pho_id.first))
                diff = True

        if diff:
            self.nrdiff +=1
        return diff



def match_by_sc(obj,objs_to_match):
    if not obj.superCluster().isAvailable(): return None
    
    for obj_to_match in objs_to_match:
        if obj_to_match.superCluster().isAvailable():
            if obj.superCluster().seed().seed().rawId()== obj_to_match.superCluster().seed().seed().rawId():
                return obj_to_match
    return None



def compare(target_file,ref_file,file_prefix="file:",out_dir="./"):

    ### Objects from file ###
    eles, ele_label = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
    eles_ref = Handle("std::vector<pat::Electron>")
    phos, pho_label = Handle("std::vector<pat::Photon>"), "slimmedPhotons"
    phos_ref = Handle("std::vector<pat::Photon>")
    ### Events loop ###

    min_pho_et = 10
    min_ele_et = 5
    do_phos=True
    do_eles=True

    evtLUT = {}

    events_ref = Events(file_prefix+ref_file)
    for event_nr,event in enumerate(events_ref):
        runnr = event.eventAuxiliary().run()
        eventnr = event.eventAuxiliary().event()
        lumi = event.eventAuxiliary().luminosityBlock()
        if runnr not in evtLUT:
            evtLUT[runnr]={}
        if lumi not in evtLUT[runnr]:
            evtLUT[runnr][lumi]={}
        evtLUT[runnr][lumi][eventnr]=event_nr

    events = Events(file_prefix+target_file)
    
    ele_diffs = EleDiffSummary()
    pho_diffs = PhoDiffSummary()

    for event_nr,event in enumerate(events):
        runnr = event.eventAuxiliary().run()
        eventnr = event.eventAuxiliary().event()
        lumi = event.eventAuxiliary().luminosityBlock()
        event_found = events_ref.to(evtLUT[runnr][lumi][eventnr])
 
        event_id=str(event.eventAuxiliary().run())+":"+str(event.eventAuxiliary().luminosityBlock())+":"+str(event.eventAuxiliary().event())

        if do_phos:
            event.getByLabel(pho_label,phos)
            events_ref.getByLabel(pho_label,phos_ref)
    
            for pho_nr,pho in enumerate(phos.product()):  
                if pho.et()<min_pho_et: continue
                pho_ref = match_by_sc(pho,phos_ref.product())
                pho_diffs.fill(pho,pho_ref)
            

        if do_eles:
            event.getByLabel(ele_label,eles)
            events_ref.getByLabel(ele_label,eles_ref) 
    
            for ele_nr,ele in enumerate(eles.product()):
                if ele.et()<min_ele_et: continue
                ele_ref = match_by_sc(ele,eles_ref.product())
                ele_diffs.fill(ele,ele_ref)

    target_path_file = os.path.split(target_file)
    ref_path_file = os.path.split(ref_file)

    hashstr = hashlib.md5(target_file).hexdigest()
    out_tag_phos = "pho_{}".format(hashstr)
    out_tag_eles = "ele_{}".format(hashstr)


    comp_strs = []
    comp_strs.append("<br><br>file = {}<br>".format(target_path_file[1]))
    comp_strs.append("target dir = {}<br>".format(target_path_file[0]))
    comp_strs.append("reference dir = {}<br>".format(ref_path_file[0]))
    comp_strs.append("Photons<br>")
    comp_strs.append(pho_diffs.create_summary(out_dir,out_tag_phos))
    comp_strs.append("Electrons<br>")
    comp_strs.append(ele_diffs.create_summary(out_dir,out_tag_eles))
    #    pho_diffs.create_summary(out_dir)
    return '\n'.join(comp_strs)


def main():
    
    import sys
    oldargv = sys.argv[:]
    sys.argv = [ '-b-' ]
    import ROOT
 #   ROOT.gROOT.SetBatch(True)
    sys.argv = oldargv
    ROOT.gSystem.Load("libFWCoreFWLite.so");
    ROOT.gSystem.Load("libDataFormatsFWLite.so");
    ROOT.FWLiteEnabler.enable()
    
    verbose=False


    import argparse
    
    parser = argparse.ArgumentParser(description='compares E/gamma pat::Electrons/Photons')
    parser.add_argument('--ref',help='ref filename',required=True)
    parser.add_argument('--target',help='target filename',required=True)
    parser.add_argument('--prefix',help='file prefex',default="file:")
    parser.add_argument('--out_dir',help='output file for validation webpage',default="./validation_results")
    args = parser.parse_args()

    target_refs = []
    if not os.path.exists(args.target) or os.path.isdir(args.target):
        if os.path.isdir(args.target):
            pattern = "{}/*MINIAOD*EDM.root".format(args.target)
        else:
            pattern = args.target
        
        for target_file in glob.glob(pattern):
            ref_file = "{}/{}".format(args.ref,target_file.split("/")[-1])
            if os.path.isfile(ref_file):
                target_refs.append({'target' : target_file,'ref' : ref_file})
            else:
                print "error reference for {} not found in {}".format(target_file,args.ref)

    #if no pattern match, then we just put the orginal pattern in the files to run
    if not target_refs:
        target_refs.append({'target' : args.target, 'ref' : args.ref})

    file_prefix=args.prefix

    comp_results = []

    for tar_ref in target_refs:
        comp_results.append(compare(tar_ref['target'],tar_ref['ref'],file_prefix,args.out_dir))
        
    with open("{}/index.html".format(args.out_dir),'w') as f:
        f.write('\n'.join(comp_results))

if __name__ == "__main__":
    main()
