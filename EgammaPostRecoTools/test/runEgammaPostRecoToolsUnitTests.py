#!/usr/bin/env python

import subprocess
import os
import argparse

def get_config_options(all_cmd_strs,cmd_str,opts,opt_vals):
    if opts == list():
        all_cmd_strs.append(cmd_str)
    else:
        opts_new = opts[1:]
        for val in opt_vals[opts[0]]:
            cmd_str_new = str(cmd_str)
            cmd_str_new+=" {}={}".format(opts[0],val)
            get_config_options(all_cmd_strs,cmd_str_new,opts_new,opt_vals)
    
def get_opt_val(options,opt_name):
    for opt in options:
        opt_split = opt.split("=")
        if opt_split[0] == opt_name: 
            return opt_split[1]
    return ""

def is_valid_option_combination(cmd_str):
    options = cmd_str.split()[2:]
    
    if get_opt_val(options,'applyVIDOnCorrectedEgamma') != get_opt_val(options,'applyEnergyCorrections'):
        return False

    if get_opt_val(options,'isMiniAOD')=='False' and get_opt_val(options,'applyVIDOnCorrectedEgamma')=='True':
        return False
    return True
    
def run_static_tests():
    """
    Runs the python of the config file only, checks for syntax errors
    Runs over all possible input parameters
    """
    opt_vals = {
        'isMiniAOD' : ["True","False"],
        'runVID' : ["True","False"],
        'runEnergyCorrections' : ["True","False"],
        'applyEnergyCorrections' : ["True","False"],
        'applyVIDOnCorrectedEgamma' : ["True","False"],
        'applyEPCombBug' : ["True","False"],
        'era' : ['2016-Legacy','2017-Nov17ReReco','2018-Prompt']
        }
    
    all_cmd_strs = []
    config = "python EgammaUser/EgammaPostRecoTools/test/runEgammaPostRecoTools.py"
    get_config_options(all_cmd_strs,config,opt_vals.keys(),opt_vals)

    from collections import OrderedDict
    results = OrderedDict()

    for cmd_str in all_cmd_strs:
        if is_valid_option_combination(cmd_str):
            out,err=subprocess.Popen(cmd_str.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
            
            test_pass = err==""

            if not test_pass:
                print cmd_str
                print err
            
            results[cmd_str] = test_pass
                
    for test,result  in results.iteritems():
        print "{} result {}".format(test,result)
    


class TestCfg:
    def __init__(self,input_file,output_file,era):
        self.input_file = input_file
        self.output_file = output_file
        self.era = era
        self.is_mc = input_file.find("MINIAODSIM")!=-1 or input_file.find("AODSIM")!=-1
        self.is_miniaod = input_file.find("MINIAOD")!=-1
        

class TestCfgMgr:
    def __init__(self,input_dir,output_dir):
        self.tests = []
        self.input_dir = input_dir
        self.output_dir = output_dir
    def add_test(self,input_file,output_file,era):
        input_full_path = "{}/{}".format(self.input_dir,input_file)
        if not output_file:
            if input_file.find(".root")==-1:
                raise ValueError('input_file "{}" must end in .root if output not set'.format(input_file))
            output_file = input_file.split("/")[-1].replace(".root","_output.root")
        output_full_path = "{}/{}".format(self.output_dir,output_file)
        self.tests.append(TestCfg(input_full_path,output_full_path,era))
        
def make_test_cfgs(input_dir,output_dir):
    cfgMgr = TestCfgMgr(input_dir,output_dir)
    cfgMgr.add_test("DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__RunIISummer19UL17MiniAOD__106X_mc2017_realistic_v6-v2__MINIAODSIM__9DA9A9A4-D568-E148-9E95-C2E2739B79B9.root",None,"2017-UL")
    cfgMgr.add_test("DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__RunIISummer19UL17RECO__106X_mc2017_realistic_v6-v2__AODSIM__191489FD-5DC9-DB4F-865F-57B7CEF6787D.root",None,"2017-UL")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18DRPremix__102X_upgrade2018_realistic_v15-v1__AODSIM__F1425090-2860-B647-8E5B-72E3A17EA48F.root",None,"2018-Prompt")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18MiniAOD__102X_upgrade2018_realistic_v15-v1__MINIAODSIM__042C8EE9-9431-5443-88C8-77F1D910B3A5.root",None,"2018-Prompt")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIFall17DRPremix__RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1__AODSIM__1641DB73-9EEF-E711-8E78-E0071B7A58B0.root",None,"2017-Nov17ReReco")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIFall17MiniAODv2__PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1__MINIAODSIM__DA1BE8CB-5444-E811-BDBF-0025905A48FC.root",None,"2017-Nov17ReReco")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16DR80Premix__PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1__AODSIM__3E10C676-9DE4-E611-827A-0CC47A7C3408.root",None,"2016-Legacy")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16MiniAODv2__PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2__MINIAODSIM__247A7B47-29C4-E611-8B5A-008CFA1113F8.root",None,"2016-Legacy")
    cfgMgr.add_test("DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16MiniAODv3__PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2__MINIAODSIM__6E4F708B-31E9-E811-8E79-44A84225C827.root",None,"2016-Legacy")
    cfgMgr.add_test("DoubleEG__Run2016H-07Aug17-v1__MINIAOD__283884-LS365__6E41299F-F792-E711-9D14-0425C5903034.root",None,"2016-Legacy")
    cfgMgr.add_test("DoubleEG__Run2017E-09Aug2019_UL2017-v1__MINIAOD__304333-LS120__47AF3530-5F96-8341-A53B-035825F454AE.root",None,"2017-UL")
    cfgMgr.add_test("DoubleEG__Run2017E-17Nov2017-v1__MINIAOD__304333-LS120__FEBB1201-C3D5-E711-A803-7845C4FC3C56.root",None,"2017-Nov17ReReco")
    cfgMgr.add_test("EGamma__Run2018D-22Jan2019-v2__AOD__323755-LS50__CEEBC4AC-EA40-7644-A167-73C8AE7D79D0.root",None,"2018-Prompt")
    cfgMgr.add_test("EGamma__Run2018D-22Jan2019-v2__MINIAOD__323755-LS50__D8108B2A-213A-9B41-8AAA-C3DC3152FC6E.root",None,"2018-Prompt")
    return cfgMgr

