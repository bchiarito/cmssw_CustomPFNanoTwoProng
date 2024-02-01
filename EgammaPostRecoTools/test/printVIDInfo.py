#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDElectronIdProducer,switchOnVIDPhotonIdProducer,setupAllVIDIdsInModule,DataFormat,setupVIDElectronSelection,setupVIDPhotonSelection
import argparse

"""
A simple script which prints out the configuration of the electron/photon VID IDs
"""

def setupVID(process):

   #define the default IDs to produce in VID
    from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import _defaultEleIDModules,_defaultPhoIDModules
  
    #as we're not running, it doesnt matter if its miniAOD or AOD
    switchOnVIDElectronIdProducer(process,DataFormat.MiniAOD)
    switchOnVIDPhotonIdProducer(process,DataFormat.MiniAOD)
    
    eleIDModules = _defaultEleIDModules
    phoIDModules = _defaultPhoIDModules

    for idmod in eleIDModules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    for idmod in phoIDModules:
        setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

def convertPSetToValueDict(pset):
    """
    converts a CMSSW PSet to a dictionary of standard python types for easier python manipulation
    """
    psetDict={}
    for paraName,para in pset.parameters_().iteritems():
        if para.pythonTypeName()=="cms.VPSet":
            psetDict[paraName]=[convertPSetToValueDict(child) for child in para]
        elif para.pythonTypeName()=="cms.PSet":
            psetDict[paraName]=convertPSetToValueDict(para)
        else:
            psetDict[paraName]=para.value()
    return psetDict

def getCutDisplayName(cut):
    """
    a function which figures out the display name for a cut
    this exists to solve the problem where the photon cuts print as PhoGenericRhoPtScaledCut
    and its hard to figure out which its actually cutting on
    """
    cutName = cut.getParameter("cutName").value()
    if cutName=="PhoGenericRhoPtScaledCut":
        return "{}:{}".format(cutName,cut.getParameter("cutVariable").value())
    else:
        return str(cutName)   

def printMinPtCut(cutCfg,indent=6):
    print "{}Et > {} ".format(" "*indent,cutCfg.getParameter("minPt").value())

def printGsfEleSCEtaMultiRangeCut(cutCfg,indent=6):
    etaRanges = cutCfg.getParameter("allowedEtaRanges")
    outStr = " "*indent
    isAbs = cutCfg.getParameter("useAbsEta")
    if isAbs: etaStr = "|eta|"
    else: etaStr = "eta"
    for etaRangeNr, etaRange in enumerate(etaRanges):
        if etaRangeNr!=0: outStr+=" || "
        outStr += "{} < {} < {}".format(etaRange.getParameter("minEta").value(),etaStr,etaRange.getParameter("maxEta").value())
    print outStr
        
def printGsfEleDEtaInSeedCut(cutCfg,indent=6):
    print "{}|dEtaInSeed| < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("dEtaInSeedCutValueEB").value(),cutCfg.getParameter("dEtaInSeedCutValueEE").value())

def printGsfEleDPhiInCut(cutCfg,indent=6):
    print "{}|dPhiIn| < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("dPhiInCutValueEB").value(),cutCfg.getParameter("dPhiInCutValueEE").value())

def printGsfEleFull5x5SigmaIEtaIEtaCut(cutCfg,indent=6):
    print "{}sigma_ietaieta (full5x5) < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("full5x5SigmaIEtaIEtaCutValueEB").value(),cutCfg.getParameter("full5x5SigmaIEtaIEtaCutValueEE").value())

def printGsfEleFull5x5SigmaIEtaIEtaWithSatCut(cutCfg,indent=6):
    print "{}sigma_ietaieta (full5x5) < {} (EB), {} (EE) || #nr sat crystals > {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("maxSigmaIEtaIEtaEB").value(),cutCfg.getParameter("maxSigmaIEtaIEtaEE").value(),cutCfg.getParameter("maxNrSatCrysIn5x5EB").value(),cutCfg.getParameter("maxNrSatCrysIn5x5EE").value())

def printGsfEleFull5x5E2x5OverE5x5WithSatCut(cutCfg,indent=6):
    print "{}E2x5Max/E5x5 (full5x5) > {} (EB), {} (EE) || E1x5/E5x5 > {} (EB), {} (EE) || #nr sat crystals > {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("minE2x5OverE5x5EB").value(),cutCfg.getParameter("minE2x5OverE5x5EE").value(),cutCfg.getParameter("minE1x5OverE5x5EB").value(),cutCfg.getParameter("minE1x5OverE5x5EE").value(),cutCfg.getParameter("maxNrSatCrysIn5x5EB").value(),cutCfg.getParameter("maxNrSatCrysIn5x5EE").value())

