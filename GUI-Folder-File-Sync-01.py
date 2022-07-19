'''
Ref:
https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function
https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
https://pypi.org/project/dirsync/
https://www.instructables.com/Syncing-Folders-With-Python/
https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-printing-34-print-to-multiline-element
https://www.programcreek.com/python/example/115993/PySimpleGUI.Multiline
'''
#python 3.10.4
import PySimpleGUI as sg #ver 4.60.1
import os
from dirsync import sync #ver 2.2.5

layoutFileFolderInput = [
    [sg.Button('Folder To Sync')],
    [sg.MLine(key='-folderfileslistInput-'+sg.WRITE_ONLY_KEY, size=(60,30))],    
]

layoutFileFolderOutput = [
    [sg.Button('Destination Folder')],
    [sg.MLine(key='-folderfileslistOutput-'+sg.WRITE_ONLY_KEY, size=(60,30))],    
]

layoutFileFolderSync = [
    [sg.Frame('Folder Path to Sync',layoutFileFolderInput), sg.Button('Sync',button_color= 'red' ),
    sg.Frame('Synchronized Folder Path to',layoutFileFolderOutput)]    
]

window = sg.Window('Sync Folder and File', layoutFileFolderSync)

while True:
    event, values = window.read()
         
    if event in (sg.WIN_CLOSED, 'Exit'):        
        window.close()
        break

    #Choose folder to sync
    if event == 'Folder To Sync':
        # clear old folder and file list of syncronized folder in multiline after sync
        window['-folderfileslistInput-'+sg.WRITE_ONLY_KEY].update('')

        # Get of folder to sync path
        filefolderinput = sg.PopupGetFolder('Select Folder to Sync', no_window=True)

        # print path of folder to sync
        window['-folderfileslistInput-'+sg.WRITE_ONLY_KEY].print('Path of Folder to Sync: \n'+ filefolderinput +'\n')

        # print folder and file list in folder to sync
        # traverse root directory, and list directories as dirs and files as files
        #for root, dirs, files in os.walk("."):
        for root, dirs, files in os.walk(filefolderinput):
            path = root.split(os.sep)
            window['-folderfileslistInput-'+
            sg.WRITE_ONLY_KEY].print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                window['-folderfileslistInput-'+sg.WRITE_ONLY_KEY].print(len(path) * '---', file)
    
    #Choose destination folder
    if event == 'Destination Folder':
        # clear old folder and file list of syncronized folder in multiline after sync
        window['-folderfileslistOutput-'+sg.WRITE_ONLY_KEY].update('')

        # Get of destination folder path
        filefolderoutput = sg.PopupGetFolder('Select Syncronized folder', no_window=True)

        # print path of destination folder
        window['-folderfileslistOutput-'+sg.WRITE_ONLY_KEY].print('Path of Syncronized Folder: \n'+ 
        filefolderoutput +'\n')

        # print folder and file list in destination folder before sync
        # traverse root directory, and list directories as dirs and files as files
        #for root, dirs, files in os.walk("."):
        for root, dirs, files in os.walk(filefolderoutput):
            path = root.split(os.sep)
            window['-folderfileslistOutput-'+
            sg.WRITE_ONLY_KEY].print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                window['-folderfileslistOutput-'+sg.WRITE_ONLY_KEY].print(len(path) * '---', file)

    #Do sync
    if event == 'Sync':
        
        #logger for sync info
        Syncloggerpathinfo = 'Sync from' + '\n' + filefolderinput + '\n' + 'to' + '\n' + filefolderoutput + '\n'
        Syncloggerinfo = sg.eprint(Syncloggerpathinfo, size = (40,10), do_not_reroute_stdout=False,
        no_titlebar = True)

        # Doing sync
        sync(filefolderinput, filefolderoutput, 'sync', logger = Syncloggerinfo)
        
        # clear old folder and file list of syncronized folder in multiline after sync
        window['-folderfileslistOutput-'+sg.WRITE_ONLY_KEY].update('')

        # print path of syncronized folder
        window['-folderfileslistOutput-'+sg.WRITE_ONLY_KEY].print('Path of Syncronized Folder: \n'+ 
        filefolderoutput +'\n')

        # update folder and file list in syncronized folder after sync
        # traverse root directory, and list directories as dirs and files as files
        #for root, dirs, files in os.walk("."):
        for root, dirs, files in os.walk(filefolderoutput):
            path = root.split(os.sep)
            window['-folderfileslistOutput-'+
            sg.WRITE_ONLY_KEY].print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                window['-folderfileslistOutput-'+sg.WRITE_ONLY_KEY].print(len(path) * '---', file)
        
    

        
