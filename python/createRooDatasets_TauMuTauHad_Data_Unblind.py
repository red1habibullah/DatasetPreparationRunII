#!/usr/bin/python
import ROOT
from ROOT import RooFit






fakebaseDir='/afs/cern.ch/user/r/rhabibul/DatasetPrepRunII_Boosted/CMSSW_10_2_13/src/DatasetPreparationRunII/data/'
baseDir = "/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/dataSideband/"
outputDir= "/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauMuTauHad_Order2/"

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
    finSignal=ROOT.TFile(baseDir+y+"/Histogram/"+"All_"+y+"_signalRegion_nominal.root")
    
    treein = fin.Get("TreeMuTau")
    treeinSignal = finSignal.Get("TreeMuTau")
    print "got trees"
    print type(treeinSignal)
    invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
    visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
    fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    
    dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))
    dataCollSignal = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))

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
        if event.mu2Pt_mt > event.mu3Pt_mt:
            invMassMuMu.setVal(event.invMassMu1Mu2_mt)
            visFourbodyMass.setVal(event.visMass3MuTau_mt)
            dataColl.add(ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))
  
    for event in treeinSignal:
        # for id,d in enumerate(dmodes): 
        #     finFakeEff = ROOT.TFile(fakebaseDir+y+"/"+"fakeTauEff_TauMuTauHad.root")
        #     histFakeEff = ROOT.TH1D()
        #     histFakeEff = finFakeEff.Get(d)
        #     nbins = histFakeEff.GetNbinsX()
             
        #     for ibin in xrange(nbins):
        #         binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
        #         binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
        #         print "decayMode from tau in event ",event.tauDM_mt
        #         print "decayMode from file ",dmodematch[d]
        #         if event.tauDM_mt == dmodematch[d] and (event.tauPt_mt >= binlowEdge and event.tauPt_mt < binhighEdge):
        #             print "match"
        #             fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1))
                # else:
                #     print "unmatch- skip"                 
        if event.mu2Pt_mt > event.mu3Pt_mt:
            invMassMuMu.setVal(event.invMassMu1Mu2_mt)
            visFourbodyMass.setVal(event.visMass3MuTau_mt)
            fakeRateEfficiency.setVal(1.0)
            dataCollSignal.add(ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))
  
    



    foutSignal = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauMuTauHad_Order2" + "_"+y+"_MVAMedium_" +"signalRegionUnblind_nominal.root", "RECREATE")
    dataCollSignal.Write()
    foutSignal.Close()
    
    fout = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauMuTauHad_Order2" + "_"+y+"_MVAMedium_" +"sideBand_nominal.root", "RECREATE")
    dataColl.Write()
    fout.Close()
   







exit()



