import sys
import ROOT

fi = ROOT.TFile(sys.argv[1])
tree = fi.Get('Events')
hist = ROOT.TH1D('hist','hist',1,0,1)
tree.Draw('nTwoProng >> hist', '', 'goff')
print 'twoprongs:'
hist.Print('all')
tree.Draw('nGenPhi >> hist', '', 'goff')
print ''
print 'genphis:'
hist.Print('all')
print ''
tree.Draw('nGenOmega >> hist', '', 'goff')
print 'genomegas:'
hist.Print('all')
print ''

branches = tree.GetListOfBranches()
for b in branches:
  name = b.GetName()
  if "GenPhi" in name: print name
  if "GenOmega" in name: print name
  if "TwoProng" in name: print name
  if "RecoPhi" in name: print name
  if "HighPtIdPhoton" in name: print name
  
