@echo off
echo Starte lokalen Webserver auf http://localhost:8080 ...
start http://localhost:8080/assessment.html
python -m http.server 8080
pause
