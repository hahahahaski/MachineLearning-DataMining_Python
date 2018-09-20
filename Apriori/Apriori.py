import random
import pymysql

def Apriori(dataSet,minSup):
    # 求 L1
    # 利用 Python 字典实现
    # 统计每一个元素的频度，然后把元素放入 L1 中
    C1 = {}
    for transaction in dataSet:
        for item in transaction:
            if item in C1:
                C1[item] += 1
            else:
                C1[item] = 1

    temp = C1.keys()
    L1_ = []
    for item in temp:
        L1_.append([item])

    n = len(dataSet)
    L1 = []
    for item in L1_[:]:
        if C1[item[0]] * 1.0 / n >= minSup:
            L1.append(item)
    L1.sort()
    print("L1:")
    print(L1)

    # 利用 Lk_1 迭代求 Lk
    Lk_1 = L1
    # freItemSet 存储每一步的频繁 k 项集
    freItemSet = []
    cnt = 1
    while Lk_1 != []:
        # 连接，求 Ck
        Ck = apriori_gen(Lk_1)
        print("C" + str(cnt+1) + ":")
        print(Ck)
        # 对 Ck 中每个 item 求 sup
        Count = getSup(dataSet,Ck)
        # 剪枝,求得 Lk
        Lk_1 = getLk(Ck,Count,minSup,n)
        # 将频繁项目加入 freItemSet
        if Lk_1 == []:
            return freItemSet
        else:
            for item in Lk_1:
                freItemSet.append(item)
            cnt += 1
            print("L"+str(cnt)+":")
            print(Lk_1)
    return freItemSet

# 连接步:由 Lk_1 求得 Ck
def apriori_gen(Lk_1):
    C = {}
    Ck = []
    # 两遍扫描，合法的频繁 k 项集的频度一定为 k*(k-1)
    for i in Lk_1:
        for j in Lk_1:
            if i != j:
                s = set()
                for item in i:
                    s.add(item)
                for item in j:
                    s.add(item)
                if len(s) == len(i)+1:
                    fs = frozenset(s)
                else:
                    continue
                if fs in C:
                    C[fs] += 1
                else:
                    C[fs] =1
    for i in C:
        temp = []
        if C[i] == len(i)*(len(i)-1):
            for j in i:
                temp.append(j)
            Ck.append(temp)
    return Ck

# 对 Ck 中每个 item 求 sup
def getSup(dataSet,Ck):
    Count = []
    for itemSet in Ck:
        cnt = 0
        for transaction in dataSet:
            # 判断两个 List 是否为父子集：Set(父) >= Set(子)
           if set(transaction) >= set(itemSet):
               cnt += 1
           else:
                continue
        Count.append(cnt)
    return Count

# 剪枝,求得 Lk
def getLk(Ck,Count,minSup,n):
    for i,itemSet in enumerate(Ck):
        if Count[i] < minSup*n:
            # Ck remove 后若 Count不跟着 remove，之前的对应关系就被破坏了
            # 还是不能直接 remove，因为 remove 过后，后面一个元素向前移动到了删除的位置，
            # 而 i 是在下一轮循环中是指向删除位置的下一个，这就导致了被删除元素的后面一位没有被进行过判断
            # Ck.remove(itemSet)
            # Count.remove(Count[i])
            Ck[i] = []
    Ck_ = []
    for itemSet in Ck:
        if itemSet != []:
            Ck_.append(itemSet)
    return Ck_

# 产生随机数据写入数据库
def initData():
    # 模拟商品 ID
    itemList = [1,2,3,4,5,6,7,8,9,0]
    try:
        conn = pymysql.connect(host='localhost',user='root',passwd='Xyz@123@00',db='KDD_1_DB',port=3306,charset='utf8')
        cur = conn.cursor()
        cur.execute('truncate table AprioriData;')
        for i in range(0,1000):
            for item in random.sample(itemList,random.randint(1,10)):
                cur.execute('INSERT INTO AprioriData(TID,GoodsID) VALUES('+str(i)+','+str(item)+');')
        conn.commit()
        cur.close()
        conn.close()
    except  Exception as e:
        print('1', e)

# 从数据库中加载记录
def loadData():
    dataSet = []
    try:
        conn = pymysql.connect(host='localhost',user='root',passwd='Xyz@123@00',db='KDD_1_DB',port=3306,charset='utf8')
        cur = conn.cursor()
        for i in range(0, 1000):
            cur.execute('select GoodsID from AprioriData where TID = ' + str(i))
            conn.commit()
            # fetchall()：获得 sql 语句的所有记录
            rs = list(cur.fetchall())
            res = list()
            for j in rs:
                res.append(j[0])
            dataSet.append(res)
    except  Exception as e:
        print(e)
    return dataSet

initData()
dataSet = loadData()
# dataSet = [[1,2,5], [2,4], [2,3], [1,2,4], [1,3], [2,3], [1,3], [1,2,3,5], [1,2,3]]
F = Apriori(dataSet, 1/10)
print('Total Frequent Itemset:\n', F)

