# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\CircleTip.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\DeskTip.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\DAO\\\\Database.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\dialogs\\\\AddDialog.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\dialogs\\\\RecordDialog.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\entity\\\\Item.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\entity\\\\Recorder.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\service\\\\DayItem.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\widgets\\\\ItemWidget.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\widgets\\\\MyCalendar.py', 'T:\\\\learning\\\\1CS\\\\python\\\\python_piece\\\\deskTip\\\\widgets\\\\MyFrame.py'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons\\4.ico',
)
