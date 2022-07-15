#!/usr/bin/python
import ROOT
from ROOT import RooFit

baseDir="/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/signalMC/"
outDir="/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauMuTauHad/"

scale =0.001
higgs_SM_xsec=48.58
higgs_BSM_xsec=0.0363647



years=["2016"]

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


mh=["hm125"] #,"hm250","hm500","hm750","hm1000"]

# hamap ={
#     "hm125":["am3p6","am5","am6","am7","am8","am9","am10","am11","am12","am13","am14","am15","am16","am17","am18","am19","am20","am21"], #am4 missing in 2018 so left out for now
#     "hm250":["am5","am10","am15","am20"],
#     "hm500":["am5","am10","am15","am20"],
#     "hm750":["am10","am20","am25","am30"],
#     "hm1000":["am10","am20","am30","am40"]
# }

hamap ={
    "hm125":["am10"], #am4 missing in 2018 so left out for now
    # "hm250":["am5","am10","am15","am20"],
    # "hm500":["am5","am10","am15","am20"],
    # "hm750":["am10","am20","am25","am30"],
    # "hm1000":["am10","am20","am30","am40"]
}

regions = ["signalRegion", "sideBand"]



for y in years:
    for h in mh:
        for ia,a in enumerate(hamap[h]):
            for ir,r in enumerate(regions):
                fname= baseDir+y+"/Histogram/"+h+"/"+a+"/HAA_MC_"+h+"_"+a+"_"+y+"_tmth_teth_MVAMedium_"+r+"_tree.root"
                print a,ir,y,lumi_map[y]
                print fname
                globals()["fin"+ a+ r]=ROOT.TFile(fname)
                globals()["treein"+ a+ r]=globals()["fin" + a + r].Get("TreeMuTau")
                globals()["dimuMass" + a + r] = ROOT.RooRealVar("invMassMuMu","invMassMuMu",2.5,60)
                globals()["visFourbodyMass" + a + r] = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
                globals()["eventWeight" + a + r] = ROOT.RooRealVar("eventWeight", "eventWeight", -1, 1)
                globals()["dataColl" + a + r] = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(globals()["dimuMass" + a + r], globals()["visFourbodyMass" + a + r], globals()["eventWeight" + a + r]))

                for event in globals()["treein" + a + r]:
                    globals()["dimuMass" + a + r].setVal(event.invMassMu1Mu2_mt)
                    globals()["visFourbodyMass" + a + r].setVal(event.visMass3MuTau_mt)
                    globals()["eventWeight" + a + r].setVal(event.eventWeight_mt*scale*lumi_map[y]*hXsecmap[h])
                    globals()["dataColl" + a + r].add(ROOT.RooArgSet(globals()["dimuMass" + a + r], globals()["visFourbodyMass" + a + r], globals()["eventWeight" + a + r]))

                globals()["fout"+ a + r]=ROOT.TFile(outDir+y+"/SignalMC/"+"Haa_MC_"+h+"_"+a+"_"+"TauMuTauHad"+"_"+y+"_"+"MVAMedium"+"_"+r+"_"+"nominal.root","RECREATE")
                print outDir+y+"/SignalMC/"+"Haa_MC_"+h+"_"+a+"_"+"TauMuTauHad"+"_"+y+"_"+"MVAMedium"+"_"+r+"_"+"nominal.root"
                globals()["dataColl" + a + r].Write()
                globals()["fout"+ a + r].Close()
exit()




