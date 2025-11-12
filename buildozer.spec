[app]
# (str) Title of your application
title = ATAGULDONER

# (str) Package name
package.name = ataguldoner

# (str) Package domain (reverse domain-style)
package.domain = org.atagul

# (str) Source code folder (relative to buildozer.spec)
source.dir = ./ATAGULDONER

# (list) Include extensions
source.include_exts = py,png,jpg,ogg,wav,mp3,json,txt

# (str) Application versioning
version = 1.0

# (str) Orientation
orientation = landscape

# (bool) Fullscreen
fullscreen = 1

# (list) Requirements
# Avoid heavy C modules here; pygame is included but note CI uses --skip-build-pygame-c
requirements = python3, pygame

# (str) Icon file (set if you have one)
icon.filename = %(source.dir)s/assets/icon.png

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# (int) Minimum Android API
android.minapi = 24

# (int) Target API
android.api = 34

# (str) NDK recommendation
android.ndk = 25.2.9519653

# (list) architectures to build for
android.archs = arm64-v8a

# accept sdk license
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
