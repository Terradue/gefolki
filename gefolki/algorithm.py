from __future__ import absolute_import
from .folki import GEFolkiIter, EFolkiIter, FolkiIter
from .pyramid import BurtOF

GEFolki = BurtOF(GEFolkiIter)
EFolki = BurtOF(EFolkiIter)
Folki = BurtOF(FolkiIter)
