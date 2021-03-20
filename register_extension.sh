#!/usr/bin/env bash

defaults write com.apple.LaunchServices LSHandlers -array-add \
  "<dict>
   <key>LSHandlerContentTag</key>
   <string>m4baker</string>
   <key>LSHandlerContentTagClass</key>
   <string>public.filename-extension</string>
   <key>LSHandlerRoleAll</key>
   <string>M4Baker</string>
</dict>"

lsregister='/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister'
$lsregister -kill -domain local -domain system -domain user
$lsregister -dump | grep -I m4baker
