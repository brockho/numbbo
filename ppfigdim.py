#! /usr/bin/env python

# Creates ERTs and convergence figures for BBOB post-processing.

import os
import sys
import matplotlib.pyplot as plt
import numpy
from pdb import set_trace
from bbob_pproc import bootstrap

#maxEvalsFactor = 1e6

#colors = ('k', 'g', 'c', 'b', 'y', 'm', 'r', 'g', 'b', 'c', 'r', 'm')  # should not be too short
colors = ('k', 'b', 'c', 'g', 'y', 'm', 'r', 'k', 'k', 'c', 'r', 'm')  # sort of rainbow style
# should correspond with the colors in pprldistr.

#Get benchmark short infos.
funInfos = {}
isBenchmarkinfosFound = True
#infofile = os.path.join(os.path.split(__file__)[0], '..', '..',
                        #'benchmarkshortinfos.txt')
infofile = os.path.join(os.path.split(__file__)[0], 'benchmarkshortinfos.txt')

try:
    f = open(infofile,'r')
    for line in f:
        if len(line) == 0 or line.startswith('%') or line.isspace() :
            continue
        funcId, funcInfo = line[0:-1].split(None,1)
        funInfos[int(funcId)] = funcId + ' ' + funcInfo
    f.close()
except IOError, (errno, strerror):
    print "I/O error(%s): %s" % (errno, strerror)
    isBenchmarkinfosFound = False
    print 'Could not find file', infofile, \
          'Titles in scaling figures will not be displayed.'

def customizeFigure(figHandle, figureName = None, title='',
                    fileFormat=('png', 'eps'), labels=None,
                    scale=('linear','linear'), legend=True,
                    locLegend='best', verbose=True):
    """ Customize a figure by adding a legend, axis label, etc. At the
        end the figure is saved.

        Inputs:
        figHandle - handle to existing figure
        figureName - name of the output figure

        Optional Inputs:
        fileFormat - list of formats of output files
        labels - list with xlabel and ylabel
        scale - scale for x-axis and y-axis
        legend - show legend
        locLegend - location of legend

    """

    # Input checking

    # Get axis handle and set scale for each axis
    axisHandle = figHandle.gca()
    axisHandle.set_xscale(scale[0])
    axisHandle.set_yscale(scale[1])

    # Annotate figure
    if labels is not None: #Couldn't it be ''?
        axisHandle.set_xlabel(labels[0])
        axisHandle.set_ylabel(labels[1])

    # Grid options
    axisHandle.grid('True')
    #ylim_org = axisHandle.get_ylim()
    #set_trace()
    ymin, ymax = plt.ylim()

    # linear and quadratic "grid"
    plt.plot((2,200), (1,1e2), 'k:')    # TODO: this should be done before the real lines are plotted? 
    plt.plot((2,200), (1,1e4), 'k:')
    plt.plot((2,200), (1e3,1e5), 'k:')  
    plt.plot((2,200), (1e3,1e7), 'k:')
    plt.plot((2,200), (1e6,1e8), 'k:')  
    plt.plot((2,200), (1e6,1e10), 'k:')

    # axes limites
    plt.xlim(1.8, 45)                # TODO should become input arg?
    #set_trace()
    plt.ylim(10**-0.2, ymax)
    #plt.ylim(10**-0.2, ylim_org[1])

    # ticks on axes
    #axisHandle.invert_xaxis()
    dimticklist = (2, 3, 4, 5, 10, 20, 40)  # TODO: should become input arg at some point? 
    dimannlist = (2, 3, '', 5, 10, 20, 40)  # TODO: should become input arg at some point? 
    # TODO: All these should depend on one given input (xlim, ylim)

    axisHandle.set_xticks(dimticklist)
    axisHandle.set_xticklabels([str(n) for n in dimannlist])

    tmp = axisHandle.get_yticks()
    tmp2 = []
    for i in tmp:
        tmp2.append('%d' % round(numpy.log10(i)))
    axisHandle.set_yticklabels(tmp2)

    # Legend
    if legend:
        plt.legend(loc=locLegend)
    axisHandle.set_title(title)

    # Save figure
    if not (figureName is None or fileFormat is None):
        if isinstance(fileFormat, basestring):
            plt.savefig(figureName + '.' + fileFormat, dpi = 300,
                        format = entry)
            if verbose:
                print 'Wrote figure in %s.' %(figureName + '.' + fileFormat)
        else:
            if not isinstance(fileFormat, basestring):
                for entry in fileFormat:
                    plt.savefig(figureName + '.' + entry, dpi = 300,
                                format = entry)
                    if verbose:
                        print 'Wrote figure in %s.' %(figureName + '.' + entry)

    # TODO:    *much more options available (styles, colors, markers ...)


