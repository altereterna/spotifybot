@echo off
SETLOCAL

REM Check if Python is installed and display version
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed.
) ELSE (
    python --version
)

REM Create a virtual environment if it doesn't exist
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip (suppressing output)
echo Upgrading pip...
pip install --upgrade pip >nul 2>&1

REM Install required dependencies (suppressing output)
echo Installing dependencies...
pip install spotipy twitchio requests psutil tk >nul 2>&1

REM Run the Python script
echo Starting config_ui.py...
python config_ui.py

REM Check if the script exited with an error
IF %ERRORLEVEL% NEQ 0 (
    echo An error occurred while running config_ui.py.
)

REM Keep the terminal open until 'x' is pressed
echo Press 'x' to close the terminal.

REM Loop to wait for 'x' key press without displaying characters
:wait_for_x
set "key="
for /F "delims=" %%A in ('xcopy /W /L /C /Y nul "%~f0" 2^>nul') do (
    set "key=%%A"
    if /I "!key:~-1!"=="X" (
        goto :EOF
    )
)
goto wait_for_x

ENDLOCAL