def printGsfEleHadronicOverEMCut(cutCfg,indent=6):
    print "{}|H/E (cone=0.15) < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("hadronicOverEMCutValueEB").value(),cutCfg.getParameter("hadronicOverEMCutValueEE").value())

def printGsfEleHadronicOverEMEnergyScaledCut(cutCfg,indent=6):
    print "{}|H/E (cone=0.15) < {} + {}/Esc + {}*{}/Esc (EB)".format(" "*indent,cutCfg.getParameter("barrelC0").value(),cutCfg.getParameter("barrelCE").value(),cutCfg.getParameter("barrelCr").value(),cutCfg.getParameter("rho").value())
    print "{}|H/E (cone=0.15) < {} + {}/Esc + {}*{}/Esc (EE)".format(" "*indent,cutCfg.getParameter("endcapC0").value(),cutCfg.getParameter("endcapCE").value(),cutCfg.getParameter("endcapCr").value(),cutCfg.getParameter("rho").value())

def printGsfEleHadronicOverEMLinearCut(cutCfg,indent=6):
    cfgDict = convertPSetToValueDict(cutCfg)
    cfgDict['indent'] = " "*indent
    if cutCfg.slopeStartEB.value()==0.0:
        print "{indent}H/E (cone=0.15) < {slopeTermEB} - {constTermEB}/Esc (EB)".format(**cfgDict)
    else:
        print "{indent}H/E (cone=0.15) < {constTermEB}/Esc - {slopeTermEB} * max(0,Esc - {slopeStartEB} (EB))".format(**cfgDict)
    if cutCfg.slopeStartEE.value()==0.0:
        print "{indent}H/E (cone=0.15) < {slopeTermEE} - {constTermEE}/Esc (EE)".format(**cfgDict)
    else:
        print "{indent}H/E (cone=0.15) < {constTermEE}/Esc - {slopeTermEE} * max(0,Esc - {slopeStartEE} (EE))".format(**cfgDict)


def printGsfEleEInverseMinusPInverseCut(cutCfg,indent=6):
    print "{}|1/E - 1/p < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("eInverseMinusPInverseCutValueEB").value(),cutCfg.getParameter("eInverseMinusPInverseCutValueEE").value())

def printGsfEleEffAreaPFIsoCut(cutCfg,indent=6):
    isRelIso = cutCfg.getParameter("isRelativeIso")
    print "{}iso = pf charged + std::max(0,pf neutral+ pf photon - {}*EA)".format(" "*indent,cutCfg.getParameter("rho").value())
    isoStr = "iso"
    if isRelIso: isoStr+="/pt"

    isoCutEBLowPt =  cutCfg.getParameter("isoCutEBLowPt").value()
    isoCutEELowPt =  cutCfg.getParameter("isoCutEELowPt").value()
    isoCutEBHighPt =  cutCfg.getParameter("isoCutEBHighPt").value()
    isoCutEEHighPt =  cutCfg.getParameter("isoCutEEHighPt").value()
    ptCutOff = cutCfg.getParameter("ptCutOff").value()

    if (isoCutEBLowPt == isoCutEBHighPt and isoCutEELowPt == isoCutEEHighPt) or ptCutOff<=0:
        print "{}{} < {} (EB) < {} (EE) ".format(" "*indent,isoStr,isoCutEBHighPt,isoCutEEHighPt)
    else:
        print "{}pt < {} GeV".format(" "*indent,ptCutOff)
        print "{}{} < {} (EB) < {} (EE) ".format(" "*(indent+2),isoStr,isoCutEBLowPt,isoCutEELowPt)
        print "{}pt >= {} GeV".format(" "*indent,ptCutOff)
        print "{}{} < {} (EB) < {} (EE) ".format(" "*(indent+2),isoStr,isoCutEBHighPt,isoCutEEHighPt)

def printGsfEleEmHadD1IsoRhoCut(cutCfg,indent=6):
    cfgDict = convertPSetToValueDict(cutCfg)
    cfgDict['indent'] = " "*indent
    printStr = "{{indent}}isol em + had depth1 < {{constTerm{region}}} + {{slopeTerm{region}}} * min(0,Et-{{slopeStart{region}}} + {{rhoConstant}}*rho ({region})"
    print printStr.format(region="EB").format(**cfgDict)
    print printStr.format(region="EE").format(**cfgDict)
    print "{}rho = {}, energy = {}".format(" "*indent,cutCfg.getParameter("rho").value(),cutCfg.getParameter("energyType").value())

