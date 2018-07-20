import sys,numpy,math,getopt,random
from array import array
import ROOT as r

##
## function: fill 1D histogram with numbers randomly generated from a unit Gaussian
##
def make_file_with_hists(outfile):
    outfile += '_hist.root'
    
    ## open ROOT file for writing
    f = r.TFile.Open(outfile,'RECREATE')

    ## create 1D histogram
    h1 = r.TH1F('h1rand','h1rand',100,-5,5)

    ## generated random numbers from a unit Gaussian and fill histogram
    rands = numpy.random.normal(0,1,10**6)
    for rand in rands:
        h1.Fill(rand)

    ## write histogram to file and close file
    f.Write()
    f.Close()
    return len(rands)

##
## function: write random data to branches of a TTree
## branches: int, float, array of ints, array of floats, array of TLorentzVectors
## TLorentzVector: https://root.cern.ch/root/html524/TLorentzVector
## 
def make_file_with_tree(outfile):
    outfile += '_tree.root'

    ## open ROOT file for writing
    ## create TTree
    ofile = r.TFile.Open(outfile,'RECREATE')
    t = r.TTree("tree","tree")

    ##
    ## declare variables to write to TTree
    ##
    p4 = r.TLorentzVector(0,0,0,0)

    i = array('I',[0])
    f = array('f',[0])
    voi = r.std.vector(int)()
    vof = r.std.vector(float)()
    voL = r.std.vector(r.TLorentzVector)()

    t._i = i
    t._f = f
    t._voi = voi
    t._vof = vof
    t._voL = voL

    ##
    ## create TBranches
    ##
    t.Branch("i",i,"i/I")
    t.Branch("f",f,"f/F")
    t.Branch("voi",voi)
    t.Branch("vof",vof)
    t.Branch("voL",voL)

    ## fill variables to be written to tree branches
    for idx in range(10**3):
        voi.clear()
        vof.clear()
        voL.clear()
        i[0] = idx
        f[0] = random.random()+i[0]
        voi_ = numpy.repeat(i[0],i[0])
        vof_ = numpy.random.normal(0,1,10**3)
        for val in voi_:
            voi.push_back(val)
        for val in vof_:
            vof.push_back(val) 
        rands = 100*numpy.random.normal(0,1,[10**3,3])
        for rand in rands:
            p4.SetPxPyPzE(rand[0],rand[1],rand[2],numpy.sqrt(numpy.sum(rand*rand)))
            voL.push_back(p4)

        ## write branches to tree
        t.Fill()

    ## write tree to file and close file
    ofile.Write()
    ofile.Close()
    return numpy.size(voi)

if __name__ == '__main__':
    make_hists = False
    make_tree = False
    outfile = 'test'
    try:
        opts, args = getopt.getopt(sys.argv[1:],'tpo:',['tree','hist','ofile='])
    except:
        print 'make_dummy_file.py [-t] [-h] -o <outfile>'
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-p':
            make_hists = True
        elif opt == '-t':
            make_tree = True
        elif opt in ('-o','--ofile'):
            outfile = arg

    if make_hists:
        make_file_with_hists(outfile)
    if make_tree:
        make_file_with_tree(outfile)
    
        
