import datetime

trackFrameDb  = '/scratch/rlohman/SMCalVal/NISAR_TrackFrame_L_20240530.gpkg' 
anciStatic    = '/scratch/rlohman/static/NISAR_SM_STATIC_ANCILLARY_002.h5'
sparseTypes   = ('SCAN','NEON')

outFile       = '/scratch/rlohman/SMCalVal/results.csv'
scanPath      = '/scratch/rlohman/SMCalVal/SCAN/'
neonPath      = '/scratch/rlohman/SMCalVal/NEON/'

neonDepths    = '/scratch/rlohman/SMCalVal/NEON/swc_depthsV2.csv'    


# Set these to initial target timespan - here only used to exclude sensors with no overlap with this timespan
startDate     = datetime.datetime(2021,4,1)
endDate       = datetime.datetime(2024,5,1)