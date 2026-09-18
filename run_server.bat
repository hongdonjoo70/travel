@echo off
title 대한민국 여행 투어 웹 서버 구동
chcp 65001 >nul
echo ========================================================
echo   대한민국 관광지 안내 및 여행 투어 (길마중) 웹 서버
echo ========================================================
echo.
echo   [1] Flask 백엔드 서버를 구동합니다...
echo   [2] 기본 웹 브라우저에서 사이트가 자동으로 열립니다.
echo.
echo   접속 주소: http://localhost:5000
echo ========================================================
echo.
timeout /t 1 /nobreak >nul
start http://localhost:5000
python app.py
pause
