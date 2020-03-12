# A simple object store implemented on a file system
# Roy Williams 2020

import os
class objectStore():
    def __init__(self, suffix='txt', fileroot='/data'):
        os.system('mkdir -p ' + fileroot)
        self.fileroot = fileroot
        self.suffix = suffix
    
    def getFileName(self, objectId, mkdir=False):
        dir = objectId[-3:] # last 3 characters
        if mkdir:
            try:
                os.makedirs(self.fileroot+'/'+dir)
            except:
                pass
        return self.fileroot +'/%s/%s.%s' % (dir, objectId, self.suffix)

    def getObject(self, objectId):
        f = open(self.getFileName(objectId))
        str = f.read()
        f.close()
        return str

    def putObject(self, objectId, objectBlob):
        f = open(self.getFileName(objectId, mkdir=True), 'wb')
        f.write(objectBlob)
        f.close()

    def getObjects(self, objectIdList):
        L = []
        for objectId in objectIdList:
            L.append(self.getObject(objectId))
        return L
    
    def putObjects(self, objectBlobList):
        for (objectId, objectBlob) in objectBlobList:
            self.putObject(objectId, objectBlob)


