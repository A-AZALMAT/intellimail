SET PYEXOSEU_ENV_NAME=intellimail_env
SET REPO=intellimail
SET TASK_NAME=IntelliMailAutoLaunch

call micromamba --version
IF %ERRORLEVEL% == 0 (GOTO HAS_MICROMAMBA) ELSE (GOTO HAS_NOT_MICROMAMBA)

:HAS_MICROMAMBA
micromamba env list | findstr / C:\Users\%USERNAME%\AppData\Roaming\mamba\envs\%PYEXOSEU_ENV_NAME% > nul
IF %ERRORLEVEL% == 0 (GOTO EXISTINGENV) ELSE (GOTO NONEXISTINGENV)

:HAS_NOT_MICROMAMBA
::call C:\\Users\\%USERNAME%\\bin\\envinstall\\envinstall.bat micromamba memurai uv git
ECHO Y | powershell -ExecutionPolicy Bypass -Command "Invoke-Expression ((Invoke-WebRequest -Uri 'https://micro.mamba.pm/install.ps1' -UseBasicParsing).Content)"
call micromamba shell init
GOTO NONEXISTINGENV

:EXISTINGENV
ECHO "%PYEXOSEU_ENV_NAME% Environment already installed"
call micromamba run -n %PYEXOSEU_ENV_NAME% pip install --upgrade pip uv
call micromamba run -n %PYEXOSEU_ENV_NAME% uv pip install -r requirements.txt
GOTO END

:NONEXISTINGENV
ECHO "%PYEXOSEU_ENV_NAME% Environment not installed" 
call micromamba create -yn %PYEXOSEU_ENV_NAME% python==3.12.8
call micromamba run -n %PYEXOSEU_ENV_NAME% pip install --upgrade pip uv
call micromamba run -n %PYEXOSEU_ENV_NAME% uv pip install -r requirements.txt
GOTO END

:END
ECHO "Successful refreshed env"

ECHO "install git"
call git --version
IF %ERRORLEVEL% == 0 (GOTO HAS_GIT) ELSE (GOTO HAS_NOT_GIT)
:HAS_GIT
ECHO "Git is already installed." 
:HAS_NOT_GIT
ECHO "Git is not installed. Installing Git..."
:: Download and install Git
start /wait https://git-scm.com/download/win
ECHO "Git installed successfully!"
:END
ECHO "Successful refreshed Git"

:: Clone the repository
ECHO "Cloning the repository..."
cd /d C:\Users\%USERNAME%\
git clone https://github.com/A-AZALMAT/intellimail.git
ECHO "Repository cloned successfully!"

:: Create scheduled task to launch IntelliMail at logon
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
IF %ERRORLEVEL% == 0 (GOTO HAS_SCHEDULER) ELSE (GOTO HAS_NOT_SCHEDULER)
:HAS_SCHEDULER
ECHO "Task %TASK_NAME% already exists. Skipping registration."
:HAS_NOT_SCHEDULER
ECHO "Registering Windows Task Scheduler for auto-launch on logon..."
schtasks /create /tn "%TASK_NAME%" /tr "\"C:\Users\%USERNAME%\%REPO%\run_intellimail.bat\"" /sc onlogon /rl HIGHEST /f
:END

:: Run the Streamlit app
ECHO "Launching IntelliMail..."
start C:\Users\%USERNAME%\%REPO%\run_intellimail.bat


pause