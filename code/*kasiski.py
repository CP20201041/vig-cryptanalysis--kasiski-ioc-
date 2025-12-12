import os
import random
import string
from collections import Counter
import math

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

def get_factors(n):
    factors = set()
    for i in range(1,int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)

    return sorted(list(factors))

def kasiski_examination(ctext,keyrange,kernel_min=4,kernal_max=7):
    all_distances = []
    
    for kernal in range(kernel_min,kernal_max+1):
        sequence_map = {}

        for i in range(len(ctext) - kernal + 1):
            sequence = ctext[i:i + kernal]

            if sequence in sequence_map:
                sequence_map[sequence].append(i)
            else:
                sequence_map[sequence] = [i]


        distances = []
        for sequence, indices in sequence_map.items():
            if len(indices) > 1:
                for i in range(1, len(indices)):
                    distances.append(indices[i] - indices[i-1])

        all_distances.extend(distances)


    if not all_distances:
        return [5,6]


    all_factors = []
    for d in all_distances:
        all_factors.extend(get_factors(d))

    factor_counts = Counter(f for f in all_factors if f > 1 and f <= keyrange)

    if not factor_counts:
        return [5,6]

    candidates = factor_counts.most_common(10)


    best_score = -1
    best_factor = candidates[0][0]
    
    for factor, frequency in candidates:
        current_score = frequency * factor 
        
        if current_score > best_score:
            best_score = current_score
            best_factor = factor
            
    a = candidates[0][0]
    b = best_factor

    
    return [a, b]

def keylength(ctext,keyrange=40):

    klgs = kasiski_examination(ctext,keyrange)
    return klgs

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
        key_char_index = Counter(contrast(counts,ln)).most_common(1)[0][0]
        kg += (abc[key_char_index])

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



""".replace("\n","").replace(" ","")
kl =  len(key)
if kl > keyrange:
    kl = keyrange
if "-" in key:
    key = "".join(random.choices(string.ascii_lowercase,k=kl))
test_bool = False

if test_bool or not key:
    test(m,keyrange)
else:
    ctext = vig(ptext,key)
    klgs = keylength(ctext,keyrange) 
    kl = len(key)

    klg = klgs[1] 
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

print ()
print ("[KASISKI EXAMINATION]")
print ()