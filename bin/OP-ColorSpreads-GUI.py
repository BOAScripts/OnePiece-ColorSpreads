#!/usr/bin/env python3
# ==IMPORTS ==
import PySimpleGUI as sg
import os.path
import requests
from bs4 import BeautifulSoup
import webbrowser

# == THEME ==
sg.theme("DarkTeal4")
font = ("Helvitica", 12)
url_font = ("Helvitica", 12,"underline")
header_font = ("Helvitica", 12, "bold")

sg.set_options(font=font)


# == VARS ==
app_ver = "OnePiece-ColorSpreads v0.1.0"
gh_url = "https://github.com/BOAScripts/OnePiece-ColorSpreads"
baseUrl = "https://onepiece.fandom.com/wiki/Category:Color_Spreads"
pMaxCounter = 0
retry=False
error=False
icon=b'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'

# == FUNCTIONS ==
def GetImgsInPath(path):
    imgs = []
    try:
        for item in os.listdir(path):
            if (os.path.isfile(f"{path}/{item}")) and ((item.endswith(".png")) or (item.endswith(".jpg")) or (item.endswith(".jpeg"))):
                imgs.append(item)
    except:
        pass
    return imgs

def DownloadImg(session, url, name, path):
    '''
    Download the content of a get request.
    '''
    r = session.get(url)
    with open(path + "/" + name, 'wb') as f:
        f.write(r.content)

# == LAYOUTS == 
about_layout = [
    [sg.Text(f"{app_ver}")],
    [sg.Text(f"{gh_url}",key='-GITHUB LINK-',font=url_font, enable_events=True)]
]

folder_layout = [
    [   
        sg.Text("Select destination folder:"),
        sg.Push(),
        sg.FolderBrowse("1.Browse",size=(25,1),target=(1, 0)),
    ],
    [sg.In(default_text="-- No folder selected --",key="-DISPLAYFOLDER-",enable_events = True, readonly=True, expand_x=True,justification="c",disabled_readonly_background_color=sg.theme_input_background_color(),disabled_readonly_text_color=sg.theme_input_text_color())],
    [
        sg.StatusBar("",key="-LENIMGS-",expand_x=True,justification="c",font=header_font),
        sg.Text(": Number of images in selected folder")
    ]
]

test_col_left = [
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Button("2.Test",key="-TEST-",size=(15,1),disabled=True)],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Push()],
    [sg.Button("3.Download",key="-DOWNLOAD-",size=(15,1),disabled=True)],
]

test_col_right= [
    [
        sg.StatusBar("",key="-BASEURLSTATUS-",expand_x=True,font=header_font),
        sg.Text(": HTTP Status code")
    ],
    [
        sg.StatusBar("",key="-TOTALREMOTEIMGS-",expand_x=True,font=header_font),
        sg.Text(": Total of remote images")
    ],
    [
        sg.StatusBar("",key="-TOTALIMGDL-",expand_x=True,font=header_font),
        sg.Text(": Images to download",tooltip="Number of remote image names that are not present in selected folder")
    ],
    [sg.Text("Download progress:")],
    [sg.ProgressBar(max_value=pMaxCounter, orientation="h", key="-PBAR-",size=(22,12),border_width=4,expand_x=True)]
]

download_layout = [
    [sg.Push(), sg.Text(f"{baseUrl}", key="-BASEURL LINK-", font=url_font, enable_events=True), sg.Push()],
    [sg.HorizontalSeparator()],
    [
        sg.Push(),
        sg.Column(test_col_left),
        sg.Push(),
        sg.Column(test_col_right,expand_x=True),
        
    ],
    [sg.HorizontalSeparator()],
    [
        sg.StatusBar("         -- No results yet --         ",key="-IMGRESULT-",expand_x=True,justification="c"),
    ]
]

