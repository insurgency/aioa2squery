# Don't use relative imports in order to create a valid PyInstaller stub script entrypoint
# See: https://github.com/pyinstaller/pyinstaller/issues/2560#issuecomment-426204837
from aioa2squery.command import main

if __name__ == '__main__':
    main()
