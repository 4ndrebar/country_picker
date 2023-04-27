import json
import pickle as pkl
import random as rd
import io, os ,time
import PySimpleGUI as sg
from PIL import ImageTk, Image
import numpy as np
from playsound import playsound
import multiprocessing
from playsound import playsound


def alphano(img, alpha):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[3] != 0:
            newData.append((item[0], item[1], item[2], alpha))
        else:
            newData.append(item)
    img.putdata(newData)
    return img


def title_bar(title, text_color, background_color):
    """
    Creates a "row" that can be added to a layout. This row looks like a titlebar
    :param title: The "title" to show in the titlebar
    :type title: str
    :param text_color: Text color for titlebar
    :type text_color: str
    :param background_color: Background color for titlebar
    :type background_color: str
    :return: A list of elements (i.e. a "row" for a layout)
    :rtype: List[sg.Element]
    """
    bc = background_color
    tc = text_color
    font = 'Helvetica 25'
    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0), background_color=bc),
            sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, font=font, key='-MINIMIZE-'), sg.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]], element_justification='r', key='-C-', grab=True,
                   pad=(0, 0), background_color=bc)]

if __name__ == "__main__":

    p = multiprocessing.Process(target=playsound, args=("song.mp3",))
    p.start()   
    os.chdir("./data")
    REGION_PROBABILITY = 1/5


    with open('codes.json') as json_file:
        data = json.load(json_file)
        regions = os.listdir("regioni")
        background_layout = [title_bar("La prossima cena Et(n)ica", sg.theme_text_color(
        ), sg.theme_background_color()), [sg.Image(r'map.png')]]
        window_background = sg.Window('Background', background_layout, no_titlebar=True, finalize=True, margins=(
            0, 0), element_padding=(0, 0), right_click_menu=[[''], ['Exit', ]])

        # expand the titlebar's rightmost column so that it resizes correctly
        window_background['-C-'].expand(True, False, False)

        text = "Esci la nazione"
        layout = [
            [sg.Image(size=(256, 192), key='-IMAGE-'), ],
            [sg.Text(font=('SFCompact', 50), key='-TEXT1-',
                    text_color='white', justification='center'), ],
            [
                sg.Button(text),
            ],
        ]
        # Create the window
        window = sg.Window("La prossima cena Et(n)ica", layout, element_justification='c', finalize=True,
                        keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)


    # Create an event loop
    while True:
        window, event, values = sg.read_all_windows()
        print(event, values)
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break  
        elif event is None or event == 'Cancel' or event == 'Exit':
            print(f'closing window = {window.Title}')
            break
        elif event == text:
            window.find_element('-TEXT1-').Update('')
            random_flag = rd.random()
            if random_flag <= REGION_PROBABILITY:
                region = rd.choice(regions)
                flagname = "regioni/"+region
                country_name = region[:-4] 
            else:
                country = rd.choice(list(data.keys()))
                if country[:2]=="us":
                    flagname = "countries/us.png"
                else:
                    flagname = "countries/"+country + ".png"
                country_name = data[country]
            print(country_name)
            if os.path.exists(flagname):
                for alpha in range(0, 255, 5):
                    bio = io.BytesIO()
                    im = Image.open(flagname)
                    im = alphano(im, alpha)
                    im.save(bio, format="PNG")
                    # source = flagname)#)
                    window["-IMAGE-"].update(data=bio.getvalue())
                    window.refresh()
                window['-TEXT1-'].update(country_name)
                window.ElementJustification = "c"
    p.terminate()
    window.close()
    window_background.close()