layout = [
    [sg.VPush()],
    [sg.Frame("About", about_layout,expand_x=True, title_location="n",font=header_font,element_justification="c")],
    [sg.Frame("Folder Selection", folder_layout, expand_x=True, title_location="n",font=header_font)],
    [sg.Frame("Download", download_layout, expand_x=True, title_location="n",font=header_font)],
    [sg.VPush()],
    
]

# == ZHU-LI, DO THE THING! == 
# request session initiation
s = requests.Session()

# window instantiation 
window = sg.Window("OP-ColorSpreads-GUI",layout,icon=icon,finalize=True)
# binding to change cursor on hover for urls
window['-GITHUB LINK-'].set_cursor('Hand1')
window['-BASEURL LINK-'].set_cursor('Hand1')

# window loop
while True:
    event, values = window.Read()
    if event == sg.WINDOW_CLOSED:
        break

    elif event == "-DISPLAYFOLDER-":
        folderPath = values["-DISPLAYFOLDER-"]
        localImgs = GetImgsInPath(folderPath)
        window["-LENIMGS-"].update(f"{len(localImgs)}")
        window["-TEST-"].update(disabled=False)

    elif event == "-TEST-":
        # reset progress counters
        pMaxCounter = 0
        pCounter=0
        # re-scan local directory if Download already pressed
        if retry:
            localImgs = GetImgsInPath(folderPath)
            window["-LENIMGS-"].update(f"{len(localImgs)}")
        # 1. Base URL
        try:
            r = s.get(baseUrl)
            window["-BASEURLSTATUS-"].update(f"{r.status_code}")
        except Exception as e:
            window["-BASEURLSTATUS-"].update(f"!Err")
        # 2. Find all images in base URL
        try:
            remoteImgs = []
            soup = BeautifulSoup(r.text, 'html.parser')
            lis = (soup.find('ul',{"class": "category-page__members-for-char"})).find_all('li')
            for li in lis:
                imgSrc = li.find('img')['src']
                imgUrl = imgSrc.split("/revision/")[0]
                imgName = imgUrl.split("/")[-1]
                remoteImgs.append({"name":imgName,"url":imgUrl})
            window["-TOTALREMOTEIMGS-"].update(f"{len(remoteImgs)}")
            # 2.1 Find total of images to download
            for img in remoteImgs:
                if img["name"] not in localImgs:
                    pMaxCounter += 1
            window["-PBAR-"].update(current_count=0, max=pMaxCounter)
            window["-TOTALIMGDL-"].update(f"{pMaxCounter}")
        except Exception as e:
            error = True
            window["-TOTALREMOTEIMGS-"].update(f"!Err")
            window["-TOTALIMGDL-"].update("!Err")

        # Enable Download button
        if pMaxCounter > 0:
            window["-DOWNLOAD-"].update(disabled=False)
        else:
            window["-IMGRESULT-"].update("Selected folder up-to-date")
        # Print error
        if error:
            window["-IMGRESULT-"].update("!! Error connecting to website !!")
        
    elif event == "-DOWNLOAD-":
        # Disable download button when downloading
        window["-DOWNLOAD-"].update(disabled=True)
        # Download and update progress bar
        for img in remoteImgs:
            if img["name"] not in localImgs:
                try:
                    # print(f"{img}")
                    DownloadImg(s, img["url"], img["name"], folderPath)
                    pCounter += 1
                    window["-PBAR-"].update(pCounter)
                    window["-IMGRESULT-"].update(f"Downloading {pCounter}/{pMaxCounter} ...")
                except Exception as e:
                    window["-IMGRESULT-"].update(f'error downloading {img["name"]}: {e}')
        window["-IMGRESULT-"].update(f'Downloaded {pCounter} images')
        retry=True

    elif event =="-GITHUB LINK-":
        webbrowser.open_new_tab(f"{gh_url}")
    
    elif event =="-BASEURL LINK-":
        webbrowser.open_new_tab(f"{baseUrl}")
        
    
window.close()
