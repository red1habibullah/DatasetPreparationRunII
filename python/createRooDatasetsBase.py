#!/usr/bin/python
import ROOT
from ROOT import RooFit

signalDir = "/eos/uscms/store/user/zfwd666/HAA/DeepTauID/TauMuTauHad/slimmedTausMuonCleanedDeep/"
sidebandDir = "/eos/uscms/store/user/zfwd666/HAA/DeepTauID/TauMuTauHad/sideband/"

path = [signalDir, sidebandDir]

scale =0.001
higgs_xsec=48.58
lumi_2017=41.529*1000
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
            globals()["dataColl" + ifile] = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeight" + ifile]))

            for event in globals()["treein" + ifile]:
                globals()["dimuMass" + ifile].setVal(event.invMassMuMu)
                globals()["visDiTauMass" + ifile].setVal(event.visMassTauTau)
                globals()["visFourbodyMass" + ifile].setVal(event.visMassMuMuTauTau)
                globals()["eventWeight" + ifile].setVal(event.eventWeight)
                globals()["dataColl" + ifile].add(ROOT.RooArgSet(globals()["dimuMass" + ifile], globals()["visDiTauMass" + ifile], globals()["visFourbodyMass" + ifile], globals()["eventWeight" + ifile]))

            globals()["fout" + ifile] = ROOT.TFile("TauMuTauHad_HaaMC_" + ifile + "_" + iName + "_" + suffix[j] + ".root", "RECREATE")
            globals()["dataColl" + ifile].Write()
            globals()["fout" + ifile].Close()
