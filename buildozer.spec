[app]
# (str) Title of your application
title = ATAGULDONER

# (str) Package name
package.name = ataguldoner
package.domain = org.atagul

# (str) Source dir (where your main .py is). Repo root uses "."
source.dir = .

# (str) Main python file (rename if main file farklı)
source.include_exts = py, png, jpg, kv, atlas, ogg, wav

# (str) Presume your entrypoint is 'möm.py' or 'main.py'. Set here:
# If your main file is 'möm.py', set: (escape non-ascii? best to rename to main.py)
# You can rename the file to main.py to avoid encoding problems.
# Example:
# (UNIX filenames): main.py
# If your entry file is named 'möm.py' you are safer renaming it to main.py before build.
# For safety, set the entrypoint:
# (If you do not set, buildozer will try main.py)
# uncomment and set if necessary:
# entrypoint = möm.py

# (str) Application versioning (must be present)
version = 1.0

# (list) Application requirements
requirements = python3, pygame

# (str) Application icon
# icon.filename = %(source.dir)s/icon.png

# (bool) Android-specific settings
android.api = 34
android.minapi = 24
android.ndk = 25.2.9519653
android.accept_sdk_license = True

# (str) Supported architectures
android.archs = arm64-v8a

# (str) Android permissions
android.permissions = INTERNET

# (bool) Copy libs into libs folder of the android project
# (useful for local native libs)
# copy-libs = True

# (str) Presplash, orientation, etc
orientation = landscape
fullscreen = 0
log_level = 2

# (int) Android bootstrap: use 'sdl2' for pygame projects
bootstrap = sdl2
