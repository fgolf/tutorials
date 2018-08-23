from reader import *
from tqdm import tqdm
import ROOT as r
import math,sys
import os
import time

for include in ["CMS3.cc", "VertexSelections.h", "ElectronSelections.h", "MuonSelections.h", "MCSelections.h", "JetSelections.h"]:
    r.gInterpreter.ProcessLine('#include "/home/users/fgolf/ugrads/carter/CORE/%s"' % include)
r.gSystem.Load('/home/users/fgolf/ugrads/carter/CORE/CMS3_CORE.so')
from ROOT import *

f = r.TFile("/home/users/namin/sandbox/reproc/CMSSW_8_0_20/src/CMS3/NtupleMaker/test/ntuple.root")
tree = f.Get("Events")

outf = TFile("hists.root","recreate")
histnames = ['mupt','mueta','mm_mass','mm_pt','nzcands']
histbins = [(40,0,200),(25,-2.5,2.5),(100,0,200),(40,0,200),(5,-0.5,4.5)]
selections = ['all','loose','tight']
hists = {}
for index,name in enumerate(histnames):
    for selection in selections:
        hists[selection+name] = TH1F('h_'+selection+'_'+name,'h_'+selection+'_'+name,histbins[index][0],histbins[index][1],histbins[index][2])

nevents = tree.GetEntries()
cms3.Init(tree)
t0 = time.time()
for event in tqdm(range(nevents)):

    cms3.GetEntry(event)

    nzs = 0
    for imu,muon in enumerate(cms3.mus_p4()):
        if muon.pt() < 20: continue
        if math.fabs(muon.eta()) > 2.4: continue
        
        for imu2,muon2 in enumerate(cms3.mus_p4()[imu+1::]):
            if muon2.pt() < 20: continue
            if math.fabs(muon2.eta()) > 2.4: continue

            if cms3.mus_charge()[imu] * cms3.mus_charge()[imu2+imu+1] > 0: continue

            zp4 = muon + muon2
            nzs += 1

            for selection in selections:
                if selection=='loose':
                    if not isLooseMuonPOG(imu) or not isLooseMuonPOG(imu2+imu+1): continue
                if selection=='tight':
                    if not isTightMuonPOG(imu) or not isTightMuonPOG(imu2+imu+1): continue

                hists[selection+'mupt'].Fill(min(muon.Pt(),histbins[0][2])) 
                hists[selection+'mupt'].Fill(min(muon2.Pt(),histbins[0][2])) 
            
                hists[selection+'mueta'].Fill(max(min(muon.Eta(),histbins[1][2]),histbins[1][1])) 
                hists[selection+'mueta'].Fill(max(min(muon2.Eta(),histbins[1][2]),histbins[1][1])) 
    
                hists[selection+'mm_mass'].Fill(min(zp4.M(),histbins[2][2])) 
                hists[selection+'mm_pt'].Fill(min(zp4.Pt(),histbins[3][2]))
                hists[selection+'nzcands'].Fill(max(min(nzs,histbins[4][2]),histbins[4][1]))

outf.Write()
outf.Close() 

t1 = time.time()
print "ran over %i events in %.2f seconds (%.1f Hz)" % (nevents, t1-t0, nevents/(t1-t0))
