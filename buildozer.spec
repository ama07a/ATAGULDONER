[app]
title = ATAGULDONER
package.name = ataguldoner
package.domain = org.atagul
source.dir = ATAGULDONER
source.include_exts = py,png,jpg,ogg,txt,json
version = 1.0
orientation = landscape
entrypoint = main.py
requirements = python3,pygame
# (if you use opencv or other heavy deps, remove here for simplicity)
#requirements = python3,pygame,opencv-python

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 34
android.ndk = 25.2.9519653
android.minapi = 24
android.archs = arm64-v8a
android.sdk_path = $HOME/android-sdk
android.ndk_path = $HOME/android-sdk/ndk/25.2.9519653
android.accept_sdk_license = True
