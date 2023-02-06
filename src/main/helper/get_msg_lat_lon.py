#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import *
import argparse

def col_lin2lat_lon(col, lin, sub_lon, COFF,LOFF,LFAC,CFAC):


	miss_val_lat=-32768
	miss_val_lon=-32768

	aux16 = 2.**(-16)
	p1=42164.
	p2=1.006803
	p3=1737121856
	pi     = 3.141592653589793238462643383279502884197
	two_pi = 2.*pi

	deg2rad=pi/180.
	rad2deg=180./pi
	
	x = (col-COFF)/(aux16*CFAC) # Degrees
	x = x*deg2rad				# Radians
	y = (lin-LOFF)/(aux16*LFAC) # Degrees
	y = y*deg2rad				# Radians


	if(((p1 * cos(x) * cos(y))**2 - (cos(y)**2 + p2 * sin(y)**2) * p3) < 0):
		lat=miss_val_lat
		lon=miss_val_lon
		return
	else:
		sd = sqrt((p1 * cos(x) * cos(y))**2 - (cos(y)**2 + p2 * sin(y)**2) * p3)
		sn = (p1 * cos(x) *cos(y) -sd)/(cos(y)**2 + p2 * sin(y)**2)
		s1 = p1 - sn * cos(x) * cos(y)
		s2 = sn * sin(x) * cos(y)
		s3 = -sn * sin(y)
		sxy = sqrt(s1**2 + s2**2)

		lon = atan((s2/s1)) 
		lon=lon*rad2deg + sub_lon
		if (lon > 180.): lon=lon-360.
		lat = atan(p2 * (s3/sxy))
		lat=lat*rad2deg

	return lat,lon

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='\tCalcule the Latitude and Longitude of an MSG pixel given the column and line of an LSA SAF pre-defined region')

	# Defining Defaults
	parser.add_argument('-col', metavar='col', dest='col', type=int, default=0 , help='Column [1,3712]')
	parser.add_argument('-lin', metavar='lin', dest='lin', type=int, default=0,  help='Line [1,3712]')
	parser.add_argument('-a', metavar='area', dest='area', type=str, default='MSG-Disk', help='One of the LSA SAF pre-defined regions (Euro, NAfr, SAfr, SAme, MSG-Disk, IODC-Disk)')

	args = parser.parse_args()

	col = args.col
	lin = args.lin
	area = args.area


	# The follwoing coefficients are required to relate the latitude/longitude with
	# the column/line within each LSA SAF pre-defined region. Those coefficients 
	# are available in the product files metadata 
	#-------------------------------------------------

	# Sub-Sattelite Longitude (from PROJECTION_NAME attribute at the products metadata)
	if "IODC-Disk" in area: sub_lon=41.5 			
	if "MSG-Disk" in area:	sub_lon=0	
	if "Euro" in area:		sub_lon=0	
	if "NAfr" in area:		sub_lon=0	
	if "SAfr" in area:		sub_lon=0	
	if "SAme" in area:		sub_lon=0	
	
	# Column and line offset (from COFF and LOFF attributes at the products metadata)
	if "IODC-Disk" in area:
		COFF=1857
		LOFF=1857
	if "MSG-Disk" in area:
		COFF=1857
		LOFF=1857
	if "Euro" in area:	
		COFF=308
		LOFF=1808
	if "NAfr" in area:	
		COFF=618
		LOFF=1158
	if "SAfr" in area:	
		COFF=-282
		LOFF=8
	if "SAme" in area:	
		COFF=1818
		LOFF=398

	# Common coefficients (from CFAC and LFAC attributes at the products metadata)
	CFAC=13642337
	LFAC=13642337

	lat,lon = col_lin2lat_lon(col, lin, sub_lon, COFF,LOFF,LFAC,CFAC)

	print('Region:   %s')%(area)		
	print('Col=   %s')%(col)
	print('Lin=   %s')%(lin)
	print('        |')
	print('        V')
	print('Lat=   %s')%(lat)
	print('Lon=   %s')%(lon)

