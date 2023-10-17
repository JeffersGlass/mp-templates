# Shim since MP has no abc module
def abstractmethod(func):
    return func