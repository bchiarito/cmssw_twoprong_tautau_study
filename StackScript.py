import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def draw_and_save_stack(plot,file_names,data_file,qcd_files,osss,has_ss):
    print(plot)
    dataclone=None
    clone1=None
    integral1=0
    clone2=None
    integral2=0
    clone3=None
    integral3=0
    clone4=None
    clone4_2=None
    integral4=0
    clone5=None
    integral5=0
    clone6=None
    integral6=0
    clone7=None
    integral7=0
    dfile=None
    file1=None
    file2=None
    file3=None
    file4= None
    file5= None
    file5 = None
    file6= None
    file7= None

    is_anti=False
    c1 = ROOT.TCanvas("canvas", "Stacked Histograms", 800, 600)
    plotname = "plots/"  + plot
    stack1 = ROOT.THStack("stack", "Stacked Histograms")
    dfile = ROOT.TFile(data_file, "READ")

    #print(plotname)
    cutValue = 25
    scale = False
    datahist=dfile.Get(plotname)

    #datahist.GetXaxis().SetRangeUser(cutValue, datahist.GetXaxis().GetXmax())
    dataclone=datahist.Clone()
    dataclone.SetLineColor(1)
    dataclone.SetLineWidth(2)
    dataintegral = dataclone.Integral()
    dataclone.SetBinErrorOption(ROOT.TH1.kPoisson)
#    if dataintegral==0: dataintegral = 1
    #dataclone.Scale(10)
    if has_ss:
        plotname_qcd = remove_last_two_characters_if_criteria_met(plotname, "_c") + "_ss_c"
        print("!!! ",plotname_qcd)
        file4 = dfile
        histogram4 = file4.Get(plotname_qcd)
        histogram4.SetFillColor(5)
         # i + 2 to avoid default colors
    #    histogram3.GetXaxis().SetRangeUser(cutValue, histogram3.GetXaxis().GetXmax());
        clone4=histogram4.Clone()
        clone4_2=histogram4.Clone()
        integral4=clone4.Integral()
    #    if integral4==0: integral4 = 1
        #clone4.Scale(10)

        file5 = ROOT.TFile(file_names[0], "READ")
        histogram5 = file5.Get(plotname_qcd)
        histogram5.SetFillColor(2)  # i + 2 to avoid default colors
    #    histogram3.GetXaxis().SetRangeUser(cutValue, histogram3.GetXaxis().GetXmax());
        clone5=histogram5.Clone()
        integral5=clone5.Integral()
    #    if integral5==0: integral5 = 1
    #    if scale: clone5.Scale(1/integral5)

        file6 = ROOT.TFile(file_names[1], "READ")
        histogram6 = file6.Get(plotname_qcd)
        histogram6.SetFillColor(3)  # i + 2 to avoid default colors
    #    histogram3.GetXaxis().SetRangeUser(cutValue, histogram3.GetXaxis().GetXmax());
        clone6=histogram6.Clone()
        integral6=clone6.Integral()
    #    if integral6==0: integral6 = 1
    #    if scale: clone6.Scale(1/integral6)

        file7 = ROOT.TFile(file_names[2], "READ")
        histogram7 = file7.Get(plotname_qcd)
        histogram7.SetFillColor(4)  # i + 2 to avoid default colors
    #    histogram3.GetXaxis().SetRangeUser(cutValue, histogram3.GetXaxis().GetXmax());
        clone7=histogram7.Clone()
        integral7=clone7.Integral()
        #if integral7==0: integral7 = 1
        #if scale: clone7.Scale(1/integral7)

        clone4.Add(clone5, -1)
        clone4.Add(clone6, -1)
        clone4.Add(clone7, -1)
        clone4.Scale(osss)
        if is_anti == False:
            stack1.Add(clone4)

    file1 = ROOT.TFile(file_names[0], "READ")
    histogram1 = file1.Get(plotname)
    histogram1.SetFillColor(2)  # i + 2 to avoid default colors
