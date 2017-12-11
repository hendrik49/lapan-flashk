#!/usr/bin/python
# Filename: landsat8_modif.py
import arcpy as ap
import numpy as np
import os, sys, time, glob, math, string
from arcpy.sa import *

##  Function to process a landsat scene directory
##
##  @output : Reprojected bands, TOA Reflectance, Calculated NDWI
class LicenseError(Exception):
    pass

class SpatialRefProjError (Exception):
    pass

class masker:
    '''Provides access to functions that produces masks from remote sensing image, according to its bit structure.'''

    def __init__(self, band, *var):
        self.bandarray = band

    def getmask(self, bitpos, bitlen, value, cummulative):
        '''Generates mask with given bit information.
        Parameters
            bitpos      -   Position of the specific QA bits in the value string.
            bitlen      -   Length of the specific QA bits.
            value       -   A value indicating the desired condition.
        '''
        lenstr = ''
        for i in range(bitlen):
            lenstr += '1'
        bitlen = int(lenstr, 2)

        if type(value) == unicode:
            value = int(value, 2)

        posValue = bitlen << bitpos
        conValue = value << bitpos

        if cummulative:
            mask = (self.bandarray & posValue) >= conValue
        else:
            mask = (self.bandarray & posValue) == conValue

        return mask.astype(int)

def mask_cloud(path, masktype, confidence, cummulative, out):
    convalue = {'High' : 3, 'Medium' : 2, 'Low' : 1, 'None' : 0}
    maskvalue = {'Cloud' : 14, 'Cirrus' : 12, 'Snow' : 10, 'Vegetation' : 8, 'Water' : 4}

    ap.env.workspace = out
    output = out+'/mask_cloud_'+str(os.path.basename(path))+'.TIF'
    ap.AddMessage('Making mask cloud using BQA')
    raster = ap.Raster(path + '/' + str(os.path.basename(path))+'_BQA.TIF')
    rasterarray = ap.RasterToNumPyArray(raster)
    bitmasker = masker(rasterarray)
    outarray = bitmasker.getmask(maskvalue[masktype], 2, convalue[confidence], cummulative)

    outraster = ap.NumPyArrayToRaster(outarray, 
                                         ap.Point(raster.extent.XMin, raster.extent.YMin),
                                         raster,
                                         raster,
                                         raster.noDataValue)

    outraster.save(output)
    ap.AddMessage('Finished Making mask cloud using BQA saved in: ' + str(output))

def reproject_mask_cloud(path, out, project):
    mask = out+'/mask_cloud_'+str(os.path.basename(path))+'.TIF'
    output = out+'/prj_mask_cloud_'+str(os.path.basename(path))+'.TIF'
    ap.ProjectRaster_management(mask, output, project)

def process_landsat(path, projection, out, flag, data_type, threshold_type, output=None):

    '''Calc/converts TOA Reflectance for each band in the directory

        @type path:     c{str}
        @param path:    Path to raw landsat directory
        @rtype output:  c{str}
        @return output: Makes directry with processed bands
    '''

    ap.env.workspace = path
    print "Workspace Environment set to " + str(path)
    ap.AddMessage("Workspace Environment set to " + str(path))

    if output is None:
        output = os.path.join(out, "processed"+flag)

        if os.path.exists(output):
            # os.system('rmdir /s /q '+ output)
            # os.mkdir(output)
            # sys.exit(0)
            print "\nDirectory for reprojection already Exisits"
            ap.AddMessage("\nDirectory for reprojection already Exisits")
        else:
            os.mkdir(output)
            print "\nCreated the output directory: " + output
            ap.AddMessage("\nCreated the output directory: " + output)
    else:
        if os.path.exists(output):
            #sys.exit(0)
            print "\nDirectory for reprojection already Exisits"
            ap.AddMessage("\nDirectory for reprojection already Exisits")
        else:
            os.mkdir(output)
            print "\nCreated the output directory: " + output
            ap.AddMessage("\nCreated the output directory: " + output)

    mtl = parse_mtl(path)
    
    try:
        tipeLandsat = str(mtl['PRODUCT_METADATA']['SPACECRAFT_ID'])
        haha = get_script_path()
        print("tipe data adalah :"+str(tipeLandsat))
        print(haha)
        kerPath = os.path.join(str(get_script_path()),"high-pass.txt")
        print(kerPath)
        toa = os.path.join(output, 'toa')
        Fcloud = os.path.join(output, 'cloud')

        reproject(path, output, projection, mtl)
        cloud_mask(path, out, output, mtl)
        calc_toa(Fcloud, toa, mtl)
        stack_bands(toa, mtl, data_type)
        pan_sharpen(toa, mtl, data_type)
        spatial_filter(toa, mtl, path)
        calc_ndwi(toa, mtl, data_type, threshold_type)

    finally:
        print "\n Completed processing landsat data for scene " + str(mtl['L1_METADATA_FILE']['LANDSAT_SCENE_ID'])
        ap.AddMessage("\n Completed processing landsat data for scene " + str(mtl['L1_METADATA_FILE']['LANDSAT_SCENE_ID']))

