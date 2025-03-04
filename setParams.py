import datetime


mainPath      = '/Users/rlohman/SMCalVal/'
sparseTypes   = ('SCAN','NEON')
superTypes    = ('SOILSCAPE')
outFile       = mainPath+'results.csv'
scanPath      = mainPath+'SCAN/'
neonPath      = mainPath+'NEON/'
soilPath      = mainPath+'SOILSCAPE/'

##move these files from supportFiles/
anciStatic    = '/Users/rlohman/Software/SMCalVal/supportFiles/NISAR_SM_STATIC_ANCILLARY_002.h5'
trackFrameDb  = mainPath+'NISAR_TrackFrame_L_20240530.gpkg' 
soilMeta      = soilPath+'soilscape_site_meta_data.csv'
neonDepths    = neonPath+'swc_depthsV2.csv'    


# Set these to initial target timespan - here only used to exclude sensors with no overlap with this timespan
startDate     = datetime.datetime(2021,4,1)
endDate       = datetime.datetime(2024,5,1)