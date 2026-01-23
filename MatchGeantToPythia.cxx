#include <TF1.h>
#include <TH1.h>
#include <TH2.h>
#include <TH3.h>
#include <TFile.h>
#include <TProfile.h>
#include <TLine.h>

#include <TROOT.h>
#include <TLorentzVector.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TObjArray.h>
#include <TClonesArray.h>
#include <TString.h>
#include <TChain.h>
#include <TBranch.h>
#include <TMath.h>
#include <TRandom.h>
#include <TSystem.h>
#include <TGraph.h>

#include <TStarJetVector.h>
#include <TStarJetVectorJet.h>
#include <TStarJetPicoReader.h>

#include <iostream>
#include <fstream>
#include <random>
#include <vector>
#include <string>
#include <set>
#include <cmath>
#include <exception>

using namespace std;

//! ----------------------------------------------------
class RootResultStruct
{
public:
    TStarJetVectorJet orig;
    double pt;
    double eta;
    double y;
    double phi;
    double m;
    int n;
    int nch;
    int runid1;
    double q;
    double rg;
    double zg;
    double mg;
    double weight;
    int reject;
    int mcevi;
    int mult;
    int b;
    double dr;
    double pt1;
    double pt2;
    double z;
    double epair;
    double qlead;
    double qsublead;
    double y1;
    double y2;
    double phi1;
    double phi2;
    double nef;
    double vz;
    RootResultStruct(TStarJetVectorJet orig, double pt, double eta, double y, double phi, double m, int runid1, double q, double rg, double zg, double mg, double nef, int n, int nch, double weight, int reject, int mcevi, int mult, double vz, int b, double dr, double pt1, double pt2, double z, double epair, double qlead, double qsublead, double y1, double y2, double phi1, double phi2) : orig(orig), pt(pt), eta(eta), y(y), phi(phi), m(m), runid1(runid1), q(q), rg(rg), zg(zg), mg(mg), nef(nef), n(n), nch(nch), weight(weight), reject(reject), mcevi(mcevi), mult(mult), vz(vz), b(b), dr(dr), pt1(pt1), pt2(pt2), z(z), epair(epair), qlead(qlead), qsublead(qsublead), y1(y1), y2(y2), phi1(phi1), phi2(phi2) {};
    ClassDef(RootResultStruct, 1)
};

typedef pair<RootResultStruct, RootResultStruct> MatchedRootResultStruct;