def reproject(input_dir, output_dir, projection, meta):
    
    ap.env.workspace = input_dir

    rasters = ap.ListRasters('*.TIF')
    #ms_bands = [band for band in rasters if (band_nmbr(band) != None)]
    
    ms_bands = [band for band in rasters if (band_nmbr(band) >= 1 and band_nmbr(band) <=8)]
    bqa_band = [band for band in rasters if (band_nmbr(band) == None)][0]
    
    try:
        checkout_Ext("Spatial")
        print "\nReprojecting and Cleaning landsat bands."
        ap.AddMessage("\nReprojecting and Cleaning landsat bands.")
        for band in ms_bands:
            print "\nReclassifying NoData for band " + band
            ap.AddMessage("\nReclassifying NoData for band " + band)
            outCon = ap.sa.Con(ap.sa.Raster(bqa_band) != 1, ap.sa.Raster(band))
            number = band_nmbr(band)
            outBand = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + 'PRJ_' + str(number) + '.TIF'
            out_band = os.path.join(output_dir, outBand)

            # ap.AddMessage(outCon)
            # ap.AddMessage(out_band)
            # ap.AddMessage(projection)

            print "Reprojecting band"
            ap.AddMessage("Reprojecting band")
            ap.ProjectRaster_management(outCon, out_band, projection)

        print "Clearing unused file"
        filelist = [ f for f in os.listdir(output_dir) if f.endswith(".tfw") or f.endswith(".xml") or f.endswith(".ovr") or f.endswith(".cpg") or f.endswith(".dbf") ]
        for f in filelist:
        	print "..."
            #os.remove(os.path.join(output_dir, f))
        print "Finished Clearing unused file"
    except SpatialRefProjError:
        ap.AddError ("Spatial Data must use a projected coordinate system to run")

    except LicenseError:
        ap.AddError ("Spatial Analyst license is unavailable")

    finally:
        checkin_Ext("Spatial")

def cloud_mask(path, out, output, meta):
    ap.env.workspace = output
    
    cloud = os.path.join(output, 'cloud')
    os.mkdir(cloud)

    ap.CheckOutExtension("Spatial")
    rasters = ap.ListRasters('*.TIF')
    mask = Raster(out+'/mask_cloud_' + str(os.path.basename(path)) + '.TIF')

    for i in range(len(rasters)):

        raster = Raster(rasters[i])
        print raster
        output_mask = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + 'CLOUDRMV_' + str(band_nmbr(rasters[i])) +'.TIF'
        out_mask = Con((mask == 0), raster, 1)
        #out_mask = Con((mask == 0), raster)
        out_mask.save(os.path.join(cloud, output_mask))

	print "Clearing unused file"
	filelist = [ f for f in os.listdir(cloud) if f.endswith(".tfw") or f.endswith(".xml") or f.endswith(".ovr") or f.endswith(".cpg") or f.endswith(".dbf") ]
	for f in filelist:
		print "..."
		#os.remove(os.path.join(cloud, f))
	print "Finished Clearing unused file"

