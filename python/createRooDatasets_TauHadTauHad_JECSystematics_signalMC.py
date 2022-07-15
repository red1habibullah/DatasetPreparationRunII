#!/usr/bin/python
import ROOT
from ROOT import RooFit

baseDir="/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/signalMC/"
outDir="/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauHadTauHad/"

scale =0.001
higgs_SM_xsec=48.58
higgs_BSM_xsec=0.0363647

fakerateUncertainty=0.20
scaleUp=1.0+fakerateUncertainty
scaleDown=1.0-fakerateUncertainty


#years=["2016","2017","2018"]
#years=["2017"]
years=["2018"]
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


#mh=["hm125","hm250","hm500","hm750","hm1000"]
#mh=["hm500","hm750"]

mh=["hm250","hm500","hm1000"]

hamap ={
    "hm125":["am3p6","am5","am6","am7","am8","am9","am10","am11","am12","am13","am14","am15","am16","am17","am18","am19","am20","am21"], #am4 missing in 2018 so left out for now
    "hm250":["am5","am10","am15","am20"],
    "hm500":["am5","am10","am15","am20"],
    "hm750":["am10","am20","am25","am30"],
    "hm1000":["am10","am20","am30","am40"]
}

regions = ["signalRegion", "sideBand"]

jectag=["_","_JecUp_","_JecDown_"]
jecmap={"_":"nominal","_JecUp_":"JECUp","_JecDown_":"JECDown"}

for y in years:
    for h in mh:
        for ia,a in enumerate(hamap[h]):
            for ir,r in enumerate(regions):
                for ij,j in enumerate(jectag):
                    fname= baseDir+y+"/Histogram/"+h+"/"+a+"/HAA_MC_"+h+"_"+a+"_"+y+"_tmth_teth_MVAMedium_"+r+j+"tree.root"
                    print a,ir,y,lumi_map[y],j
                    print fname
                    globals()["fin"+ a+ r + h + j]=ROOT.TFile(fname)
                    globals()["treein"+ a+ r + h + j]=globals()["fin" + a + r + h + j].Get("TreeTauTau")
                    globals()["dimuMass" + a + r + h + j] = ROOT.RooRealVar("invMassMuMu","invMassMuMu",2.5,60)
                    globals()["visFourbodyMass" + a + r + h + j] = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
                    globals()["eventWeight" + a + r + h + j] = ROOT.RooRealVar("eventWeight", "eventWeight", -1, 1)
                    globals()["dataColl" + a + r + h + j] = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(globals()["dimuMass" + a + r + h + j], globals()["visFourbodyMass" + a + r + h + j], globals()["eventWeight" + a + r + h + j]))

                    for event in globals()["treein" + a + r + h + j]:
                    #if event.mu1Pt_mt > event.mu3Pt_mt:
                        globals()["dimuMass" + a + r + h + j].setVal(event.invMassMu1Mu2_tt)
                        globals()["visFourbodyMass" + a + r + h + j].setVal(event.visMass2Mu2Tau_tt)
                        globals()["eventWeight" + a + r + h + j].setVal(event.eventWeight_tt*scale*lumi_map[y]*hXsecmap[h])
                        globals()["dataColl" + a + r + h + j].add(ROOT.RooArgSet(globals()["dimuMass" + a + r + h + j], globals()["visFourbodyMass" + a + r + h + j], globals()["eventWeight" + a + r + h +j]))

                    globals()["foutUp"+ a + r + h + j]=ROOT.TFile(outDir+y+"/SignalMC/"+"Haa_MC_"+h+"_"+a+"_"+"TauHadTauHad"+"_"+y+"_"+"MVAMedium"+"_"+r+"_"+jecmap[j]+".root","RECREATE")
                    print outDir+y+"/signalMC/"+"Haa_MC_"+h+"_"+a+"_"+"TauHadTauHad"+"_"+y+"_"+"MVAMedium"+"_"+r+"_"+jecmap[j]+".root"
                    globals()["dataColl" + a + r + h + j].Write()
                    globals()["foutUp"+ a + r+ h + j].Close()
                
               







exit()




