SET PYEXOSEU_ENV_NAME=intellimail_env
cd /d C:\Users\%USERNAME%\intellimail
call micromamba run -n %PYEXOSEU_ENV_NAME% streamlit run main.py