def generateData(indexEntry, targetFuncValue):
    """Returns data to be plotted."""
    # TODO: describe the data which are returned

    res = []
    data = []
    for i in indexEntry.hData:
        if i[0] <= targetFuncValue:
            tmp = []
            data = i.copy()
            for j in range(1, indexEntry.nbRuns()+1):
                if data[j + indexEntry.nbRuns()] <= i[0]:
                    tmp.append(True)
                else:
                    tmp.append(False)
                    data[j] = indexEntry.vData[-1, j]
            res.extend(bootstrap.sp(data[1:indexEntry.nbRuns()+1],
                                    issuccessful=tmp, allowinf=False))
            res.append(res[0] * max(res[2], 1)) #Sum(FE)
            res.append(bootstrap.prctile(data[1:indexEntry.nbRuns()+1], 50)[0])
            break

    # if targetFuncValue was not reached
    if not res and len(indexEntry.vData) > 0:
        #try:
            #while i[0] <= maxEvalsFactor * indexEntry.dim:
                #i = it.next()
        #except StopIteration:
            #pass
        i = indexEntry.vData[-1]
        res.extend(bootstrap.sp(i[1:indexEntry.nbRuns() + 1],
                                issuccessful=[False]*indexEntry.nbRuns(),
                                allowinf=False))
        res.append(res[0] * max(res[2], 1)) #Sum(FE)
        res.append(bootstrap.prctile(i[1:indexEntry.nbRuns() + 1], 50)[0])

    return numpy.array(res)


def main(indexEntries, _valuesOfInterest, outputdir, verbose=True):
    """From a list of IndexEntry, returns a convergence and ENFEs figure vs dim

    """

    plt.rc("axes", labelsize=20, titlesize=24)
    plt.rc("xtick", labelsize=20)
    plt.rc("ytick", labelsize=20)
    plt.rc("font", size=20)
    plt.rc("legend", fontsize=20)

    dictFunc = indexEntries.dictByFunc()

    for func in dictFunc:
        dictFunc[func] = dictFunc[func].dictByDim()
        filename = os.path.join(outputdir,'ppdata_f%d' % (func))
        fig = plt.figure()
        #legend = []
        line = []
        valuesOfInterest = list(j[func] for j in _valuesOfInterest)
        valuesOfInterest.sort(reverse=True)
        for i in range(len(valuesOfInterest)):
            #data = []
            succ = []
            unsucc = []
            displaynumber = []
            data = []
            #Collect data that have the same function and different dimension.
            for dim in sorted(dictFunc[func]):
                #set_trace()
                tmp = generateData(dictFunc[func][dim][0],
                                   valuesOfInterest[i])
                #data.append(numpy.append(dim, tmp))
                if tmp[2] > 0: #Number of success is larger than 0
                    succ.append(numpy.append(dim, tmp))
                    if tmp[2] < dictFunc[func][dim][0].nbRuns():
                        displaynumber.append((dim, tmp[0], tmp[2]))
                else:
                    unsucc.append(numpy.append(dim, tmp))

            if succ:
                tmp = numpy.vstack(succ)
                #ERT
                plt.plot(tmp[:, 0], tmp[:,1], figure=fig, color=colors[i],
                         marker='o', markersize=20)
                #median
                plt.plot(tmp[:, 0], tmp[:,-1], figure=fig, color=colors[i],
                         linestyle='', marker='+', markersize=30,
                         markeredgewidth=5)

            # To have the legend displayed whatever happens with the data.
            plt.plot([], [], color=colors[i],
                     label=' %+d' % (numpy.log10(valuesOfInterest[i])))

        #Only for the last target function value...
        if unsucc:
            tmp = numpy.vstack(unsucc)
            plt.plot(tmp[:, 0], tmp[:, 1], figure=fig, color=colors[i],
                     marker='x', markersize=20)

        if displaynumber: #displayed only for the smallest valuesOfInterest
            a = fig.gca()
            for j in displaynumber:
                plt.text(j[0], j[1]*1.85, "%.0f" % j[2], axes=a,
                         horizontalalignment="center",
                         verticalalignment="bottom")

        if isBenchmarkinfosFound:
            title = funInfos[func]
        else:
            title = ''

        legend = func in (1, 24, 101, 130)

        customizeFigure(fig, filename, title=title, legend=legend,
                        fileFormat=('eps','png'), labels=['', ''],
                        scale=['log','log'], verbose=verbose)

        plt.close(fig)

    plt.rcdefaults()

    # TODO: make a user define what color or line style
