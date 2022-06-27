#!/usr/bin/env python3
'Plotting RSF files with matplotlib'

##   Copyright (C) 2010 University of Texas at Austin
##  
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2 of the License, or
##   (at your option) any later version.
##  
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##  
##   You should have received a copy of the GNU General Public License
##   along with this program; if not, write to the Free Software
##   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##  
##  
##  Author - Sergey Fomel - 2010
##   Revised - Ray Abma and Hector Corzo Pola - December 2020
##     - added a number of options for the trace plot and the imshow options.
##     - removed movie option to be put in another program 
##   Revised - Ray Abma - sfmatplot_v05 - June 2021
##     - added interpolation='none' to imshow parameters to produce plots more like sfgrey.

import sys
import m8r
import numpy
import matplotlib.pyplot as plt
import rsf.api as rsf

# self-documentation
if len(sys.argv) < 2:

    sys.stderr.write('Usage: %s <matplotlib function> <plot options> [format=jpeg] < inp.rsf [ > out.jpeg] \n\n' % sys.argv[0])

    sys.exit(1)

inp = rsf.Input()

# matplotlib command
plot = sys.argv[1]

# default picture format
pformat = None

# default to using colorbar

# default to transpose data
ptranspose = 'y'

#  set up some defaults
pdpi = None
pcomment = ''
xcomment = 0.0
ycomment = 0.0
pclip=98.0
ptitle = ''
pxlabel = ''
pylabel = ''
pzlabel = ''
pamplabel = ''
paspect='auto'
pcmap = 'gray'
pcmap2 = 'jet'
pcolorbar = 'y'
pgrid = 'n'
legend = 'n'
pin2 = None
palpha1 = 0.6
palpha2 = 1.0
pxsize=''
pysize=''
lgndarray=None

o1 = None
o2 = None
o3 = None

o1in = None
o2in = None
o3in = None

d1 = None
d2 = None
d3 = None

d1in = None
d2in = None
d3in = None

label1 = None
label2 = None
label3 = None

unit1 = None
unit2 = None
unit3 = None

# build parameter dictionary and obtain control parameters
# There are two types of parmeters here, the matplotlib parameters and
# this program's keywords.

args = {}
args2 = {}
for a in sys.argv[2:]:
    key = a.split('=')[0]
    val =  a.replace(key+'=','')

#  -- grab the non-matplotlib parameters ---
    if key == 'format':
        pformat = val

    elif key == 'comment':
        pcomment = val

    elif key == 'xcomment':
        xcomment = float(val)

    elif key == 'ycomment':
        ycomment = float(val)

    elif key == 'xsize':
        pxsize = float(val)

    elif key == 'pclip':
        pclip = float(val)
        if (pclip < 0.0):
            print(' pclip must be greater than 0.0, set to 0.0 =',file=sys.stderr)
            pclip = 0.0
        if (pclip > 100.0):
            print(' pclip must be less than or equal to 100.0, set to 100.0 =',file=sys.stderr)
            pclip = 100.0

    elif key == 'aspect':
        paspect = val

    elif key == 'ysize':
        pysize = float(val)

    elif key == 'dpi':
        pdpi = float(val)

    elif key == 'title':
        ptitle = val

    elif key == 'xlabel':
        pxlabel = val

    elif key == 'ylabel':
        pylabel = val

    elif key == 'amplabel':
        pamplabel = val

    elif key == 'grid':
        pgrid = val

    elif key == 'legend':
        legend = val

    elif key == 'transpose':
        ptranspose = val

    elif key == 'in2':
        pin2 = val

    elif key == 'alpha1':
        palpha1 = float(val)

    elif key == 'alpha2':
        palpha2 = float(val)

    elif key == 'cmap':
        pcmap = val

    elif key == 'cmap2':
        pcmap2 = val

    elif key == 'lgnd':
        pcmap2 = val
        lgndarray = val.split(',')

    elif key == 'o1':
        o1in = val
        o1in = float(o1in)

    elif key == 'o2':
        o2in = val
        o2in = float(o2in)

    elif key == 'd1':
        d1in = val
        d1in = float(d1in)

    elif key == 'd2':
        d2in = val
        d2in = float(d2in)

    elif key == 'o3':
        o3in = val
        o3in = float(o3in)

    elif key == 'd3':
        d3in = val
        d3in = float(d3in)

    elif key == 'colorbar':
        ## don't use colorbar in args
        xdum = val

