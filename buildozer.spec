[app]
title = ¿Quién Quiere Ser Millonario? Bíblico
package.name = millonariobiblico
package.domain = org.millonario
source.dir = .
source.main = main
source.include_exts = py,png,jpg,kv,json,wav,mp3,ogg,jpeg,gif
source.include_patterns = assets/*,assets/**,sounds/*,sounds/**,audio/*,audio/**,preguntas/*,preguntas/**,comodines/*,comodines/**
source.exclude_dirs = tests, bin, venv, __pycache__, .gradle, flutter_app, .idea
source.exclude_patterns = *.pyc,*.md
version = 1.0
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pyjnius,pillow
orientation = portrait
fullscreen = 0

[android]
# Android 7.0 = API 24; compatible con 7 en adelante
api = 31
minapi = 24
ndk = 23c
sdk = 31
permissions = INTERNET
archs = arm64-v8a,armeabi-v7a
accept_sdk_license = True
wakelock = True

[buildozer]
log_level = 2
warn_on_root = 1

