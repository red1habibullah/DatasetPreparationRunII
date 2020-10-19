#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

muIdList = ["loose", "medium", "tight"]
muIdLabel = ["looseMuIso", "mediumMuIso", "tightMuIso"]

eleIdList = ["loose", "medium", "tight"]
eleIdLabel = ["looseEleId", "mediumEleId", "tightEleId"]

histList = ["deltaRTauTau", "Tau1Pt", "Tau2Pt", "invMassMuMu", "visMassMuMuTauTau"]
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

inputFakeEleFile = ROOT.TFile("fakeTauEff_TauETauE.root")
inputFakeMuFile = ROOT.TFile("fakeTauEff_TauMuTauMu.root")

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

            globals()["data3P1F1File" + str(j) + str(k)] = ROOT.TFile("3P1F1_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root")
            globals()["data3P1F2File" + str(j) + str(k)] = ROOT.TFile("3P1F2_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root")
            globals()["data2P2FFile" + str(j) + str(k)] = ROOT.TFile("2P2F_" + "MuIso_" + imuid + "_EleId_" + ieleid + ".root")
            globals()["zz3P1F1File" + str(j) + str(k)] = ROOT.TFile("3P1F1_" + "MuIso_" + imuid + "_EleId_" + ieleid + "_zz.root")
            globals()["zz3P1F2File" + str(j) + str(k)] = ROOT.TFile("3P1F2_" + "MuIso_" + imuid + "_EleId_" + ieleid + "_zz.root")
            globals()["zz4PFile" + str(j) + str(k)] = ROOT.TFile("4P_" + "MuIso_" + imuid + "_EleId_" + ieleid + "_zz.root")

            globals()["data3P1F1Tree" + str(j) + str(k)] = globals()["data3P1F1File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["data3P1F2Tree" + str(j) + str(k)] = globals()["data3P1F2File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["data2P2FTree" + str(j) + str(k)] = globals()["data2P2FFile" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["zz3P1F1Tree" + str(j) + str(k)] = globals()["zz3P1F1File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["zz3P1F2Tree" + str(j) + str(k)] = globals()["zz3P1F2File" + str(j) + str(k)].Get("TreeMuMuTauTau")
            globals()["zz4PTree" + str(j) + str(k)] = globals()["zz4PFile" + str(j) + str(k)].Get("TreeMuMuTauTau")

            histFakeMuEff = inputFakeMuFile.Get(muIdLabel[j])
            histFakeEleEff = inputFakeEleFile.Get(eleIdLabel[k])

            globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D()
            globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D()

            if "deltaR" in histKey:
                globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1", muIdLabel[j] + eleIdLabel[k] + "3P1F1", 10, 0, 1)
                globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2", muIdLabel[j] + eleIdLabel[k] + "3P1F2", 10, 0, 1)
                globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F", muIdLabel[j] + eleIdLabel[k] + "2P2F", 10, 0, 1)
                globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", 10, 0, 1)
                globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", 10, 0, 1)
                globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", 10, 0, 1)
                globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", 10, 0, 1)

            if "Pt" in histKey:
                globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1", muIdLabel[j] + eleIdLabel[k] + "3P1F1", 5, binning)
                globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2", muIdLabel[j] + eleIdLabel[k] + "3P1F2", 5, binning)
                globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F", muIdLabel[j] + eleIdLabel[k] + "2P2F", 5, binning)
                globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", 5, binning)
                globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", 5, binning)
                globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", 5, binning)
                globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", 5, binning)

            if "invMassMuMu" in histKey:
                globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1", muIdLabel[j] + eleIdLabel[k] + "3P1F1", 20, 0, 60)
                globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2", muIdLabel[j] + eleIdLabel[k] + "3P1F2", 20, 0, 60)
                globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F", muIdLabel[j] + eleIdLabel[k] + "2P2F", 20, 0, 60)
                globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", 20, 0, 60)
                globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", 20, 0, 60)
                globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", 20, 0, 60)
                globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", 20, 0, 60)

            if "visMassMuMuTauTau" in histKey:
                globals()["data3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1", muIdLabel[j] + eleIdLabel[k] + "3P1F1", 20, 10, 1000)
                globals()["data3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2", muIdLabel[j] + eleIdLabel[k] + "3P1F2", 20, 10, 1000)
                globals()["data2P2FHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F", muIdLabel[j] + eleIdLabel[k] + "2P2F", 20, 10, 1000)
                globals()["data2P2FextHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", muIdLabel[j] + eleIdLabel[k] + "2P2F_ext", 20, 10, 1000)
                globals()["zz3P1F1Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F1_ZZ", 20, 10, 1000)
                globals()["zz3P1F2Hist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", muIdLabel[j] + eleIdLabel[k] + "3P1F2_ZZ", 20, 10, 1000)
                globals()["zz4PHist" + str(j) + str(k)] = ROOT.TH1D(muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", muIdLabel[j] + eleIdLabel[k] + "4P_ZZ", 20, 10, 1000)

            for event in globals()["data3P1F1Tree" + str(j) + str(k)]:

                fakeEff = 1.0
                nbins = histFakeEleEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                        fakeEff = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))

                if "deltaR" in histKey:
                    globals()["data3P1F1Hist" + str(j) + str(k)].Fill(event.deltaRTauTau, fakeEff)

                if "Tau1Pt" in histKey:
                    globals()["data3P1F1Hist" + str(j) + str(k)].Fill(event.Tau1Pt, fakeEff)

                if "Tau2Pt" in histKey:
                    globals()["data3P1F1Hist" + str(j) + str(k)].Fill(event.Tau2Pt, fakeEff)

                if "invMassMuMu" in histKey:
                    globals()["data3P1F1Hist" + str(j) + str(k)].Fill(event.invMassMuMu, fakeEff)

                if "visMassMuMuTauTau" in histKey:
                    globals()["data3P1F1Hist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, fakeEff)

            globals()["data3P1F1Hist" + str(j) + str(k)].Sumw2()
            globals()["data3P1F1Hist" + str(j) + str(k)].SetStats(0)
            globals()["data3P1F1Hist" + str(j) + str(k)].SetFillStyle(0)
            globals()["data3P1F1Hist" + str(j) + str(k)].SetLineColor(ROOT.kRed)
            globals()["data3P1F1Hist" + str(j) + str(k)].SetLineWidth(2)
            globals()["data3P1F1Hist" + str(j) + str(k)].GetXaxis().SetTitle(histLabel[ihist])
            globals()["data3P1F1Hist" + str(j) + str(k)].GetXaxis().SetTitleOffset(1.3)
            globals()["data3P1F1Hist" + str(j) + str(k)].GetXaxis().SetTitleSize(0.05)
            globals()["data3P1F1Hist" + str(j) + str(k)].GetXaxis().SetLabelSize(0.04)
            globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetTitle("# Events")
            globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetTitleOffset(1.3)
            globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetTitleSize(0.05)
            globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetLabelSize(0.05)


            for event in globals()["data3P1F2Tree" + str(j) + str(k)]:

                fakeEff = 1.0
                nbins = histFakeMuEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau1Pt >= binlowEdge and event.Tau1Pt < binhighEdge):
                        fakeEff = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

                if "deltaR" in histKey:
                    globals()["data3P1F2Hist" + str(j) + str(k)].Fill(event.deltaRTauTau, fakeEff)

                if "Tau1Pt" in histKey:
                    globals()["data3P1F2Hist" + str(j) + str(k)].Fill(event.Tau1Pt, fakeEff)

                if "Tau2Pt" in histKey:
                    globals()["data3P1F2Hist" + str(j) + str(k)].Fill(event.Tau2Pt, fakeEff)

                if "invMassMuMu" in histKey:
                    globals()["data3P1F2Hist" + str(j) + str(k)].Fill(event.invMassMuMu, fakeEff)

                if "visMassMuMuTauTau" in histKey:
                    globals()["data3P1F2Hist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, fakeEff)

            globals()["data3P1F2Hist" + str(j) + str(k)].Sumw2()
            globals()["data3P1F2Hist" + str(j) + str(k)].SetStats(0)


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


                if "deltaR" in histKey:
                    globals()["data2P2FHist" + str(j) + str(k)].Fill(event.deltaRTauTau, (fakeEff1 + fakeEff2)*fakeEff)

                if "Tau1Pt" in histKey:
                    globals()["data2P2FHist" + str(j) + str(k)].Fill(event.Tau1Pt, (fakeEff1 + fakeEff2)*fakeEff)

                if "Tau2Pt" in histKey:
                    globals()["data2P2FHist" + str(j) + str(k)].Fill(event.Tau2Pt, (fakeEff1 + fakeEff2)*fakeEff)

                if "invMassMuMu" in histKey:
                    globals()["data2P2FHist" + str(j) + str(k)].Fill(event.invMassMuMu, (fakeEff1 + fakeEff2)*fakeEff)

                if "visMassMuMuTauTau" in histKey:
                    globals()["data2P2FHist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, (fakeEff1 + fakeEff2)*fakeEff)

            globals()["data2P2FHist" + str(j) + str(k)].Sumw2()
            globals()["data2P2FHist" + str(j) + str(k)].SetStats(0)


            for event in globals()["zz3P1F1Tree" + str(j) + str(k)]:

                fakeEff = 1.0
                nbins = histFakeEleEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                        fakeEff = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))

                if "deltaR" in histKey:
                    globals()["zz3P1F1Hist" + str(j) + str(k)].Fill(event.deltaRTauTau, event.eventWeight*fakeEff)

                if "Tau1Pt" in histKey:
                    globals()["zz3P1F1Hist" + str(j) + str(k)].Fill(event.Tau1Pt, event.eventWeight*fakeEff)

                if "Tau2Pt" in histKey:
                    globals()["zz3P1F1Hist" + str(j) + str(k)].Fill(event.Tau2Pt, event.eventWeight*fakeEff)

                if "invMassMuMu" in histKey:
                    globals()["zz3P1F1Hist" + str(j) + str(k)].Fill(event.invMassMuMu, event.eventWeight*fakeEff)

                if "visMassMuMuTauTau" in histKey:
                    globals()["zz3P1F1Hist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, event.eventWeight*fakeEff)


            globals()["zz3P1F1Hist" + str(j) + str(k)].SetStats(0)
            globals()["zz3P1F1Hist" + str(j) + str(k)].Sumw2()
            globals()["zz3P1F1Hist" + str(j) + str(k)].Scale(41.529*1.212*1000)


            for event in globals()["zz3P1F2Tree" + str(j) + str(k)]:

                fakeEff = 1.0
                nbins = histFakeMuEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.Tau1Pt >= binlowEdge and event.Tau1Pt < binhighEdge):
                        fakeEff = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

                if "deltaR" in histKey:
                    globals()["zz3P1F2Hist" + str(j) + str(k)].Fill(event.deltaRTauTau, event.eventWeight*fakeEff)

                if "Tau1Pt" in histKey:
                    globals()["zz3P1F2Hist" + str(j) + str(k)].Fill(event.Tau1Pt, event.eventWeight*fakeEff)

                if "Tau2Pt" in histKey:
                    globals()["zz3P1F2Hist" + str(j) + str(k)].Fill(event.Tau2Pt, event.eventWeight*fakeEff)

                if "invMassMuMu" in histKey:
                    globals()["zz3P1F2Hist" + str(j) + str(k)].Fill(event.invMassMuMu, event.eventWeight*fakeEff)

                if "visMassMuMuTauTau" in histKey:
                    globals()["zz3P1F2Hist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, event.eventWeight*fakeEff)


            globals()["zz3P1F2Hist" + str(j) + str(k)].SetStats(0)
            globals()["zz3P1F2Hist" + str(j) + str(k)].Sumw2()
            globals()["zz3P1F2Hist" + str(j) + str(k)].Scale(41.529*1.212*1000)


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


                if "deltaR" in histKey:
                    globals()["data2P2FextHist" + str(j) + str(k)].Fill(event.deltaRTauTau, fakeEff1*fakeEff2)

                if "Tau1Pt" in histKey:
                    globals()["data2P2FextHist" + str(j) + str(k)].Fill(event.Tau1Pt, fakeEff1*fakeEff2)

                if "Tau2Pt" in histKey:
                    globals()["data2P2FextHist" + str(j) + str(k)].Fill(event.Tau2Pt, fakeEff1*fakeEff2)

                if "invMassMuMu" in histKey:
                    globals()["data2P2FextHist" + str(j) + str(k)].Fill(event.invMassMuMu, fakeEff1*fakeEff2)

                if "visMassMuMuTauTau" in histKey:
                    globals()["data2P2FextHist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, fakeEff1*fakeEff2)

            globals()["data2P2FextHist" + str(j) + str(k)].Sumw2()
            globals()["data2P2FextHist" + str(j) + str(k)].SetStats(0)


            for event in globals()["zz4PTree" + str(j) + str(k)]:

                if "deltaR" in histKey:
                    globals()["zz4PHist" + str(j) + str(k)].Fill(event.deltaRTauTau, event.eventWeight)

                if "Tau1Pt" in histKey:
                    globals()["zz4PHist" + str(j) + str(k)].Fill(event.Tau1Pt, event.eventWeight)

                if "Tau2Pt" in histKey:
                    globals()["zz4PHist" + str(j) + str(k)].Fill(event.Tau2Pt, event.eventWeight)

                if "invMassMuMu" in histKey:
                    globals()["zz4PHist" + str(j) + str(k)].Fill(event.invMassMuMu, event.eventWeight)

                if "visMassMuMuTauTau" in histKey:
                    globals()["zz4PHist" + str(j) + str(k)].Fill(event.visMassMuMuTauTau, event.eventWeight)

            globals()["zz4PHist" + str(j) + str(k)].SetStats(0)
            globals()["zz4PHist" + str(j) + str(k)].Sumw2()
            globals()["zz4PHist" + str(j) + str(k)].Scale(41.529*1.212*1000)
            globals()["zz4PHist" + str(j) + str(k)].SetFillStyle(1001)
            globals()["zz4PHist" + str(j) + str(k)].SetFillColor(ROOT.kBlue)
            globals()["zz4PHist" + str(j) + str(k)].SetLineColor(ROOT.kBlue)


            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["data2P2FHist" + str(j) + str(k)], -1)
            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["zz3P1F1Hist" + str(j) + str(k)], -1)

            globals()["data3P1F2Hist" + str(j) + str(k)].Add(globals()["zz3P1F2Hist" + str(j) + str(k)], -1)

            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["data2P2FextHist" + str(j) + str(k)])
            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["data3P1F2Hist" + str(j) + str(k)])
            globals()["data3P1F1Hist" + str(j) + str(k)].Add(globals()["zz4PHist" + str(j) + str(k)])

            nbins = globals()["data3P1F1Hist" + str(j) + str(k)].GetNbinsX()
            for ibin in xrange(nbins):
                binValue = globals()["data3P1F1Hist" + str(j) + str(k)].GetBinContent(ibin+1)
                if binValue < 0:
                    print "***** negative bins: ", binValue
                    #globals()["data3P1F1Hist" + str(j) + str(k)].SetBinContent(ibin+1, 0)

            legend.AddEntry(globals()["data3P1F1Hist" + str(j) + str(k)],"3P1F+2P2F extr.","f")
            legend.AddEntry(globals()["zz4PHist" + str(j) + str(k)], "ZZ(4l)", "f")

            if histKey.find("Pt")!=-1:
               canvas.SetLogy()
               globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetRangeUser(0.5, globals()["data3P1F1Hist" + str(j) + str(k)].GetMaximum()*100.0)

            if histKey.find("deltaR")!=-1:
               canvas.SetLogy()
               globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetRangeUser(0.5, globals()["data3P1F1Hist" + str(j) + str(k)].GetMaximum()*100.0)

            if histKey.find("Mass")!=-1:
               globals()["data3P1F1Hist" + str(j) + str(k)].GetYaxis().SetRangeUser(0.5, globals()["data3P1F1Hist" + str(j) + str(k)].GetMaximum()*1.2)

            globals()["data3P1F1Hist" + str(j) + str(k)].Draw("HIST")
            globals()["zz4PHist" + str(j) + str(k)].Draw("HIST same")
            globals()["data3P1F1Hist" + str(j) + str(k)].Draw("HIST same")
            ROOT.gPad.RedrawAxis()
            legend.Draw("same")
            label1.Draw("same")
            label2.Draw("same")
            label3.Draw("same")

            canvas.SaveAs("plots/4P/" + histKey + "_MuIso_" + imuid + "_EleId_" + ieleid + "_Yield.pdf")
