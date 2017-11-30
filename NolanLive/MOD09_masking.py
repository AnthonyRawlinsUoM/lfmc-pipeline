# THIS CODE USE QA DATA TO RETAIN GOOD MOD09GA Band1, Band2, Band6 and Band7 DATA
# ONLY PIXELS NOT AFFECTED BY CLOUD, CLOUD SHADOW, CIRRUS AND OF HIGHEST QUALITY ARE RETAINED

# IMPORTANT: THIS CODE REQUIRES ARCMAP

############################################################################################


# IMPORT THE REQUIRED PYTHON MODULES
import sys, string, os, glob, arcpy
from arcpy import env
from arcpy.sa import *


# CHECK THE NECESSARY LICENSE
arcpy.CheckOutExtension("Spatial")

# SET THE INPUT FOLDER WITH ALL MOD09GA DATA (Bands and QA data)
#env.workspace = "D:\\ANALYSES_2017\\MODIS\\H29V12\\UNPACKED"
# env.workspace = "C:\\Users\\122590\\My Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\UNPACKED"
env.workspace = "~/Documents/UOM/NolanLive/ANALYSES_2017/MODIS/H30V12/UNPACKED"

# LIST ALL THE FILES IN THE INPUT FOLDER
rasters = arcpy.ListRasters("*", "hdf")

