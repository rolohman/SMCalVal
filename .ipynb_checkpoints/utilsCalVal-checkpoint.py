from osgeo import gdal,osr


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
  