#  -- anything that does not fit is a matplotlib parameter ---
    else:
        args[key] = val
        args2[key] = val

#print(' args =',args,file=sys.stderr)
#print(' args2 =',args2,file=sys.stderr)
# read data
n1 = inp.int("n1")
n2 = inp.int("n2")
if (n2 == None):
    n2=1
n3 = inp.int("n3")
if (n3 == None):
    n3=1

if (o1in == None):
    o1in = inp.int('o1')
    if (o1in == None):
        o1in = 1
    else:
        o1in = float(o1in)

if (d1in == None):
    d1in = inp.int('d1')
    if (d1in == None):
        d1in = 1
    else:
        print(' d1in =',d1in,file=sys.stderr)
        d1in = float(d1in)

if (o2in == None):
    o2in = inp.int('o2')
    if (o2in == None):
        o2in = 1
    else:
        o2in = float(o2in)

if (o3in == None):
    o3in = inp.int('o3')
    if (o3in == None):
        o3in = 1
    else:
        o3in = float(o3in)


d2instr = inp.string("d2")
if d2instr == None:
    d2instr = '1'
d2in = float(d2instr)

d3instr = inp.string("d3")
if d3instr == None:
    d3instr = '1'
d3in = float(d3instr)

label1in = ' '
label2in = ' '
label3in = ' '

label1in = inp.string("label1")
label2in = inp.string("label2")
label3in = inp.string("label3")

unit1in = inp.string("unit1")
unit2in = inp.string("unit2")
unit3in = inp.string("unit3")

#if (pxlabel == ''):
    #pxlabel = label1in+' (unit1in)'
#if (pylabel == ''):
    #pylabel = label2in+' (unit2in)'

if (o1 == None):
    o1 = o1in
if (o1 == None):
    o1 = 1
if (o2 == None):
    o2 = o2in
if (o2 == None):
    o2 = 1
if (o3 == None):
    o3 = o3in
if (o3 == None):
    o3 = 1

if (d1 == None):
    d1 = d1in
if (d1 == None):
    d1 = 1
if (d2 == None):
    d2 = float(d2in)
if (d2 == None):
    d2 = 1
if (label1 == None):
    label1 = label1in
if (label1 == None):
    label1 = " "
if (label2 == None):
    label2 = label2in
if (label2 == None):
    label2 = " "
if (label3 == None):
    label3 = label3in
if (label3 == None):
    label3 = " "


# set default plot format

if pformat == None:
    if plot == 'imshow':
        pformat = 'jpeg'
    elif plot == 'plot':
        pformat = 'jpeg'
    elif plot == 'transparent':
        pformat = 'jpeg'
    else:
        sys.stderr.write('Unrecognized plotting function "%s" \n\n' % plot)
        sys.exit(2)

# prepare the input data  ---------------------

#  --- we can only do up to 2 dimensions ---
n2 = n2 * n3
data = numpy.zeros([n2,n1],'f')
inp.read(data)

inp.close()

q = numpy.quantile(numpy.abs(data),pclip/100.0)
for i2 in range(n2):
    for i1 in range(n1):
        if (abs(data[i2,i1]) > q):
            if (data[i2,i1] < 0.0):
                data[i2,i1] = -q
            else:
                data[i2,i1] = q

# get the secondary input
if ( pin2 != None ):
    inp  = m8r.Input(pin2) 
    n1aux = inp.int("n1")
    n2aux = inp.int("n2")
    n3aux = inp.int("n3")
    n2aux = n2aux * n3aux
    n3aux = 1

#  -- check that the auxillary input matches the main input size

    if (n1 != n1aux or n2 != n2aux or n3 != n3aux):
        sys.stderr.write('input datasets sizes do not match \n')
        sys.stderr.write('input primary dataset sizes  \n')
        sys.stderr.write('n1= '+str(n1)+' n2= '+str(n2)+' n3='+str(n3)+'  \n')
        sys.stderr.write('input secondary dataset sizes  \n')
        sys.stderr.write('n1aux= '+str(n1aux)+' n2aux= '+str(n2aux)+
         ' n3aux='+str(n3aux)+'  \n')
        sys.exit(2)


    sdata_in = numpy.zeros((n2,n1), dtype=numpy.float32)
    data2 = numpy.zeros([n2,n1],'f')
    inp.read(sdata_in)
    for i2 in range(n2):
        for i1 in range(n1):
            data2[i2,i1] = numpy.float(sdata_in[i2,i1])

