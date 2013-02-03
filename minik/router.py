import re


class Router(object):
    """ minik url router """
    def __init__(self):
        self.routs = []

    def add_url(self, pattern, view, **defaults):
        self.routs.append((re.compile(pattern), view, defaults))

    def get_view(self, url):
        for pattern, view, defaults in self.routs:
            match = pattern.match(url)
            if match:
                kwargs = match.groupdict()
                kwargs.update(defaults)
                return load_view(view), kwargs
            return None, None


def load_view(path):
    """loading view by string path"""
    list_path = path.split('.')
    module_path = '.'.join(list_path[:-1])
    func_name = list_path[-1]
    module = __import__(module_path)
    return getattr(module, func_name)
