# THIS PYTHON CODE UNPACK RAW MOD09A1 DATA AND EXTRACT THE FOLLOWING LAYERS:

# SPECTRAL BANDS:
# MODIS Band 1 (sur_refl_b01_1), MODIS Band 2 (sur_refl_b02_1), MODIS Band 6 (sur_refl_b06_1) and MODIS Band 7 (sur_refl_b07_1)

# QUALITY DATA
# The bit 2-5, bit 6-9, bit 22-25 and bit 26-29 of SDS 'QC_500m_1' representing Band1, Band2, Band6 and Band7 data quality info
# The bit 0-1, bit 2 and bit 8-9 of SDS 'state_1km_1' representing cloud state, cloud shadow state and cirrus status

# IMPORTANT: ALL OUTPUT ARE SAVED IN HDF FORMAT (CAN BE DISPLAYED IN ARCMAP) AND DEFAULT MODIS PROJECTION (SINUSOIDAL)

# IMPORTANT MODIS LDOPE MUST BE DOWNLOADED AND INSTALLED TO RUN THIS CODE


#####################################################################################################################################

# IMPORT THE REQUIRED PYTHON MODULES
import os, glob, shutil

# PATH TO MODIS LDOPE BIN FOLDER 
#LDOPE_Bin = "C:\\Users\\30038555\\LDOPE\\bin"

# LDOPE_Bin = "C:\\Users\\122590\\LDOPE-1.7\\bin"
LDOPE_Bin = "/Applications/LDOPE-1.7/bin"

# PATH TO OUTPUT FOLDER 
# Output = "C:\\Users\\122590\\My Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\UNPACKED"
Output = "~/Documents/UOM/NolanLive/ANALYSES_2017/MODIS/H30V12/UNPACKED"

# PATH TO FOLDER WITH MOD09GA RAW DATA (HAS TO BE MODIS LDOPE BIN FOLDER)
os.chdir(LDOPE_Bin)

# CREATE A LIST OF ALL MOD09GA RAW DATA
list = glob.glob("*.hdf")

