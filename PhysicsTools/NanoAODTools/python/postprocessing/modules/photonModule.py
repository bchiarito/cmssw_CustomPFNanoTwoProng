from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math

# constants
const_rho_definition = "fixedGridRhoFastjetAll"
const_cut_HE = 0.05
const_cut_IsoCh = 5
const_cut_IsoGamma_EB = 2.75
const_cut_IsoGamma_EE = 2.0
const_cut_sieie_EBnosat = 0.0105
const_cut_sieie_EBsat = 0.0112
const_cut_sieie_EEnosat = 0.0280
const_cut_sieie_EEsat = 0.0300
const_EA_EB_1 = 0.17
const_EA_EB_2 = 0.14
const_EA_EE_1 = 0.11
const_EA_EE_2 = 0.13
const_EA_EE_3 = 0.22
const_kappa_EB = 0.0045
const_kappa_EE = 0.003
const_ESCAPE = 99999.0

class photonModule(Module):
    def __init__(self):
        self.objects = []
        self.Variables = {}
        self.addCollection('HighPtIdPhoton')
        self.addVariable('HighPtIdPhoton', 'pt', 'F', 'pt')
        self.addVariable('HighPtIdPhoton', 'phi', 'F', 'phi')
        self.addVariable('HighPtIdPhoton', 'eta', 'F', 'eta')
        self.addVariable('HighPtIdPhoton', 'mass', 'F', 'mass')
        self.addVariable('HighPtIdPhoton', 'HoE', 'F', 'hadTowOverEm')
        self.addVariable('HighPtIdPhoton', 'HoECone', 'F', 'hoe')
        self.addVariable('HighPtIdPhoton', 'chargedIso', 'F', 'chargedHadronIso')
        self.addVariable('HighPtIdPhoton', 'egammaIso', 'F', 'photonIso')
        self.addVariable('HighPtIdPhoton', 'scEta', 'F', 'scEta')

    def addVariable(self, base, name, type_, access):
        temp = {}
        temp['name'] = name
        temp['type'] = type_
        temp['access'] = access
        self.Variables[base].append(temp)

    def addCollection(self, base):
        self.objects.append(base)
        self.Variables[base] = []

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        # make num branches
        for base in self.objects:
          self.out.branch("n"+base, "I")
          # make vector branches
          for var in self.Variables[base]:
            self.out.branch(base+"_"+var['name'], var['type'], lenVar="n"+base)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        # get event info
        photons = Collection(event, "Photon")
        exec("rho = event."+const_rho_definition)

        # setup
        TempVectors = {}
        for base in self.objects:
          TempVectors[base] = {}
          for var in self.Variables[base]:
            TempVectors[base][var['name']] = []

        # calcuate high-pt-id photon
        photon_branch_name = 'HighPtIdPhoton'
        for photon in photons:
          isSat = self.photon_isSat(photon)
          passID = self.photon_passID(photon, isSat, rho)
          passConeID = self.photon_passConeID(photon, isSat, rho)
          if passID:
            for var in self.Variables[photon_branch_name]:
              if not var['access'] == None:
                exec("temp = photon."+var['access'])
                TempVectors[photon_branch_name][var['name']].append(temp)
              else:
                pass
              # one off example
              # if var['name'] == <varname that requires calculation>:
              #   temp = <any calculation here>
              #   TempVectors['TestObj'][var['name']].append(temp)

        # fill branches
        for base in self.objects:
          self.out.fillBranch("n"+base, len(self.Variables[base][0]))
          for var in self.Variables[base]:
            self.out.fillBranch(base+"_"+var['name'], TempVectors[base][var['name']])

        return True

    def photon_isSat(self, photon):
        # FIXME
        return True
    
    def photon_passID(self, photon, isSat, rho):
        return self.photon_passHE(photon) and \
               self.photon_passIsoCh(photon) and \
               self.photon_passIsoGamma(photon, rho) and \
               self.photon_passSigmaIetaIeta(photon, isSat) and \
               photon.electronVeto

    def photon_passConeID(self, photon, isSat, rho):
        return self.photon_passConeHE(photon) and \
               self.photon_passIsoCh(photon) and \
               self.photon_passIsoGamma(photon, rho) and \
               self.photon_passSigmaIetaIeta(photon, isSat) and \
               photon.electronVeto

    def photon_passHE(self, photon):
        return photon.hadTowOverEm < const_cut_HE

    def photon_passConeHE(self, photon):
        return photon.hoe < const_cut_HE

    def photon_passIsoCh(self, photon):
        return photon.chargedHadronIso < const_cut_IsoCh

    def photon_passSigmaIetaIeta(self, photon, isSat):
        if photon.isScEtaEB and not isSat: return photon.sieie < const_cut_sieie_EBnosat
        elif photon.isScEtaEB and isSat: return photon.sieie < const_cut_sieie_EBsat
        elif photon.isScEtaEE and not isSat: return photon.sieie < const_cut_sieie_EEnosat
        elif photon.isScEtaEE and isSat: return photon.sieie < const_cut_sieie_EEsat
        else: return False

    def photon_passIsoGamma(self, photon, rho):
        iso = photon.photonIso
        scEta = photon.scEta
        # alpha
        alpha = 2.5        
        # EA
        if photon.isScEtaEB and scEta < 0.9: EA = const_EA_EB_1
        elif photon.isScEtaEB and scEta >= 0.9: EA = const_EA_EB_2
        elif photon.isScEtaEE and scEta < 2.0: EA = const_EA_EE_1
        elif photon.isScEtaEE and scEta < 2.2: EA = const_EA_EE_2
        elif photon.isScEtaEE: EA = const_EA_EE_3
        else: EA = const_ESCAPE
        # kappa
        if photon.isScEtaEB: kappa = const_kappa_EB
        elif photon.isScEtaEE: kappa = const_kappa_EE
        else: kappa = const_ESCAPE
        iso = alpha * iso - rho*EA - kappa*photon.pt
        if photon.isScEtaEB: return iso < const_cut_IsoGamma_EB
        elif photon.isScEtaEE: return iso < const_cut_IsoGamma_EE
        else: return False

photonConstr_default = lambda: photonModule()
