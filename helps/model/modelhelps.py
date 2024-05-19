from helps.common.generic import Generichelps as ghelp

def setSettings(id, code, pattern, ConfigClass, BackupClass):
    if id == None:
        code = ghelp().generateUniqueCode(pattern)
    return ghelp().set_settings(ConfigClass, BackupClass, code)