#!/usr/bin/env python3
import os
content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>keychain-access-groups</key>
    <array>
        <string>$(AppIdentifierPrefix)com.adhkar.widgetapp</string>
    </array>
    <key>get-task-allow</key>
    <true/>
    <key>application-identifier</key>
    <string>$(AppIdentifierPrefix)com.adhkar.widgetapp</string>
    <key>com.apple.security.app-sandbox</key>
    <true/>
</dict>
</plist>
'''
with open('/tmp/entitlements.plist', 'w') as f:
    f.write(content)
print('Entitlements written')
