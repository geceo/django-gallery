import sys
import os
import magic
import re
import shutil
from zipfile import ZipFile
from tempfile import mkdtemp


class imagesFromZip():
    def __init__(self,file):
        self.file = file
        self.path = mkdtemp()
        self.extracted = False
        self.imagesList = []

    def _extract(self):
        myZip = ZipFile(self.file,allowZip64=True)
        myZip.extractall(self.path)
        myZip.close()
        self.extracted = True

    def listImages(self):
        if not self.extracted:
            self._extract()
        # Prepare magic system
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        regexp = re.compile('^GIF|JPEG|PNG.*')
        for (dir, dirs, files ) in os.walk(self.path):
            for file in files:
                if regexp.match(ms.file(dir+'/'+file)):
                    self.imagesList.append(dir+'/'+file)
        return(self.imagesList)

    def cleanup(self):
        shutil.rmtree(self.path)
        
