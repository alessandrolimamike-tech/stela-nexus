[app]
title = Stela Nexus
package.name = stelanexus
package.domain = org.alessandrolima
version = 1.0.0
source.dir = .
requirements = python3,kivy==2.2.1,requests==2.31.0,beautifulsoup4==4.12.2,lxml==4.9.3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.minapi = 21

[android]
accept_licenses = True
android_build_tools_version = 34.0.0

[buildozer]
log_level = 2
warn_on_root = 0
