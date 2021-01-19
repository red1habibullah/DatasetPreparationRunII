#!/usr/bin/python
import ROOT
from ROOT import RooFit

fakeDir='/eos/uscms/store/user/zfwd666/2017/bkgEffCheck/TauHadTauHad/'

fileinDir = "/eos/uscms/store/user/zfwd666/2017/bkgEffCheck/TauHadTauHad/"

outputDir="/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauHadTauHad/RooDatasets/DataDrivenSystematics/"
fakeRateUncertainty=0.2
scaleUp=1.0+fakeRateUncertainty
scaleDown = 1.0- fakeRateUncertainty

#TauMuTauHad_sideBand_looseDeepVSjet.root             
#TauMuTauHad_signalRegion_looseDeepVSjet.root

mlDisc= ["0.3","0.4","0.5","0.6","0.7","0.8","0.9"]


for i,ifile in enumerate(mlDisc):
    fin = ROOT.TFile(fileinDir + "deepDiTauRaw_" + ifile +".root")
    print fin
    treein = fin.Get("TreeMuMuTauTau")

    invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
    visDiTauMass = ROOT.RooRealVar("visDiTauMass", "visDiTauMass", 0, 60)
    visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
    fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    
    dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))
    plotname= "DiTauIso=" + ifile
    print plotname
    for event in treein:
        finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauHadTauHad.root")
        histFakeEff = ROOT.TH1D()
        
        
        histFakeEff = finFakeEff.Get(plotname)

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

    fout = ROOT.TFile(outputDir+"TauHadTauHad" + "_"+ "signalRegion"+"_"+ifile + ".root", "RECREATE")
    dataColl.Write()
    fout.Close()
    
    foutcopy= ROOT.TFile(outputDir+"TauHadTauHad" + "_"+ "sideBand"+"_"+ifile + ".root", "RECREATE")
    dataColl.Write()
    foutcopy.Close()

    
    for event in treein:
        finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauHadTauHad.root")
        histFakeEff = ROOT.TH1D()
        histFakeEff = finFakeEff.Get(plotname)

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
    foutUp =  ROOT.TFile(outputDir+"TauHadTauHad" + "_"+ "signalRegion"+"_"+ifile +"_" + "fakeUp" + ".root", "RECREATE")
    dataColl.Write()
    foutUp.Close()
    
    foutUpcopy =  ROOT.TFile(outputDir+"TauHadTauHad" + "_"+ "sideBand"+"_"+ifile +"_" + "fakeUp" + ".root", "RECREATE")
    dataColl.Write()
    foutUpcopy.Close()
    
    
    for event in treein:
        finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauHadTauHad.root")
        histFakeEff = ROOT.TH1D()
        histFakeEff = finFakeEff.Get(plotname)

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
    foutDown =  ROOT.TFile(outputDir+"TauHadTauHad" + "_"+ "signalRegion"+"_"+ifile +"_" + "fakeDown" + ".root", "RECREATE")
    dataColl.Write()
    foutDown.Close()

    foutDowncopy =  ROOT.TFile(outputDir+"TauHadTauHad" + "_"+ "sideBand"+"_"+ifile +"_" + "fakeDown" + ".root", "RECREATE")
    dataColl.Write()
    foutDowncopy.Close()