def printGsfEleTrkPtIsoCut(cutCfg,indent=6):
    varStr = "trk isol (heep)" if cutCfg.useHEEPIso.value() else "trk isol"
    if cutCfg.slopeTermEB.value()==0.0 and cutCfg.slopeTermEE.value()==0.0:
        print "{}{} < {} (EB), {} (EE)".format(" "*indent,varStr,cutCfg.getParameter("constTermEB").value(),cutCfg.getParameter("constTermEE").value())
    else:
        cfgDict = convertPSetToValueDict(cutCfg)
        cfgDict['varStr'] = varStr
        cfgDict['indent'] = " "*indent
        printStr = "{{indent}} {{varStr}} < {{constTerm{region}}} + {{slopeTerm{region}}} * min(0,Et-{{slopeStart{region}}} ({region})"
        print printStr.format(region="EB").format(**cfgDict)
        print printStr.format(region="EE").format(**cfgDict)
        
def printGsfEleRelPFIsoScaledCut(cutCfg,indent=6):
    varStr = "isol = charged + max(0.0,neutral + photon - rho*EA(eta_SC)"
    cfgDict = convertPSetToValueDict(cutCfg)
    cfgDict['varStr'] = varStr
    cfgDict['indent'] = " "*indent
    print "{indent}{varStr} < {barrelCpt} + {barrelC0} * pt (EB)".format(**cfgDict)
    print "{indent}{varStr} < {endcapCpt} + {endcapC0} * pt (EE)".format(**cfgDict)
    

def printGsfEleConversionVetoCut(cutCfg,indent=6):
    print '{}electron does not match a good conversion in "{}" / "{}"'.format(" "*indent,cutCfg.getParameter("conversionSrc").value(),cutCfg.getParameter("conversionSrcMiniAOD").value())
    print '{}with beamspot contraint : "{}"'.format(" "*indent,cutCfg.getParameter("beamspotSrc").value())

def printGsfEleMissingHitsCut(cutCfg,indent=6):
    print "{}#missing hits <= {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("maxMissingHitsEB").value(),cutCfg.getParameter("maxMissingHitsEE").value())   

def printGsfEleDxyCut(cutCfg,indent=6):
    print "{}|dxy| < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("dxyCutValueEB").value(),cutCfg.getParameter("dxyCutValueEE").value())   
    print "{}dxy w.r.t to leading vertex of {} (AOD) or {} (MINIAOD)".format(" "*indent,cutCfg.getParameter("vertexSrc").value(),cutCfg.getParameter("vertexSrcMiniAOD").value())   

def printGsfEleEcalDrivenCut(cutCfg,indent=6):
    ebVal = cutCfg.getParameter("ecalDrivenEB")
    eeVal = cutCfg.getParameter("ecalDrivenEE")
    if ebVal==-1:
        ebStr = "no requirement"
    elif ebVal==0:
        ebStr = "!isEcalDriven()"
    elif ebVal==1:
        ebStr = "isEcalDriven()"
    if eeVal==-1:
        eeStr = "no requirement"
    elif eeVal==0:
        eeStr = "!isEcalDriven()"
    elif eeVal==1:
        eeStr = "isEcalDriven()"
    print "{}{} (EB), {}(EE)".format(" "*indent,ebStr,eeStr)
    
        

def printGsfEleMVAExpodScalingCut(cutCfg,indent=6):
    return
    print "{}the cut values of this cut are difficult to succinctly express and so it is not supported by this tool".format(" "*indent)
    print "{}if you really need the values, please contact e/gamma".format(" "*indent)

def printGsfEleMVACut(cutCfg,indent=6):
    return
    print "{}the cut values of this cut are difficult to succinctly express and so it is not supported by this tool".format(" "*indent)
    print "{}if you really need the values, please contact e/gamma".format(" "*indent)

def printPhoSCEtaMultiRangeCut(cutCfg,indent=6):
    etaStr = "|eta|" if cutCfg.useAbsEta.value() else "eta"
    for etaRange in cutCfg.allowedEtaRanges:
        print "{}{} <= {} < {}".format(" "*indent,etaRange.minEta.value(),etaStr,etaRange.maxEta.value())

def printPhoSingleTowerHadOverEmCut(cutCfg,indent=6):
    print "{}H/E (single tower) < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("hadronicOverEMCutValueEB").value(),cutCfg.getParameter("hadronicOverEMCutValueEE").value())

