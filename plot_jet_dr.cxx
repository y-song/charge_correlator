#include <TStyle.h>
#include <TCanvas.h>
#include <TH1.h>
#include <TH2.h>
#include <TLegend.h>
#include <TLine.h>
#include <TFile.h>
#include <TTree.h>
#include <TVector2.h>
#include <TMath.h>

void FormatHist(TLegend *l, TH1 *hist, TString text)
{
    hist->SetMarkerSize(0.5);

    hist->GetXaxis()->SetTitleOffset(1.1);
    hist->GetYaxis()->SetTitleOffset(0.85);
    hist->GetXaxis()->SetTitleSize(0.042);
    hist->GetYaxis()->SetTitleSize(0.042);
    hist->GetXaxis()->SetTitleFont(42);
    hist->GetYaxis()->SetTitleFont(42);

    hist->GetXaxis()->SetLabelSize(0.042);
    hist->GetYaxis()->SetLabelSize(0.042);
    hist->GetXaxis()->SetLabelOffset(0.015);
    hist->GetYaxis()->SetLabelOffset(0.005);
    hist->GetXaxis()->SetLabelFont(42);
    hist->GetYaxis()->SetLabelFont(42);

    l->AddEntry(hist, text, "pl");

    return;
}

void plot_jet_dr()
{
    TH1::SetDefaultSumw2();
    gStyle->SetOptStat(0);
    // gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    gStyle->SetPadColor(10);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetPadLeftMargin(0.15);
    gStyle->SetCanvasBorderMode(0);
    gStyle->SetFrameLineWidth(1);
    gStyle->SetFrameFillColor(kWhite);

    TFile *File = new TFile("/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc_notrueptcons.root");
    TTree *t = (TTree *)File->Get("MatchedTree");
    TH1 *h_dr = new TH1D("h_dr", ";#Delta#it{R}_{jet}(truth, det.);probability", 20, 0, 0.5);
    
    double w;
    t->SetBranchAddress("w", &w);
    double pt;
    t->SetBranchAddress("pt", &pt);
    double eta;
    t->SetBranchAddress("eta", &eta);
    double phi;
    t->SetBranchAddress("phi", &phi);
    double pts;
    t->SetBranchAddress("pts", &pts);
    double etas;
    t->SetBranchAddress("etas", &etas);
    double phis;
    t->SetBranchAddress("phis", &phis);

    for (int i = 0; i < t->GetEntries(); i++)
    {
        t->GetEntry(i);
        if (pt < 5 || pts < 15 || w > 1) // matched
        {
            continue;
        }
            
        Double_t deta = eta - etas;
        Double_t dphi = TVector2::Phi_mpi_pi(phi - phis);
        Double_t dr = TMath::Sqrt(deta * deta + dphi * dphi);
        h_dr->Fill(dr, w);
        /*if (dr > 0.4)
        {
            std::cout << dr << std::endl;
        }*/
    }
    h_dr->Scale(1.0/h_dr->Integral());

    TCanvas *c = new TCanvas("c", "c");
    c->SetLogy();

    h_dr->GetXaxis()->SetTitleSize(0.05);
    h_dr->GetYaxis()->SetTitleSize(0.05);
    h_dr->GetXaxis()->SetLabelSize(0.05);
    h_dr->GetYaxis()->SetLabelSize(0.05);
    h_dr->GetXaxis()->SetRangeUser(0,0.45);
    h_dr->GetYaxis()->SetRangeUser(1e-5,1.);
    h_dr->Draw();

    c->SaveAs("jet_dr_pts15_notrueptcons.pdf");

}