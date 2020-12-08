#!/usr/bin/python
import ROOT
from ROOT import RooFit

signalDir = "/eos/uscms/store/user/zfwd666/HAA/DeepTauID/TauMuTauHad/slimmedTausMuonCleanedDeep/"
sidebandDir = "/eos/uscms/store/user/zfwd666/HAA/DeepTauID/TauMuTauHad/sideband/"

outputDir='/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauMuTauHad/RooDataSets/SignalMCSystematics/'

path = [signalDir, sidebandDir]

scale =0.001
higgs_xsec=48.58
lumi_2017=41.529*1000
fakerateUncertainty=0.20
scaleUp=1.0+fakerateUncertainty
scaleDown=1.0-fakerateUncertainty
fileinDir = ["am4", "am5", "am6", "am7", "am8", "am9", "am10", "am11", "am12", "am13", "am14", "am15", "am16", "am17", "am18", "am19", "am20", "am21"]
suffix = ["signalRegion", "sideBand"]

tauDiscVSjet = ["vvlooseDeepVSjet", "vlooseDeepVSjet", "looseDeepVSjet", "mediumDeepVSjet", "tightDeepVSjet", "vtightDeepVSjet", "vvtightDeepVSjet"]

for j,index in enumerate(path):
    for i,ifile in enumerate(fileinDir):
        for iName in tauDiscVSjet:
            finName = index + ifile + "/HAA_MC_" + iName + "Disc.root"
            globals()["fin" + ifile] = ROOT.TFile(finName)
            globals()["treein" + ifile] = globals()["fin" + ifile].Get("TreeMuMuTauTau")

            globals()["dimuMass" + ifile] = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
            globals()["visDiTauMass" + ifile] = ROOT.RooRealVar("visDiTauMass", "visDiTauMass", 0, 60)
            globals()["visFourbodyMass" + ifile] = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
            globals()["eventWeight" + ifile] = ROOT.RooRealVar("eventWeight", "eventWeight", -1, 1)
            #globals()["eventWeightUp" + ifile] = ROOT.RooRealVar("eventWeightUp", "eventWeightUp", -1, 1)
            #globals()["eventWeightDown" + ifile] = ROOT.RooRealVar("eventWeightDown", "eventWeightDown", -1, 1)

            
            globals()["dataColl" + ifile] = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeight" + ifile]))
            # globals()["dataCollUp" + ifile] = ROOT.RooDataSet("dataCollUp", "dataCollUp", ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeightUp" + ifile]))
            # globals()["dataCollDown" + ifile] = ROOT.RooDataSet("dataCollDown", "dataCollDown", ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeightDown" + ifile]))

            for event in globals()["treein" + ifile]:
                globals()["dimuMass" + ifile].setVal(event.invMassMuMu)
                globals()["visDiTauMass" + ifile].setVal(event.visMassTauTau)
                globals()["visFourbodyMass" + ifile].setVal(event.visMassMuMuTauTau)
                globals()["eventWeight" + ifile].setVal(event.eventWeight*scale*higgs_xsec*lumi_2017)
                globals()["dataColl" + ifile].add(ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeight" + ifile]))
            
            globals()["fout" + ifile] = ROOT.TFile(outputDir+"TauMuTauHad_HaaMC_" + ifile + "_" + suffix[j] + "_" + iName + ".root", "RECREATE")
            globals()["dataColl" + ifile].Write()
            globals()["fout" + ifile].Close()
            
            for event in globals()["treein" + ifile]:
                globals()["dimuMass" + ifile].setVal(event.invMassMuMu)
                globals()["visDiTauMass" + ifile].setVal(event.visMassTauTau)
                globals()["visFourbodyMass" + ifile].setVal(event.visMassMuMuTauTau)
                globals()["eventWeight" + ifile].setVal(event.eventWeight*scale*higgs_xsec*lumi_2017*scaleUp)
                globals()["dataColl" + ifile].add(ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeight" + ifile]))
  
            
            
            globals()["foutUp" + ifile] = ROOT.TFile(outputDir+"TauMuTauHad_HaaMC_" + ifile + "_" + suffix[j] + "_" + iName + "_" + "fakeUp" +".root", "RECREATE")
            globals()["dataColl" + ifile].Write()
            globals()["foutUp" + ifile].Close()
            
            for event in globals()["treein" + ifile]:
                globals()["dimuMass" + ifile].setVal(event.invMassMuMu)
                globals()["visDiTauMass" + ifile].setVal(event.visMassTauTau)
                globals()["visFourbodyMass" + ifile].setVal(event.visMassMuMuTauTau)
                globals()["eventWeight" + ifile].setVal(event.eventWeight*scale*higgs_xsec*lumi_2017*scaleDown)
                globals()["dataColl" + ifile].add(ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeight" + ifile]))

            
            globals()["foutDown" + ifile] = ROOT.TFile(outputDir+"TauMuTauHad_HaaMC_" + ifile + "_" + suffix[j] + "_" + iName +"_"+ "fakeDown" +".root", "RECREATE")
            globals()["dataColl" + ifile].Write()
            globals()["foutDown" + ifile].Close()

            
