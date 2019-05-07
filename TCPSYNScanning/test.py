from multiprocessing import Process, Manager

def f(d):
    d[1] += '1'
    d['2'] = 2
    d['e'] = 32

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    d[1] = '1'
    d['2'] = 2

    p1 = Process(target=f, args=(d,))
    p1.start()
    f(d)

    p1.join()

    print(d)
