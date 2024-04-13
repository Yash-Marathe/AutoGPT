"""The singleton decorator for ensuring only one instance of a class."""

def singleton(cls):
    """
    Singleton decorator for ensuring only one instance of a class.
    """
    _instance = {}

    def getinstance(*args, **kwargs):
        """Get the single instance of the class."""
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return getinstance


@singleton
class MyClass:
    """
    A sample class for which we want to ensure only one instance.
    """

    def __init__(self, value):
        """
        Initialize the class with a value.
        """
        self.value = value


# Test the singleton decorator
if __name__ == "__main__":
    obj1 = MyClass(10)
    obj2 = MyClass(20)
    print(obj1 is obj2)  # prints True
