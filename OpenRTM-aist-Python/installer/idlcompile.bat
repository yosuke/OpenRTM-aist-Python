@rem ------------------------------------------------------------
@rem IDL Compile bat
@rem   argument %1: Python script name
@rem   argument %2: Python version
@rem ------------------------------------------------------------
@echo off
echo --- IDL Compile Python %2 Start ---
set PATH_TMP=%PATH%
set PATH=%CD%\;%PATH_TMP%
set PYTHONPATH=%CD%\Lib\site-packages

%CD%\python %1 %2
echo --- IDL Compile Python %2 Complete ---

