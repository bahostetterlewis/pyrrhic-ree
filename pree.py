#!/usr/bin/python3 -d
#
#pree.py
#This is my Python3/PyQt4 rewrite of Kodos by Phil Schwartz ( http://kodos.sourceforge.net/ )
#A lot of the code is the same - probably the biggest difference other than using new libraries,
#is that I don't use custom controls and do use html in the qtextbrowser objects for formatting
#and creating the group table, etc. I could never have written it without having the original
#as a reference.


def main():
    try:
        from interfaces import QtGui
    except:
        pass
    else:
        QtGui.Run()
        return

    print("No gui could be loaded by your system - exiting")

if __name__ == "__main__":
    main()
