# -*- mode: python -*-

block_cipher = None

added_files = [
    ('Progs/assets', 'assets'),          # Assets folder
    ('Progs/Adjust_Session_Function.py', '.'),  # Adjust function script (in root of exe)
    ('Progs/Main_Functions.py', '.'),       # Main functions script (in root of exe)
]

a = Analysis(['Progs\\Main_Application_UI.py'],  # Main script
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=['aiohappyeyeballs', 'aiohttp', 'aiosignal', 'annotated_types', 'asttokens', 'attrs', 'cachetools', 'certifi', 'charset_normalizer', 'colorama', 'decorator', 'et_xmlfile', 'executing', 'frozenlist', 'google_ai_generativelanguage', 'google_api_core', 'google_api_python_client', 'google_auth', 'google_auth_httplib2', 'google_generativeai', 'googleapis_common_protos', 'grpcio', 'grpcio_status', 'httplib2', 'idna', 'ipython', 'jedi', 'matplotlib_inline', 'multidict', 'numpy', 'openpyxl', 'pandas', 'parso', 'prompt_toolkit', 'propcache', 'proto_plus', 'protobuf', 'pure_eval', 'pyasn1', 'pyasn1_modules', 'pydantic', 'pydantic_core', 'Pygments', 'pyparsing', 'python_dateutil', 'pytz', 'requests', 'rsa', 'six', 'stack_data', 'tabulate', 'tqdm', 'traitlets', 'typing_extensions', 'tzdata', 'uritemplate', 'urllib3', 'wcwidth', 'yarl'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          [],
          name='AbstractCategorization',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='E:\\Projects\\Applications\\AbstractCategorization\\Progs\\assets\\frame0\\icon.ico')