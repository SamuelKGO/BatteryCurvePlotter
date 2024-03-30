
for /f "delims=" %a in ('powershell -Command "(Get-ChildItem -Path . -Recurse -Filter CurveFinder.py).DirectoryName"')^
  do (cd %a & if exist %a\CurveFinder.py^
              (echo Running Python script: %a\CurveFinder.py^
              & python CurveFinder.py \^
              & if errorlevel 1 (echo Error Occurred while running CurveFinder.py))
              
              
