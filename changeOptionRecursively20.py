# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-change-options-recursively
# Addon number 751420631
# Version 2.0
from aqt.qt import *
from aqt.utils import  getText, tooltip,showWarning
from aqt import mw
from anki.hooks import addHook
from aqt.deckbrowser import DeckBrowser
from anki.hooks import runHook
import re

def switch(did):
    (confName, __)=getText("What should be the option of the descendant of this deck ?")
    (depthMin,__)=getText("Which is the minimal depth to which change must be done (0 is current depth)", default="1")
    depthMin=int (depthMin)
    (depthMax,__)=getText("Which is the maximal depth to which change must be done (0 is current depth)", default="99")
    depthMin=int (depthMin)
    col = mw.col
    decks = col.decks
    for conf in decks.allConf():
        if conf["name"]==confName:
            break
    if not conf["name"]==confName:
        tooltip("This option does not exists.")
        return
    for (name, did_) in decks.children(did):
        depth=len(re.findall("::",name))-len(re.findall("::",decks.get(did)["name"]))
        if depthMin<=depth <=depthMax:
            deck=decks.get(did_)
            deck["conf"]=conf["id"]
    col.flush()
    
# def run(m,did):
#     tooltip("showDeckOptions")
#     a = m.addAction(_("descendant"))
#     a.triggered.connect(lambda b, did=did: switch(m,did))
    

#addHook("showDeckOptions",run) 
def _showOptions(self, did):
    m = QMenu(self.mw)
    a = m.addAction(_("Rename"))
    a.triggered.connect(lambda b, did=did: self._rename(did))
    a = m.addAction(_("Options"))
    a.triggered.connect(lambda b, did=did: self._options(did))
    a = m.addAction(_("Export"))
    a.triggered.connect(lambda b, did=did: self._export(did))
    a = m.addAction(_("Delete"))
    a.triggered.connect(lambda b, did=did: self._delete(did))
    a = m.addAction(_("Descendant"))
    a.triggered.connect(lambda b, did=did: switch(did))
    runHook("showDeckOptions", m, did)
    m.exec_(QCursor.pos())

DeckBrowser._showOptions=_showOptions    
