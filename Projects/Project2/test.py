def test1():
    return (None, 0)

def test2():
    return ("Test", 1)

def test3():
    return ("", None)

def start():
    num = [1,2]
    for n in num:
        (wor, num) = test2()
        print("here1")
        if all((wor,num)):
            print("not none")
            continue

        (wor, num) = test2()

        print("here2")
        if all((wor,num)):
            print("not none")
            continue

        (wor, num) = test3()

        print("here3")
        if all((wor,num)):
            print("not none")
            continue


start()
