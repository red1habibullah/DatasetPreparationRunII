#!/usr/bin/python
import ROOT
from ROOT import RooFit








fakebaseDir='/afs/cern.ch/user/r/rhabibul/DatasetPrepRunII_Boosted/CMSSW_12_0_0_pre4/src/DatasetPreparationRunII/data/'
baseDir = "/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/dataSideband/"
outputDir= "/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauMuTauHad/"

#'/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauETauHad/RooDataSets/DataSystematics/'
years=["2016","2017","2018"]
dmodes=["decayMode0","decayMode1","decayMode10"]

dmodematch={
    "decayMode0":0.0,
    "decayMode1":1.0,
    "decayMode10":10.0
}

#fakeRateUncertainty=0.2
#scaleUp=1.0+fakeRateUncertainty
#scaleDown = 1.0- fakeRateUncertainty


for iy,y in enumerate(years):
    print baseDir+y+"/"+"All_"+y+"_sideBand_nominal.root"
    fin=ROOT.TFile(baseDir+y+"/Histogram/"+"All_"+y+"_sideBand_nominal.root")
    treein = fin.Get("TreeMuTau")
    invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
    visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
    fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    
    dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))
    
    for event in treein:
        for id,d in enumerate(dmodes): 
            finFakeEff = ROOT.TFile(fakebaseDir+y+"/"+"fakeTauEff_TauMuTauHad.root")
            histFakeEff = ROOT.TH1D()
            histFakeEff = finFakeEff.Get(d)
            nbins = histFakeEff.GetNbinsX()
             
            for ibin in xrange(nbins):
                binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
                binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
                print "decayMode from tau in event ",event.tauDM_mt
                print "decayMode from file ",dmodematch[d]
                if event.tauDM_mt == dmodematch[d] and (event.tauPt_mt >= binlowEdge and event.tauPt_mt < binhighEdge):
                    print "match"
                    fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1))
                # else:
                #     print "unmatch- skip"                 
        invMassMuMu.setVal(event.invMassMu1Mu2_mt)
        visFourbodyMass.setVal(event.visMass3MuTau_mt)
        dataColl.add(ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))





    fout = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauMuTauHad" + "_"+y+"_MVAMedium_" +"signalRegion_nominal.root", "RECREATE")
    dataColl.Write()
    fout.Close()
    
    foutcopy = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauMuTauHad" + "_"+y+"_MVAMedium_" +"sideBand_nominal.root", "RECREATE")
    dataColl.Write()
    foutcopy.Close()
   







exit()




# for i,ifile in enumerate(tauDiscVSjet):
#     fin = ROOT.TFile(fileinDir + tauVSjetNumerator[i] + ".root")
#     treein = fin.Get("TreeMuMuTauTau")

#     invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
#     visDiTauMass = ROOT.RooRealVar("visDiTauMass", "visDiTauMass", 0, 60)
#     visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
#     fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    
#     dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))

#     for event in treein:
#         finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauETauHad.root")
#         histFakeEff = ROOT.TH1D()
#         histFakeEff = finFakeEff.Get(ifile)

#         nbins = histFakeEff.GetNbinsX()
#         for ibin in xrange(nbins):
#             binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
#             binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
#             if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
#                 fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1))

#         invMassMuMu.setVal(event.invMassMuMu)
#         visDiTauMass.setVal(event.visMassTauTau)
#         visFourbodyMass.setVal(event.visMassMuMuTauTau)
#         dataColl.add(ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))

#     fout = ROOT.TFile(outputDir+"TauMuTauHad" + "_"+ "signalRegion"+"_"+ifile + ".root", "RECREATE")
#     dataColl.Write()
#     fout.Close()
    
#     foutcopy= ROOT.TFile(outputDir+"TauETauHad" + "_"+ "sideBand"+"_"+ifile + ".root", "RECREATE")
#     dataColl.Write()
#     foutcopy.Close()

    
    # for event in treein:
    #     finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauETauHad.root")
    #     histFakeEff = ROOT.TH1D()
    #     histFakeEff = finFakeEff.Get(ifile)

    #     nbins = histFakeEff.GetNbinsX()
    #     for ibin in xrange(nbins):
    #         binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
    #         binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
    #         if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
    #             fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1)*scaleUp)
                
    #     invMassMuMu.setVal(event.invMassMuMu)
    #     visDiTauMass.setVal(event.visMassTauTau)
    #     visFourbodyMass.setVal(event.visMassMuMuTauTau)
    #     dataColl.add(ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))
    # foutUp =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "signalRegion"+"_"+ifile +"_" + "fakeUp" + ".root", "RECREATE")
    # dataColl.Write()
    # foutUp.Close()
    
    # foutUpcopy =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "sideBand"+"_"+ifile +"_" + "fakeUp" + ".root", "RECREATE")
    # dataColl.Write()
    # foutUpcopy.Close()
    
    
    # for event in treein:
    #     finFakeEff = ROOT.TFile(fakeDir+"fakeTauEff_TauETauHad.root")
    #     histFakeEff = ROOT.TH1D()
    #     histFakeEff = finFakeEff.Get(ifile)

    #     nbins = histFakeEff.GetNbinsX()
    #     for ibin in xrange(nbins):
    #         binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
    #         binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
    #         if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
    #             fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1)*scaleDown)

    #     invMassMuMu.setVal(event.invMassMuMu)
    #     visDiTauMass.setVal(event.visMassTauTau)
    #     visFourbodyMass.setVal(event.visMassMuMuTauTau)
    #     dataColl.add(ROOT.RooArgSet(invMassMuMu, visDiTauMass, visFourbodyMass, fakeRateEfficiency))
    # foutDown =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "signalRegion"+"_"+ifile +"_" + "fakeDown" + ".root", "RECREATE")
    # dataColl.Write()
    # foutDown.Close()

    # foutDowncopy =  ROOT.TFile(outputDir+"TauETauHad" + "_"+ "sideBand"+"_"+ifile +"_" + "fakeDown" + ".root", "RECREATE")
    # dataColl.Write()
    # foutDowncopy.Close()

