import os
import threading
import queue as q
import time

class WorkerThread(threading.Thread):

    def __init__(self, nums_q, sq_q):
        super(WorkerThread, self).__init__()
        self.nums_q = nums_q
        self.sq_q = sq_q
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
                num = self.nums_q.get(True, 0.5)
                sq = num * num
                self.sq_q.put([num, sq])
            except Exception as e:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)


def main(args):
    nums_q = q.Queue()
    sq_q = q.Queue()

    pool = [WorkerThread(nums_q=nums_q, sq_q=sq_q) for i in range(4)]

    for thread in pool:
        thread.start()

    itr = 3
    while(itr>0):
        work_count = 0
        for num in args:
            work_count += 1
            nums_q.put(num+itr)

        print("jobs assigned")
        print("work_count ", work_count)
        while(work_count > 0):
            result = sq_q.get()
            print('the square is:', result)
            work_count -= 1
        itr -= 1

    for thread in pool:
        thread.join()

if __name__ == '__main__':
    import sys
    num_list = []
    for n in sys.argv[1:]:
        num_list.append(int(n))
    main(num_list)
