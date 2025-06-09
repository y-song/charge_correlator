void plot_fake_fraction()
{
    TH1::SetDefaultSumw2();
    gStyle->SetPaintTextFormat("5.2f");
    gStyle->SetOptStat(0);

    TFile *File = new TFile("/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc.root");
    TTree *t = (TTree *)File->Get("MatchedTree");
    
    double pt_bin[6] = {15, 20, 25, 30, 40, 60};
    TH1 *h_pt = new TH1D("h_pt", ";reco p_{T} [GeV/c]", 5, pt_bin);
    TH1 *h1_pt = new TH1D("h1_pt", ";reco p_{T} [GeV/c];matched fraction", 5, pt_bin);
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

    TCanvas *c = new TCanvas("c", "c", 600, 600);
    h1_pt->GetXaxis()->SetTitleSize(0.05);
    h1_pt->GetYaxis()->SetTitleSize(0.05);
    h1_pt->GetXaxis()->SetLabelSize(0.05);
    h1_pt->GetYaxis()->SetLabelSize(0.05);
    h1_pt->GetYaxis()->SetRangeUser(0, 1);
    h1_pt->SetLineColor(1);
    h2_pt->SetLineColor(4);
    h3_pt->SetLineColor(2);
    h1_pt->Draw();
    h2_pt->Draw("same");
    h3_pt->Draw("same");

    TLegend *legend = new TLegend(0.7, 0.1, 0.9, 0.3);
    legend->AddEntry(h1_pt);
    legend->AddEntry(h2_pt);
    legend->AddEntry(h3_pt);
    legend->Draw();
}