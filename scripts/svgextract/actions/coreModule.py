from helpers.util import *

def createCoreModule(slug, coreModuleDir = None):
    if coreModuleDir == None:
        coreModuleDir = os.getenv('METAMODULE_COREMODULE_DIR')
        if coreModuleDir is None:
            coreModuleDir = input_default("Module dir", pathFromHere("../../../src/modules/core/"))

    newCoreFileName = slug + '.hh'

    if not os.path.exists(os.path.join(coreModuleDir, newCoreFileName)):
        # Replace 'Slug' in template file with our slug, then write to a new file

        coreTemplateFilename = './template_module.hh'
        with open(coreTemplateFilename, 'r') as file :
            filedata = file.read()

        filedata = filedata.replace('Slug', slug)
        with open(os.path.join(coreModuleDir, newCoreFileName), 'w') as file:
            file.write(filedata)
            Log(f"Created new file {newCoreFileName} in {coreModuleDir} because it didn't exist")

