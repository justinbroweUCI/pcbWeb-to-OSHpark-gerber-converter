import os
import zipfile

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

openOpt = {}
openOpt['defaultextension'] = '.zip'
openOpt['filetypes'] = [('PCBWeb Gerber Zip', '.zip')]
openOpt['title'] = 'Open PCBWeb Gerber Zip'

srcFilePath = filedialog.askopenfilename(**openOpt)

if not zipfile.is_zipfile(srcFilePath):
    raise Exception("Not a Zip file");

saveOpt = {}
saveOpt['defaultextension'] = '.zip'
saveOpt['filetypes'] = [('OSHPark Gerber Zip', '.zip')]
saveOpt['title'] = 'Save as OSHPark Gerber Zip'
saveOpt['initialdir'] = os.path.dirname(srcFilePath)
saveOpt['initialfile'] = os.path.basename('OSHPark.zip')

dstFilePath = filedialog.asksaveasfilename(**saveOpt)

boardName = os.path.basename(srcFilePath).split('.')[0]
correctMapping = {
    b'Top layer': '%s.GTL' % boardName,
    b'Inner layer 1': '%s.G2L' % boardName,
    b'Inner layer 2': '%s.G3L' % boardName,
    b'Bottom layer': '%s.GBL' % boardName,
    b'Top silkscreen': '%s.GTO' % boardName,
    b'Bottom silkscreen': '%s.GBO' % boardName,
    b'Top soldermask': '%s.GTS' % boardName,
    b'Bottom soldermask': '%s.GBS' % boardName,
    b'Board outline': '%s.GKO' % boardName,
    b'Plated holes Excellon file': '%s.XLN' % boardName,
    b'Non-Plated holes Excellon file': '%s.DRL' % boardName
}

currentMapping = {}
with zipfile.ZipFile(srcFilePath) as srcZip, \
     zipfile.ZipFile(dstFilePath, 'w', zipfile.ZIP_DEFLATED) as dstZip:
    allFiles = srcZip.namelist()
    if 'README.txt' not in allFiles:
        raise Exception("Not a PCBWeb Zip file (README.txt missing)");

    with srcZip.open('README.txt') as README:
        for line in README:
            contents = line.split(b'=')
            currentMapping[contents[1].strip()] = contents[0].strip().decode('utf-8')

    for key in currentMapping.keys():
        if key in correctMapping.keys() and currentMapping[key] in allFiles:
            with srcZip.open(currentMapping[key]) as fr:
                dstZip.writestr(correctMapping[key], fr.read())
            print("Converted entry '%s'"%key)
        else:
            print("Skipped entry '%s'"%key)
