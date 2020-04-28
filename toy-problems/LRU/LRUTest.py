from LRU import LRU
class LRUTest:
    def __init__(self):
        pass

def main():
    l = [2,9,1,7,3,5,7,6,9,2,1]
    cache = LRU()
    for each in l:
        cache.put(each)
    print(cache.get_cache())
    assert cache.get_cache()==[1,2,9,6,7,5,3]
    
if __name__ == "__main__":
    main()