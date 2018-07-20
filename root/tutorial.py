import ROOT as r
import sys,os
import numpy as np
import matplotlib.pyplot as plt

def plot_histogram(f, histname):
    h = f.Get(histname)
    c = r.TCanvas('c1','c1',600,400)
    r.gStyle.SetOptStat('emrou')
    h.GetXaxis().SetTitle('x')
    h.GetYaxis().SetTitle('Entries/0.1')
    h.SetTitle('Gaus(0,1)')
    h.SetLineColor(r.kBlack)
    h.Draw()
    if not os.path.isdir('plots'):
        os.makedirs('plots')
    c.Print('plots/test_hist.pdf')
    c.Print('plots/test_hist.png')
    c.Print('plots/test_hist.root')
    c.Print('plots/test_hist.C')
    return h.GetEntries()

def make_plots_from_tree(f, treename):
    t = f.Get(treename)
    i = []
    f = []
    voi = []
    vof = []
    voL = [] 
    for event in t:
        i.append(event.i)
        f.append(event.f)
        for val in event.voi:
            voi.append(val)
        for index,val in enumerate(event.vof):
            vof.append(val)
            voL.append(event.voL[index])
    i = np.array(i)     
    f = np.array(f)     
    voi = np.array(voi)
    vof = np.array(vof)
    voL = np.array(voL)
    print 'len(i) = ', len(i)
    print 'len(f) = ', len(f)
    print 'len(voi) = ', len(voi)
    plt.hist(vof,bins=np.arange(-5,5.1,0.1))
    plt.xlabel('x')
    plt.ylabel('Entries/0.1')
    plt.title('Gaus(0,1)')
    if not os.path.isdir('plots'):
        os.makedirs('plots')
    plt.savefig('plots/test_tree_vof.pdf')
    plt.show()

    pt = np.array([x.Pt() for x in voL])
    eta = np.array([x.Eta() for x in voL])
    phi = np.array([x.Phi() for x in voL])

    plt.cla()
    plt.hist(pt)
    plt.xlabel('$p_T$ (GeV)')
    plt.ylabel('Entries/bin')
    plt.title('transverse momentum')
    plt.savefig('plots/test_tree_voL_pt.pdf')
    plt.show()

    plt.cla()
    plt.hist(eta)
    plt.xlabel('$\eta$')
    plt.ylabel('Entries/bin')
    plt.title('particle $\eta$')
    plt.savefig('plots/test_tree_voL_eta.pdf')
    plt.show()

    plt.cla()
    plt.hist(phi)
    plt.xlabel('$\phi$')
    plt.ylabel('Entries/bin')
    plt.title('particle $\phi$')
    plt.savefig('plots/test_tree_voL_phi.pdf')
    plt.show()

if __name__ == '__main__':
    fname = sys.argv[1]
    ifile = r.TFile(fname,'read')
    do_hist = False
    do_tree = False
    if 'hist' in fname:
        plot_histogram(ifile,'h1rand')         
    if 'tree' in fname:
        make_plots_from_tree(ifile,'tree') 
