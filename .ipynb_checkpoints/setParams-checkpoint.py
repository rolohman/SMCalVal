import datetime


mainPath      = '/Users/rlohman/Desktop/SMCalVal/'
mainPath      = '/home/jovyan/SMCalValdir/'
outFileTot    = mainPath+'results.csv'


scanPath      = mainPath+'SCAN/'
neonPath      = mainPath+'NEON/'
soilscapePath = mainPath+'SOILSCAPE/'

##move these files from supportFiles/
##General
anciStatic    = mainPath+'supportFiles/NISAR_SM_STATIC_ANCILLARY_002.h5'
trackFrameDb  = mainPath+'supportFiles/NISAR_TrackFrame_L_20240530.gpkg' 
##Soilscape
#soilscapeMeta = mainPath+'supportFiles/SOILSCAPE/soilscape_site_meta_data.csv'
soilscapeNode = mainPath+'supportFiles/SOILSCAPE/soilscape_site_nodeLocations.csv'
#NEON
neonDepths    = mainPath+'supportFiles/NEON/swc_depthsV2.csv'    

#Retrieval info
modNames      = ('DSG','PMI','TSR')

#output files
#Soilscape
soilscapeSitesPath = soilscapePath+'SOILSCAPESites.csv'

# Set these to initial target timespan - here only used to exclude sensors with no overlap with this timespan
startDate     = datetime.datetime(2021,4,1)
endDate       = datetime.datetime(2024,5,1)