#    histogram1.GetXaxis().SetRangeUser(cutValue, histogram1.GetXaxis().GetXmax())
    #histogram.Draw("same")
    clone1=histogram1.Clone()
    integral1=clone1.Integral()
    #if integral1==0: integral1 = 1
    #if scale: clone1.Scale(1/integral1)
    # Add the histogram to the stack
    stack1.Add(clone1)

    file2 = ROOT.TFile(file_names[1], "READ")
    histogram2 = file2.Get(plotname)
    histogram2.SetFillColor(3)  # i + 2 to avoid default colors
    #histogram.Draw("same")
#    histogram2.GetXaxis().SetRangeUser(cutValue, histogram2.GetXaxis().GetXmax())
    clone2=histogram2.Clone()
    integral2=clone2.Integral()
#    if integral2==0: integral2 = 1
    #if scale: clone2.Scale(1/integral2)
    # Add the histogram to the stack
    stack1.Add(clone2)

    file3 = ROOT.TFile(file_names[2], "READ")
    histogram3 = file3.Get(plotname)
    histogram3.SetFillColor(4)  # i + 2 to avoid default colors
#    histogram3.GetXaxis().SetRangeUser(cutValue, histogram3.GetXaxis().GetXmax());
    clone3=histogram3.Clone()
    integral3=clone3.Integral()
#    if integral3==0: integral3 = 1
#    if scale: clone3.Scale(1/integral3)
    stack1.Add(clone3)



    dataclone.Draw("e")
    stack1.Draw("hist same")
    dataclone.Draw("samee")
    legend = ROOT.TLegend(0.6, 0.6, 0.99, 0.9)
    if is_anti==False and has_ss:
        legend.AddEntry(stack1.GetHists().At(1), "WJets " + str(round(integral1,2)), "f")
        legend.AddEntry(stack1.GetHists().At(2),"TTJets " + str(round(integral2,2)), "f")
        legend.AddEntry(stack1.GetHists().At(3), "DYJets " + str(round(integral3,2)), "f")
        legend.AddEntry(stack1.GetHists().At(0), "QCD " + str(round(round(integral4,2)-round(integral5,2)-round(integral6,2)-round(integral7,2),2)), "f")
        legend.AddEntry(dataclone, "SM2018 "+ str(round(dataintegral,2)), "f")
        legend.Draw()
    else:
        legend.AddEntry(stack1.GetHists().At(0), "WJets " + str(round(integral1,2)), "f")
        legend.AddEntry(stack1.GetHists().At(1),"TTJets " + str(round(integral2,2)), "f")
        legend.AddEntry(stack1.GetHists().At(2), "DYJets " + str(round(integral3,2)), "f")
        legend.AddEntry(dataclone, "SM2018 "+ str(round(dataintegral,2)), "f")
        legend.Draw()
    savename = plot + ".png"
    c1.SaveAs(savename)

    # Create a new ROOT file
    #output_file = ROOT.TFile("stacked_histograms.root", "RECREATE")
    output_file_name = "stacked_histograms.root"
    is_existing_file = os.path.isfile(output_file_name)
    output_file = ROOT.TFile(output_file_name, "UPDATE" if is_existing_file else "RECREATE")
    #stack1.Write()
    stack1=None
    stack2 = None
    c1.Write(plot)
    legend = None
    legend2= None
    c1.Clear()
    if has_ss:
#    if plotname == "plots/Z_massTau_os" or plotname == "plots/Z_massTau_ss":
        c1.Clear()
        stack2 = ROOT.THStack("stack", "Stacked Histograms AntiIso")
        stack2.Add(clone5)
        stack2.Add(clone6)
        stack2.Add(clone7)

        #clone4.Add(clone5, 1)
        #clone4.Add(clone6, 1)
        #clone4.Add(clone7, 1)
        clone4_2.SetFillColor(0)
        clone4_2.SetLineColor(1)
        clone4_2.SetLineWidth(2)
        clone4_2.SetBinErrorOption(ROOT.TH1.kPoisson)

        clone4_2.Draw("E")
        stack2.Draw("HISTSAME")
        clone4_2.Draw("SAMEE")
        legend2 = ROOT.TLegend(0.6, 0.6, 0.99, 0.9)

        legend2.AddEntry(stack2.GetHists().At(0), "WJets " + str(round(integral5,2)), "f")
        legend2.AddEntry(stack2.GetHists().At(1),"TTJets " + str(round(integral6,2)), "f")
        legend2.AddEntry(stack2.GetHists().At(2), "DYJets " + str(round(integral7,2)), "f")
        legend2.AddEntry(clone4_2, "SM2018 "+ str(round(integral4,2)), "f")
        legend2.Draw()

        savename2 = plot + "_ss" +".png"
        c1.SaveAs(savename2)
        c1.Write(plot+"_ss")



    output_file.Close()
    file1.Close()
    file2.Close()
    file3.Close()
    dfile.Close()


