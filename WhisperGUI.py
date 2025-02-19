import FreeSimpleGUI as sg
import subprocess

def main():
    # Define the window's contents
    layout = [
                [sg.Text("Select the media file (ensure file path does not have spaces)")],
                [sg.Input(key='-INPUT-'), sg.Button('Browse')],
                [sg.Text("Select the output folder (ensure file path does not have spaces)")],
                [sg.Input(key='-DEST-'), sg.Button('Folder')],
                [sg.Text("Select Whisper model (larger = more accurate results but longer processing time)")],
                [sg.Combo(['tiny', 'small', 'medium', 'large'], default_value='small', key='-MODEL-')],
                [sg.Text("Select language (if none selected, Whisper will detect language from first 30 seconds)")],
                [sg.Combo(['', 'English', 'Spanish', 'Korean'], default_value='', key='-LANG-')],
                [sg.Text("Transcribe to same language or translate to English (default is transcribe)")],
                [sg.Combo(['transcribe', 'translate'], default_value='transcribe', key='-TASK-')],
                [sg.Button(('Run Whisper'), key='-RUN-', visible=False)],
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
            model = values['-MODEL-']
            outdir = values['-DEST-']
            language = values['-LANG-']
            task = values['-TASK-']
            if language != "":
                command = "whisper {} --model {} --output_dir {}/ --language {} --task {}".format(mediafile, model, outdir, language, task)
            else:
                command = "whisper {} --model {} --output_dir {}/ --task {}".format(mediafile, model, outdir, task)
    # Do the thing
            window['-OUTPUT-'].update(visible=True)
            window['-OUTPUT-'].update("Running Whisper, please wait...")
            window['-TEST-'].print('File to process: ' + mediafile)
            window['-TEST-'].print('Running command: \n' + command)
            window['-TEST-'].print('Processing, please wait...')
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            window['-TEST-'].update(result)

    window.close()

if __name__ == '__main__':
    main()
