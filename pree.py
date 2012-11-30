#!/usr/bin/python3 -d
#	pree.py
#	This is my Python3/PyQt4 rewrite of Kodos by Phil Schwartz ( http://kodos.sourceforge.net/ )
#       

import sys
import re
import os


try:
    from PyQt4 import QtGui, QtCore
except:
    print( "Could not locate the PyQt4 module.")
    sys.exit(1)

import os.path
from distutils.sysconfig import get_python_lib

sys.path.insert(0, os.path.join(get_python_lib(), "pree"))

from modules.mainWindow import *


# colors for normal & examination mode
QCOLOR_WHITE  = QtCore.Qt.white     # normal
QCOLOR_YELLOW = QtGui.QColor(255,255,127)  # examine

class MyForm(QtGui.QMainWindow):
  def __init__(self, parent=None):
    super(MyForm, self).__init__(parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.tedReg.textChanged.connect(self.regChange)
    self.ui.tedString.textChanged.connect(self.strChange)
    self.ui.actionShow_Variables.activated.connect(self.showVariables)
    self.ui.actionExit.activated.connect(self.close)
    self.ui.chkCase.toggled.connect(self.checkChange)
    self.ui.chkMulti.toggled.connect(self.checkChange)
    self.ui.chkDot.toggled.connect(self.checkChange)
    self.ui.chkVerbose.toggled.connect(self.checkChange)
    self.ui.chkLocale.toggled.connect(self.checkChange)
    self.ui.chkAscii.toggled.connect(self.checkChange)
    
    self.regex = ""
    self.matchstring = ""
    self.flags = 0
  
  def checkChange(self):
      self.flags = 0
        
      if self.ui.chkCase.isChecked():
        self.flags = self.flags + re.IGNORECASE

      if self.ui.chkMulti.isChecked():
        self.flags = self.flags + re.MULTILINE

      if self.ui.chkDot.isChecked():
        self.flags = self.flags + re.DOTALL

      if self.ui.chkVerbose.isChecked():
        self.flags = self.flags + re.VERBOSE

      if self.ui.chkLocale.isChecked():
        self.flags = self.flags + re.LOCALE

      if self.ui.chkAscii.isChecked():
        self.flags = self.flags + re.ASCII

      self.process_regex()
  
  def regChange(self):
    try:
      self.regex = str(self.ui.tedReg.toPlainText())
      
    except UnicodeError:
      self.regex = unicode(self.ui.tedReg.text())
      
    self.process_regex()
    
    
  def strChange(self):
    try:
      self.matchstring = str(self.ui.tedString.toPlainText())
      
    except UnicodeError:
      self.matchstring = unicode(self.ui.tedString.text())
      
    self.process_regex()
    
  def colorize_strings(self, strings, widget, cursorOffset=0):
        widget.clear()

        colors = (QtCore.Qt.black,QtCore.Qt.blue )
        i = 0
        pos = widget.getCursorPosition()
        for s in strings:
            widget.setColor(colors[i%2])            
            widget.insert(s)
            if i == cursorOffset: pos = widget.getCursorPosition()
            i += 1
            
        widget.setCursorPosition(pos[0], pos[1])
    
  def populate_matchAll_textbrowser(self, spans):
    self.ui.tedMatchAll.clear()
    if not spans: return

    idx = 0
    text = self.matchstring
    strings = []
    for span in spans:
      if span[0] != 0:
        s = text[idx:span[0]]
      else:
        s = ""
                
      idx = span[1]
      strings.append(s)
      strings.append(text[span[0]:span[1]])

      if 0 <= idx <= len(text): 
        strings.append(text[span[1]:])
    
    #I lifted the line below from the colorize function        
    #for s in strings:
    #    self.ui.tedMatchAll.append(s)
        
    self.colorize_strings(strings, self.ui.tedMatchAll)
    
    
  def process_regex(self):
    compile_obj = re.compile(self.regex, self.flags)
    allmatches = compile_obj.findall(self.matchstring)
    
    match_obj = compile_obj.search(self.matchstring)
    if match_obj is None:
      self.ui.txtMatch.setPlainText("No Match")
    else:
      self.ui.tedMatch.setPlainText(match_obj.group())
      
    spans = self.findAllSpans(compile_obj)
    self.populate_matchAll_textbrowser(spans)  

  def findAllSpans(self, compile_obj):
    spans = []
        
    match_obj = compile_obj.search(self.matchstring)

    last_span = None
        
    while match_obj:
      start = match_obj.start()
      end   = match_obj.end()
      span = (start, end)
      if last_span == span: break
            
      spans.append(span)
            
      last_span = span
      match_obj = compile_obj.search(self.matchstring, end)

    return spans

 
  def showVariables(self):
    message = "Regex: " + self.regex + "\nString: " + self.matchstring
    self.ui.tedMatch.setPlainText(message)
    

    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