inp.close()


fig = plt.figure()
if (pxsize != '' and pysize != ''):
    fig.set_size_inches(pxsize,pysize)

# recognize the plotting type

# do a simple line plot

if plot == 'plot':
    y1 = numpy.zeros_like(data)
    lgnleng = numpy.size(lgndarray)
    for iplot in range(n2):
        for ii in range(numpy.shape(data)[1]):
            y1[iplot,ii] = o1 + (ii * d1)

        if (iplot < lgnleng and lgndarray != None):
            plt.plot(y1[iplot,:],data[iplot,:],label=lgndarray[iplot],**args)
        else:

            plt.plot(y1[iplot,:],data[iplot,:],label=str(iplot), **args)

        plt.xlabel(pxlabel)
        plt.ylabel(pamplabel)
        plt.title(ptitle)
        if (legend == 'y'):
            plt.legend(loc="upper right")
        plt.text(xcomment,ycomment,pcomment)
    if (pgrid == 'y'):
        plt.grid()


# this is a simple matrix plot

elif plot == 'imshow':
    if ptranspose == 'y':
        datat = numpy.transpose(data)
        plt.text(xcomment,ycomment,pcomment)
        plt.imshow(datat, cmap=pcmap,aspect=paspect,interpolation='none',
         extent=[o2,o2+d2*(n2-1),o1+d1*(n1-1),o1], **args)
        plt.xlabel(pylabel)
        plt.ylabel(pxlabel)
    else:
        datar = numpy.zeros_like(data)
        for itrace in range(0,n2):
            datar[itrace,:] = data[n2-itrace-1,:]
        plt.imshow(datar, cmap=pcmap, aspect=paspect,interpolation='none',
         extent=[o1,o1+d1*(n1-1),o2,o2+d2*(n2-1)], **args)
        plt.xlabel(pxlabel)
        plt.ylabel(pylabel)
    plt.title(ptitle)
    if pcolorbar == 'y':
        plt.colorbar()


# do a transparency plot

elif plot == 'transparent':
    if ptranspose == 'y':
        datat = numpy.transpose(data)
        datat2 = numpy.transpose(data2)
        plt.imshow(datat2,alpha=palpha2,cmap=pcmap2, interpolation='none',
         aspect=paspect,extent=[o2,o2+d2*(n2-1),o1+d1*(n1-1),o1], **args2)
        plt.imshow(datat,alpha=palpha1,cmap=pcmap, interpolation='none',
         aspect=paspect,extent=[o2,o2+d2*(n2-1),o1+d1*(n1-1),o1], **args)
        plt.xlabel(pylabel)
        plt.ylabel(pxlabel)
        plt.title(ptitle)
        plt.xlabel(pylabel)
        plt.ylabel(pxlabel)
        if pcolorbar == 'y':
            plt.colorbar()
    else:
        datar = numpy.zeros_like(data)
        data2in = numpy.reshape(data2,(n2,n1))
        for itrace in range(0,n2):
            datar[itrace,:] = data2in[n2-itrace-1,:]
        plt.imshow(datar,alpha=palpha2,cmap=pcmap2, interpolation='none',
         aspect=paspect,extent=[o1,o1+d1*(n1-1),o2,o2+d2*(n2-1)], **args2)
        datain = numpy.reshape(data,(n2,n1))
        for itrace in range(0,n2):
            datar[itrace,:] = data[n2-itrace-1,:]
        plt.imshow(datar,alpha=palpha1,cmap=pcmap, interpolation='none',
         aspect=paspect,extent=[o1,o1+d1*(n1-1),o2,o2+d2*(n2-1)], **args)
        plt.title(ptitle)
        plt.xlabel(pxlabel)
        plt.ylabel(pylabel)
        if pcolorbar == 'y':
            plt.colorbar()

else:
    sys.stderr.write('Unrecognized plotting function "%s" \n\n' % plot)
    sys.exit(2)

# check if standard output
if sys.stdout.isatty():
    plt.show()
else:
    if sys.version_info[0] >= 3:
        if  pdpi == None:
            plt.savefig(sys.stdout.buffer,format=pformat)
        else:
            plt.savefig(sys.stdout.buffer,format=pformat,dpi=pdpi)
    else:
        if  pdpi == None:
            plt.savefig(sys.stdout,format=pformat)
        else:
            plt.savefig(sys.stdout,format=pformat,dpi=pdpi)


sys.exit(0)
