This project is a playground for experimenting with different kronos related auth systems

## Project setup

1. Clone this repo
1. Create a dedicated virtual environment
    ```bash
    ᐅ pyenv virtualenv 2.7.16 kronos-auth-test-2.7.16
    New python executable in /Users/starver/.pyenv/versions/2.7.16/envs/kronos-auth-test-2.7.16/bin/python2.7
    Also creating executable in /Users/starver/.pyenv/versions/2.7.16/envs/kronos-auth-test-2.7.16/bin/python
    Installing setuptools, pip, wheel...
    done.    
    ```
1. Create the pyenv version file at project root with name `.python-version` and contents `kronos-auth-test-2.7.16`.
1. If using PyCharm, set the project interpreter.
    1. Copy the python location given when you created the virtual env. In the above case: `/Users/starver/.pyenv/versions/2.7.16/envs/kronos-auth-test-2.7.16/bin/python`
    1. Open PyCharm preferences
    1. Type `interpreter` in the search field at top-left on the dialog
    1. Select Project Interpreter
    1. Click the settings icon (gear) at top right of the dialog and select "Add..."
    1. Check "Existing environment" and click the "..." button right of the dropdown
    1. Paste the python location copied above into the text field and click OK
1. Install dependencies
    ```
    pip install -r requirements.txt
    ```

## Google Calendar

* [Google calendar api](https://developers.google.com/calendar/)

The google calendar section (`src/gcal`) is this [Quickstart](https://developers.google.com/calendar/quickstart/python)

Visit that page, click the "ENABLE THE GOOGLE CALENDAR API" button to create your `credentials.json` file and store that file in the `private` directory at project root.