int MatchGeantToPythia(string McFile, string PpFile, string OutFile = "test.root", int RADIUS = 4, int mode = 0)
{
    bool RejectHiweights = true;
    float RCut = (float)RADIUS / 10;
    float EtaCut = 1.0 - RCut;
    int nj = 0;

    TString dir = "/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/";

    TFile *Mcf = new TFile(dir + "pythia/" + McFile);
    TTree *McChain = (TTree *)Mcf->Get("ResultTree");
    McChain->BuildIndex("runid", "eventid");

    TClonesArray *McJets = new TClonesArray("TStarJetVectorJet");
    McChain->GetBranch("Jets")->SetAutoDelete(kFALSE);
    McChain->SetBranchAddress("Jets", &McJets);

    int mcrunid;
    McChain->SetBranchAddress("runid", &mcrunid);
    int mcrunid1;
    McChain->SetBranchAddress("runid1", &mcrunid1);
    int mceventid;
    McChain->SetBranchAddress("eventid", &mceventid);
    double mcweight;
    McChain->SetBranchAddress("weight", &mcweight);
    int mcnjets = 0;
    McChain->SetBranchAddress("njets", &mcnjets);
    double mcvz = 0;
    McChain->SetBranchAddress("vz", &mcvz);
    int mcmult;
    McChain->SetBranchAddress("mult", &mcmult);
    int mcreject;
    McChain->SetBranchAddress("reject", &mcreject);
    float mcpttot;
    McChain->SetBranchAddress("pttot", &mcpttot);
    double mcpt[1000];
    McChain->SetBranchAddress("pt", mcpt);
    double mcm[1000];
    McChain->SetBranchAddress("m", mcm);
    double mcq[1000];
    McChain->SetBranchAddress("q", mcq);
    double mcrg[1000];
    McChain->SetBranchAddress("rg", mcrg);
    double mczg[1000];
    McChain->SetBranchAddress("zg", mczg);
    double mcmg[1000];
    McChain->SetBranchAddress("mg", mcmg);
    int mcn[1000];
    McChain->SetBranchAddress("n", mcn);
    double mcnef[1000];
    McChain->SetBranchAddress("nef", mcnef);
    int mcb[1000];
    McChain->SetBranchAddress("b", mcb);
    double mcdr[1000];
    McChain->SetBranchAddress("dr", mcdr);
    int mcnch[1000];
    McChain->SetBranchAddress("nch", mcnch);
    double mcpt1[1000];
    McChain->SetBranchAddress("pt1", mcpt1);
    double mcpt2[1000];
    McChain->SetBranchAddress("pt2", mcpt2);
    double mcqlead[1000];
    McChain->SetBranchAddress("qlead", mcqlead);
    double mcqsublead[1000];
    McChain->SetBranchAddress("qsublead", mcqsublead);
    double mcy1[1000];
    McChain->SetBranchAddress("y1", mcy1);
    double mcy2[1000];
    McChain->SetBranchAddress("y2", mcy2);
    double mcphi1[1000];
    McChain->SetBranchAddress("phi1", mcphi1);
    double mcphi2[1000];
    McChain->SetBranchAddress("phi2", mcphi2);
    double mcz[1000];
    McChain->SetBranchAddress("z", mcz);
    double mcepair[1000];
    McChain->SetBranchAddress("epair", mcepair);

    TFile *Ppf = new TFile(dir + "geant/" + PpFile);
    TTree *PpChain = (TTree *)Ppf->Get("ResultTree");
    PpChain->BuildIndex("runid", "eventid");

    TClonesArray *PpJets = new TClonesArray("TStarJetVectorJet");
    PpChain->GetBranch("Jets")->SetAutoDelete(kFALSE);
    PpChain->SetBranchAddress("Jets", &PpJets);

    int ppeventid;
    PpChain->SetBranchAddress("eventid", &ppeventid);
    int pprunid;
    PpChain->SetBranchAddress("runid", &pprunid);
    int pprunid1;
    PpChain->SetBranchAddress("runid1", &pprunid1);
    double ppweight;
    PpChain->SetBranchAddress("weight", &ppweight);
    int rcreject;
    PpChain->SetBranchAddress("reject", &rcreject);
    int rcmult;
    PpChain->SetBranchAddress("mult", &rcmult);
    int ppnjets = 0;
    PpChain->SetBranchAddress("njets", &ppnjets);
    double ppvz = 0;
    PpChain->SetBranchAddress("vz", &ppvz);
    float pppttot;
    PpChain->SetBranchAddress("pttot", &pppttot);
    double rcpt[1000];
    PpChain->SetBranchAddress("pt", rcpt);
    double rcm[1000];
    PpChain->SetBranchAddress("m", rcm);
    double rcq[1000];
    PpChain->SetBranchAddress("q", rcq);
    double rcrg[1000];
    PpChain->SetBranchAddress("rg", rcrg);
    double rczg[1000];
    PpChain->SetBranchAddress("zg", rczg);
    double rcmg[1000];
    PpChain->SetBranchAddress("mg", rcmg);
    int rcn[1000];
    PpChain->SetBranchAddress("n", rcn);
    double rcnef[1000];
    PpChain->SetBranchAddress("nef", rcnef);
    int rcb[1000];
    PpChain->SetBranchAddress("b", rcb);
    double rcdr[1000];
    PpChain->SetBranchAddress("dr", rcdr);
    int rcnch[1000];
    PpChain->SetBranchAddress("nch", rcnch);
    double rcpt1[1000];
    PpChain->SetBranchAddress("pt1", rcpt1);
    double rcpt2[1000];
    PpChain->SetBranchAddress("pt2", rcpt2);
    double rcqlead[1000];
    PpChain->SetBranchAddress("qlead", rcqlead);
    double rcqsublead[1000];
    PpChain->SetBranchAddress("qsublead", rcqsublead);
    double rcy1[1000];
    PpChain->SetBranchAddress("y1", rcy1);
    double rcy2[1000];
    PpChain->SetBranchAddress("y2", rcy2);
    double rcphi1[1000];
    PpChain->SetBranchAddress("phi1", rcphi1);
    double rcphi2[1000];
    PpChain->SetBranchAddress("phi2", rcphi2);
    double rcz[1000];
    PpChain->SetBranchAddress("z", rcz);
    double rcepair[1000];
    PpChain->SetBranchAddress("epair", rcepair);

    //! Output and histograms
    TFile *fout = new TFile(dir + "matched/" + OutFile, "RECREATE");
    TTree *MatchedTree = new TTree("MatchedTree", "Matched Jets");
    double pt;
    MatchedTree->Branch("pt", &pt, "pt/D");
    double pts;
    MatchedTree->Branch("pts", &pts, "pts/D");
    double eta;
    MatchedTree->Branch("eta", &eta, "eta/D");
    double etas;
    MatchedTree->Branch("etas", &etas, "etas/D");
    double phi;
    MatchedTree->Branch("phi", &phi, "phi/D");
    double phis;
    MatchedTree->Branch("phis", &phis, "phis/D");
    double m;
    MatchedTree->Branch("m", &m, "m/D");
    double ms;
    MatchedTree->Branch("ms", &ms, "ms/D");
    double q;
    MatchedTree->Branch("q", &q, "q/D");
    double qs;
    MatchedTree->Branch("qs", &qs, "qs/D");
    double rg;
    MatchedTree->Branch("rg", &rg, "rg/D");
    double rgs;
    MatchedTree->Branch("rgs", &rgs, "rgs/D");
    double zg;
    MatchedTree->Branch("zg", &zg, "zg/D");
    double zgs;
    MatchedTree->Branch("zgs", &zgs, "zgs/D");
    double mg;
    MatchedTree->Branch("mg", &mg, "mg/D");
    double mgs;
    MatchedTree->Branch("mgs", &mgs, "mgs/D");
    int n;
    MatchedTree->Branch("n", &n, "n/I");
    int ns;
    MatchedTree->Branch("ns", &ns, "ns/I");
    int nch;
    MatchedTree->Branch("nch", &nch, "nch/I");
    int nchs;
    MatchedTree->Branch("nchs", &nchs, "nchs/I");
    double w;
    MatchedTree->Branch("w", &w, "w/D");
    double ws;
    MatchedTree->Branch("ws", &ws, "ws/D");
    int reject;
    MatchedTree->Branch("reject", &reject, "reject/I");
    int rejects;
    MatchedTree->Branch("rejects", &rejects, "rejects/I");
    int mcevi;
    MatchedTree->Branch("mcevi", &mcevi, "mcevi/I");
    int mult;
    MatchedTree->Branch("mult", &mult, "mult/I");
    int mults;
    MatchedTree->Branch("mults", &mults, "mults/I");
    int b;
    MatchedTree->Branch("b", &b, "b/I");
    int bs;
    MatchedTree->Branch("bs", &bs, "bs/I");
    double dr;
    MatchedTree->Branch("dr", &dr, "dr/D");
    double drs;
    MatchedTree->Branch("drs", &drs, "drs/D");
    double pt1;
    MatchedTree->Branch("pt1", &pt1, "pt1/D");
    double pt1s;
    MatchedTree->Branch("pt1s", &pt1s, "pt1s/D");
    double pt2;
    MatchedTree->Branch("pt2", &pt2, "pt2/D");
    double pt2s;
    MatchedTree->Branch("pt2s", &pt2s, "pt2s/D");
    double z;
    MatchedTree->Branch("z", &z, "z/D");
    double zs;
    MatchedTree->Branch("zs", &zs, "zs/D");
    double epair;
    MatchedTree->Branch("epair", &epair, "epair/D");
    double epairs;
    MatchedTree->Branch("epairs", &epairs, "epairs/D");
    double qlead;
    MatchedTree->Branch("qlead", &qlead, "qlead/D");
    double qleads;
    MatchedTree->Branch("qleads", &qleads, "qleads/D");
    double qsublead;
    MatchedTree->Branch("qsublead", &qsublead, "qsublead/D");
    double qsubleads;
    MatchedTree->Branch("qsubleads", &qsubleads, "qsubleads/D");
    double y1;
    MatchedTree->Branch("y1", &y1, "y1/D");
    double y1s;
    MatchedTree->Branch("y1s", &y1s, "y1s/D");
    double y2;
    MatchedTree->Branch("y2", &y2, "y2/D");
    double y2s;
    MatchedTree->Branch("y2s", &y2s, "y2s/D");
    double phi1;
    MatchedTree->Branch("phi1", &phi1, "phi1/D");
    double phi1s;
    MatchedTree->Branch("phi1s", &phi1s, "phi1s/D");
    double phi2;
    MatchedTree->Branch("phi2", &phi2, "phi2/D");
    double phi2s;
    MatchedTree->Branch("phi2s", &phi2s, "phi2s/D");
    double nef;
    MatchedTree->Branch("nef", &nef, "nef/D");
    double nefs;
    MatchedTree->Branch("nefs", &nefs, "nefs/D");
    int run;
    MatchedTree->Branch("run", &run, "run/I");

    TH1::SetDefaultSumw2();
    TH2::SetDefaultSumw2();
    gStyle->SetOptStat(0);

    int N = McChain->GetEntries();
    cout << "Number of Pythia events: " << N << endl;
    cout << "Number of Geant events:  " << PpChain->GetEntries() << endl;
    TStarJetVectorJet *dummyjet = new TStarJetVectorJet();

    // read lists of bad runs
    set<int> badrun_list;
    FILE *file = fopen("/gpfs01/star/pwg/youqi/run12/final/badrun_isaac.list", "r");
    char file_content[256];
    badrun_list.insert(0);
    while (fgets(file_content, 256, file) != NULL)
    {
        file_content[strcspn(file_content, "\n")] = 0;
        badrun_list.insert(atoi(file_content));
    }

    int tot_recojets = 0;
    int tot_recoevts = 0;

    for (Long64_t mcEvi = 0; mcEvi < N; ++mcEvi) // event loop
    {
        if (!(mcEvi % 100000))
            cout << "Working on " << mcEvi << " / " << N << endl;

        McChain->GetEntry(mcEvi);

        if (mcreject > 0) // skip bad events with high weights
        {
            continue; // go to the next MC event
        }
        if (abs(mcvz) > 30)
        /*
            see embedding_qa.pptx for why this is needed
            without this cut, tot_recoevts, tot_recojets = 7425500, 4240809
        */
        {
            continue;
        }
        if (badrun_list.find(mcrunid1) != badrun_list.end()) // this should always be false for 20235003 since bad runs are rejected in creating pythia.root already
        {
            return -1;
        }
        vector<RootResultStruct> mcresult;
        for (int j = 0; j < mcnjets; ++j)
        {
            TStarJetVectorJet *mcjet = (TStarJetVectorJet *)McJets->At(j);
            mcresult.push_back(RootResultStruct(*mcjet, mcjet->Pt(), mcjet->Eta(), mcjet->Rapidity(), mcjet->Phi(), mcjet->M(), mcrunid1, mcq[j], mcrg[j], mczg[j], mcmg[j], mcnef[j], mcn[j], mcnch[j], mcweight, mcreject, mcEvi, mcmult, mcvz, mcb[j], mcdr[j], mcpt1[j], mcpt2[j], mcz[j], mcepair[j], mcqlead[j], mcqsublead[j], mcy1[j], mcy2[j], mcphi1[j], mcphi2[j]));
        } // end of mcjet loop

        // ! Reset event variables
        pprunid1 = -9;
        ppweight = -9;

        int ppevi = PpChain->GetEntryNumberWithIndex(mcrunid, mceventid);
        PpChain->GetEntry(ppevi);
        vector<RootResultStruct> ppresult;

        if (ppevi >= 0)
        {
            if (abs(ppvz) > 30) // this should always be false for 20235003 since bad |vz| is rejected in MuDsts already
                return -1;
            if (badrun_list.find(pprunid1) != badrun_list.end()) // this should always be false for 20235003 since bad runs are rejected in creating geant.root already
                return -1;
            tot_recoevts += 1;
            for (int j = 0; j < ppnjets; ++j)
            {
                TStarJetVectorJet *ppjet = (TStarJetVectorJet *)PpJets->At(j);
                ppresult.push_back(RootResultStruct(*ppjet, ppjet->Pt(), ppjet->Eta(), ppjet->Rapidity(), ppjet->Phi(), ppjet->M(), pprunid1, rcq[j], rcrg[j], rczg[j], rcmg[j], rcnef[j], rcn[j], rcnch[j], ppweight, rcreject, mcEvi, rcmult, ppvz, rcb[j], rcdr[j], rcpt1[j], rcpt2[j], rcz[j], rcepair[j], rcqlead[j], rcqsublead[j], rcy1[j], rcy2[j], rcphi1[j], rcphi2[j]));
                tot_recojets += 1;
            }
        } // end of ppjet loop

        //! Sort them together
        vector<MatchedRootResultStruct> MatchedResult;
        if (mcresult.size() > 0)
        {
            for (vector<RootResultStruct>::iterator mcit = mcresult.begin(); mcit != mcresult.end();)
            {
                bool matched = false;
                if (ppresult.size() > 0)
                {
                    for (vector<RootResultStruct>::iterator ppit = ppresult.begin(); ppit != ppresult.end();)
                    {
                        Double_t deta = mcit->y - ppit->y;
                        Double_t dphi = TVector2::Phi_mpi_pi(mcit->phi - ppit->phi);
                        Double_t dr = TMath::Sqrt(deta * deta + dphi * dphi);
                        if (dr < RCut)
                        {
                            MatchedResult.push_back(MatchedRootResultStruct(*mcit, *ppit));
                            ppit = ppresult.erase(ppit);
                            matched = true;
                            break;
                        }
                        else
                        {
                            ++ppit;
                        }
                    }
                }
                if (matched)
                {
                    mcit = mcresult.erase(mcit);
                }
                else // misses
                {
                    MatchedResult.push_back(MatchedRootResultStruct(*mcit, RootResultStruct(*dummyjet, -9, -9, -9, -9, -9, pprunid1, -9, -9, -9, -9, -9, -9, -9, ppweight, rcreject, mcEvi, rcmult, ppvz, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9)));
                    ++mcit;
                }
            }
        }
        for (vector<RootResultStruct>::iterator ppit = ppresult.begin(); ppit != ppresult.end();) // fakes
        {
            MatchedResult.push_back(MatchedRootResultStruct(RootResultStruct(*dummyjet, -9, -9, -9, -9, -9, mcrunid1, -9, -9, -9, -9, -9, -9, -9, mcweight, mcreject, mcEvi, mcmult, mcvz, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9), *ppit));
            ++ppit;
        }

        for (vector<MatchedRootResultStruct>::iterator res = MatchedResult.begin(); res != MatchedResult.end(); ++res)
        {
            pt = res->first.pt;
            pts = res->second.pt;
            eta = res->first.eta;
            etas = res->second.eta;
            phi = res->first.phi;
            phis = res->second.phi;
            m = res->first.m;
            ms = res->second.m;
            n = res->first.n;
            ns = res->second.n;
            nch = res->first.nch;
            nchs = res->second.nch;
            q = res->first.q;
            qs = res->second.q;
            rg = res->first.rg;
            rgs = res->second.rg;
            zg = res->first.zg;
            zgs = res->second.zg;
            mg = res->first.mg;
            mgs = res->second.mg;
            w = res->first.weight;
            ws = res->second.weight;
            reject = res->first.reject;
            rejects = res->second.reject;
            mult = res->first.mult;
            mults = res->second.mult;
            nef = res->first.nef;
            nefs = res->second.nef;
            b = res->first.b;
            bs = res->second.b;
            dr = res->first.dr;
            drs = res->second.dr;
            pt1 = res->first.pt1;
            pt1s = res->second.pt1;
            pt2 = res->first.pt2;
            pt2s = res->second.pt2;
            qlead = res->first.qlead;
            qleads = res->second.qlead;
            qsublead = res->first.qsublead;
            qsubleads = res->second.qsublead;
            y1 = res->first.y1;
            y1s = res->second.y1;
            y2 = res->first.y2;
            y2s = res->second.y2;
            phi1 = res->first.phi1;
            phi1s = res->second.phi1;
            phi2 = res->first.phi2;
            phi2s = res->second.phi2;
            z = res->first.z;
            zs = res->second.z;
            epair = res->first.epair;
            epairs = res->second.epair;

            if ((res->second.mcevi != res->first.mcevi) && res->first.mcevi > 0 && res->second.mcevi > 0)
            {
                cout << "Event mismatch!" << endl;
                return -1;
            }

            if (res->second.mcevi > res->first.mcevi)
            {
                mcevi = res->second.mcevi;
            }
            else
            {
                mcevi = res->first.mcevi;
            }

            if ((res->second.runid1 != res->first.runid1) && res->first.runid1 > 0 && res->second.runid1 > 0)
            {
                cout << res->first.runid1 << ", " << res->second.runid1 << ", mismatch!" << endl;
                return -1;
            }

            if (res->second.runid1 > res->first.runid1)
            {
                run = res->second.runid1;
            }
            else
            {
                run = res->first.runid1;
            }
            MatchedTree->Fill();
        }
    }

    std::cout << tot_recoevts << ", " << tot_recojets << std::endl;
    fout->Write();

    return 0;
}