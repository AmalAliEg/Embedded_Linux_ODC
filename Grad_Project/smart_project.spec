# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add this to collect all resource files
added_files = [
    # Main icons
    ('icons/*.png', 'icons'),
    ('icons/*.jpg', 'icons'),
    ('*.mp4', '.'),
    # Add any other resource file types you're using
]

a = Analysis(
    ['MainScreen.py'],
    pathex=[],
    binaries=[],
    datas=added_files,  # Add the resource files here
    hiddenimports=[
        'PyQt5',
        'cv2',
        'vlc',
        'yt_dlp',
        'speech_recognition',
        'paho.mqtt.client',
        'numpy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SmartProject',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='LOGO.png'
)