# LOOP THROUGH ALL THE FILES
for raster in rasters:

    # FIND MOD09GA Band 1
    if raster[3:7] == "SRb1":

	# READ THE DATE OF ACQUISITION OF EACH MOD09GA Band 1
        date = raster[8:15]

	# SET THE VARIABLES: Cirrus = inRaster, Cloud = inRaster3, Cloud shadow = inRaster2 and Band1 Data Quality = inRaster4
        inRaster1 = "PR_cide_" + date + ".hdf"
        inRaster2 = "PR_clsh_" + date + ".hdf"
        inRaster3 = "PR_clst_" + date + ".hdf"
        inRaster4 = "PR_QCb1_" + date + ".hdf"
        
	# SET THE CONDITION: IF A SPECIFIC PIXEL IS NOT AFFECTED BY CLOUD, CLOUD SHADOW, CIRRUS AND IT IS OF HIGHEST QUALITY THEN RETAIN IT, OTHERWISE ASSIGN NODATA
        inTrueRaster = raster
        inFalseConstant = ""
        whereClause = "VALUE = 0"
        
	# APPLY THAT CONDITION USING RASTER CALCULATOR
        if inRaster1 in rasters:
            if inRaster2 in rasters:
               if inRaster3 in rasters:
                    if inRaster4 in rasters:

                        outCon = Con(inRaster1, inTrueRaster, inFalseConstant, whereClause)
                        outCon2 = Con(inRaster2, outCon, inFalseConstant, whereClause)
                        outCon3 = Con(inRaster3, outCon2, inFalseConstant, whereClause)
                        outCon4 = Con(inRaster4, outCon3, inFalseConstant, whereClause)
                        #outCon4.save("D:\\ANALYSES_2017\\MODIS\\H29V12\\BANDS_MASKED\\" + "b1_" + date + ".tif")
                        outCon4.save("C:\\Users\\122590\\My Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\"+ "b1_" + date + ".tif")


    # DO THE SAME THING WITH BAND2..............                        
   # if raster[3:7] == "SRb2":

#        date = raster[8:15]

 #       inRaster = "PR_cide_" + date + ".hdf"
  #      inRaster2 = "PR_clsh_" + date + ".hdf"
  #      inRaster3 = "PR_clst_" + date + ".hdf"
  #      inRaster4 = "PR_QCb2_" + date + ".hdf"
        
  #      inTrueRaster = raster
  #      inFalseConstant = ""
  #      whereClause = "VALUE = 0"
       
  #      if inRaster in rasters:
  #          if inRaster2 in rasters:
  #              if inRaster3 in rasters:
  #                  if inRaster4 in rasters:

  #                      outCon = Con(inRaster, inTrueRaster, inFalseConstant, whereClause)
  #                      outCon2 = Con(inRaster2, outCon, inFalseConstant, whereClause)
  #                      outCon3 = Con(inRaster3, outCon2, inFalseConstant, whereClause)
  #                      outCon4 = Con(inRaster4, outCon3, inFalseConstant, whereClause)
  #                      outCon4.save("E:\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\" + "b2_" + date + ".tif")

    # DO THE SAME THING WITH BAND3..............                        
    if raster[3:7] == "SRb3":

        date = raster[8:15]

        inRaster = "PR_cide_" + date + ".hdf"
        inRaster2 = "PR_clsh_" + date + ".hdf"
        inRaster3 = "PR_clst_" + date + ".hdf"
        inRaster4 = "PR_QCb3_" + date + ".hdf"
        inTrueRaster = raster
        inFalseConstant = ""
        whereClause = "VALUE = 0"
       
        if inRaster in rasters:
            if inRaster2 in rasters:
                if inRaster3 in rasters:
                    if inRaster4 in rasters:

                        outCon = Con(inRaster, inTrueRaster, inFalseConstant, whereClause)
                        outCon2 = Con(inRaster2, outCon, inFalseConstant, whereClause)
                        outCon3 = Con(inRaster3, outCon2, inFalseConstant, whereClause)
                        outCon4 = Con(inRaster4, outCon3, inFalseConstant, whereClause)
                        outCon4.save("C:\\Users\\122590\\My Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\" + "b3_" + date + ".tif")


    # DO THE SAME THING WITH BAND4..............                        
    if raster[3:7] == "SRb4":

        date = raster[8:15]

        inRaster = "PR_cide_" + date + ".hdf"
        inRaster2 = "PR_clsh_" + date + ".hdf"
        inRaster3 = "PR_clst_" + date + ".hdf"
        inRaster4 = "PR_QCb4_" + date + ".hdf"
        
        inTrueRaster = raster
        inFalseConstant = ""
        whereClause = "VALUE = 0"
       
        if inRaster in rasters:
            if inRaster2 in rasters:
                if inRaster3 in rasters:
                    if inRaster4 in rasters:

                        outCon = Con(inRaster, inTrueRaster, inFalseConstant, whereClause)
                        outCon2 = Con(inRaster2, outCon, inFalseConstant, whereClause)
                        outCon3 = Con(inRaster3, outCon2, inFalseConstant, whereClause)
                        outCon4 = Con(inRaster4, outCon3, inFalseConstant, whereClause)
                        outCon4.save("C:\\Users\\122590\\My Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\" + "b4_" + date + ".tif")




    # DO THE SAME THING WITH BAND6..............  
 #   if raster[3:7] == "SRb6":

#        date = raster[8:15]

 #       inRaster = "PR_cide_" + date + ".hdf"
 #       inRaster2 = "PR_clsh_" + date + ".hdf"
 #       inRaster3 = "PR_clst_" + date + ".hdf"
 #       inRaster4 = "PR_QCb6_" + date + ".hdf"
        
 #       inTrueRaster = raster
 #       inFalseConstant = ""
 #       whereClause = "VALUE = 0"
        
 #       if inRaster in rasters:
 #           if inRaster2 in rasters:
 #               if inRaster3 in rasters:
 #                   if inRaster4 in rasters:

 #                       outCon = Con(inRaster, inTrueRaster, inFalseConstant, whereClause)
 #                       outCon2 = Con(inRaster2, outCon, inFalseConstant, whereClause)
 #                       outCon3 = Con(inRaster3, outCon2, inFalseConstant, whereClause)
 #                       outCon4 = Con(inRaster4, outCon3, inFalseConstant, whereClause)
 #                       outCon4.save("E:\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\" + "b6_" + date + ".tif")







    # DO THE SAME THING WITH BAND7..............  
  #  if raster[3:7] == "SRb7":

#        date = raster[8:15]

#        inRaster = "PR_cide_" + date + ".hdf"
#        inRaster2 = "PR_clsh_" + date + ".hdf"
#        inRaster3 = "PR_clst_" + date + ".hdf"
#        inRaster4 = "PR_QCb7_" + date + ".hdf"
        
#        inTrueRaster = raster
#        inFalseConstant = ""
#        whereClause = "VALUE = 0"
        
#        if inRaster in rasters:
#            if inRaster2 in rasters:
#                if inRaster3 in rasters:
#                    if inRaster4 in rasters:
#                       outCon = Con(inRaster, inTrueRaster, inFalseConstant, whereClause)
#                       outCon2 = Con(inRaster2, outCon, inFalseConstant, whereClause)
#                       outCon3 = Con(inRaster3, outCon2, inFalseConstant, whereClause)
#                       outCon4 = Con(inRaster4, outCon3, inFalseConstant, whereClause)
#                       outCon4.save("E:\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\" + "b7_" + date + ".tif")
