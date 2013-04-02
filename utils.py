def SetUndo(func):

    def wrapper(self, *args, **kwargs):
        revert = self.SaveState()
        self._undo.append(revert)
        self._redo = []

        return func(self, *args, **kwargs)

    return wrapper
