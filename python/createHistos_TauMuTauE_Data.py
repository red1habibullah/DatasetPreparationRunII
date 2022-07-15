#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


muIdList = ["loose"]
muIdLabel = ["looseMuIso"]

eleIdList = ["tight"]
eleIdLabel = ["tightEleId"]

years=["2016","2017","2018"]

#histList = ["deltaRTauTau", "Tau1Pt", "Tau2Pt", "invMassMuMu", "visMassMuMuTauTau"]
histKey ="invMassMu1Mu2_me"
histKey2D="invMassMu1Mu2_mevisMass3MuEle_me"
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

baseDir='/afs/cern.ch/work/r/rhabibul/FlatTreeProductionRunII/CMSSW_10_6_24/src/MuMuTauTauAnalyzer/flattrees/dataSideband/'
#outputDir='/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauMuTauE_Order_Scale/'
outputDir='/eos/cms/store/user/rhabibul/BoostedRooDatasets/TauMuTauE_Rebin/'
fakebaseDir='/afs/cern.ch/user/r/rhabibul/DatasetPrepRunII_Boosted/CMSSW_10_2_13/src/DatasetPreparationRunII/data/'

#inputFakeEleFile = ROOT.TFile(fakebaseDir+"fakeTauEff_TauETauE.root")
#inputFakeMuFile = ROOT.TFile(fakebaseDir+"fakeTauEff_TauMuTauMu.root")
#nbins = 240
nbins = 480
nbinsy = 400

