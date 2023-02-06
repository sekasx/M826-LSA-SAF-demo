#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import *
import argparse


def lat_lon2col_lin(lat, lon, sub_lon, COFF,LOFF,LFAC,CFAC):


	pi     = 3.141592653589793238462643383279502884197
	two_pi = 2.*pi

	aux16 = 2.**(-16)
	p1=42164.
	p2=0.00675701
	p3=0.993243
	rp=6356.5838

	deg2rad=pi/180.
	rad2deg=180./pi

	lat = lat*deg2rad			# Radians
	lon = lon*deg2rad			# Radians
	sub_lon = sub_lon*deg2rad	# Radians


	c_lat = atan(p3 * tan(lat))
	rl = rp / sqrt(1. - p2 * (cos(c_lat))**2)
	r1 = p1 - rl * cos(c_lat) * cos(lon - sub_lon)
	r2 = -rl * cos(c_lat) * sin(lon - sub_lon)
	r3 = rl * sin(c_lat)
	rn = sqrt(r1**2 + r2**2 + r3**2)

	x = atan(-r2/r1)
	y = asin(-r3/rn)

	x = x*rad2deg
	y = y*rad2deg

	col = COFF + round(x*aux16*CFAC)
	lin = LOFF + round(y*aux16*LFAC)


	return col,lin

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='\tCalcule the MSG pixel (column and line) within the LSA SAF pre-defined regions given the Latitude and Longitude')

	# Defining Defaults
	parser.add_argument('-lat', metavar='lat', dest='lat', type=float, default=0 , help='[80,80]')
	parser.add_argument('-lon', metavar='lon', dest='lon', type=float, default=0,  help='[-180,180]')
	parser.add_argument('-a', metavar='area', dest='area', type=str, default='MSG-Disk', help='One of the LSA SAF pre-defined regions (Euro, NAfr, SAfr, SAme, MSG-Disk, IODC-Disk)')

	args = parser.parse_args()

	lat = args.lat
	lon = args.lon
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

	col,lin = lat_lon2col_lin(lat, lon, sub_lon, COFF,LOFF,LFAC,CFAC)

	print('Region:   ', area)
	print('Lat=   ', lat)
	print('Lon=   ', lon)
	print('        |')
	print('        V')
	print('Col=   ', col)
	print('Lin=   ', lin)