# LOOP THROUGH LIST OF ALL MOD09GA RAW DATA
for hdf in list:

    # EACH HDF FILE WILL BE PROCESSED NOW
    input0 = hdf

    # HERE THE CODE UNPACK sur_refl_qc_500m bits 2-5 (Band1 quality data info), 6-9 (Band2 quality data info), 10-13 (Band3 quality data info),
    # 14-17 (Band4 quality data info), 22-25 (Band6 quality data info) and 26-29 (Band7 quality data info)

    outputb1_0= "-of=" + "QCb1" + hdf[9:16]+ ".hdf"
    # os.system("unpack_sds_bits.exe -sds=sur_refl_qc_500m -bit=2-5 %s %s"%(outputb1_0, input0))
    os.system("unpack_sds_bits -sds=sur_refl_qc_500m -bit=2-5 %s %s" % (outputb1_0, input0))

    #outputb2_0= "-of=" + "QCb2" + hdf[9:16]+ ".hdf"
    #os.system("unpack_sds_bits.exe -sds=sur_refl_qc_500m -bit=6-9 %s %s"%(outputb2_0, input0))

    outputb3_0= "-of=" + "QCb3" + hdf[9:16]+ ".hdf"
    # os.system("unpack_sds_bits.exe -sds=sur_refl_qc_500m -bit=10-13 %s %s"%(outputb3_0, input0))
    os.system("unpack_sds_bits -sds=sur_refl_qc_500m -bit=10-13 %s %s" % (outputb3_0, input0))

    outputb4_0= "-of=" + "QCb4" + hdf[9:16]+ ".hdf"
    # os.system("unpack_sds_bits.exe -sds=sur_refl_qc_500m -bit=14-17 %s %s"%(outputb4_0, input0))
    os.system("unpack_sds_bits -sds=sur_refl_qc_500m -bit=14-17 %s %s" % (outputb4_0, input0))

    #outputb6_0= "-of=" + "QCb6" + hdf[9:16]+ ".hdf"
    #os.system("unpack_sds_bits.exe -sds=sur_refl_qc_500m -bit=22-25 %s %s"%(outputb6_0, input0))

    #outputb7_0= "-of=" + "QCb7" + hdf[9:16]+ ".hdf"
    #os.system("unpack_sds_bits.exe -sds=sur_refl_qc_500m -bit=26-29 %s %s"%(outputb7_0, input0))
    
    # HERE THE CODE RE-PROJECT THE FILES JUST CREATED TO MAKE SURE THEY ARE IN MODIS DEFAULT COORDINATE SYSTEM (SINUSOIDAL)

    outputb1_1= outputb1_0[4:]
    outputb1_2= "-of=" + "PR_QCb1_" + hdf[9:16]+ ".hdf"
    input1 = "-ref="+ hdf
    # os.system("cp_proj_param.exe %s %s %s"%(outputb1_1, input1, outputb1_2))
    os.system("cp_proj_param %s %s %s"%(outputb1_1, input1, outputb1_2))

   # outputb2_1= outputb2_0[4:]
   # outputb2_2= "-of=" + "PR_QCb2_" + hdf[9:16]+ ".hdf"
   # input1 = "-ref="+ hdf
   # os.system("cp_proj_param.exe %s %s %s"%(outputb2_1, input1, outputb2_2))

    outputb3_1= outputb3_0[4:]
    outputb3_2= "-of=" + "PR_QCb3_" + hdf[9:16]+ ".hdf"
    input1 = "-ref="+ hdf
    # os.system("cp_proj_param.exe %s %s %s"%(outputb3_1, input1, outputb3_2))
    os.system("cp_proj_param %s %s %s" % (outputb3_1, input1, outputb3_2))

    outputb4_1= outputb4_0[4:]
    outputb4_2= "-of=" + "PR_QCb4_" + hdf[9:16]+ ".hdf"
    input1 = "-ref="+ hdf
    # os.system("cp_proj_param.exe %s %s %s"%(outputb4_1, input1, outputb4_2))
    os.system("cp_proj_param %s %s %s"%(outputb4_1, input1, outputb4_2))

   # outputb6_1= outputb6_0[4:]
   # outputb6_2= "-of=" + "PR_QCb6_" + hdf[9:16]+ ".hdf"
   # input1 = "-ref="+ hdf
   # os.system("cp_proj_param.exe %s %s %s"%(outputb6_1, input1, outputb6_2))

    #outputb7_1= outputb7_0[4:]
    #outputb7_2= "-of=" + "PR_QCb7_" + hdf[9:16]+ ".hdf"
    #input1 = "-ref="+ hdf
    #os.system("cp_proj_param.exe %s %s %s"%(outputb7_1, input1, outputb7_2))

    # HERE THE CODE UNPACK sur_refl_state_500m bits 0-1 (cloud state), 2 (cloud shadow), 8-9 (cirrus detected)
    outputcst_0= "-of=" + "clst" + hdf[9:16]+ ".hdf"
    # os.system("unpack_sds_bits.exe -sds=sur_refl_state_500m -bit=0-1 %s %s"%(outputcst_0, input0))
    os.system("unpack_sds_bits -sds=sur_refl_state_500m -bit=0-1 %s %s"%(outputcst_0, input0))

    outputcsh_0= "-of=" + "clsh" + hdf[9:16]+ ".hdf"
    # os.system("unpack_sds_bits.exe -sds=sur_refl_state_500m -bit=2 %s %s"%(outputcsh_0, input0))
    os.system("unpack_sds_bits -sds=sur_refl_state_500m -bit=2 %s %s"%(outputcsh_0, input0))

    outputcde_0= "-of=" + "cide" + hdf[9:16]+ ".hdf"
    # os.system("unpack_sds_bits.exe -sds=sur_refl_state_500m -bit=8-9 %s %s"%(outputcde_0, input0))
    os.system("unpack_sds_bits -sds=sur_refl_state_500m -bit=8-9 %s %s"%(outputcde_0, input0))

    # HERE THE CODE RE-PROJECT THE FILES JUST CREATED TO MAKE SURE THEY ARE IN MODIS DEFAULT COORDINATE SYSTEM (SINUSOIDAL)
    outputcst_1= outputcst_0[4:]
    outputcst_2= "-of=" + "PR_clst_" + hdf[9:16]+ ".hdf"
    input1 = "-ref="+ hdf
    # os.system("cp_proj_param.exe %s %s %s"%(outputcst_1, input1, outputcst_2))
    os.system("cp_proj_param %s %s %s"%(outputcst_1, input1, outputcst_2))

    outputcsh_1= outputcsh_0[4:]
    outputcsh_2= "-of=" + "PR_clsh_" + hdf[9:16]+ ".hdf"
    input1 = "-ref="+ hdf
    # os.system("cp_proj_param.exe %s %s %s"%(outputcsh_1, input1, outputcsh_2))
    os.system("cp_proj_param %s %s %s"%(outputcsh_1, input1, outputcsh_2))

    outputcde_1= outputcde_0[4:]
    outputcde_2= "-of=" + "PR_cide_" + hdf[9:16]+ ".hdf"
    input1 = "-ref="+ hdf
    # os.system("cp_proj_param.exe %s %s %s"%(outputcde_1, input1, outputcde_2))
    os.system("cp_proj_param %s %s %s"%(outputcde_1, input1, outputcde_2))




    # HERE THE CODE EXTRACT sur_refl_b01, sur_refl_b02, sur_refl_b03, sur_refl_b04, sur_refl_b06 and sur_refl_b07
    output_srb1_0= "-of=" + "SRb1" + hdf[9:16]+ ".hdf"
    # os.system("subset_sds.exe -sds=sur_refl_b01 -row=0,2400 -col=0,2400 %s %s"%(output_srb1_0, input0))
    os.system("subset_sds -sds=sur_refl_b01 -row=0,2400 -col=0,2400 %s %s" % (output_srb1_0, input0))

  #  output_srb2_0= "-of=" + "SRb2" + hdf[9:16]+ ".hdf"
  #  os.system("subset_sds.exe -sds=sur_refl_b02 -row=0,2400 -col=0,2400 %s %s"%(output_srb2_0, input0))

    output_srb3_0= "-of=" + "SRb3" + hdf[9:16]+ ".hdf"
    os.system("subset_sds.exe -sds=sur_refl_b03 -row=0,2400 -col=0,2400 %s %s"%(output_srb3_0, input0))
    os.system("subset_sds -sds=sur_refl_b03 -row=0,2400 -col=0,2400 %s %s"%(output_srb3_0, input0))

    output_srb4_0= "-of=" + "SRb4" + hdf[9:16]+ ".hdf"
    # os.system("subset_sds.exe -sds=sur_refl_b04 -row=0,2400 -col=0,2400 %s %s"%(output_srb4_0, input0))
    os.system("subset_sds -sds=sur_refl_b04 -row=0,2400 -col=0,2400 %s %s"%(output_srb4_0, input0))

   # output_srb6_0= "-of=" + "SRb6" + hdf[9:16]+ ".hdf"
   # os.system("subset_sds.exe -sds=sur_refl_b06 -row=0,2400 -col=0,2400 %s %s"%(output_srb6_0, input0))

    #output_srb7_0= "-of=" + "SRb7" + hdf[9:16]+ ".hdf"
    #os.system("subset_sds.exe -sds=sur_refl_b07 -row=0,2400 -col=0,2400 %s %s"%(output_srb7_0, input0))

    # HERE THE CODE RE-PROJECT THE FILES JUST CREATED TO MAKE SURE THEY ARE IN MODIS DEFAULT COORDINATE SYSTEM (SINUSOIDAL)
    output_srb1_1= output_srb1_0[4:]
    output_srb1_2= "-of=" + "PR_SRb1_" + hdf[9:16]+ ".hdf"
    # os.system("cp_proj_param.exe %s %s %s"%(output_srb1_1, input1, output_srb1_2))
    os.system("cp_proj_param %s %s %s"%(output_srb1_1, input1, output_srb1_2))

    #output_srb2_1= output_srb2_0[4:]
    #output_srb2_2= "-of=" + "PR_SRb2_" + hdf[9:16]+ ".hdf"
    #os.system("cp_proj_param.exe %s %s %s"%(output_srb2_1, input1, output_srb2_2))

    output_srb3_1= output_srb3_0[4:]
    output_srb3_2= "-of=" + "PR_SRb3_" + hdf[9:16]+ ".hdf"
    # os.system("cp_proj_param.exe %s %s %s"%(output_srb3_1, input1, output_srb3_2))
    os.system("cp_proj_param %s %s %s"%(output_srb3_1, input1, output_srb3_2))

    output_srb4_1= output_srb4_0[4:]
    output_srb4_2= "-of=" + "PR_SRb4_" + hdf[9:16]+ ".hdf"
    # os.system("cp_proj_param.exe %s %s %s"%(output_srb4_1, input1, output_srb4_2))
    os.system("cp_proj_param %s %s %s"%(output_srb4_1, input1, output_srb4_2))
    
    #output_srb6_1= output_srb6_0[4:]
    #output_srb6_2= "-of=" + "PR_SRb6_" + hdf[9:16]+ ".hdf"
    #os.system("cp_proj_param.exe %s %s %s"%(output_srb6_1, input1, output_srb6_2))

    #output_srb7_1= output_srb7_0[4:]
    #output_srb7_2= "-of=" + "PR_SRb7_" + hdf[9:16]+ ".hdf"
    #os.system("cp_proj_param.exe %s %s %s"%(output_srb7_1, input1, output_srb7_2))


###############################################################################################################################
# HERE THE CODE MOVE THE OUTPUT FILES TO THE (USER DEFINED) OUTPUT FOLDER
# IMPORTANT: ONLY FINAL OUTPUTS (REPROJECTED BANDS and QUALITY DATA) WILL BE MOVED, INTERMEDIATE FILES MUST BE DELETED MANUALLY FROM MODIS LDOPE BIN FOLDER


# MODIS LDOPE BIN FOLDER
os.chdir(LDOPE_Bin)

# LIST ALL FILES
list = glob.glob("*.hdf")

# LOOP THROUGH ALL FILES 
for hdf in list:

    # ONLY SELECT FINAL OUTPUTS
    if hdf[0:3] == "PR_":       

        # COPY FINAL OUTPUTS TO OUTPUT FOLDER
        shutil.copy(hdf, Output)

        # REMOVE FINAL OUTPUTS FROM MODIS LDOPE BIN FOLDER
        os.remove(hdf)


# END!!!!!!!!!!

    
