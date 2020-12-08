#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


muIdList = ["loose", "medium", "tight"]
muIdLabel = ["looseMuIso", "mediumMuIso", "tightMuIso"]

eleIdList = ["loose", "medium", "tight"]
eleIdLabel = ["looseEleId", "mediumEleId", "tightEleId"]

#histList = ["deltaRTauTau", "Tau1Pt", "Tau2Pt", "invMassMuMu", "visMassMuMuTauTau"]
histList =["invMassMuMu"]
histLabel = ["#DeltaR(#mu_{3}e)", "p_{T}(#mu_{3})[GeV]", "p_{T}(e)[GeV]", "M(#mu_{1}#mu_{2})[GeV]", "M(3#mue)[GeV]"]
binning = array.array('d', [3, 10, 20, 30, 50, 100, 200])

Colors = [ROOT.kBlue, ROOT.kMagenta, ROOT.kRed, ROOT.kOrange, ROOT.kGreen+1, ROOT.kGreen-8, ROOT.kCyan-7, ROOT.kOrange+3]

label1 = ROOT.TLatex(0.21,0.87, "CMS")
label1.SetNDC()
label1.SetTextSize(0.03)

label2 = ROOT.TLatex(0.19,0.96, "#sqrt{s} = 13 TeV, Lumi = 41.529 fb^{-1} (2017)")
label2.SetNDC()
label2.SetTextFont(42)
label2.SetTextSize(0.04)

label3 = ROOT.TLatex(0.21,0.82, "Preliminary")
label3.SetNDC()
label3.SetTextFont(52)
label3.SetTextSize(0.03)

inputDir='/eos/uscms/store/user/zfwd666/2017/bkgEffCheck/TauMuTauE/'
outputDirData='/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauMuTauE/RooDatasets/Data/'
outputDirDataDriven='/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauMuTauE/RooDatasets/DataDriven/'
inputFakeEleFile = ROOT.TFile("../data/fakeTauEff_TauETauE.root")

inputFakeMuFile = ROOT.TFile("../data/fakeTauEff_TauMuTauMu.root")

