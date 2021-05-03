@echo off

echo test script started, cwd ^-^> %cd% args ^-^> %*
timeout /t 5 /nobreak > nul
echo normal msg 1
timeout /t 5 /nobreak > nul
echo normal msg 2
timeout /t 5 /nobreak > nul
echo error msg com^.android 1>&2
timeout /t 5 /nobreak > nul
echo error msg com^.android 1>&2
