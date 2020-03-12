# A simple object store implemented on a file system
# Roy Williams 2020

import os
class objectStore():
    def __init__(self, suffix='txt', fileroot='/data'):
        os.system('mkdir -p ' + fileroot)
        self.fileroot = fileroot
        self.suffix = suffix
    
    def getFileName(self, objectId, mkdir=False):
        dir = '%03d' % (hash(objectId) % 1000)
        if mkdir:
            try:
                os.makedirs(self.fileroot+'/'+dir)
                print('made %s' % dir)
            except:
                pass
        return self.fileroot +'/%s/%s.%s' % (dir, objectId, self.suffix)

    def getObject(self, objectId):
        f = open(self.getFileName(objectId))
        str = f.read()
        f.close()
        return str

    def putObject(self, objectId, objectBlob):
        filename = self.getFileName(objectId, mkdir=True)
#        print(objectId, filename)
        f = open(filename, 'wb')
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


