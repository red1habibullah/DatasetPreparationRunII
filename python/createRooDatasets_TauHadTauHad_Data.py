#!/usr/bin/python
import ROOT
from ROOT import RooFit



fakebaseDir='/afs/cern.ch/user/r/rhabibul/DatasetPrepRunII_Boosted/CMSSW_10_2_13/src/DatasetPreparationRunII/data/'
baseDir = "/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/dataSideband/"
outputDir= "/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauHadTauHad/"

#'/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauETauHad/RooDataSets/DataSystematics/'
years=["2016","2017","2018"]
disc=["DeepDiTauDCM=0.7;1"]

dmodematch={
    "decayMode0":0.0,
    "decayMode1":1.0,
    "decayMode10":10.0
}



for iy,y in enumerate(years):
    print baseDir+y+"/"+"All_"+y+"_sideBand_nominal.root"
    fin=ROOT.TFile(baseDir+y+"/Histogram/"+"All_"+y+"_sideBand_nominal.root")
    treein = fin.Get("TreeTauTau")
    invMassMuMu = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
    visFourbodyMass = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
    fakeRateEfficiency = ROOT.RooRealVar("fakeRateEfficiency", "fakeRateEfficiency", 0, 1)
    
    dataColl = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))
    
    for event in treein:
        for id,d in enumerate(disc): 
            finFakeEff = ROOT.TFile(fakebaseDir+y+"/"+"fakeTauEff_TauHadTauHad.root")
            histFakeEff = ROOT.TH1D()
            histFakeEff = finFakeEff.Get(d)
            #print "got histfake"
            nbins = histFakeEff.GetNbinsX()
             
            for ibin in xrange(nbins):
                binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
                binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
                #print "decayMode from tau in event ",event.tauDM_mt
                #print "decayMode from file ",dmodematch[d]
                if (event.tau2Pt_tt >= binlowEdge and event.tau2Pt_tt < binhighEdge):
                    print "match"
                    fakeRateEfficiency.setVal(histFakeEff.GetBinContent(ibin+1))
                # else:
                #     print "unmatch- skip"                 
        #if event.mu1Pt_mt > event.mu3Pt_mt:
        invMassMuMu.setVal(event.invMassMu1Mu2_tt)
        visFourbodyMass.setVal(event.visMass2Mu2Tau_tt)
        dataColl.add(ROOT.RooArgSet(invMassMuMu, visFourbodyMass, fakeRateEfficiency))





    fout = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauHadTauHad" + "_"+y+"_MVAMedium_" +"signalRegion_nominal.root", "RECREATE")
    dataColl.Write()
    fout.Close()
    
    foutcopy = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauHadTauHad" + "_"+y+"_MVAMedium_" +"sideBand_nominal.root", "RECREATE")
    dataColl.Write()
    foutcopy.Close()
    print "done!"







exit()



