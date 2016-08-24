#!/usr/bin/python

##
## Copyright (C) 2011-2012 Andrew Atkinson
##
##-------------------------------------------------------------------
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##-------------------------------------------------------------------

import os
import struct
import time


def dateticks(F):
    ticks = struct.unpack('<Q', F.read(8))
    #Need to convert this date from .NET
    NANOSEC = 10000000
    #Number of python tick since 1/1/1 00:00
    PTICKS = 62135596800
    tripdate = time.gmtime((ticks[0] / NANOSEC) - PTICKS)
    return tripdate


def comments(F):
    #byte is the comment length
    commentlength = struct.unpack('<B', F.read(1))
    #print(commentlength)
    if commentlength[0] >= 128:
        commentlength2 = struct.unpack('<B', F.read(1))
        clen = commentlength[0] - 128 + (128 * commentlength2[0])
        if commentlength2[0] >= 128:
            print('comment is rediculously long, this will break things')
            #probably should raise an error here
    else:
        clen = commentlength[0]
    #print(clen)
    C = F.read(clen)
    
    if clen == 0:
        return ""
    
    # Test if it's not DistoX2 sensor readouts 
    if C[0] == "{":
        i = 1 
        while i < clen and C[i] <> "}":
            i += 1
        if i < clen:
            C = C[(i + 1):]
    return str(C)
    #In python 3
    #return str(C,'utf-8')


def trip(F):
    #First 8 (int64) is the date in ticks
    tdate = dateticks(F)
    #print(time.strftime("%Y.%m.%d", tdate))
    comment = comments(F)
    #Next 2 bytes (int16) is declination
    declination = struct.unpack('<H', F.read(2))
    dec = adegrees(declination[0])
    return {'date': tdate, 'comment': comment, 'dec': dec}


def distmm(pnt):
    '''Points in mm, convert to metres'''
    return float(pnt) / 1000


def adegrees(angle):
    '''convert angle from internal units to degrees'''
    return (360 * float(angle) / 65536)


def roll(angle):
    '''convert angle from internal units to degrees'''
    return (360 * float(angle) / 256)


def shot(F):
    thline = {'from': station(F)}
    thline['to'] = station(F)
    Dist = struct.unpack('<L', F.read(4))
    thline['tape'] = distmm(Dist[0])
    azimuth = struct.unpack('<H', F.read(2))
    thline['compass'] = adegrees(azimuth[0])
    inclination = struct.unpack('<h', F.read(2))
    thline['clino'] = adegrees(inclination[0])
    flags = struct.unpack('<B', F.read(1))
    #Roll of the DistoX on taking reading can be ignored
    #Internal angle interger 0-256
    #F.read(1)
    rawroll = struct.unpack('<B', F.read(1))
    thline['rollangle'] = roll(rawroll[0])
    tripindex = struct.unpack('<h', F.read(2))
    thline['trip'] = tripindex[0]
    #bit 1 of flags is flip (left or right)
    #bit 2 of flags indicates a comment
    if (flags[0] & 0b00000001) == 0b000000001:
        thline['direction'] = '<'
    else:
        thline['direction'] = '>'
    if (flags[0] & 0b00000010) == 0b000000010:
        thline['comment'] = comments(F)
    
    return thline


def reference(F):
    #Totally untested
    stnid = station(F)
    east = struct.unpack('<Q', F.read(8))
    west = struct.unpack('<Q', F.read(8))
    altitude = struct.unpack('<L', F.read(4))
    comment = comments(F)
    return [stnid, distmm(east[0]), distmm(west[0]),
            distmm(altitude[0]), comment]


def Point(F):
    x = struct.unpack('<l', F.read(4))
    y = struct.unpack('<l', F.read(4))
    #original y is screen coordinates from the top
    coor = {'x': distmm(x[0]), 'y': (-1 * distmm(y[0]))}
    #print(coor)
    return coor


def Polygon(F):
    A = struct.unpack('<L', F.read(4))
    #print('points ', A[0])
    poly = []
    z = 1
    while z <= A[0]:
        poly.append(Point(F))
        z += 1
    Colour = struct.unpack('<B', F.read(1))
    Colours = ('black', 'gray', 'brown', 'blue', 'red', 'green', 'orange')
    XVIpoly = {}
    XVIpoly['colour'] = Colours[Colour[0] - 1]
    templist = []
    for p in poly:
        templist.append(p)
    XVIpoly['coord'] = templist
    return XVIpoly


def station(F):
    #id's split into major.decimal(minor)
    idd = struct.unpack('<H', F.read(2))
    idm = struct.unpack('<H', F.read(2))
    #Turn stn into string, andnulls into -
    if idm[0] == 32768:
        if idd[0] == 0:
            stnid = "-"
        else:
            stnid = str(idd[0] - 1)
    else:
        stnid = str(idm[0]) + "." + str(idd[0])
    return stnid


def xsection(F):
    pnt = Point(F)
    stn = station(F)
    #Need to look up the coordinate of the station
    d = struct.unpack('<l', F.read(4))
    direction = d[0]
    #-1: horizontal, >=0; projection azimuth (internal angle units)
    if direction != -1:
        direction = adegrees(direction)
    #print(pnt['x'], pnt['y'], stn, direction)
    return [pnt['x'], pnt['y'], stn, direction]


def mapping(F):
    """centrepoint and scale of a map screen"""
    #not used by therion import
    F.read(12)
##    X = struct.unpack('<L', F.read(4))
##    Y = struct.unpack('<L', F.read(4))
##    Scale = struct.unpack('<L', F.read(4))
##    print(X[0], Y[0], Scale[0])
    return


def drawing(F):
    mapping(F)
    polys = []
    xsec = []
    element = struct.unpack('<B', F.read(1))
    while element[0] != 0:
        if element[0] == 1:
            #1 is a standard line
            polys.append(Polygon(F))
        elif element[0] == 3:
            #3 is location and orientation of a xsection
            xsec.append(xsection(F))
        else:
            print('undefined object number: ', element[0])
        element = struct.unpack('<B', F.read(1))
    return {'polys': polys, 'xsec': xsec}


def fsection(F, section):
    #Next 4 Bytes (Int32) is the number times repeated
    length = struct.unpack('<L', F.read(4))
#    print(length[0])
    if length[0] != 0:
        A = []
        x = 1
        while x <= length[0]:
            A.append(section(F))
            x += 1
        return A
    else:
        return


def readfile(pockettoponame, dooutline=True, dosideview=True):
    with open(pockettoponame, "rb") as tfile:
    #First 3 bytes should read Top
        if tfile.read(3) == b'Top':
            #Next Byte should be the version number
            version = struct.unpack('B', tfile.read(1))
            #print('We have a top file version ' + str(version[0]))
            #print('Reading Trips')
            trips = fsection(tfile, trip)
            #print('Reading Shots')
            shots = fsection(tfile, shot)
            #print('Reading Reference points')
            references = fsection(tfile, reference)
            #print('Reading Map scales')
            mapping(tfile)
            #print('Reading the shot data')
            if dooutline | dosideview:
                outline = drawing(tfile)
                print('Reading the plan (outline)')
#                print(trips)
                if dosideview:
                    sideview = drawing(tfile)
                    #print('Reading elevation (sideview)')
                    return {'trips': trips, 'shots': shots, 'ref': references,
                            'outline': outline, 'sideview': sideview}
                return {'trips': trips, 'shots': shots, 'ref': references, 'outline': outline}
            return {'trips': trips, 'shots': shots, 'ref': references}
        else:
            #need to raise an error here really
            return {}