for j,imuid in enumerate(muIdList):

    for k,ieleid in enumerate(eleIdList):

        for ihist,histKey in enumerate(histList):

            # ===========  prepare the canvas for comparison  ===============
            canvas = ROOT.TCanvas("comparison","data",900,900)
            canvas.cd()
            canvas.SetTopMargin(0.06)
            canvas.SetLeftMargin(0.16)
            canvas.SetBottomMargin(0.14)
            # ==============================================================

            legend = ROOT.TLegend(0.55,0.74,0.95,0.94)
            legend.SetFillColor(0)
            legend.SetTextSize(0.04)

            globals()["data3P1F1File" + str(j) + str(k)] = ROOT.TFile(inputDir+"3P1F1_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root")
            globals()["data3P1F2File" + str(j) + str(k)] = ROOT.TFile(inputDir+"3P1F2_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root")
            globals()["data2P2FFile" + str(j) + str(k)] = ROOT.TFile(inputDir+"2P2F_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root")
            globals()["zz3P1F1File" + str(j) + str(k)] = ROOT.TFile(inputDir+"3P1F1_" + "MuIso_" + imuid + "_EleId_" + ieleid + "_zz.root")
            globals()["zz3P1F2File" + str(j) + str(k)] = ROOT.TFile(inputDir+"3P1F2_" + "MuIso_" + imuid + "_EleId_" + ieleid + "_zz.root")
            globals()["zz4PFile" + str(j) + str(k)] = ROOT.TFile(inputDir+"4P_" + "MuIso_" + imuid + "_EleId_" + ieleid + "_zz.root")
            #print "1"
            globals()["data3P1F1Tree" + str(j) + str(k)] = globals()["data3P1F1File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["data3P1F2Tree" + str(j) + str(k)] = globals()["data3P1F2File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["data2P2FTree" + str(j) + str(k)] = globals()["data2P2FFile" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["zz3P1F1Tree" + str(j) + str(k)] = globals()["zz3P1F1File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["zz3P1F2Tree" + str(j) + str(k)] = globals()["zz3P1F2File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["zz4PTree" + str(j) + str(k)] = globals()["zz4PFile" + str(j) + str(k)].Get("TreeMuMuTauTau")
            #print"2"

            histFakeMuEff = inputFakeMuFile.Get(muIdLabel[j])
            histFakeEleEff = inputFakeEleFile.Get(eleIdLabel[k])

            #Final Extrapolated DataHist in Signal Region
            globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D()
            #Data on sideband FP
            globals()["data3P1F1HistOnly" + str(j) + str(k)] = ROOT.TH1D()

            globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D()
            #Data on sideband2 FF
            globals()["data2P2FHistOnly" + str(j) + str(k)] = ROOT.TH1D()
            globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D()

            
            if "invMassMuMu" in histKey:
                globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(histKey + "3P1F1",histKey+"3P1F1", 10, 0, 60)
                globals()["data3P1F1HistOnly" + str(j) + str(k)] = ROOT.TH1D(histKey+"3P1F1Only",histKey + "3P1F1Only", 10, 0, 60)
                globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(histKey+"3P1F2", histKey+"3P1F2", 10, 0, 60)
                globals()["data2P2FHistOnly" + str(j) + str(k)] = ROOT.TH1D(histKey+"2P2FOnly",histKey+ "2P2FOnly", 10, 0, 60)
                globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D(histKey+"2P2F",histKey+"2P2F", 10, 0, 60)
                globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D(histKey+"2P2Fext",histKey+"2P2Fext", 10, 0, 60)
                globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(histKey+"zz3P1F1",histKey+"zz3P1F1", 10, 0, 60)
                globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(histKey + "zz3P1F2",histKey+"zz3P1F2", 10, 0, 60)
                globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D(histKey+"zz4P",histKey+"zz4P", 10, 0, 60)
                #####################


            
            for event in globals()["data3P1F1Tree" + str(j) + str(k)]:

                fakeEff = 1.0
                nbins = histFakeEleEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                        fakeEff = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))

            
                if "invMassMuMu" in histKey:
                    globals()["data3P1F1Hist" + str(j) + str(k)].Fill(event.invMassMuMu, fakeEff)
                    #globals()["data3P1F1HistOnly" + str(j) + str(k)].Fill(event.invMassMuMu)
            
            # globals()["data3P1F1Hist" + str(j) + str(k)].Sumw2()
            # globals()["data3P1F1Hist" + str(j) + str(k)].SetStats(0)
            # globals()["data3P1F1HistOnly" + str(j) + str(k)].Sumw2()
            # globals()["data3P1F1HistOnly" + str(j) + str(k)].SetStats(0)


            for event in globals()["data3P1F2Tree" + str(j) + str(k)]:

                fakeEff = 1.0
                nbins = histFakeMuEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau1Pt >= binlowEdge and event.Tau1Pt < binhighEdge):
                        fakeEff = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

            
                if "invMassMuMu" in histKey:
                    globals()["data3P1F2Hist" + str(j) + str(k)].Fill(event.invMassMuMu, fakeEff)
                    
            
            # globals()["data3P1F2Hist" + str(j) + str(k)].Sumw2()
            # globals()["data3P1F2Hist" + str(j) + str(k)].SetStats(0)
            
            
            
            for event in globals()["data2P2FTree" + str(j) + str(k)]:
                if "invMassMuMu" in histKey:
                    globals()["data2P2FHistOnly" + str(j) + str(k)].Fill(event.invMassMuMu)
            
            # globals()["data2P2FHistOnly" + str(j) + str(k)].Sumw2()
            # globals()["data2P2FHistOnly" + str(j) + str(k)].SetStats(0)



            for event in globals()["data2P2FTree" + str(j) + str(k)]:

                fakeEff1 = 0.5
                fakeEff2 = 0.5
                fakeEff = 1.0
                nbinsMu = histFakeMuEff.GetNbinsX()
                nbinsEle = histFakeEleEff.GetNbinsX()

                for ibin in xrange(nbinsMu):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau1Pt >= binlowEdge and event.Tau1Pt < binhighEdge):
                        fakeEff1 = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

                for ibin in xrange(nbinsEle):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                        fakeEff2 = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))
                        fakeEff = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))


            
                if "invMassMuMu" in histKey:
                    globals()["data2P2FHist" + str(j) + str(k)].Fill(event.invMassMuMu, (fakeEff1 + fakeEff2)*fakeEff)
                    globals()["data3P1F1HistOnly" + str(j) + str(k)].Fill(event.invMassMuMu,(fakeEff1+fakeEff2))  


            for event in globals()["data2P2FTree" + str(j) + str(k)]:

                fakeEff1 = 1.0
                fakeEff2 = 1.0
                nbinsMu = histFakeMuEff.GetNbinsX()
                nbinsEle = histFakeEleEff.GetNbinsX()

                for ibin in xrange(nbinsMu):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau1Pt >= binlowEdge and event.Tau1Pt < binhighEdge):
                        fakeEff1 = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

                for ibin in xrange(nbinsEle):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                        fakeEff2 = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))


            
                if "invMassMuMu" in histKey:
                    globals()["data2P2FextHist" + str(j) + str(k)].Fill(event.invMassMuMu, fakeEff1*fakeEff2)

            

            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["data2P2FHist" + str(j) + str(k)], -1)
            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["data2P2FextHist" + str(j) + str(k)])
            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["data3P1F2Hist" + str(j) + str(k)])
            
            #globals()["data3P1F1HistOnly" + str(j) + str(k)].Add(globals()["data2P2FHist" + str(j) + str(k)], -1)


            nbins = globals()["data3P1F1Hist" + str(j) + str(k)].GetNbinsX()
            for ibin in xrange(nbins):
                binValue = globals()["data3P1F1Hist" + str(j) + str(k)].GetBinContent(ibin+1)
                if binValue < 0:
                    print "***** negative bins: ", binValue
                    globals()["data3P1F1Hist" + str(j) + str(k)].SetBinContent(ibin+1, 0)  
                    binval = globals()["data3P1F1Hist" + str(j) + str(k)].GetBinContent(ibin+1)
                    print " ###### changed bins: ", binval
            globals()["fout1" + str(j) + str(k) ] = ROOT.TFile(outputDirData+"TauMuTauE_" + "sideBand" + "_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root", "RECREATE")
            globals()["fout2" + str(j) + str(k) ] = ROOT.TFile(outputDirData+"TauMuTauE_" + "sideBand2" + "_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root", "RECREATE")
            globals()["fout3" + str(j) + str(k) ] = ROOT.TFile(outputDirDataDriven+"TauMuTauE_" + "signalRegion" + "_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root", "RECREATE")
            
            globals()["fout1" + str(j) + str(k) ].cd()
            globals()["data3P1F1HistOnly" + str(j) + str(k)].Write()
            globals()["fout1" + str(j) + str(k) ].Close()

            globals()["fout2" + str(j) + str(k) ].cd()
            globals()["data2P2FHistOnly" + str(j) + str(k)].Write()
            globals()["fout2" + str(j) + str(k) ].Close()

            globals()["fout3" + str(j) + str(k) ].cd()
            globals()["data3P1F1Hist" + str(j) + str(k)].Write()
            globals()["fout3" + str(j) + str(k) ].Close()

