import socket

class Resolver():
    def __init__(self):
        self._cache = {}

    def __call__(self, host):
        if host not in self._cache:
            self._cache[host] = socket.gethostbyname(host)
        return self._cache[host]

    def clear(self):
        self._cache.clear()
        ## is clear a built in fucntion

    def has_host(self, host):
        return host in self._cache


if __name__ == "__main__":
    res = Resolver()
    print(res.has_host("google.co.uk"))
    print(res("google.co.uk"))
    print(res.has_host("google.co.uk"))
    res.clear()
    print(res.__call__("google.com"))
    print(res.has_host("google.co.uk"))
