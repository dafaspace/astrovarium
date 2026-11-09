"""What the tz database knows that Intl does not: when local mean time ended,
and the history before 1970 that the browsers' copy of the database has lost.

    python3 -I tools-tz-history.py <zic build with backzone>   # prints the block for index.html

Build the directory from IANA's tzdata (data.iana.org/time-zones/releases):
the main files plus backzone, with every Link that backzone defines as a Zone
dropped, compiled by zic -d <dir>. Without an argument the system's zoneinfo
is read, which gives TZ_LMT_END only and no TZ_BACK.

Intl reports an offset to the second but never says what kind of time it was,
and the old rule in placeOffset guessed it from the number: anything off the
quarter hour was local mean time, so the birthplace's own longitude was used.
That threw away every legal time the world kept off the quarter hour - Paris
Mean Time for all of France 1891-1911, Dublin Mean Time, Singapore's +07:20,
Liberia's -00:44:30 until 1972, Newfoundland, Dublin's own summer time - and
put the LMT of Marseille where the law said Paris.

The compiled zone files do say what kind of time it was: every period carries
an abbreviation, and local mean time is written LMT. So this reads the TZif
files (version 2 body, 64-bit times) and writes, per zone of the atlas, the
UTC second its first non-LMT period began. Before it, a birth was on the
birthplace's own mean time; from it on, the database's offset is the law.

The second table is for zones that became links in 2022 (Reykjavik,
Amsterdam, Oslo, much of Africa): ICU in every browser and Apple's own data are
built without backzone, so before 1970 they answer with another zone's history
- Reykjavik 1960 as UTC instead of UTC-1, Amsterdam 1920 as Brussels. For every
atlas zone whose transitions before 1970 differ between the backzone build and
the system's, TZ_BACK carries them: UTC second, offset in seconds, and whether
it was LMT, all base 36. From 1970 on the two agree and Intl is used.
"""
import os, struct, sys

SYS = '/usr/share/zoneinfo'
ZDIR = sys.argv[1] if len(sys.argv) > 1 else SYS
HERE = os.path.dirname(os.path.abspath(__file__))
zones = open(os.path.join(HERE, 'cities.txt'), encoding='utf-8').readline().strip().split(',')

def periods(z, d=None):
    b = open(os.path.join(d or ZDIR, z), 'rb').read()
    def counts(o):
        return struct.unpack('>6l', b[o + 20:o + 44])
    isut, isstd, leap, n, typecnt, charcnt = counts(0)
    o = 44 + n * 5 + typecnt * 6 + charcnt + leap * 8 + isstd + isut
    isut, isstd, leap, n, typecnt, charcnt = counts(o)
    o += 44
    times = struct.unpack('>%dq' % n, b[o:o + 8 * n]); o += 8 * n
    idx = b[o:o + n]; o += n
    types = [struct.unpack('>lBB', b[o + 6 * i:o + 6 * i + 6]) for i in range(typecnt)]; o += 6 * typecnt
    chars = b[o:o + charcnt]
    abbr = lambda i: chars[i:chars.index(b'\0', i)].decode()
    return [(None, types[0][0], abbr(types[0][2]))] + \
           [(times[i], types[idx[i]][0], abbr(types[idx[i]][2])) for i in range(n)]

out = []
for z in zones:
    p = periods(z)
    if p[0][2] != 'LMT':
        continue                      # no LMT at all (UTC-like zones): nothing to say
    end = next((t for t, off, a in p if a != 'LMT'), None)
    if end is not None:
        out.append(f'{z}:{end}')
version = open(os.path.join(ZDIR, '+VERSION')).read().strip() if os.path.exists(os.path.join(ZDIR, '+VERSION')) else '?'
print(f"/* tz {version}{' with backzone' if ZDIR != SYS else ', system zoneinfo'}, by tools-tz-history.py: zone:UTC second its LMT ended. */")
def b36(n):
    n = int(n); neg = n < 0; n = abs(n); d = ''
    while True:
        d = '0123456789abcdefghijklmnopqrstuvwxyz'[n % 36] + d; n //= 36
        if not n: break
    return ('-' if neg else '') + d
back = []
if ZDIR != SYS:
    for z in zones:
        a = [q for q in periods(z) if q[0] is None or q[0] < 0]
        s_ = [q for q in periods(z, SYS) if q[0] is None or q[0] < 0]
        if [(t, o) for t, o, _ in a] != [(t, o) for t, o, _ in s_]:
            back.append(z + '|' + '|'.join(f"{'' if t is None else b36(t)},{b36(o)}{',L' if ab == 'LMT' else ''}" for t, o, ab in a))
print("const TZ_LMT_END=Object.fromEntries('" + ','.join(out) + "'.split(',').map(s=>{const i=s.lastIndexOf(':');return [s.slice(0,i),+s.slice(i+1)];}));")
print("/* Zone|UTC second,offset seconds[,L for LMT]|... before 1970, base 36; the first period has no start. */")
print("const TZ_BACK=Object.fromEntries(" + repr(';'.join(back)) + ".split(';').filter(Boolean).map(r=>{const [z,...p]=r.split('|');"
      "return [z,p.map(x=>{const [t,o,l]=x.split(',');return [t===''?-Infinity:parseInt(t,36),parseInt(o,36),l==='L'];})];}));")
