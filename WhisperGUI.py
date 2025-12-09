import FreeSimpleGUI as sg
import subprocess
import os
    

def main():
    home_folder = os.path.expanduser("~")
    count = 0
    # Define the window's contents
    layout = [
                [sg.Text("Accepted file types: MOV, MP4, MP3, WAV, MXF, M4A, MPEG, FLAC")],
                [sg.Text("Single-file input: select media file (ensure file path does not have spaces)")],
                [sg.Input(key='-INPUTFILE-'), sg.Button('Browse')],
                [sg.Text("Folder input: select media folder (ensure file path does not have spaces)")],
                [sg.Input(key='-INPUTFOLDER-'), sg.Button('Media folder')],
                [sg.Text("Select the output folder (ensure file path does not have spaces)")],
                [sg.Input(key='-DEST-'), sg.Button('Destination folder')],
                [sg.Text("Select Whisper model (larger = more accurate results but longer processing time)")],
                [sg.Combo(['tiny', 'small', 'medium', 'large'], default_value='tiny', key='-MODEL-')],
                [sg.Text("Select language (if none selected, Whisper will detect language from first 30 seconds)")],
                [sg.Combo(['', 'Afrikaans', 'Albanian', 'Amharic', 'Arabic',
                           'Armenian', 'Assamese', 'Azerbaijani', 'Bashkir',
                           'Basque', 'Belarusian', 'Bengali', 'Bosnian', 'Breton',
                           'Bulgarian', 'Burmese', 'Cantonese', 'Castilian',
                           'Catalan', 'Chinese', 'Croatian', 'Czech', 'Danish',
                           'Dutch', 'English', 'Estonian', 'Faroese', 'Finnish',
                           'Flemish', 'French', 'Galician', 'Georgian', 'German',
                           'Greek', 'Gujarati', 'Haitian', 'Haitian Creole',
                           'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hungarian',
                           'Icelandic', 'Indonesian', 'Italian', 'Japanese',
                           'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Korean',
                           'Lao', 'Latin', 'Latvian', 'Letzeburgesch', 'Lingala',
                           'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy',
                           'Malay', 'Malayalam', 'Maltese', 'Mandarin', 'Maori',
                           'Marathi', 'Moldavian', 'Moldovan', 'Mongolian',
                           'Myanmar', 'Nepali', 'Norwegian', 'Nynorsk', 'Occitan',
                           'Panjabi', 'Pashto', 'Persian', 'Polish', 'Portuguese',
                           'Punjabi', 'Pushto', 'Romanian', 'Russian', 'Sanskrit',
                           'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Sinhalese',
                           'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese',
                           'Swahili', 'Swedish', 'Tagalog', 'Tajik', 'Tamil',
                           'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Turkish',
                           'Turkmen', 'Ukrainian', 'Urdu', 'Uzbek', 'Valencian',
                           'Vietnamese', 'Welsh', 'Yiddish', 'Yoruba'],
                          default_value='', key='-LANG-')],
                [sg.Text("Transcribe to same language or translate to English (default is transcribe)")],
                [sg.Combo(['transcribe', 'translate'], default_value='transcribe', key='-TASK-')],
                [sg.Text("Choose output format")],
                [sg.Radio('txt', group_id=1, key='-TXT-'), sg.Radio('vtt', group_id=1, key='-VTT-'),
                         sg.Radio('srt', group_id=1, key='-SRT-'), sg.Radio('tsv', group_id=1, key='-TSV-'),
                         sg.Radio('json', group_id=1, key='-JSON-'), sg.Radio('all', group_id=1, key='-ALL-')],
                [sg.Button(('Run Whisper'), key='-RUN-', visible=False)],
                [sg.ProgressBar(count, orientation='h', size=(20, 20), key='-PROGRESSBAR-', visible=False)],
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
            file_chosen = sg.popup_get_file('', initial_folder=home_folder, no_window=True)
            if file_chosen:
                window['-INPUTFILE-'].update(file_chosen)
        if event == 'Media folder':
            media_folder_chosen = sg.popup_get_folder('', initial_folder=home_folder, no_window=True)
            if media_folder_chosen:
                window['-INPUTFOLDER-'].update(media_folder_chosen)
        if event == 'Destination folder':
            dest_folder_chosen = sg.popup_get_folder('', initial_folder=home_folder, no_window=True)
            if dest_folder_chosen:
                window['-DEST-'].update(dest_folder_chosen)
                window['-RUN-'].update(visible=True)
                
        if event == '-RUN-' and values['-INPUTFILE-'] != '' and values['-INPUTFOLDER-'] != '':
            window['-OUTPUT-'].update(visible=True)
            window['-OUTPUT-'].update("choose input file or input folder but not both")
            
        elif event == '-RUN-' and values['-INPUTFILE-'] != '' and values['-INPUTFOLDER-'] == '':
            mediafile = values['-INPUTFILE-']
            model = values['-MODEL-']
            outdir = values['-DEST-']
            language = values['-LANG-']
            task = values['-TASK-']
            if values['-TXT-']:
                output_format = 'txt'
            elif values['-VTT-']:
                output_format = 'vtt'
            elif values['-SRT-']:
                output_format = 'srt'
            elif values['-TSV-']:
                output_format = 'tsv'
            elif values['-JSON-']:
                output_format = 'json'
            elif values['-ALL-']:
                output_format = 'all'
            else:
                output_format = 'all'
            if language != "":
                command = "whisper {} --model {} --output_dir {}/ --output_format {} --language {} --task {}".format(mediafile, model, outdir, output_format, language, task)
            else:
                command = "whisper {} --model {} --output_dir {}/ --output_format {} --task {}".format(mediafile, model, outdir, output_format, task)
            window['-OUTPUT-'].update(visible=True)
            window['-OUTPUT-'].update("Running Whisper, please wait...")
            window['-TEST-'].print('File to process: ' + mediafile)
            window['-TEST-'].print('Running command: \n' + command)
            window['-TEST-'].print('Processing, please wait...')
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            window['-TEST-'].update(result)
            window['-OUTPUT-'].update("Done!")
            
        elif event == '-RUN-' and values['-INPUTFILE-'] == '' and values['-INPUTFOLDER-'] != '':
            input_folder = values['-INPUTFOLDER-']
            model = values['-MODEL-']
            outdir = values['-DEST-']
            language = values['-LANG-']
            task = values['-TASK-']
            if values['-TXT-']:
                output_format = 'txt'
            elif values['-VTT-']:
                output_format = 'vtt'
            elif values['-SRT-']:
                output_format = 'srt'
            elif values['-TSV-']:
                output_format = 'tsv'
            elif values['-JSON-']:
                output_format = 'json'
            elif values['-ALL-']:
                output_format = 'all'
            else:
                output_format = 'all'
            window['-OUTPUT-'].update(visible=True)
            window['-OUTPUT-'].update("Running Whisper, please wait...")
            window['-PROGRESSBAR-'].update(visible=True)
            
            file_types = (".mov", ".MOV", ".mp4", ".MP4", ".mp3", ".MP3", ".wav", ".WAV", ".mxf", ".MXF", ".m4a", ".M4A", ".mpeg", ".MPEG", ".flac", ".FLAC")
            for file in os.listdir(input_folder):
                if file.endswith(file_types):
                    count += 1
            file_num = str(count)
            window['-TEST-'].print('Number of files to process: ' + file_num)
            window['-PROGRESSBAR-'].update(max=count)
            window['-PROGRESSBAR-'].update(visible=True)
            files_done = 0
            for file in os.listdir(input_folder):
                if file.endswith(file_types):
                    mediafile = os.path.join(input_folder, file)
                    window['-TEST-'].print('File to process: ' + mediafile)
                    if language != "":
                        command = "whisper {} --model {} --output_dir {}/ --output_format {} --language {} --task {}".format(mediafile, model, outdir, output_format, language, task)
                    else:
                        command = "whisper {} --model {} --output_dir {}/ --output_format {} --task {}".format(mediafile, model, outdir, output_format, task)  
                    window['-TEST-'].print('Running command: \n' + command)
                    window['-TEST-'].print('Processing, please wait...')
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    files_done += 1
                    window['-PROGRESSBAR-'].update(current_count=files_done)
                    window['-TEST-'].update(result)
            window['-OUTPUT-'].update("Done!")

            
    window.close()

if __name__ == '__main__':
    main()
