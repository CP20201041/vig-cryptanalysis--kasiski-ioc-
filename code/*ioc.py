import os
import random
import string
from collections import Counter
import matplotlib.pyplot as plt

abc = list(string.ascii_lowercase)
ln = "e t a o i n s r h l d c u m f p g w y b v k x j q z".split()
abc_idx = {c: i for i,c in enumerate(abc)}

#--------------------

def file(name) -> list:
    locations = ["Documents","Downloads"]

    for x in locations:
        path = "/Users/chris/" + x
        for root,dirs,files in os.walk(path):
            if name in files:
                return open(os.path.join(root,name)).read()

    print ("PATH NOT FOUND")
    return []

def vig(ptext,key):
    ctext = []
    kl = len(key)
    key_idx = [abc_idx[x] for x in key]

    for i,char in enumerate(ptext):
        ctext.append(abc[(abc_idx[char] + key_idx[i % kl]) % 26])

    return ("".join(ctext))

def vig_dec(ptext,kg):
    ctext = []
    kl = len(kg)
    key_idx = [abc_idx[x] for x in kg]

    for i,char in enumerate(ptext):
        ctext.append(abc[(abc_idx[char] - key_idx[i % kl]) % 26])

    return ("".join(ctext))

def pack(ctext,m):
    return [ctext[i::m] for i in range(m)]

def ioc(ctext):
    counts = Counter(ctext)
    s = sum(n * (n - 1) for n in counts.values())
    N = len(ctext)
    return s/(N*(N-1))

def graph():
        plt.figure(figsize=(8,5))
        plt.plot(range(1,len(vals)+1), [x[0] for x in vals], color="blue", marker='o', alpha=0.6)

        # plt.plot(range(2,len(fence)+2), fence, color="black", marker='o', alpha=0.6)
        # plt.scatter([x[1] for x in peaks], [x[0] for x in peaks], color="red", marker='x', s=70)
        # plt.axhline(y=s, color='r', linestyle='--')

        plt.title(f"Key: {key} ({len(key)})")
        plt.xlabel('Key Length')
        plt.xticks(range(1,keyrange+2), fontsize=4)
        plt.ylabel('IC(k)')
        plt.grid(True)
        plt.show()

def spike(lst,n=2,keyrange=40):
    global fence,peaks,s,graph_bool

    L = len(lst)
    lst0 = [x[0] for x in lst]
    lst1 = [x[1] for x in lst]

    peaks = []
    fence = []

    mid = sum(lst0)/L
    s = 0
    for x in lst0:
        s += (x-mid)**2
    s /= L
    s **= 0.5

    for i in range(1,L-1):
        fence.append(1.1*s+(lst0[i-1]+lst0[i+1])/2)

    #----------

    kgs = []
    for i in range(1,len(lst0)-1):
        if lst0[i] > fence[i-1]:
            peaks.append([lst0[i],lst1[i]])
            kgs.append(lst1[i])

    def factor(n):
        divisors = []
        for i in range(1,n+1):
            if n % i == 0:
                divisors.append(i)
        return divisors

    factors = []
    if kgs == []:
        graph()
        return (None)

    gs = min(kgs)
    for x in kgs:
        f = factor(x)
        for y in f:
            if y >= gs:
                factors.append(y)

    com = [x[0] for x in Counter(factors).most_common(n)]

    #----------

    a = peaks[0][1]

    b = Counter(factors).most_common(1)[0][0]
    maxpeak = max(peaks)[1]

    if len(peaks) == 1:
        return ([a,a])
    else:
        return ([b,maxpeak])

def keylength(ctext,keyrange=40):
    global vals

    vals = []
    for i in range(1,keyrange+2):
        group = pack(ctext,i)
        s = 0
        for j in range(i):
            s += ioc(group[j])
        vals.append([s/i,i])

    return(spike(vals,keyrange))

def contrast(str1,str2):
    contrast = []

    for i in range(len(str1)):
        contrast.append((abc_idx[str1[i]]-abc_idx[str2[i]])%26)
    return (contrast)

def keyp(ctext,klg):
    parts = pack(ctext,klg)
    kg = ""

    for x in parts:
        counts = [x[0] for x in list(Counter(x).most_common())]
        kg += (abc[Counter(contrast(counts,ln)).most_common(1)[0][0]])

    return kg

def dupl(strng):
    period_len = (strng + strng).index(strng,1)
    
    if len(strng) % period_len == 0:
        return strng[:period_len]
    else:
        return strng

def test(m,keyrange):
    global key

    l0 = 0
    l1 = 0
    s0 = 0
    s1 = 0
    acc0 = []
    acc1 = []

    for i in range(1,keyrange+1):
        cn0 = 0
        cn1 = 0
        
        for j in range(m):
            kl = i
            key = "".join(random.choices(string.ascii_lowercase,k=kl))

            ctext = vig(ptext,key)
            klgs = keylength(ctext,keyrange)

            klg0 = klgs[0]
            klg1 = klgs[1]
            kg0 = dupl(keyp(ctext,klg0))
            kg1 = dupl(keyp(ctext,klg1))
            if klg0 == len(key):
                l0 += 1
            if klg1 == len(key):
                l1 += 1

            klg0 = len(kg0)
            klg1 = len(kg1)
            
            if kl > klg0:
                kg0 = [kg0[i%klg0] for i in range(kl)]
            if kl > klg1:
                kg1 = [kg1[i%klg1] for i in range(kl)]
            if klg0 > kl:
                key_new = [key[i%kl] for i in range(klg0)]
            if klg1 < kl:
                key_new = [key[i%kl] for i in range(klg1)]


            c0 = sum(char_a != char_b for char_a,char_b in zip(key,kg0)) 
            c1 = sum(char_a != char_b for char_a,char_b in zip(key,kg1)) 

            cn0 += c0
            cn1 += c1

            print (f"kl: {kl} , {klgs[0]}({c0}) ,{klgs[1]}({c1})")


        s0 += cn0
        s1 += cn1

        if cn0 == 0:
            acc0.append("0%")
        else:
            acc0.append(str(100*(cn0/(m*i)))[:5] + "%")

        if cn1 == 0:
            acc1.append("0%")
        else:
            acc1.append(str(100*(cn1/(m*i)))[:5] + "%")

    print ()
    
    print (f"average letter accuracy: {str(100-200*s0/(m*keyrange*(keyrange+1)))[:5]}%")
    print (f"average length accuracy: {str(100-100*(l0/(m*keyrange)))[:5]}%")
    print (acc0)

    print ()

    print (f"average letter accuracy: {str(100-200*s1/(m*keyrange*(keyrange+1)))[:5]}%")
    print (f"average length accuracy: {str(100-100*(l1/(m*keyrange)))[:5]}%")
    print (acc1)

#--------------------

# txt = file("The Modern Prometheus.txt")

# txt = file("Jekyll & Hyde.txt")

# txt = file("The Lottery.txt")

txt = file("Do not go gentle into that good night.txt")


ptext = "".join([x for x in txt.lower() if x.isalpha()])

#--------------------

keyrange = 60
m = 10

key = """

asdf

""".replace("\n","").replace(" ","")
kl =  len(key)
if kl > keyrange:
    kl = keyrange

if "-" in key:
    key = "".join(random.choices(string.ascii_lowercase,k=kl))
graph_bool = False
test_bool = False
# graph_bool = False

if test_bool or not key:
    test(m,keyrange)
else:
    ctext = vig(ptext,key)
    
    # print (ctext)
    # print ()

    klgs = keylength(ctext,keyrange)
    kl = len(key)

    klg = klgs[0]
    # klg = klgs[1]

    kg = dupl(keyp(ctext,klg))
    klg_new = len(kg)
    key_new = key
    
    if kl > klg_new:
        kg = ''.join([kg[i%klg_new] for i in range(kl)])
    if klg_new > kl:
        key_new = [key[i%kl] for i in range(klg_new)]

    c = sum(char_a != char_b for char_a,char_b in zip(key_new,kg))

    print (kl,":",key)
    print (klg,":",kg)
    print (f"({c})")

    # print (vig_dec(ctext,kg))

    if graph_bool or input() == "":
        graph()

print ()
print ("[IOC]")
print ()