from reader import *
from tqdm import tqdm
from ROOT import *
import math,sys

fname = "/hadoop/cms/store/group/snt/run2_mc2017//DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_MINIAODSIM_CMS4_V09-04-13/merged_ntuple_1.root"
reader = Reader(fname, treename="Events")

outf = TFile("hists.root","recreate")
histnames = ['mupt','mueta','mm_mass','mm_pt','nzcands']
histbins = [(40,0,200),(25,-2.5,2.5),(100,0,200),(40,0,200),(5,-0.5,4.5)]
hists = {}
for index,name in enumerate(histnames):
    hists[name] = TH1F('h'+name,'h'+name,histbins[index][0],histbins[index][1],histbins[index][2])

for cnt,event in enumerate(reader):

    if cnt%1000 == 0:
        print '%d/%d' % (cnt,reader.nevents)

    nzs = 0
    for imu,muon in enumerate(event.mus_p4):
        if muon.pt() < 20: continue
        if math.fabs(muon.eta()) > 2.4: continue
        
        for imu2,muon2 in enumerate(event.mus_p4[imu+1::]):
            if muon2.pt() < 20: continue
            if math.fabs(muon2.eta()) > 2.4: continue

            if event.mus_charge[imu] * event.mus_charge[imu2+imu+1] > 0: continue

            zp4 = muon + muon2
            nzs += 1

            hists['mupt'].Fill(min(muon.Pt(),histbins[0][2])) 
            hists['mupt'].Fill(min(muon2.Pt(),histbins[0][2])) 
        
            hists['mueta'].Fill(max(min(muon.Eta(),histbins[1][2]),histbins[1][1])) 
            hists['mueta'].Fill(max(min(muon2.Eta(),histbins[1][2]),histbins[1][1])) 

            hists['mm_mass'].Fill(min(zp4.M(),histbins[2][2])) 
            hists['mm_pt'].Fill(min(zp4.Pt(),histbins[3][2]))
            hists['nzcands'].Fill(max(min(nzs,histbins[4][2]),histbins[4][1]))
        
outf.Write()
outf.Close() 