for j,imuid in enumerate(muIdList):

    for k,ieleid in enumerate(eleIdList):
        
        for iy,y in enumerate(years):
            inputFakeEleFile = ROOT.TFile(fakebaseDir+y+"/"+"fakeTauEff_TauETauE.root")
            inputFakeMuFile = ROOT.TFile(fakebaseDir+y+"/"+"fakeTauEff_TauMuTauMu.root")

            globals()["data3P1F1File" + str(j) + str(k) +str(iy)] = ROOT.TFile(baseDir+y+"/Histogram/"+"All_"+y+"_sideBand_nominal.root")
            globals()["data3P1F2File" + str(j) + str(k)+str(iy)] = ROOT.TFile(baseDir+y+"/Histogram/"+"All_"+y+"_sideBand1_nominal.root")
            globals()["data2P2FFile" + str(j) + str(k)+str(iy)] = ROOT.TFile(baseDir+y+"/Histogram/"+"All_"+y+"_sideBand2_nominal.root")
            
            globals()["data3P1F1Tree" + str(j) + str(k)+ str(iy)] = globals()["data3P1F1File" + str(j) + str(k)+str(iy)].Get("TreeMuEle")
            globals()["data3P1F2Tree" + str(j) + str(k)+str(iy)] = globals()["data3P1F2File" + str(j) + str(k)+str(iy)].Get("TreeMuEle")
            globals()["data2P2FTree" + str(j) + str(k)+str(iy)] = globals()["data2P2FFile" + str(j) + str(k) +str(iy)].Get("TreeMuEle")

            
            

            histFakeMuEff = inputFakeMuFile.Get(muIdLabel[j])
            histFakeEleEff = inputFakeEleFile.Get(eleIdLabel[k])

            #Final Extrapolated DataHist in Signal Region
            globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            globals()["data3P1F2Hist" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            
            globals()["2Ddata3P1FHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            globals()["2Ddata3P1F2Hist" + str(j) + str(k)+str(iy)] = ROOT.TH2D()


            #Data on sideband FP
            globals()["data3P1F1HistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH1D()

            globals()["2Ddata3P1F1HistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            
            




            #Data on sideband2 FF
            globals()["data2P2FHistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            globals()["data2P2FHist" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            globals()["data2P2FextHist" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            
            globals()["data2P2FHistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            globals()["data2P2FHist" + str(j) + str(k)+str(iy)] = ROOT.TH1D()
            globals()["data2P2FextHist" + str(j) + str(k)+str(iy)] = ROOT.TH1D()



            globals()["2Ddata2P2FHistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            globals()["2Ddata2P2FHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            globals()["2Ddata2P2FextHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            
            globals()["2Ddata2P2FHistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            globals()["2Ddata2P2FHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D()
            globals()["2Ddata2P2FextHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D()

            
            
            if "invMassMu1Mu2_me" in histKey:
                globals()["data3P1F1Hist" + str(j) + str(k) +str(iy)] = ROOT.TH1D("invMassMuMu" + "3P1F1","invMassMuMu"+"3P1F1", nbins, 0, 60)
                globals()["data3P1F1HistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH1D("invMassMuMu"+"3P1F1Only","invMassMuMu" + "3P1F1Only", nbins, 0, 60)
                globals()["data3P1F2Hist" + str(j) + str(k)+str(iy)] = ROOT.TH1D("invMassMuMu"+"3P1F2", "invMassMuMu"+"3P1F2", nbins, 0, 60)
                globals()["data2P2FHistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH1D("invMassMuMu"+"2P2FOnly","invMassMuMu"+ "2P2FOnly", nbins, 0, 60)
                globals()["data2P2FHist" + str(j) + str(k)+str(iy)] = ROOT.TH1D("invMassMuMu"+"2P2F","invMassMuMu"+"2P2F", nbins, 0, 60)
                globals()["data2P2FextHist" + str(j) + str(k)+str(iy)] = ROOT.TH1D("invMassMuMu"+"2P2Fext","invMassMuMu"+"2P2Fext", nbins, 0, 60)
                
                #####################

            if "invMassMu1Mu2_mevisMass3MuEle_me" in histKey2D:
                globals()["2Ddata3P1F1Hist" + str(j) + str(k) +str(iy)] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau" + "3P1F1","invMassMuMuVisMassMuMuTauTau"+"3P1F1", nbins, 0, 60,nbinsy,0,1000)
                globals()["2Ddata3P1F1HistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau"+"3P1F1Only","invMassMuMuVisMassMuMuTauTau" + "3P1F1Only", nbins, 0, 60,nbinsy,0,1000)
                globals()["2Ddata3P1F2Hist" + str(j) + str(k)+str(iy)] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau"+"3P1F2", "invMassMuMuVisMassMuMuTauTau"+"3P1F2", nbins, 0, 60,nbinsy,0,1000)
                globals()["2Ddata2P2FHistOnly" + str(j) + str(k)+str(iy)] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau"+"2P2FOnly","invMassMuMuVisMassMuMuTauTau"+ "2P2FOnly", nbins, 0, 60,nbinsy,0,1000)
                globals()["2Ddata2P2FHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau"+"2P2F","invMassMuMuVisMassMuMuTauTau"+"2P2F", nbins, 0, 60,nbinsy,0,1000)
                globals()["2Ddata2P2FextHist" + str(j) + str(k)+str(iy)] = ROOT.TH2D("invMassMuMuVisMassMuMuTauTau"+"2P2Fext","invMassMuMuVisMassMuMuTauTau"+"2P2Fext", nbins, 0, 60,nbinsy,0,1000)
                
            
            for event in globals()["data3P1F1Tree" + str(j) + str(k)+str(iy)]:
                
                fakeEff = 1.0
                nbins = histFakeEleEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.elePt_me >= binlowEdge and event.elePt_me < binhighEdge and event.mu2Pt_me > event.mu3Pt_me):
                        fakeEff = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))
                globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, fakeEff)
                globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, event.visMass3MuEle_me, fakeEff)
                

            for event in globals()["data3P1F2Tree" + str(j) + str(k)+str(iy)]:

                fakeEff = 1.0
                nbins = histFakeMuEff.GetNbinsX()
                for ibin in xrange(nbins):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.mu3Pt_me >= binlowEdge and event.mu3Pt_me < binhighEdge and event.mu2Pt_me > event.mu3Pt_me):
                        fakeEff = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

                    
                globals()["data3P1F2Hist" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, fakeEff)
                globals()["2Ddata3P1F2Hist" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, event.visMass3MuEle_me, fakeEff)
                    
                
                
            for event in globals()["data2P2FTree" + str(j) + str(k)+str(iy)]:
                globals()["data2P2FHistOnly" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me)
                globals()["2Ddata2P2FHistOnly" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me,event.visMass3MuEle_me)
            
            


            for event in globals()["data2P2FTree" + str(j) + str(k)+str(iy)]:

                fakeEff1 = 0.5
                fakeEff2 = 0.5
                fakeEff = 1.0
                nbinsMu = histFakeMuEff.GetNbinsX()
                nbinsEle = histFakeEleEff.GetNbinsX()

                for ibin in xrange(nbinsMu):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.mu3Pt_me >= binlowEdge and event.mu3Pt_me < binhighEdge and event.mu2Pt_me > event.mu3Pt_me):
                        fakeEff1 = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))
                for ibin in xrange(nbinsEle):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.elePt_me >= binlowEdge and event.elePt_me < binhighEdge and event.mu2Pt_me > event.mu3Pt_me):
                        fakeEff2 = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))
                        fakeEff = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))


            
                globals()["data2P2FHist" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, (fakeEff1 + fakeEff2)*fakeEff)
                globals()["data3P1F1HistOnly" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me,(fakeEff1+fakeEff2))  
                
                globals()["2Ddata2P2FHist" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, event.visMass3MuEle_me,(fakeEff1 + fakeEff2)*fakeEff)
                
                globals()["2Ddata3P1F1HistOnly" + str(j) + str(k)+str(iy)].Fill(event.invMassMu1Mu2_me, event.visMass3MuEle_me,(fakeEff1+fakeEff2))

                
            for event in globals()["data2P2FTree" + str(j) + str(k)+str(iy)]:

                fakeEff1 = 1.0
                fakeEff2 = 1.0
                nbinsMu = histFakeMuEff.GetNbinsX()
                nbinsEle = histFakeEleEff.GetNbinsX()

                for ibin in xrange(nbinsMu):
                    binlowEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeMuEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeMuEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.mu3Pt_me >= binlowEdge and event.mu3Pt_me < binhighEdge and event.mu2Pt_me > event.mu3Pt_me):
                        fakeEff1 = histFakeMuEff.GetBinContent(ibin+1)/(1.0-histFakeMuEff.GetBinContent(ibin+1))

                for ibin in xrange(nbinsEle):
                    binlowEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1)
                    binhighEdge = histFakeEleEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEleEff.GetXaxis().GetBinWidth(ibin+1)
                    if (event.elePt_me >= binlowEdge and event.elePt_me < binhighEdge and event.mu2Pt_me > event.mu3Pt_me):
                        fakeEff2 = histFakeEleEff.GetBinContent(ibin+1)/(1.0-histFakeEleEff.GetBinContent(ibin+1))
                
            
                globals()["data2P2FextHist" + str(j) + str(k) +str(iy)].Fill(event.invMassMu1Mu2_me, fakeEff1*fakeEff2)
                globals()["2Ddata2P2FextHist" + str(j) + str(k) +str(iy)].Fill(event.invMassMu1Mu2_me,event.visMass3MuEle_me,fakeEff1*fakeEff2)
                
            

            globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Add(globals()["data2P2FHist" + str(j) + str(k)+str(iy)], -1)
            globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Add(globals()["2Ddata2P2FHist" + str(j) + str(k)+str(iy)], -1)

            

            globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Add(globals()["data2P2FextHist" + str(j) + str(k)+str(iy)])
            globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Add(globals()["2Ddata2P2FextHist" + str(j) + str(k)+str(iy)])
            
            
            globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Add(globals()["data3P1F2Hist" + str(j) + str(k)+str(iy)])
            globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Add(globals()["2Ddata3P1F2Hist" + str(j) + str(k)+str(iy)])
         
            #globals()["data3P1F1HistOnly" + str(j) + str(k)].Add(globals()["data2P2FHist" + str(j) + str(k)], -1)

            nbins = globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].GetNbinsX()
            Integral_pre_zero= globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Integral()
            print "integral before: ",Integral_pre_zero
            for ibin in xrange(nbins):
                binValue = globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].GetBinContent(ibin+1)
                if binValue < 0:
                    print "***** negative bins: ", binValue
                    globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].SetBinContent(ibin+1, 0)  
                    binval = globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].GetBinContent(ibin+1)
                    #print " ###### changed bins: ", binval
            Integral_post_zero= globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Integral()
            print "integral after: ",Integral_post_zero
            globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Scale(Integral_post_zero/Integral_pre_zero)


            nbinsX = globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].GetNbinsX()
            nbinsY = globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].GetNbinsY()
            Integral_pre_zero_2D= globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Integral()
            
            print "integral before 2D: ",Integral_pre_zero_2D
           
            for ibinx in xrange(nbinsX):
                for ibiny in xrange(nbinsY):
                    #binValue1 = globals()["data3P1F1Hist" + str(j) + str(k)].GetBinContent(ibin+1)
                    #binValue2 = globals()["data3P1F2Hist" + str(j) + str(k)].GetBinContent(ibin+1)
                    binValue = globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].GetBinContent(ibinx+1, ibiny+1)
                    if binValue < 0:
                        print "***** negative bins: ", ibinx+1, ibiny+1, binValue
                        globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].SetBinContent(ibinx+1, ibiny+1, 0)
                        globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].SetBinError(ibinx+1, ibiny+1, 0)
            #binval = globals()["data3P1F1Hist" + str(j) + str(k)].GetBinContent(ibin+1)
            Integral_post_zero_2D= globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Integral()
            print "integral after 2D: ",Integral_post_zero_2D
            globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Scale(Integral_post_zero_2D/Integral_pre_zero_2D)
            



            globals()["fout1" + str(j) + str(k)+str(iy) ] = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauMuTauE_Rebin_" +y+"_"+muIdLabel[j]+"_"+eleIdLabel[k]+"_"+ "sideBand" +"_"+"nominal"+ ".root", "RECREATE")
            globals()["fout2" + str(j) + str(k)+str(iy) ] = ROOT.TFile(outputDir+y+"/"+"DataDriven/"+"TauMuTauE_Rebin_" +y+"_"+muIdLabel[j]+"_"+eleIdLabel[k]+"_"+ "signalRegion" +"_"+"nominal"+ ".root", "RECREATE")
            

            globals()["fout1" + str(j) + str(k) +str(iy)].cd()
            globals()["data3P1F1HistOnly" + str(j) + str(k)+str(iy)].Write()
            globals()["fout1" + str(j) + str(k) +str(iy)].Close()

            globals()["fout2" + str(j) + str(k)+str(iy) ].cd()
            globals()["data3P1F1Hist" + str(j) + str(k)+str(iy)].Write()
            globals()["2Ddata3P1F1Hist" + str(j) + str(k)+str(iy)].Write()
           
            globals()["fout2" + str(j) + str(k) + str(iy)].Close()

