@echo off
echo ========================================
echo    Burj Bot GitHub'ga yuklash
echo ========================================

REM Git konfiguratsiya
git config --global user.name "inomjonergashev208-oss"
git config --global user.email "inomjonergashev208@gmail.com"

REM Git repository yaratish (agar mavjud bo'lmasa)
if not exist ".git" (
    echo Git repository yaratilmoqda...
    git init
)

REM Remote qo'shish
git remote remove origin 2>nul
git remote add origin https://github.com/inomjonergashev208-oss/burjbot.git

REM Barcha fayllarni qo'shish
echo Fayllar qo'shilmoqda...
git add .

REM Commit qilish
echo Commit qilinmoqda...
git commit -m "Burj Apteka Bot - Complete functionality: Anketa, Murojaat, Dori buyurtma, Admin chat system"

REM Push qilish
echo GitHub'ga yuklanmoqda...
git branch -M main
git push -u origin main

echo ========================================
echo    Muvaffaqiyatli yuklandi!
echo ========================================
pause