import PySimpleGUI as sg
import subprocess

def main():
    # Define the window's contents
    layout = [
                [sg.Text("Select the media file")],
                [sg.Input(key='-INPUT-'), sg.Button('Browse')],
                [sg.Text("Select the output folder")],
                [sg.Input(key='-DEST-'), sg.Button('Folder')],
                [sg.Button(('Go'), key='-RUN-', visible=False)],
                [sg.Text(size=(40,1), key='-OUTPUT-', visible=False)],
                [sg.Multiline(size=(50, 10), echo_stdout_stderr=True, key='-TEST-')],
                [sg.Button('Quit')]
                ]

    # Make the window
    window = sg.Window('Whisper GUI', layout)

    # Make the event loop that does the things
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        if event == 'Browse':
            file_chosen = sg.popup_get_file('', no_window=True)
            if file_chosen:
                window['-INPUT-'].update(file_chosen)
        if event == 'Folder':
            folder_chosen = sg.popup_get_folder('', no_window=True)
            if folder_chosen:
                window['-DEST-'].update(folder_chosen)
                window['-RUN-'].update(visible=True)
        if event == '-RUN-':
    # Define the whisper command
            mediafile = values['-INPUT-']
            outdir = values['-DEST-']
            command = "whisper {} --model small.en --output_dir {}/ --task transcribe".format(mediafile, outdir)
    # Do the thing
            window['-OUTPUT-'].update("Let's run Whisper!")
            window['-OUTPUT-'].update(visible=True)
            window['-TEST-'].print('File to process: ' + mediafile)
            window['-TEST-'].print('Running command: \n' + command)
            window['-TEST-'].print('Processing, please wait...')
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            window['-TEST-'].update(result)

    window.close()

if __name__ == '__main__':
    main()