def get_total_entries_greater_than_value(file_path, histogram_name, threshold):
    # Open a ROOT file containing your histogram
    file = ROOT.TFile.Open(file_path)

    # Get the TH1D histogram from the file
    histogram = file.Get(histogram_name)

    # Get the number of bins in the histogram
    num_bins = histogram.GetNbinsX()

    # Initialize a variable to store the total number of entries
    total_entries_greater_than_value = 0
    #print("histogram ", histogram_name)
    # Loop over each bin of the histogram
    for i in range(0, num_bins + 1):
        # Get the bin center value
        bin_center = histogram.GetBinCenter(i)

        # Check if the bin center value is greater than the threshold
        if bin_center > threshold:
            # Increment the total entries count by the bin content
        #    print("Bin Content ",  i, histogram.GetBinContent(i))
            total_entries_greater_than_value += histogram.GetBinContent(i)

    # Close the file
    #file.Close()

    # Return the total number of entries greater than the threshold
    return total_entries_greater_than_value
def get_total_entries_one_bin(file_path, histogram_name,threshold,bin):
    # Open a ROOT file containing your histogram
    file = ROOT.TFile.Open(file_path)

    # Get the TH1D histogram from the file
    histogram = file.Get(histogram_name)
    bin_center = histogram.GetBinCenter(bin)

    # Check if the bin center value is greater than the threshold
    if bin_center > threshold:
        # Increment the total entries count by the bin content
        #    print("Bin Content ",  i, histogram.GetBinContent(i))
        return histogram.GetBinContent(bin)
    else:
        return 0


    # Close the file
    #file.Close()

    # Return the total number of entries greater than the threshold
    return total_entries_greater_than_value
def qcd_bin_dist(qcd_files):
        plotname_os = "plots/Z_massTau_c"
        plotname_ss = "plots/Z_massTau_ss_c"
        threshold = -100
        file = ROOT.TFile.Open(qcd_files[0])
        histogram = file.Get(plotname_os)
        sf_bin_dist = ROOT.TH1D("OS-SS Scale Factor By Bin", "OS-SS Scale Factor By Bin", 100, 0, 400)
        num_bins = histogram.GetNbinsX()
        for i in range(0, num_bins + 1):
            #Data
            os4 = get_total_entries_one_bin(qcd_files[0], plotname_os, threshold,i)
            ss4 = get_total_entries_one_bin(qcd_files[0], plotname_ss, threshold,i)
            #WJets
            os5 = get_total_entries_one_bin(qcd_files[1], plotname_os, threshold,i)
            ss5 = get_total_entries_one_bin(qcd_files[1], plotname_ss, threshold,i)
            #TTJets
            os6 = get_total_entries_one_bin(qcd_files[2], plotname_os, threshold,i)
            ss6 = get_total_entries_one_bin(qcd_files[2], plotname_ss, threshold,i)
            #DyJets
            os7 = get_total_entries_one_bin(qcd_files[3], plotname_os, threshold,i)
            ss7 = get_total_entries_one_bin(qcd_files[3], plotname_ss, threshold,i)

            os = os4 - os5 - os6 - os7
            ss = ss4 - ss5 - ss6 - ss7
            print("Anti Iso SM18 os " , os4)
            print("Anti Iso WJets os " , os5)
            print("Anti Iso TTJets os " , os6)
            print("Anti Iso DYJets os " , os7)
            print("Anti Iso SM18 ss " , ss4)
            print("Anti Iso WJets ss " , ss5)
            print("Anti Iso TTJets ss " , ss6)
            print("Anti Iso DYJets ss " , ss7)
            print("ss " , ss)
            print("os " , os)
            if ss!=0:
                osss=abs(os/ss)
            else:
                osss = 0
            sf_bin_dist.SetBinContent(i,osss)

        canvas = ROOT.TCanvas("canvas", "TH1D Example", 800, 600)
        #canvas.SetLogy()
        sf_bin_dist.Draw()



        #canvas.Modified()
        canvas.Update()
        canvas.Draw()
        canvas.SaveAs("os_ss_bin_dist.png")
    #    print("os ss DY" , os7, " " , ss7)
        return 0
