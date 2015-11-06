#!/usr/bin/python

import SimpleITK as sitk
import sys
import numpy

def PrintUsage():
  print "Usage: "+sys.argv[0]+" LabelMap SplitMask/axis=index {x=12|y=24|z=36} OutputFileName"
  exit(-1)

def main():
  if len(sys.argv) != 4:
    PrintUsage()

  labelmap=sitk.ReadImage( sys.argv[1] )
  zsize=labelmap.GetSize()[2]
  ysize=labelmap.GetSize()[1]
  xsize=labelmap.GetSize()[0]

  SplitMaskArg=sys.argv[2]
  splitArgs=SplitMaskArg.split('=')
  if len(splitArgs) == 2:
    [axis,value]=splitArgs
    if not value.isdigit():
      PrintUsage()
    [minx,miny,minz]=[xsize,ysize,zsize]
    if axis=='x':
      minx=int(value)
    elif axis=='y':
      miny=int(value)
    elif axis=='z':
      minz=int(value)
    else:
      PrintUsage()
    splitmask=sitk.Image(xsize,ysize,zsize,sitk.sitkInt16)
    for z in range( 0, zsize ):
      for y in range( 0, ysize ):
        for x in range( 0, xsize ):
          if x < minx and y < miny and z < minz:
            splitmask.SetPixel(x,y,z,1)
          else:
            splitmask.SetPixel(x,y,z,0)
  else:
    splitmask=sitk.ReadImage( SplitMaskArg )
  zmasksize=splitmask.GetSize()[2]
  ymasksize=splitmask.GetSize()[1]
  xmasksize=splitmask.GetSize()[0]
  if zsize != zmasksize or ysize != ymasksize or xsize != xmasksize :
    print "Labelmap and SplitMask must have the same size"
    exit(-1)
  array=sitk.GetArrayFromImage(labelmap)
  max=numpy.amax(array)
  for z in range( 0, zsize ):
    for y in range( 0, ysize ):
      for x in range( 0, xsize ):
        if( splitmask.GetPixel( x, y, z ) and labelmap.GetPixel( x , y , z ) ):
          val = labelmap.GetPixel( x , y , z ) +  max
          labelmap.SetPixel( x, y, z, int(val) )
  sitk.WriteImage(labelmap, sys.argv[3])

if __name__ == "__main__":
  main()
