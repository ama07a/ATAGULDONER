[app]
title = ATAGUL DONER
package.name = atagul_doner
package.domain = org.atagul
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,wav,ogg,ttf,kv,json,txt
version = 1.0.0
requirements = python3, kivy
orientation = landscape
fullscreen = 1
android.arch = armeabi-v7a
android.api = 34
android.minapi = 21
android.ndk = 25.2.9519653
android.sdk = 34
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.allow_backup = False
android.debug = False
android.entrypoint = main.py
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = .buildozer
output_dir = bin
