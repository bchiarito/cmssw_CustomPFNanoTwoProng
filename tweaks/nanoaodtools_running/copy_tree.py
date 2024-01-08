import ROOT
import sys

fi = ROOT.TFile(sys.argv[1])
tree = fi.Get('Events')
if tree == None:
  print "Error: No Events tree found in file, failing"
  sys.exit()
newfile = ROOT.TFile("NANOAOD_TwoProng.root", "recreate")
newtree = tree.CloneTree()
newtree.Write()
tree = fi.Get('Runs')
if tree == None:
  print "Error: No Runs tree found in file, failing"
  sys.exit()
newtree = tree.CloneTree()
newtree.Write()
