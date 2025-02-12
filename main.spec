# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

# Get the project root directory
PROJECT_ROOT = Path(os.getcwd())

added_files = [
    ('assets/sounds/*.wav', 'assets/sounds'),
    ('assets/images/*.jpg', 'assets/images'),
    ('assets/images/*.ico', 'assets/images'),
    ('assets/images/*.png', 'assets/images'),
    ('assets/gifs/gen1/normal/*', 'assets/gifs/gen1/normal'),
    ('assets/gifs/gen1/shiny/*', 'assets/gifs/gen1/shiny'),
    ('assets/gifs/gen2/normal/*', 'assets/gifs/gen2/normal'),
    ('assets/gifs/gen2/shiny/*', 'assets/gifs/gen2/shiny'),
    ('assets/gifs/gen3/normal/*', 'assets/gifs/gen3/normal'),
    ('assets/gifs/gen3/shiny/*', 'assets/gifs/gen3/shiny'),
    ('assets/gifs/gen4/normal/*', 'assets/gifs/gen4/normal'),
    ('assets/gifs/gen4/shiny/*', 'assets/gifs/gen4/shiny'),
    ('assets/gifs/gen5/normal/*', 'assets/gifs/gen5/normal'),
    ('assets/gifs/gen5/shiny/*', 'assets/gifs/gen5/shiny'),
    ('assets/data/*', 'assets/data'),
    ('config.json', '.'),
    ('logs', 'logs'),  # Include empty logs directory for development mode
]

a = Analysis(
    ['src/main.py'],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PIL._tkinter_finder',
        'pygame',
        'pygame.mixer',
        'pygame.mixer_music',
        'pygame.image',
        'pygame.transform',
        'pygame.surface',
        'pygame.display',
        'pygame.time',
        'pygame.event',
        'colorama',
        'colorama.initialise',
    ],
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
    name='IdleMon',
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
    icon='assets/images/icon_png.png' if os.path.exists('assets/images/icon_png.png') else None,
) 