def run_live_tests(input_dir,output_dir,valid_eras=[],only_mini=False):
    test_cfgs = make_test_cfgs(input_dir,output_dir)
    cfg_file = "EgammaUser/EgammaPostRecoTools/test/runEgammaPostRecoTools.py"
    base_options = "runVID=True runEnergyCorrections=True maxEvents=5000"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for test in test_cfgs.tests:
        if valid_eras and test.era not in valid_eras:
            continue
        if only_mini and not test.is_miniaod:
            continue

        cmd_base = "{{exec_name}} {cfg_file} inputFiles=file:{cfg.input_file} outputFile={cfg.output_file} era={cfg.era} isMC={cfg.is_mc} isMiniAOD={cfg.is_miniaod} {base_options}".format(cfg_file=cfg_file,cfg=test,base_options=base_options)
        print "running {}".format(cmd_base.format(exec_name="cmsRun"))
        out,err = subprocess.Popen(cmd_base.format(exec_name="python").split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        if err=="":
            cmsrun_process = subprocess.Popen(cmd_base.format(exec_name="cmsRun").split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err = cmsrun_process.communicate()
            log_file = test.output_file.replace(".root",".log") 
            with open(log_file,'w') as f:
                f.write("stdout:\n{}\n\n stderr:\n{}\n".format(out,err))
            if cmsrun_process.returncode != 0:
                print "    FAILED due to runtime error {}".format(cmsrun_process.returncode)
                print "       log file: {}".format(log_file)
            else:
                print "    SUCCEEDED : log {}".format(log_file)
        else:
            print "    FAILED due to python errors: {}".format(err.replace("\n","\n     "))
            
def main():

    parser = argparse.ArgumentParser(description='gives the files and optional picks the events given')
    parser.add_argument('--static',action='store_true',help='run static tests')
    parser.add_argument('--live',action='store_true',help='run live lests')
    parser.add_argument('--eras','-e',default=None,help='eras for live tests, comma seperated')
    parser.add_argument('--input_dir','-i',default="./",help='input directory')
    parser.add_argument('--output_dir','-o',default="./",help='output directory')
    parser.add_argument('--only_mini',action='store_true',help='only run miniAOD tests')
    args = parser.parse_args()

    
    if args.static:
        run_static_tests()
    if args.live:
        valid_eras = []
        if args.eras:
            valid_eras = args.eras.split(',')

        run_live_tests(input_dir=args.input_dir,output_dir=args.output_dir,valid_eras=valid_eras,only_mini=args.only_mini)

if __name__ == '__main__':
    main()
    
