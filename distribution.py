import os
import shutil
import stat

from pyexo_seu.settings import (
    GIT_REPO_URL,
    PYEXOSEU_ENV_NAME,
    PACKAGE_DUMP_FOLDER,
    CMDS_FOLDER,
    LOCAL_CACHE_FOLDER,
)


class Distribution:
    REFRESH_ENV_CMD = "refresh_env.cmd"
    REFRESH_ENV_CMD_PATH = CMDS_FOLDER / REFRESH_ENV_CMD
    LOCAL_DISTRIBUTION_DUMP_FOLDER = LOCAL_CACHE_FOLDER / "local_distribution"

    @staticmethod
    def _on_rm_error(*args):
        os.chmod(args[1], stat.S_IWRITE)
        os.unlink(args[1])

    @staticmethod
    def dump_remote_git_repo():
        from git import Repo

        if os.path.exists(PACKAGE_DUMP_FOLDER):
            shutil.rmtree(PACKAGE_DUMP_FOLDER, onerror=Distribution._on_rm_error)

        Repo.clone_from(GIT_REPO_URL, PACKAGE_DUMP_FOLDER)

    @staticmethod
    def dump_local_distribution():
        if os.path.exists(Distribution.LOCAL_DISTRIBUTION_DUMP_FOLDER):
            shutil.rmtree(
                Distribution.LOCAL_DISTRIBUTION_DUMP_FOLDER,
                onerror=Distribution._on_rm_error,
            )

        shutil.copytree(PACKAGE_DUMP_FOLDER, Distribution.LOCAL_DISTRIBUTION_DUMP_FOLDER)

    @staticmethod
    def dump_env_refresher():
        cmd_str = f"""
                    call micromamba activate
                    IF %ERRORLEVEL% == 0 (GOTO HAS_MICROMAMBA) ELSE (GOTO HAS_NOT_MICROMAMBA)

                    :HAS_MICROMAMBA
	                call micromamba deactivate 
                    call micromamba activate {PYEXOSEU_ENV_NAME}
                    IF "%CONDA_PREFIX%"=="" (GOTO NONEXISTINGENV) ELSE (GOTO EXISTINGENV)

                    :HAS_NOT_MICROMAMBA
                    call C:\\Users\\%USERNAME%\\bin\\envinstall\\envinstall.bat micromamba memurai uv git
                    call micromamba shell init
                    GOTO NONEXISTINGENV

                    :EXISTINGENV
                    ECHO "{PYEXOSEU_ENV_NAME} Environment already installed"
                    call micromamba activate {PYEXOSEU_ENV_NAME}
                    python -m pip install --upgrade pip uv
                    uv pip install {PACKAGE_DUMP_FOLDER}
                    C:
                    cd "%CONDA_PREFIX%\\Lib\\site-packages\\pyexo_seu\\scripts"
                    python dump_local_distribution.py
                    GOTO END

                    :NONEXISTINGENV
                    ECHO "{PYEXOSEU_ENV_NAME} Environment not installed" 
                    call micromamba create -yn {PYEXOSEU_ENV_NAME} python==3.12.8
                    call micromamba activate {PYEXOSEU_ENV_NAME}
                    python -m pip install --upgrade pip uv
                    uv pip install {PACKAGE_DUMP_FOLDER}
                    C:
                    cd "%CONDA_PREFIX%\\Lib\\site-packages\\pyexo_seu\\scripts"
                    python dump_local_distribution.py
                    GOTO END

                    :END
                    ECHO "Successful refreshed env"
                  """

        with open(Distribution.REFRESH_ENV_CMD_PATH, "w") as f:
            f.write(cmd_str)

    @staticmethod
    def dump_jupyter_cmd():
        cmd_str = f"""
                    call micromamba activate
                    IF %ERRORLEVEL% == 0 (GOTO HAS_MICROMAMBA) ELSE (GOTO HAS_NOT_MICROMAMBA)
                    
                    :HAS_MICROMAMBA
                    GOTO CONTINUE
            
                    :HAS_NOT_MICROMAMBA
                    call C:\\Users\\%USERNAME%\\bin\\envinstall\\envinstall.bat micromamba memurai uv git
                    call micromamba shell init
                    GO TO CONTINUE
                    
                    :CONTINUE
                    call {Distribution.REFRESH_ENV_CMD_PATH}
                   call micromamba activate {PYEXOSEU_ENV_NAME}
                    C:
                    cd "%CONDA_PREFIX%\\Lib\\site-packages\\pyexo_seu\\notebooks"
                    jupyter notebook
                  """

        (CMDS_FOLDER / "notebooks.cmd").write_text(cmd_str)

    @staticmethod
    def dump_webapp_cmd():
        cmd_str = f"""
                    call micromamba activate
                    IF %ERRORLEVEL% == 0 (GOTO HAS_MICROMAMBA) ELSE (GOTO HAS_NOT_MICROMAMBA)

                    :HAS_MICROMAMBA
                    GOTO CONTINUE

                    :HAS_NOT_MICROMAMBA
                    call C:\\Users\\%USERNAME%\\bin\\envinstall\\envinstall.bat micromamba memurai uv git
                    call micromamba shell init
                    GO TO CONTINUE

                    :CONTINUE
                    call {Distribution.REFRESH_ENV_CMD_PATH}
                    call micromamba activate {PYEXOSEU_ENV_NAME}
                    C:
                    cd "%HOME%\\.pyexo_seu\\local_distribution\\pyexo_seu\\app\\webapp"
                    start "PYEXOSEU WEBAPP" streamlit run Welcome.py
                    
                  """
        # C:
        # cd
        # "%CONDA_PREFIX%\\Lib\\site-packages\\pyexo_seu\\app\\webapp"

        (CMDS_FOLDER / "webapp.cmd").write_text(cmd_str)

    # @staticmethod
    # def dump_flower_cmd():
    #     cmd_str = f"""
    #                 call micromamba activate
    #                 IF %ERRORLEVEL% == 0 (GOTO HAS_MICROMAMBA) ELSE (GOTO HAS_NOT_MICROMAMBA)
    #
    #                 :HAS_MICROMAMBA
    #                 GOTO CONTINUE
    #
    #                 :HAS_NOT_MICROMAMBA
    #                 ECHO "Please install MICROMAMBA"
    #                 start msedge https://devportal.group.socgen/dev-tool/mircromamba
    #                 PAUSE
    #                 exit
    #
    #                 :CONTINUE
    #                 C:
    #                 cd "%CONDA_PREFIX%\\Lib\\site-packages\\pyexo_seu\\app\\services"
    #                 start "PYEXOSEU WORKERS MONITORING" celery -A service_celery_worker --broker=redis://{REDIS_URL}:{REDIS_PORT}/ flower
    #               """
    #
    #     (CMDS_FOLDER / 'workers_monitoring.cmd').write_text(cmd_str)

    @staticmethod
    def dump_distribution():
        Distribution.dump_remote_git_repo()
        Distribution.dump_env_refresher()
        Distribution.dump_jupyter_cmd()
        # Distribution.dump_flower_cmd()
        Distribution.dump_webapp_cmd()
