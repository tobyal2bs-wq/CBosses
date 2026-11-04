"""The craft pass: turns every boss from a set of clean boxes into a finished, hand-made looking model.
It runs on every model after the shapes, elbows and hands are made and adds, in this order:

  veins    glowing cracks running over the torso and limbs, in the boss's own glow block (tag "vein")
  trim     darker bands round the bottom of the big pieces, a jagged hem under the waist, rivets on
           metal plates (tag "trim")
  detail   small lighter and darker patches on the big faces so no surface is one flat colour, the
           blocky shading of hand-painted mob textures (tag "detail")

Every boss ends up with at least MIN blocks. The pieces sit a fraction of a pixel proud of the face
under them and are tagged, so the plugin can drop them on a slow server (effects.model-detail) and the
spawn and death steps can move them on their own (only: vein / trim / detail / plain)."""
import random, zlib
from palette import P, base

MIN = 130
SOFT_MAX = 230
BIG = {"hollow_king": 260, "the_listener": 260, "withered_tyrant": 250, "ender_wyrm": 250, "the_unmaker": 260}

SKIP_PAT = {"glow", "glass", "face", "ice", "leaves", "ore"}
_cache = {}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(block, f):
    """The palette block closest to this block's colour times f (darker below 1, lighter above)."""
    key = (base(block), f)
    if key in _cache: return _cache[key]
    b = base(block)
    if b not in P:
        _cache[key] = block
        return block
    pat, main, _ = P[b]
    r, g, bl = _rgb(main)
    goal = tuple(max(0, min(255, v * f + (8 if f > 1 else 0))) for v in (r, g, bl))
    best, bd = b, 1e18
    for k, (kp, km, _) in P.items():
        if k == b or kp in SKIP_PAT or "glazed" in k or k in ("tnt", "target", "bookshelf", "note_block", "crafting_table",
                "barrel", "beacon", "respawn_anchor", "lever", "hopper", "cauldron", "chain", "iron_bars", "anvil", "cobweb",
                "lightning_rod", "chain_command_block", "dark_oak_trapdoor", "furnace", "blast_furnace", "sponge", "slime_block",
                "honey_block", "melon", "pumpkin", "hay_block", "bone_block", "cactus", "powder_snow", "white_concrete_powder"):
            continue
        cr, cg, cb = _rgb(km)
        d = (cr - goal[0]) ** 2 * 1.0 + (cg - goal[1]) ** 2 * 1.3 + (cb - goal[2]) ** 2 * 0.9
        # keep the same kind of surface where it can (wool stays soft, stone stays stone)
        if kp != pat: d *= 1.35
        if d < bd: best, bd = k, d
    _cache[key] = best
    return best


def _vol(c):
    return (c["t"][0] - c["f"][0]) * (c["t"][1] - c["f"][1]) * (c["t"][2] - c["f"][2])


def _inside(p, c, pad=0.0):
    return all(c["f"][i] - pad < p[i] < c["t"][i] + pad for i in range(3))


