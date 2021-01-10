class simplemap:
    """ 用迭代器协议实现 map 功能 """
    def __init__(self, func, *sequences):
        self.func = func
        self.sequences = sequences
        self.i = -1
       
    def __iter__(self):
        return self

    def __next__(self):
        if len(self.sequences) > 0:
            minlen = min(len(subseq) for subseq in self.sequences)
            if self.i <= minlen:
                self.i += 1
                return self.func(*[list(subseq)[self.i] for subseq in self.sequences])

def mapper(func, *sequences):
    """用函数方式实现 map 的功能"""
    if len(sequences) > 0:
        minlen = min(len(subseq) for subseq in sequences)
        for i in range(minlen):
            yield func(*[list(subseq)[i] for subseq in sequences])

def add_one(x, y, z):
    return x + y + z

lst = [1, 2, 3]
lst2 = [4, 5]
lst3 = [7, 8, 9, 10]

result = simplemap(add_one, lst, lst2, lst3)
result = mapper(add_one, lst, lst2, lst3)
type(result)