#!/usr/bin/python3
import r2pipe
import re

prg = re.compile(r'^(\d\.\d+).*  (\S*)$')
stats = {
    "total": 0,
    "zb useless": 0,
    "perfect fp" : 0,
    "perfect with fp" : 0,
    "zb best" : 0,
    "in top 5" : 0,
    "in top 10": 0,
    "in top 10" : 0,
    "in top 15" : 0,
    "in top 20" : 0,
}

def parsezb(zb):
    global prg
    ret = []
    for line in zb.split("\n"):
        k = prg.search(line)
        if not k: continue
        ret.append(k.groups())
    return ret

def dostats(zb, name):
    global stats
    info = parsezb(zb)
    if not info: return

    fpflag = False
    perfmatch = False
    stats["total"] += 1
    for i,d in enumerate(info):
        score = float(d[0])
        n = d[1]
        ### assums name only shows up once
        if name == n:
            if score == 1.0:
                stats["zb useless"] += 1
                perfmatch = True
                print("perfect match %s" % name)
            if i == 0:
                stats["zb best"] += 1
                print("top match %s" % name)
            if i < 5: stats["in top 5"] += 1
            if i < 10: stats["in top 10"] += 1
            if i < 15: stats["in top 15"] += 1
            stats["in top 20"] += 1
        else:
            if score == 1.0 and not fpflag:
                stats["perfect fp"] += 1
                fpflag = True
    if perfmatch and fpflag:
        stats["perfect with fp"] += 1

r = r2pipe.open("./static")
r.cmd("zo ./libc.sdb")
r.cmd("aa")
# r.cmd("e zign.graph = false")
funcs = r.cmdj("aflj")

print("Version: %s" % r.cmd("?V"))

count = 0
for i in funcs:
    if i["size"] <= 16:
        continue
    if i["name"].find("sym.") != 0:
        continue
    print(i["name"])
    r.cmd("s 0x%x" % i["offset"])
    zb = r.cmd("zb 20")
    dostats(zb, i["name"])
    print(zb)
    print("\n+++++++++++++++++++++++++++++++++++++++++++")
    count += 1

for i in stats:
    print("%s : %d" % (i, stats[i]))

total = stats["total"]
print("+++++++++++++++++ percents +++++++++++++++++++++++++")
print("%2.2f%% chance signature would be found without zb" %        ((stats["zb useless"]/total)*100))
print("%2.2f%% chance correct signature is number 1 result of zb" % ((stats["zb best"]/total)*100))
print("%2.2f%% chance correct signature is in top 5 results" %      ((stats["in top 5"]/total)*100))
print("%2.2f%% chance correct signature is in top 10 results" %     ((stats["in top 10"]/total)*100))
print("%2.2f%% chance correct signature is in top 15 results" %     ((stats["in top 15"]/total)*100))
print("%2.2f%% chance correct signature is in top 20 results" %     ((stats["in top 20"]/total)*100))
