#!/usr/bin/python
import ROOT
from ROOT import RooFit

tauVSjetNumerator = ["deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vvloose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vloose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_loose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_tight", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vtight", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vvtight"]
tauDiscVSjet = ["vvlooseDeepVSjet", "vlooseDeepVSjet", "looseDeepVSjet", "mediumDeepVSjet", "tightDeepVSjet", "vtightDeepVSjet", "vvtightDeepVSjet"]

fileinDir = "/eos/uscms/store/user/zfwd666/2017/bkgEffCheck/TauMuTauHad/"

for i,ifile in enumerate(tauDiscVSjet):
    fin = ROOT.TFile(fileinDir + tauVSjetNumerator[i] + ".root")
    treein = fin.Get("TreeMuMuTauTau")

    invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
    visDiTauMass = ROOT.RooRealVar("visDiTauMass", "visDiTauMass", 0, 60)
    visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
    fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))

    for event in treein:
        finFakeEff = ROOT.TFile("fakeTauEff_TauMuTauHad.root")
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

    fout = ROOT.TFile(ifile + ".root", "RECREATE")
    dataColl.Write()
    fout.Close()
