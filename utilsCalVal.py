from osgeo import osr
import numpy as np
import glob
import re
import os
import datetime
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

def read_WalnutGulch():

    workDir      = '/scratch/rlohman/'
    retDir       = workDir+'R4/'
    outFiles     = np.array(glob.glob(retDir+('[0-9]'*8)+'.h5'))

    tmp          = re.search(r'2[0-9]{7}',outFiles[0])
    inds         = tmp.span()
    dates        = np.array([datetime.datetime.strptime(x[inds[0]:inds[1]],'%Y%m%d') for x in outFiles])

    sort_index   = np.argsort(dates)
    gcovs        = outFiles[sort_index]
    dates        = dates[sort_index]

    allgcovs      = np.reshape([dirName+os.path.basename(x) for dirName in retDir for x in gcovs],[len(modDirs),len(dates)])




    idx = np.array([np.linalg.norm(x) for x in eci-ptezc]).argmin()
    idy = np.array([np.linalg.norm(x) for x in eri-ptezr]).argmin()
    print(lon[idx],lat[idy],ptezr,ptezc,idx,idy)
    retr= np.zeros([len(modDirs),len(gcovs),3])*np.nan
    rete= np.zeros([len(modDirs),len(gcovs),3])*np.nan
    HH  = np.zeros([len(modDirs),len(gcovs)])*np.nan
    mods=('DSG','PMI','TSR')
    for j in range(len(modDirs)):
        for i in range(len(dates)):
                if os.path.isfile(allgcovs[j,i]):
                    fo=h5py.File(allgcovs[j,i],'r')
                    dataset='/science/LSAR/SME2/grids/radarData/frequencyA/sigma0HH'
                    if dataset in fo:
                        HH[j,i] =fo[dataset][idy,idx]

                    for k in range(len(mods)):
                        dataset='/science/LSAR/SME2/grids/algorithmCandidates/'+mods[k]+'/soilMoisture'
                        if dataset in fo:
                            retr[j,i,k] =fo[dataset][idy,idx]
                    for k in range(len(mods)):
                        dataset='/science/LSAR/SME2/grids/algorithmCandidates/'+mods[k]+'/soilMoistureUncertainty'
                        if dataset in fo:
                            rete[j,i,k] =fo[dataset][idy,idx]
                    
                    fo.close()
    retr[retr<0] = np.nan
    rete[rete<0] = np.nan
    HH[HH<0]     = np.nan