def qcd_scale_factor(qcd_files):
        plotname_os = "plots/Z_massTau_c"
        plotname_ss = "plots/Z_massTau_ss_c"
        threshold = -100

        os4 = get_total_entries_greater_than_value(qcd_files[0], plotname_os, threshold)
        ss4 = get_total_entries_greater_than_value(qcd_files[0], plotname_ss, threshold)
        os5 = get_total_entries_greater_than_value(qcd_files[1], plotname_os, threshold)
        ss5 = get_total_entries_greater_than_value(qcd_files[1], plotname_ss, threshold)
        os6 = get_total_entries_greater_than_value(qcd_files[2], plotname_os, threshold)
        ss6 = get_total_entries_greater_than_value(qcd_files[2], plotname_ss, threshold)
        os7 = get_total_entries_greater_than_value(qcd_files[3], plotname_os, threshold)
        ss7 = get_total_entries_greater_than_value(qcd_files[3], plotname_ss, threshold)

        os = os4 - os5 - os6 - os7
        ss = ss4 - ss5 - ss6 - ss7
        print("Anti Iso SM18 os " , os4)
        print("Anti Iso WJets os " , os5)
        print("Anti Iso TTJets os " , os6)
        print("Anti Iso DYJets os " , os7)
        print("Anti Iso SM18 ss " , ss4)
        print("Anti Iso WJets ss " , ss5)
        print("Anti Iso TTJets ss " , ss6)
        print("Anti Iso DYJets ss " , ss7)
        print("ss " , ss)
        print("os " , os)

        osss=abs(os/ss)

    #    print("os ss DY" , os7, " " , ss7)
        return osss
def process_all_histograms(file_names,data_file,qcd_files):
    # Open the ROOT file
    file = ROOT.TFile(data_file, "READ")
    traverse_directory(file, file)

            # Call the generic method with the histogram name as input
        #draw_and_save_stack(histogram_name)
def traverse_directory(directory, file, parent_dir=""):
    # Recursively traverse the directory structure
    osss = qcd_scale_factor(qcd_files_)
    has_ss = False
    for key in directory.GetListOfKeys():
        if key.IsFolder():
            # If the key is a folder, recursively call traverse_directory
            folder_name = key.GetName()
            new_parent_dir = f"{parent_dir}/{folder_name}" if parent_dir else folder_name
            traverse_directory(key.ReadObj(), file, new_parent_dir)
        #elif key.GetClassName() == "TH1":
        else:
            # If the key is a TH1 histogram, construct the full histogram name
            histogram_name = key.GetName()
        #    full_histogram_name = f"{parent_dir}/{histogram_name}" if parent_dir else histogram_name
            # Call the generic method with the full histogram name as input
            histogram_name_ss = remove_last_two_characters_if_criteria_met(histogram_name, "_c") + "_ss_c"
            print("have ss? ", histogram_name_ss)
            hist_ss_test = file.Get("plots/"+histogram_name_ss)
            if hist_ss_test or isinstance(hist_ss_test, ROOT.TH1D):
                print("have ss! ", histogram_name_ss)
                has_ss = True
            else: has_ss = False
            print(histogram_name)
            if string_criteria4(histogram_name,"_ss_c")==False: draw_and_save_stack(histogram_name,file_names_,data_file_,qcd_files_,osss,has_ss)
    # Close the file
    print("OS/SS Scale Factor: " ,osss)

    file.Close()

