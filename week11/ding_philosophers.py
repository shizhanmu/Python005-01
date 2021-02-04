from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore, Thread

PICK_LEFT_FORK  = [1, 1]
PICK_RIGHT_FORK = [2, 1]
EAT             = [0, 3]
PUT_LEFT_FORK   = [1, 2]
PUT_RIGHT_FORK   = [2, 2]
forks = [Semaphore() for _ in range(5)]
eat_log = []

class DiningPhilosophers(Thread):
    
    def pickLeftFork(self):
        eat_log.append([self.pid] + PICK_LEFT_FORK)

    def pickRightFork(self):
        eat_log.append([self.pid] + PICK_RIGHT_FORK)

    def eat(self):
        eat_log.append([self.pid] + EAT)

    def putLeftFork(self):
        eat_log.append([self.pid] + PUT_LEFT_FORK)

    def putRightFork(self):
        eat_log.append([self.pid] + PUT_RIGHT_FORK)
    
    def __call__(self, pid):
        self.pid = pid
        a, b = forks[self.pid], forks[(self.pid+1)%5]
        if self.pid == 3:  # 指定一个人拿叉子的顺序相反，避免死锁
            a, b = b, a
        with a:
            with b:
                self.pickLeftFork()
                self.pickRightFork()
                self.eat()
                self.putLeftFork()
                self.putRightFork()

n = 3  # 每人进食次数
philos = list(range(5))
with ThreadPoolExecutor(5) as executor:
    for i in range(n):
        executor.map(DiningPhilosophers(), philos)

print(eat_log)