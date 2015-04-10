from models import FileSystem
from functools import partial


def check_is_disabled(func):
    def inner(self, pathname, *args, **kwargs):
        if len(args) == 2:
            previous_version = FileSystem.objects(path_name=args[1], has_next=False).first()
        else:
            previous_version = FileSystem.objects(path_name=pathname, has_next=False).first()
        if hasattr(previous_version, "disabled"):
            if not previous_version.disabled:
                pfnx = partial(func, self, pathname, *args, **kwargs)
                return pfnx(previous_version)
        else:
            return func(self, pathname, *args, **kwargs)
    return inner