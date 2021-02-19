# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src/m4baker.py'],
             pathex=['/Users/iwo16283/dev/ivonet-audiobook/'],
             binaries=[],
             datas=[ ("src/resources", "./resources")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='m4baker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='m4baker')
app = BUNDLE(coll,
             name='M4Baker.app',
             icon="./Yoda.icns",
             bundle_identifier=None)
