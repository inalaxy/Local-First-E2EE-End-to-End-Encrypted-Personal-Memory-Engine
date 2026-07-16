[app]
title = L1MemoryEngine
package.name = l1memoryengine
package.domain = org.localfirst
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Android specific requirements
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
