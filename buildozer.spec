[app]

# (str) Title of your application
title = ATAGULDONER

# (str) Package name
package.name = ataguldoner

# (str) Package domain (unique)
package.domain = org.atagul

# (str) Source code where main.py is located
source.dir = ./ATAGULDONER

# (list) Source files to include (let empty to include all)
#source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,pygame

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation: portrait, landscape, all
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (bool) Presplash image (optional)
#presplash.filename = %(source.dir)s/presplash.png

# (bool) Include all dependencies for the Android build
#android.add_libs_armeabi_v7a = 

# (bool) Accept Android SDK licenses automatically
android.accept_sdk_license = True

# (int) Target Android API
android.api = 34

# (int) Minimum Android API your APK will support
android.minapi = 24

# (str) Android NDK version
android.ndk = 25.2.9519653

# (str) Android Build Tools version
android.build_tools = 34.0.0

# (bool) Copy permissions from main.py to Android manifest
#android.permissions = INTERNET

# (str) Presplash orientation
#presplash.orientation = portrait

# (bool) Use Python3 for the build
#python3 = True

[buildozer]

# (str) log level (0-2)
log_level = 2

# (bool) Copy source files to .buildozer/android/platform/python-for-android
copy_source = True

# (str) Directory for the compiled APK
bin_dir = bin
