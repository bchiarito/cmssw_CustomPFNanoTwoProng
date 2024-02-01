#!/usr/bin/env

import subprocess
import argparse
import os
import time
import shutil

def setupcmd_106X():
    return """
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {dir}
cmsrel CMSSW_10_6_3
cd CMSSW_10_6_3/src
cmsenv
git cms-init
git cms-merge-topic cms-egamma:EgammaPostRecoTools #just adds in an extra file to have a setup function to make things easier 
#now build everything
scram b -j 8
{extra_cmds}
"""

def setupcmd_10210():
    return """
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {dir}
cmsrel CMSSW_10_2_10
cd CMSSW_10_2_10/src
cmsenv
git cms-init
git cms-merge-topic cms-egamma:EgammaPostRecoTools #just adds in an extra file to have a setup function to make things easier 
git cms-merge-topic cms-egamma:PhotonIDValueMapSpeedup1029 #optional but speeds up the photon ID value module so things fun faster
git cms-merge-topic cms-egamma:slava77-btvDictFix_10210 #fixes the Run2018D dictionary issue, see https://github.com/cms-sw/cmssw/issues/26182, may not be necessary for later releases, try it first and see if it works
#now to add the scale and smearing for 2018 (eventually this will not be necessary in later releases but is harmless to do regardless)
git cms-merge-topic cms-egamma:ModifiedRecoEgammaProducers_1020 #for workflows that modify AOD electrons
git cms-addpkg EgammaAnalysis/ElectronTools
rm EgammaAnalysis/ElectronTools/data -rf
git clone git@github.com:cms-data/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data
#now build everything
scram b -j 8
{extra_cmds}
"""

def setupcmd_102X():
    return """
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {dir}
cmsrel CMSSW_10_2_15
cd CMSSW_10_2_15/src
cmsenv
git cms-init
git cms-merge-topic cms-egamma:EgammaPostRecoTools #just adds in an extra file to have a setup function to make things easier 
git cms-merge-topic cms-egamma:PhotonIDValueMapSpeedup1029 #optional but speeds up the photon ID value module so things run faster
git cms-merge-topic cms-egamma:ModifiedRecoEgammaProducers_1020 #for workflows that modify AOD electrons
#now build everything
scram b -j 8
{extra_cmds}
"""
def setupcmd_9413():
    return """
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {dir}
cmsrel CMSSW_9_4_13
cd CMSSW_9_4_13/src
cmsenv
git cms-init
git cms-merge-topic cms-egamma:ModifiedRecoEgammaProducers_940 #for workflows that modify AOD electrons
git cms-merge-topic cms-egamma:EgammaPostRecoTools #just adds in an extra file to have a setup function to make things easier
scram b -j 8
{extra_cmds}
"""

def setupcmd_94X():
    return """
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {dir}
cmsrel CMSSW_9_4_13
cd CMSSW_9_4_13/src
cmsenv
git cms-init
git cms-merge-topic cms-egamma:ModifiedRecoEgammaProducers_940 #for workflows that modify AOD electrons
git cms-merge-topic cms-egamma:EgammaPostRecoTools #just adds in an extra file to have a setup function to make things easier
scram b -j 8
{extra_cmds}
"""


def create_area(area,release_dir,input_dir,output_dir_base,egtools_branch="master"):
    areas = {"94X" : setupcmd_94X,
             "9413" : setupcmd_9413,
             "102X" : setupcmd_102X,
             "10210" : setupcmd_10210,
             "106X" : setupcmd_106X
         }

    eras_to_test = {"94X" : "2017-Nov17ReReco,2016-Legacy",
                    "9413" : "2017-Nov17ReReco,2016-Legacy",
                    "102X" : "2018-Prompt,2017-Nov17ReReco,2016-Legacy",
                    "10210" : "2018-Prompt,2017-Nov17ReReco,2016-Legacy",
                    "106X" : "2018-Prompt,2017-Nov17ReReco,2016-Legacy,2017-UL",
                }
                    
                    
    output_dir = output_dir_base+"/{release}/".format(release=area)

    extra_cmds = """
git clone git@github.com:cms-egamma/EgammaPostRecoTools.git  EgammaUser/EgammaPostRecoTools
cd  EgammaUser/EgammaPostRecoTools
git checkout {egtools_branch}
cd -
echo $CMSSW_BASE
cd $CMSSW_BASE/src
scram b -j 8
python EgammaUser/EgammaPostRecoTools/test/runEgammaPostRecoToolsUnitTests.py --live --eras {eras} --input_dir {input_dir} --output_dir {output_dir}
""".format(eras=eras_to_test[area],input_dir=input_dir,output_dir=output_dir,egtools_branch=egtools_branch)
    cmd_str = areas[area]().format(dir=release_dir,extra_cmds = extra_cmds)

    subprocess.check_call(cmd_str, shell=True)


def main():
    
    parser = argparse.ArgumentParser(description='gives the files and optional picks the events given')
    parser.add_argument('--release_dir',default="/mercury/data1/harper/egammaPostRecoTools/testReleases",help='dir for releases')
    parser.add_argument('--input_dir',default="/mercury/data1/harper/egammaPostRecoTools/testInputs",help='input directory for files')
    parser.add_argument('--output_dir',default="/mercury/data1/harper/egammaPostRecoTools/testResults",help='output directory for files')
    parser.add_argument('--releases','-r',default='102X,94X',help='comma seperated list of release areas to make')
    parser.add_argument('--clean',action='store_true',help='cleans existing release area')
    args = parser.parse_args()

    if os.path.exists(args.release_dir) and args.clean:
        print "warning will delete {} in 10s".format(args.release_dir)
        time.sleep(10)
        shutil.rmtree(args.release_dir)
    

    if not os.path.exists(args.release_dir):
        os.makedirs(args.release_dir)
    for release in args.releases.split(","):
        create_area(release,args.release_dir,args.input_dir,args.output_dir)

if __name__=="__main__":
    main()
