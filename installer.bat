SET PYEXOSEU_ENV_NAME=intellimail_env
SET REPO=intellimail
SET TASK_NAME=IntelliMailAutoLaunch

ECHO "install git"
call git --version >nul 2>&1

IF %ERRORLEVEL% == 0 (GOTO HAS_GIT) ELSE (GOTO HAS_NOT_GIT)
:HAS_GIT
ECHO "Git is already installed." 
GOTO END_GIT

:HAS_NOT_GIT
ECHO "Git is not installed. Installing Git..."
set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/Git-2.42.0-64-bit.exe
set INSTALLER=%TEMP%\Git-installer.exe
:: Download the installer using PowerShell with ExecutionPolicy Bypass
:: should be modified by envinstall
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%GIT_URL%' -OutFile '%INSTALLER%'"
:: Run the installer silently
ECHO Running Git installer...
start /wait %INSTALLER% /VERYSILENT /NORESTART
:: Clean up the installer after installation
del %INSTALLER%
ECHO Git installed successfully.
GOTO END_GIT

:END_GIT
ECHO "Successful refreshed Git"
:: Clone the repository
set "PATH=C:\Program Files\Git\cmd;%PATH%"
ECHO "Cloning the repository..."
cd /d %USERPROFILE%
:: should be modified by sgithub repo
git clone https://github.com/A-AZALMAT/intellimail.git
ECHO "Repository cloned successfully!"


call micromamba --version >nul 2>&1
IF %ERRORLEVEL% == 0 (GOTO HAS_MICROMAMBA) ELSE (GOTO HAS_NOT_MICROMAMBA)

:HAS_MICROMAMBA
micromamba env list | findstr / %USERPROFILE%\AppData\Roaming\mamba\envs\%PYEXOSEU_ENV_NAME% >nul 2>&1
IF %ERRORLEVEL% == 0 (GOTO EXISTINGENV) ELSE (GOTO NONEXISTINGENV)

:HAS_NOT_MICROMAMBA
:: should be modified by envinstall
ECHO Y | powershell -ExecutionPolicy Bypass -Command "Invoke-Expression ((Invoke-WebRequest -Uri 'https://micro.mamba.pm/install.ps1' -UseBasicParsing).Content)"
set "PATH=C:\Users\aazal\AppData\Local\micromamba\;%PATH%"
call micromamba shell init
GOTO NONEXISTINGENV

:EXISTINGENV
ECHO "%PYEXOSEU_ENV_NAME% Environment already installed"
call micromamba run -n %PYEXOSEU_ENV_NAME% pip install --upgrade pip uv
call micromamba run -n %PYEXOSEU_ENV_NAME% uv pip install -r %USERPROFILE%\%REPO%\requirements.txt
GOTO END_MAMBA

:NONEXISTINGENV
ECHO "%PYEXOSEU_ENV_NAME% Environment not installed" 
call micromamba create -yn %PYEXOSEU_ENV_NAME% python==3.12.8
call micromamba run -n %PYEXOSEU_ENV_NAME% pip install --upgrade pip uv
call micromamba run -n %PYEXOSEU_ENV_NAME% uv pip install -r %USERPROFILE%\%REPO%\requirements.txt
GOTO END_MAMBA

:END_MAMBA
ECHO "Successful refreshed env"

:: Create scheduled task to launch IntelliMail at logon
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
IF %ERRORLEVEL% == 0 (GOTO HAS_SCHEDULER) ELSE (GOTO HAS_NOT_SCHEDULER)
:HAS_SCHEDULER
ECHO "Task %TASK_NAME% already exists. Skipping registration."
GOT END_SCHEDULER
:HAS_NOT_SCHEDULER
ECHO "Registering Windows Task Scheduler for auto-launch on logon..."
schtasks /create /tn "%TASK_NAME%" /tr "\"%USERPROFILE%\%REPO%\run_intellimail.bat\"" /sc onlogon /rl LIMITED /f

GOTO END_SCHEDULER
:END_SCHEDULER

:: Run the Streamlit app
ECHO "Launching IntelliMail..."
start %USERPROFILE%\%REPO%\run_intellimail.bat


pause