import sys
import ROOT

fi = ROOT.TFile(sys.argv[1])
tree = fi.Get('Events')
hist = ROOT.TH1D('hist','hist',1,0,1)
tree.Draw('nTwoProng >> hist', '', 'goff')
print ''
hist.Print('all')
#hist.Draw()
#raw_input()
print ''
branches = tree.GetListOfBranches()
for b in branches:
  name = b.GetName()
  if "TwoProng" in name: print name