def printPhoFull5x5SigmaIEtaIEtaCut(cutCfg,indent=6):
    print "{}sigma_ietaieta (full5x5) < {} (EB), {} (EE)".format(" "*indent,cutCfg.getParameter("cutValueEB").value(),cutCfg.getParameter("cutValueEE").value())

def printPhoGenericRhoPtScaledCut(cutCfg,indent=6):
    cfgDict = convertPSetToValueDict(cutCfg)
    cfgDict['opStr'] = '<' if cutCfg.lessThan.value() else ">="
    cfgDict['indent'] = " "*indent
    print "{indent}{cutVariable} {opStr} {constTermEB} + {linearPtTermEB}*Et + EA(|eta|)*rho + {quadPtTermEB}*Et*Et (EB)".format(**cfgDict)
    print "{indent}{cutVariable} {opStr} {constTermEE} + {linearPtTermEE}*Et + EA(|eta|)*rho + {quadPtTermEE}*Et*Et (EE)".format(**cfgDict)
    
def printPhoMVACut(cutCfg,indent=6):
    print "{} {} > {}".format(" "*indent,cutCfg.mvaValueMapName.getProductInstanceLabel(),cutCfg.mvaCuts.value()) 

def processCut(cutCfg,indent=6):
    cutName = cutCfg.getParameter("cutName").value()
    if "print"+cutName in globals():
        globals()["print"+cutName](cutCfg,indent=7)
    else:
        print "{}cut {} does not have a defined print function print{}, please add it".format(" "*indent,cutName,cutName)
        print cutCfg.parameters_()

def printListOfAvailableIDs(vidProducer):
    availableIDs = [cfg.getParameter("idDefinition").idName.value() for cfg in vidProducer.physicsObjectIDs]
    print "availible IDs are:"
    for idName in availableIDs:
        print "   {}".format(idName)
        
def _printID(idConfig,printCutValues=True):
    idDef = idConfig.getParameter("idDefinition")
    idName = idDef.idName.value()
    headerStr = "   {:^2} {:<42} {:^9} {:^9}"
    bodyStr   = "   {:^2} {:<42} {:^9} {:^9}"
    if printCutValues:
        headerStr = "   {} {} {} {}"
        bodyStr   = "   {} {} {} {}"

    if not printCutValues:
        print idName
        print headerStr.format("#","cutname","mask(dec)","mask(hex)")
    else:
        print "{} ({},{},{},{})".format(idName,"#","cutname","mask(dec)","mask(hex)")
    for cutNr,cut in enumerate(idDef.getParameter("cutFlow")):
        bitMask = 0x1 << cutNr
        
        print bodyStr.format(cutNr,getCutDisplayName(cut),bitMask,hex(bitMask))
        if printCutValues:
            processCut(cut)


def printAllIDs(vidProducer,printCutValues=True):
    for idConfig in vidProducer.physicsObjectIDs:
        _printID(idConfig,printCutValues)

def printID(vidProducer,idName,printCutValues=True):
    availableIDs = [cfg.getParameter("idDefinition").idName.value() for cfg in vidProducer.physicsObjectIDs]
    if idName in availableIDs:
        for idConfig in vidProducer.physicsObjectIDs:
            if idName==idConfig.getParameter("idDefinition").idName.value():
                _printID(idConfig,printCutValues)
                break
    else:
        print "{} not found".format(idName)
        printListOfAvailableIDs(vidProducer)
            

def main():

    parser = argparse.ArgumentParser(description='prints E/gamma VID info')
    parser.add_argument('--obj',default="ele",choices=["ele","pho"],help="displays electron or photon IDs")
    parser.add_argument('--idname',default=None,help="ID to print otherwise prints all IDs")
    parser.add_argument('--values',action='store_true',help="prints the cut values")
    parser.add_argument('--listids',action='store_true',help="lists the availible IDs")
    args = parser.parse_args()

    # set up process
    process = cms.Process("VIDDump")
    setupVID(process)
    
    if args.obj=="ele":
        #eleVIDModule = getEleVIDModule(process)
        vidModule = process.egmGsfElectronIDs
    elif args.obj=="pho":
        vidModule = process.egmPhotonIDs

    if args.listids:
        print "printing available IDs and exiting"
        printListOfAvailableIDs(vidModule)
    elif args.idname:
        printID(vidModule,args.idname,args.values)
    else:
        printAllIDs(vidModule,args.values)
            
if __name__ == '__main__':
    main()