def create_ratio_histogram(file_path, histogram_name1, histogram_name2, ratio_hist_name):
    # Open ROOT files containing your histograms
    file1 = ROOT.TFile(file_path, "READ")


    # Get the TH1D histograms from the files
    histogram1 = file1.Get(histogram_name1)
    print(isinstance(histogram1, ROOT.TH1D))
    histogram2 = file1.Get(histogram_name2)
    print(isinstance(histogram2, ROOT.TH1D))
    # Create a new TH1D for the ratio
    ratio_histogram = ROOT.TH1D(ratio_hist_name,ratio_hist_name, 100, 0, 100)
    #ratio_histogram = ratio_histogram_temp.Clone()
    # Loop over each bin of the histograms
    for i in range(1, histogram1.GetNbinsX() + 1):
        # Get the bin content for each histogram
        content1 = histogram1.GetBinContent(i)
        content2 = histogram2.GetBinContent(i)

        # Calculate the ratio of bin contents, avoiding division by zero
        if content2 != 0:
            ratio = content1 / content2
        else:
            ratio = 0

        # Set the bin content of the ratio histogram
        ratio_histogram.SetBinContent(i, ratio)

    # Close the files
    #file1.Close()
    print("ratio ", isinstance(ratio_histogram, ROOT.TH1D))
    return ratio_histogram

def string_criteria(input_string,criteria):
    if input_string[-2:] == criteria: return True
    else: return False
def string_criteria4(input_string,criteria):
    if input_string[-4:] == criteria: return True
    else: return False
def remove_last_two_characters_if_criteria_met(input_string, criteria):
    # Check if the input string's last two characters meet the criteria
    if string_criteria(input_string,criteria):
        # Remove the last two characters
        modified_string = input_string[:-2]
    else:
        modified_string = input_string
        print(modified_string)
    return modified_string
def traverse_directory2(directory, file, file_names,parent_dir=""):
    # Recursively traverse the directory structure
    for key in directory.GetListOfKeys():
        if key.IsFolder():
            # If the key is a folder, recursively call traverse_directory
            folder_name = key.GetName()
            new_parent_dir = f"{parent_dir}/{folder_name}" if parent_dir else folder_name
            traverse_directory2(key.ReadObj(), file, new_parent_dir)
        else:
            histogram_name = key.GetName()
            plot_normalizer(histogram_name,file_names)
def plot_normalizer(plot,file_names):
    c1 = ROOT.TCanvas("canvas", "Norm Histograms", 800, 600)
    file1 = ROOT.TFile(files_norm[0], "READ")
    file2 = ROOT.TFile(files_norm[1], "READ")
    tot1=238631794
    tot2=206506162
    # Get the TH1D histograms from the files
    histogram1 = file1.Get("plots/"+plot)
    histogram2 = file2.Get("plots/"+plot)
    if ( histogram1 or isinstance(histogram1, ROOT.TH1D)) and (histogram2 or isinstance(histogram2, ROOT.TH1D)):
        integral1=histogram1.Integral()
        if integral1==0: integral1 = 1
        histogram1.Scale(1/integral1)
        print(isinstance(histogram1, ROOT.TH1D))
        integral2=histogram2.Integral()
        if integral2==0: integral2 = 1
        histogram2.Scale(1/integral2)
        print(isinstance(histogram2, ROOT.TH1D))
        histogram1.Draw()
        c1.SaveAs(plot+"_old_norm.png")
        histogram2.Draw()
        c1.SaveAs(plot+"_new_norm.png")
        histogram1.SetLineColor(2)
        histogram1.Draw()
        histogram1.SetLineColor(2)
        histogram2.Draw("SAME")
        #legend2 = ROOT.TLegend(0.6, 0.6, 0.99, 0.9)
        #legend2.AddEntry(histogram1, "Old ", "f")
        #legend2.AddEntry(histogram2,"New " , "f")
        #legend2.Draw()
        c1.SaveAs("Comparison_"+plot+"_norm.png")
