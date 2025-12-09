# WhisperGUI

A graphic interface for running Whisper locally on a single file or folder of files, with options to select model, language, task, and output format.

![GUI_2025-02-20_9 18](https://github.com/user-attachments/assets/d9facbba-4a1e-443c-8ee6-f2881373f962)


## Install from source:

* Clone or download WhisperGUI repository, then navigate to the directory
    * `cd WhisperGUI`
* Create a new Python Virtual Environment for WhisperGUI
    * Unix based (Mac or Linux):
      `python3 -m venv venv`
    * Windows:
      `py -m venv venv`
* Activate virtual env
    * Unix based:
      `source ./venv/bin/activate`
    * Windows:
      (this step may need admin permissions)
      `venv\scripts\activate`
* Install Package
    * Unix based:
      `python -m pip install .`
    * Windows:
      `python -m pip install -e .`

## Launch from executable file
* Executable file is in:
    * Unix based:
      `WhisperGUI/venv/bin/WhisperGUI`
    * Windows:
      `WhisperGUI\venv\Scripts\WhisperGUI`
