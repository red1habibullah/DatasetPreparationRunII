#!/usr/bin/python
import ROOT
from ROOT import RooFit

#signalDir = "/eos/uscms/store/user/zfwd666/HAA/DeepTauID/TauMuTauHad/slimmedTausMuonCleanedDeep/"
#sidebandDir = "/eos/uscms/store/user/zfwd666/HAA/DeepTauID/TauMuTauHad/sideband/"
#HAA_MC_signalRegion_tauScale.root

baseDir='/uscms_data/d3/rhabibul/DatasetPrepRunII/CMSSW_10_2_18/src/DatasetPreparationRunII/data/ComninedTrees/TauMuTauHad/'
outputDir='/eos/uscms/store/user/rhabibul/HtoAA/HtoAA2017Deep/TauMuTauHad/RooDataSets/SignalMCSystematics/'

region = ["signalRegion", "sideband"]

scale =0.001
higgs_xsec=48.58
lumi_2017=41.529*1000
types=['tauScale','tauScaleUp','tauScaleDown']
#fakerateUncertainty=0.20
#scaleUp=1.0+fakerateUncertainty
#scaleDown=1.0-fakerateUncertainty
fileinDir = ["am4", "am5", "am6", "am7", "am8", "am9", "am10", "am11", "am12", "am13", "am14", "am15", "am16", "am17", "am18", "am19", "am20", "am21"]
region = ["signalRegion", "sideBand"]

#tauDiscVSjet = ["vvlooseDeepVSjet", "vlooseDeepVSjet", "looseDeepVSjet", "mediumDeepVSjet", "tightDeepVSjet", "vtightDeepVSjet", "vvtightDeepVSjet"]

#for j,index in enumerate(path):
for i,index in enumerate(fileinDir):
    for j,jregion in enumerate(region):
        for k,ktype in enumerate(types):
        
        #for iName in tauDiscVSjet:
        #finName = index + ifile + "/HAA_MC_" + iName + "Disc.root"
        
            finName = baseDir + index + "/HAA_MC_" + jregion +"_" +ktype+".root"  
            #print finName
            globals()["fin" + str(index) + str(jregion) + str(ktype)] = ROOT.TFile(finName)
            globals()["treein" + str(index)+ str(jregion) + str(ktype)] = globals()["fin" + str(index)+ str(jregion) + str(ktype)].Get("TreeMuMuTauTau")

            globals()["dimuMass" + str(index)+ str(jregion) + str(ktype)] = ROOT.RooRealVar("invMassMuMu", "invMassMuMu", 2.5, 60)
            globals()["visDiTauMass" + str(index)+ str(jregion) + str(ktype)] = ROOT.RooRealVar("visDiTauMass", "visDiTauMass", 0, 60)
            globals()["visFourbodyMass" + str(index)+ str(jregion) + str(ktype)] = ROOT.RooRealVar("visFourbodyMass", "visFourbodyMass", 0, 1000)
            globals()["eventWeight" + str(index)+ str(jregion) + str(ktype)] = ROOT.RooRealVar("eventWeight", "eventWeight", -1, 1)
            globals()["dataColl" + str(index)+ str(jregion) + str(ktype)] = ROOT.RooDataSet("dataColl", "dataColl", ROOT.RooArgSet(globals()["dimuMass" + str(index)+ str(jregion) + str(ktype)], globals()["visDiTauMass" + str(index)+ str(jregion) + str(ktype)], globals()["visFourbodyMass" + str(index)+ str(jregion) + str(ktype)], globals()["eventWeight" + str(index)+ str(jregion) + str(ktype)]))
            for event in globals()["treein" + str(index)+ str(jregion) + str(ktype)]:
                globals()["dimuMass" + str(index)+ str(jregion) + str(ktype)].setVal(event.invMassMuMu)
                globals()["visDiTauMass" + str(index)+ str(jregion) + str(ktype)].setVal(event.visMassTauTau)
                globals()["visFourbodyMass" + str(index)+ str(jregion) + str(ktype)].setVal(event.visMassMuMuTauTau)
                globals()["eventWeight" + str(index)+ str(jregion) + str(ktype)].setVal(event.eventWeight*scale*higgs_xsec*lumi_2017)
                globals()["dataColl" + str(index)+ str(jregion) + str(ktype)].add(ROOT.RooArgSet(globals()["dimuMass" + str(index)+ str(jregion) + str(ktype)], globals()["visDiTauMass" + str(index)+ str(jregion) + str(ktype)], globals()["visFourbodyMass" + str(index)+ str(jregion) + str(ktype)], globals()["eventWeight" + str(index)+ str(jregion) + str(ktype)]))
            
            globals()["fout" + str(index)+ str(jregion) + str(ktype)] = ROOT.TFile(outputDir+ "TauMuTauHad_HaaMC_" + index + "_" + jregion + "_" +"mediumDeepVsjet"+ "_" + ktype + ".root", "RECREATE")
            print  globals()["fout" + str(index)+ str(jregion) + str(ktype)]
            globals()["dataColl" + str(index)+ str(jregion) + str(ktype)].Write()
            globals()["fout" + str(index)+ str(jregion) + str(ktype)].Close()
            
            
            
