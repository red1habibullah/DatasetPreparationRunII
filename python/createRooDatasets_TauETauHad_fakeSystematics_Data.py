#!/usr/bin/python
import ROOT
from ROOT import RooFit

tauVSjetNumerator = ["deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vvloose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vloose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_loose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_tight", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vtight", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vvtight"]
tauDiscVSjet = ["vvlooseDeepVSjet", "vlooseDeepVSjet", "looseDeepVSjet", "mediumDeepVSjet", "tightDeepVSjet", "vtightDeepVSjet", "vvtightDeepVSjet"]
fakeDir='/uscms_data/d3/zfwd666/MuMuTauTauAnalyzer/CMSSW_9_4_13/src/MuMuTauTauAnalyzer/2017/DeepTauID/bkgEffCheck/TauETauHad/RooDatasets/'
fileinDir = "/eos/uscms/store/user/zfwd666/2017/bkgEffCheck/TauETauHad/"
#TauMuTauHad_sideBand_vvlooseDeepVSjet.root
outputDir='/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauETauHad/RooDataSets/DataSystematics/'
fakeRateUncertainty=0.2
scaleUp=1.0+fakeRateUncertainty
scaleDown = 1.0- fakeRateUncertainty
for i,ifile in enumerate(tauDiscVSjet):
    fin = ROOT.TFile(fileinDir + tauVSjetNumerator[i] + ".root")
    treein = fin.Get("TreeMuMuTauTau")

    invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
    visDiTauMass = ROOT.RooRealVar("visDiTauMass", "visDiTauMass", 0, 60)
    visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
    fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    
    dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))

    for event in treein:
        finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauETauHad.root")
        histFakeEff = ROOT.TH1D()
        histFakeEff = finFakeEff.Get(ifile)

        nbins = histFakeEff.GetNbinsX()
        for ibin in xrange(nbins):
            binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
            binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
            if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1))

        invMassMuMu.setVal(event.invMassMuMu)
        visDiTauMass.setVal(event.visMassTauTau)
        visFourbodyMass.setVal(event.visMassMuMuTauTau)
        dataColl.add(ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))

    fout = ROOT.TFile(outputDir+"TauETauHad" + "_"+ "signalRegion"+"_"+ifile + ".root", "RECREATE")
    dataColl.Write()
    fout.Close()
    
    foutcopy= ROOT.TFile(outputDir+"TauETauHad" + "_"+ "sideBand"+"_"+ifile + ".root", "RECREATE")
    dataColl.Write()
    foutcopy.Close()

    
    for event in treein:
        finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauETauHad.root")
        histFakeEff = ROOT.TH1D()
        histFakeEff = finFakeEff.Get(ifile)

        nbins = histFakeEff.GetNbinsX()
        for ibin in xrange(nbins):
            binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
            binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
            if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1)*scaleUp)
                
        invMassMuMu.setVal(event.invMassMuMu)
        visDiTauMass.setVal(event.visMassTauTau)
        visFourbodyMass.setVal(event.visMassMuMuTauTau)
        dataColl.add(ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))
    foutUp =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "signalRegion"+"_"+ifile +"_" + "fakeUp" + ".root", "RECREATE")
    dataColl.Write()
    foutUp.Close()
    
    foutUpcopy =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "sideBand"+"_"+ifile +"_" + "fakeUp" + ".root", "RECREATE")
    dataColl.Write()
    foutUpcopy.Close()
    
    
    for event in treein:
        finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauETauHad.root")
        histFakeEff = ROOT.TH1D()
        histFakeEff = finFakeEff.Get(ifile)

        nbins = histFakeEff.GetNbinsX()
        for ibin in xrange(nbins):
            binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
            binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
            if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1)*scaleDown)

        invMassMuMu.setVal(event.invMassMuMu)
        visDiTauMass.setVal(event.visMassTauTau)
        visFourbodyMass.setVal(event.visMassMuMuTauTau)
        dataColl.add(ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))
    foutDown =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "signalRegion"+"_"+ifile +"_" + "fakeDown" + ".root", "RECREATE")
    dataColl.Write()
    foutDown.Close()

    foutDowncopy =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "sideBand"+"_"+ifile +"_" + "fakeDown" + ".root", "RECREATE")
    dataColl.Write()
    foutDowncopy.Close()



