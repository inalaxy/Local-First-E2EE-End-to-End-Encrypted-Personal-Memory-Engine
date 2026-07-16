[app]
# (str) Title of your application
title = L1MemoryEngine

# (str) Package name
package.name = l1memoryengine

# (str) Package domain
package.domain = org.localfirst

# (str) Source code directory
source.dir = .

# (list) Source files to include (added png and jpg to make sure your assets are packaged!)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.0

# -----------------------------------------------------------------------------
# Icon and Presplash (Loading Screen) Configuration
# -----------------------------------------------------------------------------

# (str) Icon of the application (What shows on the phone's home screen)
icon.filename = %(source.dir)s/icon.png

# (str) Presplash of the application (The screen that pops up when the app is opened)
presplash.filename = %(source.dir)s/presplash.png

# (str) Presplash background color (Changes the background color behind your splash image)
# You can change #121212 (dark grey) to any hex color code that matches your design!
android.presplash_color = #121212

# -----------------------------------------------------------------------------
# Android specific requirements
# -----------------------------------------------------------------------------
requirements = python3,kivy

# Permissions: we only require Storage to store the secure DB locally
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (str) Supported orientations
orientation = portrait

# (bool) Use Android's private directory for storage instead of public
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
