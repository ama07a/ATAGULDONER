[app]
# (str) Title of your application
title = ATAGULDONER

# (str) Package name
package.name = ataguldoner
package.domain = org.atagul

# (str) Source code dir
source.dir = .

# (str) The main file of the application (Buildozer expects main.py)
# If your file is named anders (möm.py) we copied it to main.py in workflow step.
source.include_exts = py,kv,png,jpg,ogg,ogg,ttf,atlas,json

# (list) Application requirements
requirements = python3, pygame

# (str) Supported orientation
orientation = landscape

# (int) Android API to use (will be installed by CI)
android.api = 34
android.minapi = 24
android.ndk = 25.2.9519653

# (str) Android entry point (optional - default is main.py)
# android.entrypoint = main.py

# (bool) accept SDK licenses automatically in CI
android.accept_sdk_license = True

# (str) version
version = 1.0

# (str) Android archs (use arm64 to avoid armeabi complexities)
android.archs = arm64-v8a

# (int) Android build tool
android.build_tools_version = 34.0.0

# (str) Presplash / icon — optional
# icon.filename = %(source.dir)s/assets/icon.png
