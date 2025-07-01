# utils/debug_helpers.py

def add_safe_str_repr(cls):
    def safe_repr(self, visited=None, level=0, max_level=5):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return f"<recursive {type(self).__name__}>"
        if level > max_level:
            return f"<max recursion {type(self).__name__}>"
        visited.add(id(self))
        children = getattr(self, 'children', [])
        child_reprs = [repr(child) for child in children]
        return f"{self.__class__.__name__}({child_reprs})"

    cls.__repr__ = safe_repr
    cls.__str__ = safe_repr
    return cls
