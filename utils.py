def SetUndo(clearRedo=True):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if clearRedo:
                self._redo = []
            elif not self._redo:
                    return func(self, *args, **kwargs)

            revert = self.SaveState()
            self._undo.append(revert)

            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def SetRedo(func):
    def wrapper(self, *args, **kwargs):
        if self._undo:
            revert = self.SaveState()
            self._redo.append(revert)
        return func(self, *args, **kwargs)
    return wrapper
