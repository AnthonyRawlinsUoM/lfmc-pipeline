.libPaths(c("C:\\Users\\122590\\DOCUMENTS\\R", .libPaths()))
library(raster)
library(rgdal)

###########################################################################################################
############################### Calculate VARI ##########################################################
###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\VARI")

# List the files,
b1<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\BANDS_MASKED\\b1", pattern=".tif", full.names=TRUE)
b3<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\BANDS_MASKED\\b3", pattern=".tif", full.names=TRUE)
b4<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\BANDS_MASKED\\b4", pattern=".tif", full.names=TRUE)

NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\BANDS_MASKED\\b1", pattern=".tif")
NAMES<-gsub("b1_", "VARI_", NAMES)

#The range of values for the bands is 0 to 16000, so this reclassifies any values outside of this range to NA.
classify <- c(16001, Inf, NA, -Inf, 0, NA)
rcl <-matrix(classify, ncol=3, byrow=TRUE)


for(i in 1:length(b1)){
  Rb1<- raster (b1[i])
  Rb1_cls <- reclassify(Rb1, rcl)
  Rb3<- raster (b3[i])
  Rb3_cls <- reclassify(Rb3, rcl)
  Rb4<- raster (b4[i])
  Rb4_cls <- reclassify(Rb4, rcl)
  VARI<-((Rb4_cls - Rb1_cls)/(Rb4_cls + Rb1_cls - Rb3_cls)) 
  writeRaster(VARI, NAMES[i], format="GTiff", overwrite=TRUE)
  }
###############
rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\VARI")

# List the files,
b1<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\b1", pattern=".tif", full.names=TRUE)
b3<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\b3", pattern=".tif", full.names=TRUE)
b4<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\b4", pattern=".tif", full.names=TRUE)

NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\BANDS_MASKED\\b1", pattern=".tif")
NAMES<-gsub("b1_", "VARI_", NAMES)

#The range of values for the bands is 0 to 16000, so this reclassifies any values outside of this range to NA.
classify <- c(16001, Inf, NA, -Inf, 0, NA)
rcl <-matrix(classify, ncol=3, byrow=TRUE)


for(i in 1:length(b1)){
  Rb1<- raster (b1[i])
  Rb1_cls <- reclassify(Rb1, rcl)
  Rb3<- raster (b3[i])
  Rb3_cls <- reclassify(Rb3, rcl)
  Rb4<- raster (b4[i])
  Rb4_cls <- reclassify(Rb4, rcl)
  VARI<-((Rb4_cls - Rb1_cls)/(Rb4_cls + Rb1_cls - Rb3_cls)) 
  writeRaster(VARI, NAMES[i], format="GTiff", overwrite=TRUE)
}
###########################################################################################################
############################### Calculate VARI max-min ####################################################
###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\SI_VARI")

#List max and min files:
MAX_VARI<-raster("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\AVG_MAX_MIN_TO_2014_FIRE_MASKED/AVG_MAX_VARI.tif")
MIN_VARI<-raster("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\AVG_MAX_MIN_TO_2014_FIRE_MASKED/AVG_MIN_VARI.tif")
MAX_MINUS_MIN_VARI<-MAX_VARI - MIN_VARI

VARI<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\VARI", pattern=".tif", full.names=TRUE)

NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\VARI", pattern=".tif")
NAMES<-gsub("VARI", "SI_VARI", NAMES)


#The range of the SI_max_min is 0-1, if values outside of this, set to 0 and 1 respectively
#(this may happen if the value is less than or higher than the average max or min)
classify <- c(1, Inf, 1, -Inf, 0, 0)
rcl <-matrix(classify, ncol=3, byrow=TRUE)

for(i in 1:length(VARI)){
  RVARI<- raster (VARI[i])  
  # Calc spectral index:
  VARI_MAX_MIN<-((RVARI - MIN_VARI)/MAX_MINUS_MIN_VARI)
  #reclassify (scale to 0-1):
  VARI_MAX_MIN_cls <- reclassify(VARI_MAX_MIN, rcl)
  writeRaster(VARI_MAX_MIN_cls, NAMES[i], format="GTiff", overwrite=TRUE)
}

###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\SI_VARI")

#List max and min files:
MAX_VARI<-raster("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\AVG_MAX_MIN_TO_2014_FIRE_MASKED/AVG_MAX_VARI.tif")
MIN_VARI<-raster("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\AVG_MAX_MIN_TO_2014_FIRE_MASKED/AVG_MIN_VARI.tif")
MAX_MINUS_MIN_VARI<-MAX_VARI - MIN_VARI

VARI<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\VARI", pattern=".tif", full.names=TRUE)

NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\VARI", pattern=".tif")
NAMES<-gsub("VARI", "SI_VARI", NAMES)


#The range of the SI_max_min is 0-1, if values outside of this, set to 0 and 1 respectively
#(this may happen if the value is less than or higher than the average max or min)
classify <- c(1, Inf, 1, -Inf, 0, 0)
rcl <-matrix(classify, ncol=3, byrow=TRUE)

