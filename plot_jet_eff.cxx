void plot_jet_eff()
{
    TH1::SetDefaultSumw2();
    gStyle->SetPaintTextFormat("5.2f");
    gStyle->SetOptStat(0);

    TFile *File = new TFile("/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124.root");
    TTree *t = (TTree *)File->Get("MatchedTree");

    double pt_bin[5] = {20, 25, 30, 40, 60};
    TH1 *h_pt = new TH1D("h_pt", ";truth p_{T} [GeV/c]", 4, pt_bin);
    TH1D *h_numerator[4];
    TH1D *h_denominator[4];
    for (int i = 0; i < 4; i++)
    {
        h_numerator[i] = new TH1D(Form("h_numerator_%i", i), Form("p_{T} bin %i; truth M [GeV/c^{2}];efficiency", i), 10, 0, 10);
        h_denominator[i] = new TH1D(Form("h_denominator_%i", i), Form("p_{T} bin %i; truth M [GeV/c^{2}];efficiency", i), 10, 0, 10);
    } 
    
    double w;
    t->SetBranchAddress("w", &w);
    double pt;
    t->SetBranchAddress("pt", &pt);
    double pts;
    t->SetBranchAddress("pts", &pts);
    double m;
    t->SetBranchAddress("m", &m);

    for (int i = 0; i < t->GetEntries(); i++)
    {
        t->GetEntry(i);
        if (pt < 20 || pt > 60 || w > 1)
        {
            continue;
        }
            
        int i_pt_bin = h_pt->FindBin(pt)-1;
        //std::cout << pt << ", " << i_pt_bin << std::endl;
        h_denominator[i_pt_bin]->Fill(m, w);
        if (pts > 0) // matched
        {
            h_numerator[i_pt_bin]->Fill(m, w);
        }
    }

    TCanvas *c;
    for (int i = 0; i < 4; i++)
    {
        c = new TCanvas(Form("c%i", i), "c");
        h_numerator[i]->Divide(h_denominator[i]);
        h_numerator[i]->GetYaxis()->SetRangeUser(0, 1);
        h_numerator[i]->Draw("text00");
        h_numerator[i]->GetXaxis()->SetTitleSize(0.05);
        h_numerator[i]->GetYaxis()->SetTitleSize(0.05);
        h_numerator[i]->GetXaxis()->SetLabelSize(0.05);
        h_numerator[i]->GetYaxis()->SetLabelSize(0.05);
    }
}