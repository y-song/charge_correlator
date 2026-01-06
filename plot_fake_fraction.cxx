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

void plot_fake_fraction()
{
    TH1::SetDefaultSumw2();
    gStyle->SetPaintTextFormat("5.2f");
    gStyle->SetOptStat(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    gStyle->SetPadColor(10);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetPadLeftMargin(0.15);
    gStyle->SetCanvasBorderMode(0);
    gStyle->SetFrameLineWidth(1);
    gStyle->SetFrameFillColor(kWhite);

    TFile *File = new TFile("/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc_notrueptcons.root");
    TTree *t = (TTree *)File->Get("MatchedTree");
    
    double pt_bin[6] = {15, 20, 25, 30, 40, 60};
    TH1 *h_pt = new TH1D("h_pt", ";reco p_{T} [GeV/c]", 5, pt_bin);
    TH1 *h1_pt = new TH1D("h1_pt", ";#it{p}_{T}^{det} [GeV/#it{c}];matched jet fraction", 5, pt_bin);
    TH1 *h2_pt = new TH1D("h2_pt", ";reco p_{T} [GeV/c]", 5, pt_bin);
    TH1 *h3_pt = new TH1D("h3_pt", ";reco p_{T} [GeV/c]", 5, pt_bin);
    
    double w;
    t->SetBranchAddress("w", &w);
    double ws;
    t->SetBranchAddress("ws", &ws);
    double pt;
    t->SetBranchAddress("pt", &pt);
    int nch;
    t->SetBranchAddress("nch", &nch);
    double y1;
    t->SetBranchAddress("y1", &y1);
    double y2;
    t->SetBranchAddress("y2", &y2);
    double phi1;
    t->SetBranchAddress("phi1", &phi1);
    double phi2;
    t->SetBranchAddress("phi2", &phi2);
    double pts;
    t->SetBranchAddress("pts", &pts);
    int nchs;
    t->SetBranchAddress("nchs", &nchs);
    double y1s;
    t->SetBranchAddress("y1s", &y1s);
    double y2s;
    t->SetBranchAddress("y2s", &y2s);    
    double phi1s;
    t->SetBranchAddress("phi1s", &phi1s);
    double phi2s;
    t->SetBranchAddress("phi2s", &phi2s);

    for (int i = 0; i < t->GetEntries(); i++)
    {
        t->GetEntry(i);
        if (pts < 15 || w >= 1 || nchs < 2) // all reco
        {
            continue;
        }
 
        h_pt->Fill(pts, w);
        
        if (pt > 5)
        {
            h1_pt->Fill(pts, w);

            if (nch >= 2)
            {
                h2_pt->Fill(pts, w);

                Double_t dy1 = y1 - y1s;
                Double_t dphi1 = TVector2::Phi_mpi_pi(phi1 - phi1s);
                Double_t dr1 = TMath::Sqrt(dy1 * dy1 + dphi1 * dphi1);
                Double_t dy2 = y2 - y2s;
                Double_t dphi2 = TVector2::Phi_mpi_pi(phi2 - phi2s);
                Double_t dr2 = TMath::Sqrt(dy2 * dy2 + dphi2 * dphi2);
                if (dr1 < 0.02 && dr2 < 0.02)
                {
                    h3_pt->Fill(pts, w);
                }
            }
        }

    }
    h1_pt->Divide(h_pt);
    h2_pt->Divide(h_pt);
    h3_pt->Divide(h_pt);

    TCanvas *c = new TCanvas("c", "c", 525, 375);
    TLegend *leg = new TLegend(0.45, 0.17, 0.9, 0.37);

    FormatHist(leg, h1_pt, "cut 1: #Delta#it{R}_{jet} < 0.4");
    FormatHist(leg, h2_pt, "cut 2: cut 1 + truth #it{N}_{#it{ch}} #geq 2");
    FormatHist(leg, h3_pt, "cut 3: cut 2 + #Delta#it{R}_{track} < 0.02");
    h1_pt->GetYaxis()->SetRangeUser(0, 1.1);
    h1_pt->SetLineColor(1);
    h2_pt->SetLineColor(4);
    h3_pt->SetLineColor(2);
    h1_pt->Draw();
    h2_pt->Draw("same");
    h3_pt->Draw("same");

    leg->SetTextSize(0.042);
    leg->SetBorderSize(0);
    leg->SetFillStyle(0); 
    leg->Draw();

    c->SaveAs("fake_fraction_pts15_notrueptcons.pdf");
}