for(i in 1:length(VARI)){
  RVARI<- raster (VARI[i])  
  # Calc spectral index:
  VARI_MAX_MIN<-((RVARI - MIN_VARI)/MAX_MINUS_MIN_VARI)
  #reclassify (scale to 0-1):
  VARI_MAX_MIN_cls <- reclassify(VARI_MAX_MIN, rcl)
  writeRaster(VARI_MAX_MIN_cls, NAMES[i], format="GTiff", overwrite=TRUE)
}
###########################################################################################################
############################### Calculate Live FM #########################################################
###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\LIVE_FM\\MODIS_PR")

SI_VARI<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\SI_VARI", pattern=".tif", full.names=TRUE)
NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\VARI\\SI_VARI", pattern=".tif")
NAMES<-gsub("SI_VARI", "LIVE_FM", NAMES)


for(i in 1:length(SI_VARI)){
  RVARI<- raster (SI_VARI[i])  
  LIVE_FM <- (52.51 * exp(1.36*RVARI))
  writeRaster(LIVE_FM, NAMES[i], format="GTiff", overwrite=TRUE)
}

############

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\LIVE_FM\\MODIS_PR")

SI_VARI<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\SI_VARI", pattern=".tif", full.names=TRUE)
NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\VARI\\SI_VARI", pattern=".tif")
NAMES<-gsub("SI_VARI", "LIVE_FM", NAMES)


for(i in 1:length(SI_VARI)){
  RVARI<- raster (SI_VARI[i])  
  LIVE_FM <- (52.51 * exp(1.36*RVARI))
  writeRaster(LIVE_FM, NAMES[i], format="GTiff", overwrite=TRUE)
}

###########################################################################################################
############################### Reproject to GDA94 ########################################################
###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\LIVE_FM\\GDA94_PR")

FM<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\LIVE_FM\\MODIS_PR", pattern=".tif", full.names=TRUE)
NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\LIVE_FM\\MODIS_PR", pattern=".tif")

newproj<-("+proj=longlat +ellps=GRS80 +no_defs+datum=GDA94")

for(i in 1:length(FM)){
  FM_R<- raster (FM[i])  
  projection(FM_R) <- CRS("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")
  FM_pr <-projectRaster(FM_R, crs=newproj, method='bilinear')
  writeRaster(FM_pr, NAMES[i], format="GTiff")
}
###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\LIVE_FM\\GDA94_PR")

FM<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\LIVE_FM\\MODIS_PR", pattern=".tif", full.names=TRUE)
NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\LIVE_FM\\MODIS_PR", pattern=".tif")

newproj<-("+proj=longlat +ellps=GRS80 +no_defs+datum=GDA94")

for(i in 1:length(FM)){
  FM_R<- raster (FM[i])  
  projection(FM_R) <- CRS("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")
  FM_pr <-projectRaster(FM_R, crs=newproj, method='bilinear')
  writeRaster(FM_pr, NAMES[i], format="GTiff")
}


###########################################################################################################
#     merge MODIS files                      
###########################################################################################################

rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\LIVE_FM_MERGED\\MERGED")

FM_h29<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H29V12\\LIVE_FM\\GDA94_PR", pattern=".tif", full.names=TRUE)
FM_h30<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\LIVE_FM\\GDA94_PR", pattern=".tif", full.names=TRUE)

# Create a list of names for the masked rasters:
NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\H30V12\\LIVE_FM\\GDA94_PR", pattern=".tif")

#rasterOptions(tolerance = 0.1)
#.Machine$double.eps <- 0.000000001

for(i in 1:length(FM_h29)){
  R_h29<- raster (FM_h29[i])  
  R_h30<- raster (FM_h30[i])  
  FM_merged <- merge (R_h29, R_h30, tolerance=0.5) 
  writeRaster(FM_merged, NAMES[i], format="GTiff")
}


###########################################################################################################
#    Clip to veg and mask fire              
###########################################################################################################
rm(list=ls(all=TRUE))
setwd("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\LIVE_FM_MERGED\\MERGED_CLIPPED_TO_VEG_FIRE_MASKED")

#Read the shapefile(s)
VEG <- readOGR("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\ArcGIS\\SPATIAL_LAYERS", "VEG_FIRE_ERASED")
eVEG <- extent(VEG)

#Read the raster
FM<-list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\LIVE_FM_MERGED\\MERGED", pattern=".tif", full.names=TRUE)

NAMES<- list.files("C:\\Users\\122590\\Documents\\DOCUMENTS\\Fuel Moisture Project\\ANALYSES_2017\\MODIS\\LIVE_FM_MERGED\\MERGED", pattern=".tif")

for(i in 1:length(FM)){
  R_MODIS<- raster (FM[i])  
  R_MODIS.crop <- crop(R_MODIS, eVEG, snap="out")
  crop_MODIS<- setValues(R_MODIS.crop, NA)
  fireVEG.MODIS <- rasterize(VEG, crop_MODIS)
  MODIS.masked <- mask(x=R_MODIS.crop, mask=fireVEG.MODIS)
  writeRaster(MODIS.masked, NAMES[i], format="GTiff")

}


