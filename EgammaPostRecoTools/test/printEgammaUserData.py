#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from DataFormats.FWLite import Events, Handle
import ROOT    
import argparse

def convert_to_str(vec_str):
    output = ""
    for entry in vec_str:
        if output != "": output+="\n  "
        output+=entry
    return output

def convertpair_to_str(vec_str):
    output = ""
    for entry in vec_str:
        if output != "": output+="\n  "
        output+=entry.first
    return output

def print_ele_user_data(ele):
    print("ele userfloats:")
    print("  "+convert_to_str(ele.userFloatNames()))
    print("ele userints:")
    print("  "+convert_to_str(ele.userIntNames()))
    print("ele IDs:")
    print("  "+convertpair_to_str(ele.electronIDs()))

def print_pho_user_data(pho):
    print("pho userfloats:")
    print("  "+convert_to_str(pho.userFloatNames()))
    print("pho userints:")
    print("  "+convert_to_str(pho.userIntNames()))
    print("pho IDs:")
    print("  "+convertpair_to_str(pho.photonIDs()))

if __name__ == "__main__":

    """
    prints electron and photon miniAOD user data
    
    note: it assumes that all electrons and photons have exactly the same userdata so we can just print 
    the first one. This is currently true except for low pt electrons and photons hence we put a >20 GeV
    cut on the ele/pho we print
    """
    ROOT.gSystem.Load("libFWCoreFWLite.so");
    ROOT.gSystem.Load("libDataFormatsFWLite.so");
    ROOT.FWLiteEnabler.enable()

    parser = argparse.ArgumentParser(description='prints E/gamma pat::Electrons/Photons user data')
    parser.add_argument('filename',help='input filename')
    args = parser.parse_args()
    
    eles, ele_label = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
    phos, pho_label = Handle("std::vector<pat::Photon>"), "slimmedPhotons"

    #we put a minimum et as low et electrons/photons may not have all the variables
    min_pho_et = 20
    min_ele_et = 20
    
    done_ele = False
    done_pho = False

    events = Events(args.filename)
    for event_nr,event in enumerate(events):
        if done_ele and done_pho: break
        
        if not done_pho:
            event.getByLabel(pho_label,phos)
    
            for pho_nr,pho in enumerate(phos.product()):  
                if pho.et()<min_pho_et: 
                    continue
                else:
                    print_pho_user_data(pho)
                    done_pho = True
                    break

        if not done_ele:
            event.getByLabel(ele_label,eles)            
            for ele_nr,ele in enumerate(eles.product()):
                if ele.et()<min_ele_et: 
                    continue
                else:
                    print_ele_user_data(ele)
                    done_ele = True
                    break
