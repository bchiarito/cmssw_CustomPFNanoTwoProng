from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math

class dataFiltersModule(Module):
    def __init__(self, year):
        self.year = year
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
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        flags = Object(event, "Flag")

        if self.year == 'UL18':
          pass_filters = (
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
          if not (pass_filters): return False
          return True
        elif self.year == 'UL18':
          # FIXME
          return True
        elif self.year == 'UL18':
          # FIXME
          return True
        else: return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

filtersConstr_default = lambda: dataFiltersModule('UL18')
filtersConstr_UL18 = lambda: dataFiltersModule('UL18')
filtersConstr_UL17 = lambda: dataFiltersModule('UL17')
filtersConstr_UL16 = lambda: dataFiltersModule('UL16')
