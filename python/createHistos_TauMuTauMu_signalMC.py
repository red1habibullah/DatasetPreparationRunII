#!/usr/bin/python
import ROOT
from ROOT import RooFit
import math
import array


baseDir="/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/signalMC/"
outDir="/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauMuTauMu/"


#path = [signalDir, sidebandDir1, sidebandDir2]

scale =0.001
higgs_SM_xsec=48.58
higgs_BSM_xsec=0.0363647




years=["2016","2017","2018"]

lumi_map={"2017":41.529*1000,
          "2016":35.92*1000,
          "2018":59.74*1000
}

hXsecmap={"hm125":48.58,
          "hm250":10.2,
          "hm500":1.7089,
          "hm750":0.4969,
          "hm1000":0.1845


}


mh=["hm125","hm250","hm500","hm750","hm1000"]
hamap ={
    "hm125":["am3p6","am5","am6","am7","am8","am9","am10","am11","am12","am13","am14","am15","am16","am17","am18","am19","am20","am21"],
    "hm250":["am5","am10","am15","am20"],
    "hm500":["am5","am10","am15","am20"],
    "hm750":["am10","am20","am25","am30"],
    "hm1000":["am10","am20","am30","am40"]
}

regions = ["signalRegion", "sideBand"]

MuonIso=["looseMuIso"]

EleId=["tightEleId"]




for y in years:
    for h in mh:
        for ia,a in enumerate(hamap[h]):
            for ir,r in enumerate(regions):
                for m in MuonIso:
                    for m2 in MuonIso:
                        fname= baseDir+y+"/Histogram/"+h+"/"+a+"/HAA_MC_"+h+"_"+a+"_"+y+"_tmth_teth_MVAMedium_"+r+"_tree.root"
                        globals()["fin" + h+a+r]=ROOT.TFile(fname)
                        globals()["treein" + h+a+r]=globals()["fin" +h+a+r].Get("Tree2Mu")
                        globals()["hist" + h+a+r]=ROOT.TH1D("invMassMuMu","invMassMuMu",600,0,60)
                        globals()["2Dhist" + h+a+r] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau","InvMassMuMuVisMassMuMuTauTau",600,0,60, 500, 0, 1000)
                        
                        
                        for event in globals()["treein" + h +a+r]:
                            globals()["hist" + h+a+r].Fill(event.invMassMu1Mu2_mm, event.eventWeight_mm*scale*lumi_map[y]*hXsecmap[h])
                            globals()["2Dhist" + h+a+r].Fill(event.invMassMu1Mu2_mm, event.visMass4Mu_mm, event.eventWeight_mm*scale*lumi_map[y]*hXsecmap[h])  
                           
                        print outDir+y+"/SignalMC/"+"Haa_MC_"+h+"_"+a+"_"+"TauMuTauE"+"_"+y+"_"+m+"_"+m2+"_"+r+"_"+"nominal.root"
                        globals()["fout"+ h+a+r]=ROOT.TFile(outDir+y+"/SignalMC/"+"Haa_MC_"+h+"_"+a+"_"+"TauMuTauMu"+"_"+y+"_"+m+"_"+m2+"_"+r+"_"+"nominal.root","RECREATE")
                        globals()["fout"+ h+a+r].cd()
                        globals()["hist"+ h+a+r].Write()
                        globals()["2Dhist"+ h+a+r].Write()
                        globals()["fout"+ h+a+r].Close()
                         
                         



exit()