def calc_toa(input_dir, output_dir, meta):
    '''Raster Algebra to run reflectance equation

        @param   input_dir: landsat 8 directory after unzip
        @type    input_dir: c{str}
        @param   meta: metadata parsed from MTL file
        @type    meta: dictionary
        @return  output: out raster path
    '''

    ##  Setting output directory id not defined
    ap.env.workspace = input_dir

    if output_dir is None:
        output_dir = os.path.join(input_dir, "TOA")
        if os.path.exists(output_dir):
            sys.exit(0)
            print "\nDirectory for reprojection already Exisits"
            ap.AddMessage("\nDirectory for reprojection already Exisits")
        else:
            os.mkdir(output_dir)
            print "\nCreated the output directory: " + output_dir
            ap.AddMessage("\nCreated the output directory: " + output_dir)
    else:
        if os.path.exists(output_dir):
            sys.exit(0)
            print "\nDirectory for reprojection already Exisits"
            ap.AddMessage("\nDirectory for reprojection already Exisits")
        else:
            os.mkdir(output_dir)
            print "\nCreated the output directory: " + output_dir
            ap.AddMessage("\nCreated the output directory: " + output_dir)

    rasters = ap.ListRasters('*.TIF')
    ms_bands = [band for band in rasters if (band_nmbr(band) != None)]

    try:
        checkout_Ext("Spatial")

        print "\nCalculating TOA Reflectance for landsat 8 bands"
        ap.AddMessage("\nCalculating TOA Reflectance for landsat 8 bands")
        for band in ms_bands:

            print "\nBegining to calculate TOA for " + band
            ap.AddMessage("\nBegining to calculate TOA for " + band)
            number = band_nmbr(band)
            raster_band = ap.sa.Raster(band)
            out_band = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + 'TOA_B' + str(number) + '.img'
        
            sun_elev = float(meta['IMAGE_ATTRIBUTES']['SUN_ELEVATION'])
            rad_mult = float(meta['RADIOMETRIC_RESCALING']['RADIANCE_MULT_BAND_' + str(number)])
            rad_add = float(meta['RADIOMETRIC_RESCALING']['RADIANCE_ADD_BAND_' + str(number)])
        
            toa_refl = (rad_mult*raster_band + rad_add)/(math.sin(sun_elev))

            print "Writing " + str(out_band)
            ap.AddMessage("Writing " + str(out_band))
            toa_refl.save(os.path.join(output_dir, out_band))

    except SpatialRefProjError:
        ap.AddError ("Spatial Data must use a projected coordinate system to run")

    except LicenseError:
        ap.AddError ("Spatial Analyst license is unavailable") 	

    finally:
        checkin_Ext("Spatial")


def stack_bands(path, meta, data_type):
    '''Stack Landsat bands 1 - 11 within a directory

        @param output: path of output reflectance.
        @ptype output: c{str}
    '''

    print "\nStacking bands to create a composite raster"
    ap.AddMessage("\nStacking bands to create a composite raster")

    ap.env.workspace = path

    ap.CheckOutExtension("Spatial")
    rasters = ap.ListRasters()

    if(data_type == "Landsat8"):
        print "Landsat8"
        rgb_rasters = [rgb for rgb in rasters if band_nmbr(rgb) >= 2 and band_nmbr(rgb) <= 5]

    else:
        rgb_rasters = [rgb for rgb in rasters if band_nmbr(rgb) >= 1 and band_nmbr(rgb) <= 4]

    print "\nRGB Bands:"
    print " " + str(rgb_rasters)

    out_stack = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + 'STACK_RGB.img'

    ap.AddMessage("Stacking R, G, B, and NIR bands")

    ap.CompositeBands_management(rgb_rasters, out_stack)    


    print "\nComposite Stack Complete!"
    ap.AddMessage("Composite Stack Complete")


