from osgeo import osr
import numpy as np
import glob
import re
import os
import datetime
import h5py
from datetime import timedelta

def EASEconvert(x,y,LatLon): 
    #LatLon=1 go from LatLon to EASE2: x = lon, y=lat
    #LatLon=2 go from EASE2 to LatLon, x = easecol, y=easerow
    
    LatLonsrs   = osr.SpatialReference()
    EASEsrs     = osr.SpatialReference()
    LatLonsrs.ImportFromEPSG(4326) 
    EASEsrs.ImportFromEPSG(6933) #EASEGRID 2.0

    #200m grid
    map_scale_m = 200.17900466991
    cols        = 173520
    rows        = 73080
    col0        = (cols-1)/2
    row0        = (rows-1)/2
    
    if LatLon==1:
        transform   = osr.CoordinateTransformation(LatLonsrs, EASEsrs) 
        coords      = transform.TransformPoint(y,x) #expects lat, lon
        ezr         = row0-coords[1]/map_scale_m
        ezc         = col0+coords[0]/map_scale_m
        x           = ezc
        y           = ezr
    else:
        #convert 200m easegrid2 to global version used in transformation
        x           = (x-col0)*map_scale_m
        y           = (row0-y)*map_scale_m
        
        transform   = osr.CoordinateTransformation(EASEsrs, LatLonsrs) #transform from to EASE to Lat/Lon (4326) 
        coords      = transform.TransformPoint(x,y) #expects column, row
        x           = coords[1] #lon
        y           = coords[0] #lat
    return x,y

def read_WalnutGulch(ptezr,ptezc):

    mods         = ('DSG','PMI','TSR')
    workDir      = '/scratch/rlohman/WalnutGulchA/Path62Frame620BeamFP66'
    retDir       = workDir+'R4/'
    gcovs        = np.array(glob.glob(retDir+('[0-9]'*8)+'.h5'))

    #read in first date, find pixel matching ezr,ezc for target insitu location
    fo  = h5py.File(gcovs[0],'r')
    eci = fo['/science/LSAR/SME2/grids/EASEGridColumnIndex'][()]
    eri = fo['/science/LSAR/SME2/grids/EASEGridRowIndex'][()]
    idx = np.array([np.linalg.norm(x) for x in eci-ptezc]).argmin()
    idy = np.array([np.linalg.norm(x) for x in eri-ptezr]).argmin()

    ngcov = len(gcovs)
    nmods = len(mods)
    dates = np.zeros([ngcov])
    retr= np.zeros([ngcov,nmods])*np.nan
    rete= np.zeros([ngcov,nmods])*np.nan
 
    for i in range(ngcov):
         if os.path.isfile(gcovs[i]):
                    fo=h5py.File(gcovs[i],'r')
                    dataset='science/LSAR/identification/zeroDopplerStartTime'
                    if dataset in fo:
                        d =fo[dataset]
                        dates[i]=d[()].decode()

                    for j in range(len(mods)):
                        dataset='/science/LSAR/SME2/grids/algorithmCandidates/'+mods[j]+'/soilMoisture'
                        if dataset in fo:
                            retr[i,j] =fo[dataset][idy,idx]
                        dataset='/science/LSAR/SME2/grids/algorithmCandidates/'+mods[j]+'/soilMoistureUncertainty'
                        if dataset in fo:
                            rete[i,j] =fo[dataset][idy,idx]
                    
                    fo.close()
   
    retr[retr<0] = np.nan
    rete[rete<0] = np.nan
   