import ROOT as r
import sys,os
import numpy as np
import matplotlib.pyplot as plt

##
## function: read histogram from file, plot histogram, save in various formats
##
def plot_histogram(f, histname):
    ## get histogram from file
    h = f.Get(histname)

    ## create TCanvas to which histogram is plotted
    c = r.TCanvas('c1','c1',600,400)

    ## set options for stat output printed to stat box on canvas
    r.gStyle.SetOptStat('emrou')
    
    ## set axis labels and line properties for histogram
    h.GetXaxis().SetTitle('x')
    h.GetYaxis().SetTitle('Entries/0.1')
    h.SetTitle('Gaus(0,1)')
    h.SetLineColor(r.kBlack)
    h.Draw()

    if not os.path.isdir('plots'):
        os.makedirs('plots')

    ## save canvas in various formats
    c.Print('plots/test_hist.pdf')
    c.Print('plots/test_hist.png')
    c.Print('plots/test_hist.root')
    c.Print('plots/test_hist.C')

    return h.GetEntries()

##
## function: read data from TTree, plot data, save output
##
def make_plots_from_tree(f, treename):
    ## get ttree from file
    t = f.Get(treename)

    ## containers to store data from tree
    i = []
    f = []
    voi = []
    vof = []
    voL = [] 

    ## loop over events in tree
    for event in t:
        i.append(event.i)
        f.append(event.f)
        for val in event.voi:
            voi.append(val)
        for index,val in enumerate(event.vof):
            vof.append(val)
            voL.append(event.voL[index])

    ## convert lists to numpy arrays to plot with matplotlib
    i = np.array(i)     
    f = np.array(f)     
    voi = np.array(voi)
    vof = np.array(vof)
    voL = np.array(voL)
    
    print 'len(i) = ', len(i)
    print 'len(f) = ', len(f)
    print 'len(voi) = ', len(voi)

    ## plot transverse momentum, Pt(), from TLorentzVectors
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

    ## plot random values from unit Gaussian
    ## important 1: after first use of plt, call plt.cla() before all subsequent uses to clear object of previous plots/histograms
    ## important 2: call plt.savefig() before plt.show()
    plt.cla()
    plt.hist(pt)
    plt.xlabel('$p_T$ (GeV)')
    plt.ylabel('Entries/bin')
    plt.title('transverse momentum')
    plt.savefig('plots/test_tree_voL_pt.pdf')
    plt.show()

    ## plot transverse momentum, Pt(), from TLorentzVectors
    plt.cla()
    plt.hist(eta)
    plt.xlabel('$\eta$')
    plt.ylabel('Entries/bin')
    plt.title('particle $\eta$')
    plt.savefig('plots/test_tree_voL_eta.pdf')
    plt.show()

    ## plot Phi(), from TLorentzVectors
    plt.cla()
    plt.hist(phi)
    plt.xlabel('$\phi$')
    plt.ylabel('Entries/bin')
    plt.title('particle $\phi$')
    plt.savefig('plots/test_tree_voL_phi.pdf')
    plt.show()

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except:
        print 'Usage: python tutorial.py <filename>'
        sys.exit(2)
    ifile = r.TFile(fname,'read')
    do_hist = False
    do_tree = False
    if 'hist' in fname:
        plot_histogram(ifile,'h1rand')         
    if 'tree' in fname:
        make_plots_from_tree(ifile,'tree') 