def calc_ndwi(path, meta, data_type, threshold_type):
    '''Use the pan chromatic layer to pan-sharen the Blue, Green, Red, & NIR stack

        @param   path:  Directory containing @param stack
        @ptype   path:  c{str}
        @param   meta:  Metadat built from MTL.txt
        @ptype   meta:  Dictionary of landsat scene metadata
        @return  Output composite image with pan-sharpening
    '''

    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")
    output_ndwi = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + '_NDWI.img'
    output_ndvi = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + '_NDVI.img'

    if(data_type == "Landsat8"):
        print('Landsat8')
        green = Float(ap.sa.Raster(ap.ListRasters('*B3.img')[0]))
        red = Float(ap.sa.Raster(ap.ListRasters('*B4.img')[0]))
        nir = Float(ap.sa.Raster(ap.ListRasters('*B5.img')[0]))
        swir = Float(ap.sa.Raster(ap.ListRasters('*B6.img')[0]))

    else:
        green = Float(ap.sa.Raster(ap.ListRasters('*B2.img')[0]))
        red = Float(ap.sa.Raster(ap.ListRasters('*B3.img')[0]))
        nir = Float(ap.sa.Raster(ap.ListRasters('*B4.img')[0]))
        swir = Float(ap.sa.Raster(ap.ListRasters('*B5.img')[0]))

    try:
        checkout_Ext("Spatial")
        
        print "\nCalculating NDWI"
        ap.AddMessage("\nCalculating NDWI")

        if(threshold_type == "Gao (1996)"):
            print('Gao (1996)')
            #ndwi = (nir - swir) / (nir + swir)
            #ndvi = (nir-red) / (nir+red)
            ndwi = (green - nir) / (green + nir)

        else:
            ndwi = (green - nir) / (green + nir)
            #ndvi = (nir-red) / (nir+red)

        print "\nSaving NDWI As: " + str(output_ndwi)
        ap.AddMessage("\nSaving NDWI As: " + str(output_ndwi))
        ndwi.save(output_ndwi)
        #ndvi.save(output_ndvi)

        print "\nFinished NDWI"
        ap.AddMessage("\nFinished NDWI")

        filelist = [ f for f in os.listdir(path) if f.endswith(".tfw") or f.endswith(".xml") or f.endswith(".ovr") or f.endswith(".cpg") or f.endswith(".dbf") ]
        for f in filelist:
        	print "..."
            #os.remove(os.path.join(path, f))

    except SpatialRefProjError:
        ap.AddError ("Spatial Data must use a projected coordinate system to run")

    except LicenseError:
        ap.AddError ("Spatial Analyst license is unavailable") 	

    finally:
        checkin_Ext("Spatial")
        
        # ap.Delete_management("forGettingLoc")

def diffNDWI(path, pre_flood, post_flood):

    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")
    output_ndwi_diff = 'DIFF_NDWI.img'
    output_ndvi_diff = 'DIFF_NDVI.img'

    if(os.path.exists(path+"/"+output_ndwi_diff)):
    	print "..."
        #os.remove(path+"/"+output_ndwi_diff)

    ndwiPre = ap.sa.Raster(path+"/processed_PreFlood/toa/"+pre_flood+"_NDWI.img")
    ndwiPost = ap.sa.Raster(path+"/processed_PostFlood/toa/"+post_flood+"_NDWI.img")

    ap.AddMessage("\nCalculating different NDWI") 

    ndwiDiff = ndwiPost - ndwiPre
    ndwiDiff.save(output_ndwi_diff)

    # ndviPre = ap.sa.Raster(path+"/processed_PreFlood/toa/"+pre_flood+"_NDVI.img")
    # ndviPost = ap.sa.Raster(path+"/processed_PostFlood/toa/"+post_flood+"_NDVI.img")

    # ndviDiff = ndviPost - ndviPre
    # ndviDiff.save(output_ndvi_diff)


    ap.AddMessage("\nFinished saved NDWI different")

