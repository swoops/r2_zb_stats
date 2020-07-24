#!/usr/bin/python3
import r2pipe
import re

prg = re.compile(r'^(\d\.\d+).*  (\S*)$')
stats = {
    "total": 0,
    "zb useless": 0,
    "total not perfect": 0,
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

    fpflag = False
    perfmatch = False
    stats["total"] += 1
    stats["total not perfect"] += 1 # assume, update later
    for i,d in enumerate(info):
        score = float(d[0])
        n = d[1]
        if name == n:
            if score == 1.0:
                stats["zb useless"] += 1
                stats["total not perfect"] -= 1
                perfmatch = True
            else:
                if i == 0: stats["zb best"] += 1
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
funcs = r.cmdj("aflj")

print("Version: %s" % r.cmd("?V"))

count = 0
for i in funcs:
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
