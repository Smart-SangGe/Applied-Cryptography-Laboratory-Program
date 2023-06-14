import hashlib
import bitarray

class BloomFilter:
    def __init__(self, size, hash_num):
        self.size = size
        self.hash_num = hash_num
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)

    def add(self, s):
        for seed in range(self.hash_num):
            result = hashlib.md5(s.encode('utf-8')).hexdigest()
            dig = int(result, 16)
            loc = dig % self.size
            self.bit_array[loc] = 1

    def lookup(self, s):
        for seed in range(self.hash_num):
            result = hashlib.md5(s.encode('utf-8')).hexdigest()
            dig = int(result, 16)
            loc = dig % self.size
            if self.bit_array[loc] == 0:
                return False
        return True

# 创建一个布隆过滤器，位数组大小为500000，使用3个哈希函数
bf = BloomFilter(500000, 3)

# 添加元素
bf.add("hello")
bf.add("world")

# 查询元素
print(bf.lookup("hello"))  # 输出 True
print(bf.lookup("world"))  # 输出 True
print(bf.lookup("liangjunyong"))  # 输出 False