def pixelExtraction(path, pre_flood, post_flood, NDWIDiff, NDWIPost):
    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")
    output_permWater = 'PERMANENT_WATER.img'
    output_floodWater = 'FLOOD_WATER.img'
    output_preInudate = 'PREVIOUSLY_INUNDATED.img'
    output_nonFlood = 'NON_FLOOD_AREA.img'

    outFlood1 = 'Output_flood1.img'
    outFlood2 = 'Output_flood2.img'
    outFinal = 'out_final.img'

    if(os.path.exists(path+"/"+outFinal)):
    	print "..."
        #os.remove(path+"/"+outFinal)

    redPre = ap.sa.Raster(path+"/processed_PreFlood/toa/"+pre_flood+"TOA_B4.img")
    nirPost = ap.sa.Raster(path+"/processed_PostFlood/toa/"+post_flood+"TOA_B5.img")
    swirPost = ap.sa.Raster(path+"/processed_PostFlood/toa/"+post_flood+"TOA_B6.img")

    ndwiDiff = ap.sa.Raster(path+"/DIFF_NDWI.img")
    ndwiPost = ap.sa.Raster(path+"/processed_PostFlood/toa/"+post_flood+"_NDWI.img")
    ndwiPre = ap.sa.Raster(path+"/processed_PreFlood/toa/"+pre_flood+"_NDWI.img")

    # ndviDiff = ap.sa.Raster(path+"/DIFF_NDVI.img")
    # ndviPost = ap.sa.Raster(path+"/processed_PostFlood/toa/"+post_flood+"_NDVI.img")
    # ndviPre = ap.sa.Raster(path+"/processed_PreFlood/toa/"+pre_flood+"_NDVI.img")


    ap.AddMessage("\nBegin condition data class")

    out1 = Con (((ndwiDiff >= float(NDWIDiff)) & (ndwiPost >= float(NDWIPost))), 1, 0)
    out1.save(outFinal)

    ap.AddMessage("\nFinished grouping data area")
    
def spatial_filter(path, meta, filterpath):
    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")
    out_filter = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + 'STACK_FILTER.img'
    print out_filter

    print ""
    print "Begining Spatial Filtering"
    ap.AddMessage("Begining Spatial Filtering")

    # Check out the ArcGIS Spatial Analyst extension license
    ap.CheckOutExtension("Spatial")

    rasters = ap.ListRasters()
    inRaster = [img for img in rasters if 'STACK_PANSHARP.img' in img]

    # Execute FocalStatistics
    kerPath = os.path.join(str(get_script_path()),"high-pass.txt")
    print(kerPath)
    outFocalStatistics = ap.sa.FocalStatistics(inRaster[0], ap.sa.NbrIrregular(kerPath))

    # Save the output 
    outFocalStatistics.save(out_filter)

    print ""
    print "Spatial Filtering Complete"
    ap.AddMessage("Spatial Filtering Complete")

def final_spatial_filter(path, filterpath):
    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")
    out_filter = 'out_final_mask_filter.img'
    if(os.path.exists(path+"/"+out_filter)):
    	print "..."
        #os.remove(path+"/"+out_filter)
    print "Saved as: " + out_filter
 
    inRaster = path + "/out_final_mask.img"

    print ""
    print "Begining Spatial Filtering"
    ap.AddMessage("Begining Spatial Filtering")

    # Check out the ArcGIS Spatial Analyst extension license
    ap.CheckOutExtension("Spatial")

    kerPath = os.path.join(str(get_script_path()),"majority.txt")
    print(kerPath)
    outFocalStatistics = ap.sa.FocalStatistics(inRaster, ap.sa.NbrIrregular(kerPath))
    out_final_filter = Con((outFocalStatistics == 1), 1, 0)
    # Save the output 
    out_final_filter.save(out_filter)

    print ""
    print "Spatial Filtering Complete"
    ap.AddMessage("Spatial Filtering Complete")

    print "Clearing unused file"
    filelist = [ f for f in os.listdir(path) if f.endswith(".tfw") or f.endswith(".xml") or f.endswith(".ovr") or f.endswith(".cpg") or f.endswith(".dbf") ]
    for f in filelist:
    	print "..."
        #os.remove(os.path.join(path, f))
	print "Finished Clearing unused file"

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
## Funtion not built into function "process_landsat"
def pan_sharpen(path, meta, data_type):
    '''Use the pan chromatic layer to pan-sharen the Blue, Green, Red, & NIR stack

        @param   stack: Input composite image stack
        @ptype   stack: c{string}
        @param   meta:  Metadat built from MTL.txt
        @ptype   meta:  Dictionary of landsat scene metadata
        @return  Output composite image with pan-sharpening
    '''
    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")
    out_stack = str(meta['L1_METADATA_FILE']['LANDSAT_SCENE_ID']) + 'STACK_PANSHARP.img'

    rasters = ap.ListRasters()
    rgb = [img for img in rasters if 'STACK_RGB.img' in img]
    pan = [img for img in rasters if 'B8.img' in img]

    print rgb
    print pan
    print ""
    print "Begining Pan Sharpen"

    if(data_type == "Landsat8"):
        print "Landsat8"
        ap.CreatePansharpenedRasterDataset_management(rgb[0], "4", "3", "2", "5", out_stack, pan[0], "Brovey") 
    else:
        ap.CreatePansharpenedRasterDataset_management(rgb[0], "3", "2", "1", "4", out_stack, pan[0], "Brovey")

    print ""
    print "Pan Sharpen Complete"


