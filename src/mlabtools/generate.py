#  python generate.py Sensors/SHT31V01A/SCH_PCB/SHT31V01A.kicad_pcb Sensors/SHT31V01A/SCH_PCB/SHT31V01A.sch 


import sys

import subprocess
import pcbnew
from pcbnew import FromMM, wxPoint
from pcbnew import PLOT_FORMAT_GERBER, PLOT_FORMAT_SVG, PLOT_FORMAT_PDF, PLOT_CONTROLLER, EXCELLON_WRITER
from pcbnew import F_Cu, B_Cu, B_SilkS, F_SilkS, B_Mask, F_Mask, Edge_Cuts, B_Paste, F_Paste

import kicad_netlist_reader
import csv
import sys

filename=sys.argv[1]


plotDir = "../new_CAM_PROFI/"

board = pcbnew.LoadBoard(filename)
pctl = pcbnew.PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()

popt.SetOutputDirectory(plotDir)

popt.SetPlotFrameRef(False) 
popt.SetLineWidth(FromMM(0.35))

popt.SetAutoScale(False)
popt.SetScale(1)
popt.SetMirror(False)
popt.SetUseGerberAttributes(True)
popt.SetUseGerberProtelExtensions(False)
popt.SetExcludeEdgeLayer(False);
popt.SetScale(1)
popt.SetUseAuxOrigin(True)

popt.SetSubtractMaskFromSilk(False)



plot_plan = [
    ( "F_Cu", F_Cu, "Top layer" ),
    ( "B_Cu", B_Cu, "Bottom layer" ),
    ( "F_SilkS", F_SilkS, "Silk top" ),
    ( "B_Mask", B_Mask, "Mask bottom" ),
    ( "F_Mask", F_Mask, "Mask top" ),
    ( "Edge_Cuts", Edge_Cuts, "Edges" ),
]


for layer_info in plot_plan:
    pctl.SetLayer(layer_info[1])
    pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
    pctl.PlotLayer()

    
    pctl.SetLayer(layer_info[1])
    pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_SVG, layer_info[2])
    pctl.PlotLayer()
    #subprocess.Popen(["inkscape", "-z", "--verb=FitCanvasToDrawing", "--verb=FileSave", pctl.GetPlotFileName()])
    


drlwriter = EXCELLON_WRITER( board )
drlwriter.SetMapFileFormat( PLOT_FORMAT_SVG )

mirror = False
minimalHeader = False
offset = wxPoint(0,0)

mergeNPTH = False
drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH)

metricFmt = True
drlwriter.SetFormat( metricFmt )

genDrl = True
genMap = True
drlwriter.CreateDrillandMapFilesSet( pctl.GetPlotDirName(), genDrl, genMap );



popt = pctl.GetPlotOptions()

popt.SetOutputDirectory("../DOC/new_src/")

popt.SetPlotFrameRef(False)
popt.SetLineWidth(FromMM(0.35))

popt.SetAutoScale(False)
popt.SetScale(1)
popt.SetMirror(False)
popt.SetUseGerberAttributes(True)
popt.SetExcludeEdgeLayer(False);
popt.SetScale(1)
popt.SetUseAuxOrigin(True)

popt.SetSubtractMaskFromSilk(False)


pctl.OpenPlotfile("MLABa", PLOT_FORMAT_SVG, "MLAB A")
pctl.SetLayer(F_SilkS)
pctl.PlotLayer()
pctl.SetLayer(F_Mask)
pctl.PlotLayer()
#proc = subprocess.Popen(["inkscape", "--without-gui", "--verb=FitCanvasToDrawing", "--verb=FileSave", pctl.GetPlotFileName()])
#proc = subprocess.Popen(["inkscape", "--verb=FitCanvasToDrawing", "--verb=FileSave", pctl.GetPlotFileName()])
#proc.wait()
#proc = subprocess.Popen(["convert", "-density 600", pctl.GetPlotFileName(), pctl.GetPlotFileName().replace('.svg', '.png') ])
#proc.wait()


popt.SetMirror(True)
pctl.OpenPlotfile("MLABb", PLOT_FORMAT_SVG, "MLAB A")
pctl.SetLayer(B_SilkS)
pctl.PlotLayer()
#proc = subprocess.Popen(["inkscape", "--without-gui", "--verb=FitCanvasToDrawing", "--verb=FileSave", pctl.GetPlotFileName()])
#proc = subprocess.Popen(["inkscape", "--verb=FitCanvasToDrawing", "--verb=FileSave", pctl.GetPlotFileName()])
#proc.wait()
#proc = subprocess.Popen(["inkscape", "-z -d 600", pctl.GetPlotFileName(), '-e', pctl.GetPlotFileName().replace('.svg', '.png') ])
#proc = subprocess.Popen(["convert", "-density 600", pctl.GetPlotFileName(), '-set density 1200', pctl.GetPlotFileName().replace('.svg', '.png') ])
#proc.wait()



pctl.ClosePlot()


import sqlite3
import numpy as np
import csv
conn = sqlite3.connect('example.db')
try:
    conn.execute('''DROP TABLE parts''')
except Exception, e:
    pass
conn.execute('''CREATE TABLE parts (name text, package text, value text, fingerprint text)''')
conn.commit()


filename2=sys.argv[2]

sch = open(filename2, 'r').read()
sch_parts = sch.split("$")

#print sch

for area in sch_parts:
    if area[:4] == 'Comp':
        try:
            comp = area
            comp = comp.replace('F 0', 'F_0')
            comp = comp.replace('F 1', 'F_1')
            comp = comp.replace('F 2', 'F_2')
            comp = comp.replace('F 3', 'F_3')
            comp = comp.replace('\r\n', ' ')
            comp = comp.replace('  ', ' ')
            comp = comp.replace('  ', ' ')
            comp = comp.split(' ')
            #print comp
            Cname = comp[comp.index('L')+2]
            Cvalue= comp[comp.index('F_1')+1]
            Cpackage= comp[comp.index('F_2')+1]
            print ">>", Cname, Cvalue, Cpackage
            if not "#" in Cname:
                conn.execute("INSERT INTO parts VALUES ('%s', '%s', '%s', '%s')" %(Cname, Cpackage.replace('"', ''), Cvalue.replace('"', ''), ""))
        except Exception, e:
            print e


mydt = np.dtype([ ('name', np.str_, 5), 
                 ('package', np.str_, 20),
                 ('value', np.str_, 10),
                 ('fingerprint', np.str_, 10)] )

array = conn.execute("select min(name), package, count(*), value FROM parts GROUP BY package;").fetchall()
print array

with open(pctl.GetPlotDirName()+'../../NewBOM.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    #writer.writerow("ID", "Urcovatel", "Pouzdro", "pocet", "Hodnota")
    for i, part in enumerate(array):
        print (i+1,)+part
        writer.writerow((i+1,)+part)
#array.tofile("newOut.csv", sep=';')

#print sch_parts

conn.commit()