class Crafter:
    def __init__(self, m):
        self.m = m
        self.rnd = random.Random(zlib.crc32(m.id.encode()))
        self.parent = {b["name"]: b["parent"] for b in m.bones}
        self.solid = [c for c in m.cubes if "r" not in c and not self._shell(c["b"])]
        # faces already used, per (cube id, face): rectangles in face coordinates
        self.used = {}

    def _shell(self, b):
        while b:
            if b.startswith("shell"): return True
            b = self.parent[b]
        return False

    def chain(self, b):
        out = []
        while b: out.append(b); b = self.parent[b]
        return out

    def is_head(self, c):
        return any(n in ("head", "jaw") or n.startswith("skull") for n in self.chain(c["b"]))

    def add(self, bone, block, f, t, tag, light=False):
        self.m.box(bone, block, f, t, light=light)
        self.m.cubes[-1]["g"] = tag

    def covered(self, point, me):
        """Is a point just outside a face buried in another piece of the same model."""
        for c in self.m.cubes:
            if c is me or "r" in c: continue
            if _inside(point, c): return True
        return False

    # faces: (axis, sign) -> the two in-face axes
    FACES = [(2, 1), (0, 1), (0, -1), (1, 1), (2, -1)]

    def face_rect(self, c, axis, sign):
        a, b = [i for i in range(3) if i != axis]
        return a, b, (c["f"][a], c["t"][a]), (c["f"][b], c["t"][b]), (c["t"][axis] if sign > 0 else c["f"][axis])

    def plate(self, c, axis, sign, u0, u1, v0, v1, block, tag, proud=0.14, light=False, depth=0.06):
        """A thin piece lying on one face of cube c, from u0..u1, v0..v1 in that face."""
        a, b, _, _, plane = self.face_rect(c, axis, sign)
        f, t = [0, 0, 0], [0, 0, 0]
        f[a], t[a] = u0, u1
        f[b], t[b] = v0, v1
        if sign > 0: f[axis], t[axis] = plane - depth, plane + proud
        else: f[axis], t[axis] = plane - proud, plane + depth
        mid = [(f[i] + t[i]) / 2 for i in range(3)]
        out = list(mid); out[axis] = plane + sign * (proud + 0.3)
        if self.covered(out, c): return False
        self.add(c["b"], block, f, t, tag, light)
        return True

    def free(self, key, rect):
        u0, u1, v0, v1 = rect
        for (a0, a1, b0, b1) in self.used.get(key, []):
            if u0 < a1 and a0 < u1 and v0 < b1 and b0 < v1: return False
        self.used.setdefault(key, []).append(rect)
        return True

    # ------------------------------------------------------------------ veins

    def glow_block(self):
        lit = [c["k"] for c in self.m.cubes if c.get("l") and base(c["k"]) not in ("end_rod", "lantern", "soul_lantern", "beacon")]
        if not lit: return None
        counts = {}
        for k in lit: counts[k] = counts.get(k, 0) + 1
        return max(counts, key=counts.get)

    def veins(self, glow, budget):
        if not glow or budget <= 0: return 0
        cands = [c for c in self.solid if not c.get("l") and not self.is_head(c) and c.get("g") is None
                 and min(c["t"][0] - c["f"][0], c["t"][1] - c["f"][1]) >= 3.5]
        cands.sort(key=_vol, reverse=True)
        made = 0
        for c in cands[:7]:
            for axis, sign in ((2, 1), (0, 1 if c["f"][0] + c["t"][0] >= 0 else -1)):
                if made >= budget: return made
                made += self.crack(c, axis, sign, glow, min(5, budget - made))
        return made

    def crack(self, c, axis, sign, glow, most):
        a, b, (ua, ub), (va, vb), _ = self.face_rect(c, axis, sign)
        w, h = ub - ua, vb - va
        if w < 2.5 or h < 3: return 0
        th = max(0.45, min(0.8, min(w, h) * 0.09))
        u = ua + w * self.rnd.uniform(0.25, 0.75)
        v = vb - h * self.rnd.uniform(0.05, 0.2)
        made = 0
        down = True
        for _ in range(most):
            if down:
                L = h * self.rnd.uniform(0.18, 0.34)
                v1 = max(va + th, v - L)
                if v - v1 < th: break
                if self.plate(c, axis, sign, u - th / 2, u + th / 2, v1, v, glow, "vein", proud=0.22, light=True): made += 1
                v = v1
            else:
                L = w * self.rnd.uniform(0.15, 0.3) * self.rnd.choice((-1, 1))
                u1 = max(ua + th, min(ub - th, u + L))
                if abs(u1 - u) < th: down = not down; continue
                lo, hi = sorted((u, u1))
                if self.plate(c, axis, sign, lo - th / 2, hi + th / 2, v - th / 2, v + th / 2, glow, "vein", proud=0.22, light=True): made += 1
                u = u1
            down = not down
        return made

    # ------------------------------------------------------------------ trim

    def bands(self, budget):
        made = 0
        groups = {}
        for c in self.solid:
            if c.get("l") or c.get("g"): continue
            if c["t"][1] - c["f"][1] < 4 or min(c["t"][0] - c["f"][0], c["t"][2] - c["f"][2]) < 2.5: continue
            groups.setdefault(c["b"], []).append(c)
        order = sorted(groups.values(), key=lambda cs: -max(_vol(c) for c in cs))
        for cs in order:
            if made >= budget: break
            c = max(cs, key=_vol)
            h = c["t"][1] - c["f"][1]
            dark = shade(c["k"], 0.72)
            if dark == base(c["k"]): continue
            bh = max(0.7, min(2.2, h * 0.16))
            self.add(c["b"], dark, (c["f"][0] - 0.18, c["f"][1], c["f"][2] - 0.18), (c["t"][0] + 0.18, c["f"][1] + bh, c["t"][2] + 0.18), "trim")
            made += 1
        return made

    def hem(self, budget):
        """A jagged hem hanging under the waist piece (the torn edge of a tunic, a skirt of plates)."""
        if self.m.rig not in ("biped", "float") or budget <= 0: return 0
        cands = [c for c in self.solid if c["b"] in ("hips", "body") and not c.get("l") and not c.get("g")
                 and c["t"][0] - c["f"][0] >= 6 and c["t"][2] - c["f"][2] >= 3]
        if not cands: return 0
        c = min(cands, key=lambda c: (c["f"][1], -_vol(c)))
        if c["f"][1] < 2: return 0
        block = shade(c["k"], 0.8)
        made = 0
        x0, x1, z0, z1, y = c["f"][0], c["t"][0], c["f"][2], c["t"][2], c["f"][1]
        n = max(3, min(7, int((x1 - x0) / 1.7)))
        tw = (x1 - x0) / n
        for k in range(n):
            if made >= budget: break
            L = self.rnd.choice((0.9, 1.6, 2.3, 1.2)) * min(1.6, (x1 - x0) / 9 + 0.6)
            self.add(c["b"], block, (x0 + k * tw + 0.12, y - L, z1 - 0.7), (x0 + (k + 1) * tw - 0.12, y + 0.3, z1 + 0.2), "trim")
            made += 1
        m = max(2, min(4, int((z1 - z0) / 2)))
        td = (z1 - z0) / m
        for sx, xe in ((1, x1), (-1, x0)):
            for k in range(m):
                if made >= budget: break
                L = self.rnd.choice((0.8, 1.5, 2.1)) * min(1.5, (x1 - x0) / 9 + 0.6)
                xa, xb = (xe - 0.6, xe + 0.2) if sx > 0 else (xe - 0.2, xe + 0.6)
                self.add(c["b"], block, (xa, y - L, z0 + k * td + 0.12), (xb, y + 0.3, z0 + (k + 1) * td - 0.12), "trim")
                made += 1
        return made

    METAL = ("iron_block", "gold_block", "netherite_block", "polished_deepslate", "copper", "polished_blackstone",
             "chiseled_", "cut_copper", "lodestone", "reinforced_deepslate", "polished_andesite", "smooth_stone")

    def rivets(self, budget):
        made = 0
        metal = [c for c in self.solid if not c.get("g") and any(base(c["k"]).startswith(x) or x in base(c["k"]) for x in self.METAL)]
        metal.sort(key=_vol, reverse=True)
        for c in metal:
            if made + 4 > budget: break
            a, b, (ua, ub), (va, vb), _ = self.face_rect(c, 2, 1)
            if ub - ua < 3 or vb - va < 3: continue
            stud = shade(c["k"], 1.35)
            s = max(0.5, min(0.9, (ub - ua) * 0.1))
            m = s * 0.7
            for u, v in ((ua + m, va + m), (ub - m - s, va + m), (ua + m, vb - m - s), (ub - m - s, vb - m - s)):
                if self.plate(c, 2, 1, u, u + s, v, v + s, stud, "trim", proud=0.32): made += 1
        return made

    # ------------------------------------------------------------------ armour and silhouette

    CUTE = {"clucksworth", "killer_bunny", "brain_freeze", "king_gloop", "great_gourd", "sunscorch", "frostbottom"}

    def main_block(self, bones):
        counts = {}
        for c in self.solid:
            if c["b"] in bones and not c.get("l") and not c.get("g"):
                counts[c["k"]] = counts.get(c["k"], 0) + _vol(c)
        return max(counts, key=counts.get) if counts else None

    def armour_block(self):
        counts = {}
        for c in self.solid:
            if c.get("l") or c.get("g"): continue
            if any(base(c["k"]).startswith(x) or x in base(c["k"]) for x in self.METAL):
                counts[c["k"]] = counts.get(c["k"], 0) + _vol(c)
        if counts: return max(counts, key=counts.get)
        body = self.main_block({"body", "hips", "core"})
        return shade(body, 0.6) if body else "polished_blackstone"

    def pauldrons(self, budget):
        """Layered shoulder plates: a big cap, a lip that steps out over the arm and a bright edge."""
        if self.m.rig not in ("biped",) or self.m.id in self.CUTE or budget < 6: return 0
        plate = self.armour_block()
        edge = shade(plate, 1.4)
        made = 0
        for side, sx in (("L", 1), ("R", -1)):
            arm = "arm" + side
            mine = [c for c in self.solid if c["b"] == arm and not c.get("g")]
            if not mine: continue
            top = max(mine, key=lambda c: c["t"][1])
            f, t = top["f"], top["t"]
            w, d = t[0] - f[0], t[2] - f[2]
            if w < 2: continue
            y = t[1]
            out_x = t[0] if sx > 0 else f[0]
            in_x = f[0] if sx > 0 else t[0]
            ox = lambda v: out_x + sx * v
            lo, hi = sorted((in_x - sx * 0.3, ox(1.1)))
            self.add(arm, plate, (lo, y - 1.6, f[2] - 0.8), (hi, y + 1.2, t[2] + 0.8), "trim"); made += 1
            lo, hi = sorted((in_x + sx * w * 0.25, ox(1.7)))
            self.add(arm, plate, (lo, y - 3.0, f[2] - 0.5), (hi, y - 1.4, t[2] + 0.5), "trim"); made += 1
            lo, hi = sorted((ox(1.1), ox(1.9)))
            self.add(arm, edge, (lo, y - 3.1, f[2] - 0.55), (hi, y - 2.4, t[2] + 0.55), "trim"); made += 1
            lo, hi = sorted((in_x - sx * 0.3, ox(1.1)))
            self.add(arm, edge, (lo, y + 1.1, f[2] - 0.9), (hi, y + 1.5, f[2] - 0.3), "trim"); made += 1
        return made

    def knees(self, budget):
        if self.m.rig != "biped" or self.m.id in self.CUTE or budget < 2: return 0
        plate = self.armour_block()
        made = 0
        for leg in ("legL", "legR"):
            mine = [c for c in self.solid if c["b"] == leg and not c.get("g")]
            if not mine: continue
            big = max(mine, key=_vol)
            f, t = big["f"], big["t"]
            h = t[1] - f[1]
            if h < 4: continue
            ky = f[1] + h * 0.55
            w = t[0] - f[0]
            self.add(leg, plate, (f[0] + w * 0.12, ky - 1.2, t[2] - 0.2), (t[0] - w * 0.12, ky + 1.2, t[2] + 0.7), "trim"); made += 1
        return made

    def spine(self, budget):
        """A ridge of spikes down the back of beasts: base plates with sharper tips on top."""
        if self.m.rig not in ("quad", "spider", "wyrm") or self.m.id in self.CUTE or budget < 6: return 0
        mine = [c for c in self.solid if c["b"] == "body" and not c.get("g") and not c.get("l")]
        if not mine: return 0
        top = max(mine, key=lambda c: (c["t"][1], _vol(c)))
        f, t = top["f"], top["t"]
        L = t[2] - f[2]
        if L < 6: return 0
        n = max(3, min(6, int(L / 3.2), budget // 2))
        tipb = "bone_block" if base(top["k"]) not in ("bone_block", "calcite", "quartz_block") else "polished_blackstone"
        baseb = shade(top["k"], 0.65)
        cx = (f[0] + t[0]) / 2
        made = 0
        for k in range(n):
            z = f[2] + L * (k + 0.7) / (n + 0.4)
            hgt = 1.6 + 1.4 * (1 - abs(k - (n - 1) * 0.45) / n)
            self.add("body", baseb, (cx - 1.1, t[1] - 0.3, z - 1.0), (cx + 1.1, t[1] + hgt * 0.55, z + 1.0), "trim")
            self.add("body", tipb, (cx - 0.55, t[1] + hgt * 0.5, z - 0.5), (cx + 0.55, t[1] + hgt * 1.15, z + 0.5), "trim")
            made += 2
        return made

    def emblem(self, budget):
        """A layered badge in the middle of the chest: dark plate, bright frame, glowing centre."""
        if self.m.rig not in ("biped", "float") or self.m.id in self.CUTE or budget < 3: return 0
        bones = ("body", "core")
        mine = [c for c in self.solid if c["b"] in bones and not c.get("g")]
        if not mine: return 0
        big = max(mine, key=_vol)
        f, t = big["f"], big["t"]
        w, h = t[0] - f[0], t[1] - f[1]
        if w < 6 or h < 5: return 0
        cx, cy, z = (f[0] + t[0]) / 2, f[1] + h * 0.62, t[2]
        s = min(w, h) * 0.26
        probe = (cx, cy, z + 1.2)
        for c in self.m.cubes:
            if c is not big and "r" not in c and _inside((cx, cy, z + 0.4), c): return 0
        plate = self.armour_block()
        glow = self.glow_block()
        self.add(big["b"], shade(plate, 0.7), (cx - s, cy - s, z - 0.1), (cx + s, cy + s, z + 0.35), "trim")
        self.add(big["b"], shade(plate, 1.45), (cx - s * 0.7, cy - s * 0.7, z + 0.3), (cx + s * 0.7, cy + s * 0.7, z + 0.55), "trim")
        made = 2
        if glow:
            self.add(big["b"], glow, (cx - s * 0.38, cy - s * 0.38, z + 0.5), (cx + s * 0.38, cy + s * 0.38, z + 0.8), "vein", light=True)
            made += 1
        return made

    # ------------------------------------------------------------------ surface patches

    def patches(self, budget):
        made = 0
        faces = []
        for c in self.solid:
            if c.get("l") or c.get("g"): continue
            for axis, sign in self.FACES:
                a, b, (ua, ub), (va, vb), _ = self.face_rect(c, axis, sign)
                area = (ub - ua) * (vb - va)
                if ub - ua >= 1.7 and vb - va >= 1.7: faces.append((area, id(c), c, axis, sign))
        faces.sort(key=lambda x: -x[0])
        rounds = 0
        while made < budget and faces and rounds < 10:
            rounds += 1
            for area, _, c, axis, sign in faces:
                if made >= budget: break
                # bigger faces get more patches
                if rounds > 1 and area < 22 * rounds: continue
                a, b, (ua, ub), (va, vb), _ = self.face_rect(c, axis, sign)
                w, h = ub - ua, vb - va
                for _ in range(6):
                    pw = max(0.8, w * self.rnd.uniform(0.18, 0.42))
                    ph = max(0.8, h * self.rnd.uniform(0.12, 0.3))
                    if axis == 1: ph = max(0.8, h * self.rnd.uniform(0.18, 0.42))
                    u0 = self.rnd.uniform(ua + 0.15, max(ua + 0.15, ub - pw - 0.15))
                    v0 = self.rnd.uniform(va + 0.15, max(va + 0.15, vb - ph - 0.15))
                    rect = (u0, u0 + pw, v0, v0 + ph)
                    if not self.free((id(c), axis, sign), rect): continue
                    # light on top, dark low down and on the back, mixed elsewhere
                    rel = (v0 + ph / 2 - va) / max(1e-3, h) if axis != 1 else 0.8
                    f = 1.32 if (axis == 1 and sign > 0) else 0.68 if (rel < 0.35 or (axis == 2 and sign < 0)) else self.rnd.choice((0.72, 1.3))
                    blk = shade(c["k"], f)
                    if blk == base(c["k"]): break
                    if self.plate(c, axis, sign, *rect, blk, "detail", proud=0.1): made += 1
                    break
        return made


def craft(m):
    cr = Crafter(m)
    n0 = len(m.cubes)
    cap = BIG.get(m.id, SOFT_MAX)
    target = max(MIN, min(cap, int(n0 * 1.7)))
    room = lambda: target - len(m.cubes)
    glow = cr.glow_block()
    cr.veins(glow, min(28, max(0, room())))
    cr.pauldrons(min(8, max(0, room())))
    cr.knees(min(2, max(0, room())))
    cr.spine(min(12, max(0, room())))
    cr.emblem(min(3, max(0, room())))
    cr.bands(min(10, max(0, room())))
    cr.hem(min(16, max(0, room())))
    cr.rivets(min(24, max(0, room())))
    cr.patches(max(0, room()))
    m.crafted = len(m.cubes) - n0
    return m.crafted