def createRandomPoint(path):
    ap.CheckOutExtension("Spatial")
    outFolder = path
    numPoints = 40
    outName = "random_point.shp"
    conFC = path+"/out_final.img"

    ap.AddMessage("Creating Random Point")
    ap.CreateRandomPoints_management(outFolder, outName, "", conFC, numPoints) 
    ap.AddMessage("Finished creat random point")


def valuesToPoint(path):

    # Set environment settings
    ap.env.workspace = path
    ap.CheckOutExtension("Spatial")

    # Set local variables
    inPointFeatures = path+"/random_point.shp"
    inRaster = ap.sa.Raster(path+"/out_final.img")
    outPointFeatures = "random_point_values.shp"

    ap.AddMessage("Extract raster value to poin")
    # Execute ExtractValuesToPoints
    ExtractValuesToPoints(inPointFeatures, inRaster, outPointFeatures, "INTERPOLATE", "VALUE_ONLY")

    ap.AddMessage("Finished Extract value to point")

def rasterToVector(path):
    ap.CheckOutExtension("Spatial")
    ap.env.workspace = path
    out_vector = 'out_final_mask_filter.shp'

    rasters = ap.ListRasters()
    inRaster = [img for img in rasters if 'out_final_mask_filter.img' in img]
    field = "VALUE"

    ap.RasterToPolygon_conversion(inRaster[0], out_vector, "NO_SIMPLIFY", field)

def maskOutFinal(outPath, maskPath):
    # Set local variables
    inRaster = outPath + "/out_final.img"
    kerPath = os.path.join(str(get_script_path()),"INDONESIA_PROP.shp")
    print(kerPath)
    inMaskData = str(kerPath)

    if(os.path.exists(outPath+"/"+ "out_final_mask.img")):
    	print "..."
        #os.remove(outPath+"/"+ "out_final_mask.img")
    # Check out the ArcGIS Spatial Analyst extension license
    ap.CheckOutExtension("Spatial")


    ap.AddMessage("Shp Indonesia masking")
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(inRaster, inMaskData)

    # Save the output 
    outExtractByMask.save( outPath + "/out_final_mask.img")
    ap.AddMessage("Finished masking")

def layerToKml(outPath):
	ap.env.workspace = outPath
	pathLayer = outPath + "/out_final_mask_filter.shp"
	outKML = outPath + "/out_final_mask_filter_kml.kmz"
	ap.AddMessage("Converting to kml: "+ pathLayer)
	rasters = ap.ListRasters()
	inRaster = [img for img in rasters if 'out_final.img' in img]

	ap.LayerToKML_conversion(pathLayer, outKML)
	ap.AddMessage("Finished convert to kml")

def mergeClass(outPath):
    output = outPath + "/out_combine.tif"
    permWater = Raster(outPath + "/permWaterCrr.tif")
    outFinal = Raster(outPath + "/out_final.img")
    out = Con((permWater == 1), 1, Con((outFinal == 0), 2, Con(( outFinal == 1), 3)))
    out.save(output)

