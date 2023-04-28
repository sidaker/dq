def outer_func(msg):
    def inner_func(name):
        print(msg + ' ' + name)
    return inner_func


hi_func = outer_func("Hi")
bye_func = outer_func("bye")


hi_func("sid")
bye_func("Advik")