def norm_plot_comp(file_names):
    fn=file_names
    file = ROOT.TFile(file_names[1], "READ")
    traverse_directory2(file,file,fn)
#file_names = ["/mnt/c/Users/Sean/mumu/histograms_WJets_mumu.root","/mnt/c/Users/Sean/mumu/histograms_TTJets_mumu.root", "/mnt/c/Users/Sean/mumu/histograms_DYJets_mumu.root"]
#data_file = "/mnt/c/Users/Sean/mumu/histograms_SingleMuon2018_mumu.root"

#file_names = ["/mnt/c/Users/Sean/tpcheck/histograms_WJets_tpcheck.root","/mnt/c/Users/Sean/tpcheck/histograms_TTJets_tpcheck.root", "/mnt/c/Users/Sean/tpcheck/histograms_DYJets_tpcheck.root"]
#data_file = "/mnt/c/Users/Sean/tpcheck/histograms_SingleMuon2018_tpcheck.root"

#file_names = ["/mnt/c/Users/Sean/Trig_Muon_Cuts/histograms_WJets_trig_muon_cuts.root","/mnt/c/Users/Sean/Trig_Muon_Cuts/histograms_TTJets_trig_muon_cuts.root", "/mnt/c/Users/Sean/Trig_Muon_Cuts/histograms_DYJetsToLL_trig_muon_cuts.root"]
#data_file = "/mnt/c/Users/Sean/Trig_Muon_Cuts/histograms_SingleMuon2018_Trig_Muon_Cuts.root"


file_names_ = ["/mnt/c/Users/Sean/Crunch/WJets_oct24_iso_hists.root","/mnt/c/Users/Sean/Crunch/TTJets_oct24_iso_hists.root","/mnt/c/Users/Sean/Crunch/DYJets_oct24_iso_hists.root"]
qcd_files_ = ["/mnt/c/Users/Sean/Crunch/SM18A_oct24_anti_histograms.root","/mnt/c/Users/Sean/Crunch/WJets_oct24_anti_hists.root","/mnt/c/Users/Sean/Crunch/TTJets_oct24_anti_hists.root","/mnt/c/Users/Sean/Crunch/DYJets_oct24_anti_hists.root"]
data_file_ = "/mnt/c/Users/Sean/Crunch/SM18A_oct24_iso_histograms.root"

#file_names_ = ["/mnt/c/Users/Sean/tight_and_HEM/WJets_tight_antiiso_histograms.root","/mnt/c/Users/Sean/tight_and_HEM/TTJets_tight_antiiso_histograms.root","/mnt/c/Users/Sean/tight_and_HEM/DYJets_tight_antiiso_histograms.root"]
#data_file_ ="/mnt/c/Users/Sean/tight_and_HEM/SingleMuon2018_tight_antiiso_histograms.root"

#files_norm = ["/mnt/c/Users/Sean/tight_and_HEM/SingleMuon2018A_tight_iso_histograms.root","/mnt/c/Users/Sean/SM18/SM18A_aug24_iso_hists.root"]


#qcd_files_ = ["/mnt/c/Users/Sean/iso_antiiso/histograms_SingleMuon2018_antiiso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_WJets_antiiso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_TTJets_antiiso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_DYJets_antiiso.root"]
#file_names_ = ["/mnt/c/Users/Sean/iso_antiiso/histograms_WJets_iso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_TTJets_iso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_DYJets_iso.root"]
#data_file_ = "/mnt/c/Users/Sean/iso_antiiso/histograms_SingleMuon2018_iso.root"

#file_names_ = ["/mnt/c/Users/Sean/iso_antiiso/histograms_WJets_antiiso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_TTJets_antiiso.root","/mnt/c/Users/Sean/iso_antiiso/histograms_DYJets_antiiso.root"]
#data_file_ = "/mnt/c/Users/Sean/iso_antiiso/histograms_SingleMuon2018_antiiso.root"

#norm_plot_comp(files_norm)
process_all_histograms(file_names_,data_file_,qcd_files_)
#qcd_bin_dist(qcd_files_)