def sampleClassification(outPath, rgbPath, gsgPath):
    # Set local variables

    if(os.path.exists(outPath+"/"+ "out_final.img")):
    	print "..."
        #os.remove(outPath+"/"+ "out_final.img")
    inRaster = ap.sa.Raster(outPath+"/processed_PostFlood/toa/"+rgbPath+"STACK_RGB.img")
    sigFile = gsgPath
    probThreshold = "0.0"
    aPrioriWeight = "EQUAL"
    aPrioriFile = ""
    #outConfidence = "c:/sapyexamples/output/redconfmlc"


    # Check out the ArcGIS Spatial Analyst extension license
    ap.CheckOutExtension("Spatial")
    ap.AddMessage("Classify data with training sample")
    # Execute 
    mlcOut = MLClassify(inRaster, sigFile, probThreshold, aPrioriWeight, 
                        aPrioriFile, "") 

    # Save the output 
    mlcOut.save(outPath + "/out_final.img")
    ap.AddMessage("Finished classify data")
##  
##  Helper FUnctions
##  
def band_nmbr(filename):
    ''' Find the landsat band number

        @param   filename: Input landsat band to extract band number
        @ptype   filename: c{str}
        @return  Band number
        @rtype   c{int}
    '''
    try:
        band_num = int(filename.split('_')[1].split('.')[0].replace('B', ''))
        return band_num
    except:
        pass
    

##  Verify and create directory
def check_Dir(input_path, named_path):
    if input_path is None:
        input_path = os.path.join(input_path, named_path)
        if os.path.exists(input_path):
            sys.exit(0)
            print "\nDirectory for reprojection already Exisits"
        else:
            os.mkdir(input_path)
            print "\nCreated the output directory: " + input_path
    else:
        if os.path.exists(input_path):
            sys.exit(0)
            print "\nDirectory for reprojection already Exisits"
        else:
            os.mkdir(input_path)
            print "\nCreated the output directory: " + input_path

    
##  Checkout ArcGIS extension by name
def checkout_Ext(ext_type):
    if ap.CheckExtension(ext_type) == 'Available':
        ap.CheckOutExtension(ext_type)
        print "\nChecking out " + ext_type + " Extension"
    else:
        raise LicenseError
        print "\nCannot checkout " + ext_type + " Extension"


##  Checkin ArcGIS extension by name
def checkin_Ext(ext_type):
    ap.CheckInExtension(ext_type)
    print "\nChecking in " + ext_type + " Extension"
    
##  'parse_mtl' Function Thanks To:
##      Copyright (c) 2011 Australian Government, Department of Sustainability, Environment, Water, Population and Communities
##      https://code.google.com/p/metageta/source/browse/trunk/lib/formats/landsat_mtl.py?r=608    
def parse_mtl(path=None):
    '''Traverse the downloaded landsat directory and read MTL file

        @type    path: c{str}
        @param   path: Path to landsat file directory
        @rtype   C{dict}
        @return  Dictionary
    '''

    if path is None:
        path = "c:/landsat"

    
    files = os.listdir(path)
    mtl = [txt for txt in files if 'MTL.txt' in txt][0]
    lines = iter(open(os.path.join(path, mtl)).readlines())
    hdrdata= {}

    line = lines.next()

    while line:
        line=[item.strip() for item in line.replace('"','').split('=')]
        group=line[0].upper()
        if group in ['END;','END']:break
        value=line[1]
        if group in ['END_GROUP']:pass
        elif group in ['GROUP']:
            group=value
            subdata={}
            while line:
                line=lines.next()
                line = [l.replace('"','').strip() for l in line.split('=')]
                subgroup=line[0]
                subvalue=line[1]
                if subgroup == 'END_GROUP':
                    break
                elif line[1] == '(':
                    while line:
                        line=lines.next()
                        line = line.replace('"','').strip()
                        subvalue+=line
                        if line[-1:]==';':
                            subvalue=eval(subvalue.strip(';'))
                            break
                else:subvalue=subvalue.strip(';')
                subdata[subgroup]=subvalue
            hdrdata[group]=subdata
        else: hdrdata[group]=value.strip(');')
        line=lines.next()
    return hdrdata

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)


version = '0.2'
utm_zone12 = "PROJCS['NAD_1983_UTM_Zone_12N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-111.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "NEAREST", "30", "WGS_1984_(ITRF00)_To_NAD_1983", "", "PROJCS['WGS_84_UTM_zone_12N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['false_easting',500000.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-111.0],PARAMETER['scale_factor',0.9996],PARAMETER['latitude_of_origin',0.0],UNIT['Meter',1.0]]"
