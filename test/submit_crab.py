#!/usr/bin/env python
import os
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('runname', help='used in crab dir and output dir')
parser.add_argument('dataset', help='dataset name')
parser.add_argument('cfg', help='path to cmssw config e.g. ../PhysicsTools/PFNano/test/NANOAOD_data_UL18_cfg.py')
parser.add_argument('--out', default='/store/user/bchiari1/eos_area/crab/', help='')
parser.add_argument('--totalUnits', default=-1, help='')
parser.add_argument('--unitsPerJob', default=20000, help='')
parser.add_argument('-f', '--force', action='store_true', default=False, help='overwrite crab dir if already exists')
args = parser.parse_args()

import CRABClient
from CRABAPI.RawCommand import crabCommand

crab_dir = 'crab_'+str(args.runname)
if os.path.isdir(crab_dir):
  if args.force: os.system('rm -rf '+crab_dir)
  else: raise SystemExit("ERROR: dir exists, run with --force")

config = CRABClient.UserUtilities.config()
config.General.requestName = args.runname
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = args.cfg
config.JobType.disableAutomaticOutputCollection = True
config.JobType.outputFiles = ['NANOAOD_TwoProng.root']
config.JobType.scriptExe = 'execute.sh'
config.Data.inputDataset = args.dataset
config.Data.splitting = 'EventAwareLumiBased' # FileBased, EventBased
config.Data.lumiMask = '../PhysicsTools/PFNano/test/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Data.totalUnits = int(args.totalUnits)
config.Data.unitsPerJob = int(args.unitsPerJob)
config.Data.publication = False
config.Site.storageSite = 'T3_US_Rutgers'
config.Data.outLFNDirBase = args.out
config.Data.outputDatasetTag = str(args.runname)
config.JobType.maxMemoryMB = 2500 # 5000 is max for single core 
config.JobType.inputFiles = ['nanoaodtools.tgz', 'dropPF.txt']
#config.JobType.maxJobRuntimeMin = 1315 # (minutes) default 1315 (just under 22 hours)
#config.Data.outputPrimaryDataset

try: input = raw_input
except NameError: pass
print(config)
response = input('Continue [Enter] or Quit (q): ')
if response == '':
  crabCommand('submit', config = config)
  command = ''
  for a in sys.argv: command += a + ' '
  with open(crab_dir+"/cmd.log", 'wt') as f:
    f.write('Command:\n'+command)
