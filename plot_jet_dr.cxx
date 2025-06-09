void plot_jet_dr()
{
    TH1::SetDefaultSumw2();
    gStyle->SetPaintTextFormat("5.2f");
    gStyle->SetOptStat(0);

    TFile *File = new TFile("/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124.root");
    TTree *t = (TTree *)File->Get("MatchedTree");
    TH1 *h_dr = new TH1D("h_dr", ";#DeltaR(truth, reco);probability", 20, 0, 0.5);
    
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
        if (pt < 5 || pts < 20 || w > 1) // matched
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
    h_dr->Draw();
}