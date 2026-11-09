"""When each atlas zone stopped keeping local mean time, from the tz database.

    python3 -I tools-tz-history.py [zoneinfo dir]   # prints the TZ_LMT_END block for index.html

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

The directory defaults to the system's /usr/share/zoneinfo. That build has no
backzone, so zones that became links in 2022 (Reykjavik, Amsterdam, Oslo, much
of Africa) carry another zone's history before 1970; pass a zic build made
with backzone to fix that, and the same table then covers them too.
"""
import os, struct, sys

ZDIR = sys.argv[1] if len(sys.argv) > 1 else '/usr/share/zoneinfo'
HERE = os.path.dirname(os.path.abspath(__file__))
zones = open(os.path.join(HERE, 'cities.txt'), encoding='utf-8').readline().strip().split(',')

def periods(z):
    b = open(os.path.join(ZDIR, z), 'rb').read()
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
print(f"/* tz {version}, {ZDIR}, by tools-tz-history.py: zone:UTC second its LMT ended. */")
print("const TZ_LMT_END=Object.fromEntries('" + ','.join(out) + "'.split(',').map(s=>{const i=s.lastIndexOf(':');return [s.slice(0,i),+s.slice(i+1)];}));")
