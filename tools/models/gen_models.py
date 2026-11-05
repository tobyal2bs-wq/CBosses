"""Builds models.json from the boss modules: the 25 general bosses, the seasonal ones, the chapter bosses and
the legends. Every model gets its elbows and hit zones, its small pieces are tagged so low detail can drop
them, and its own opening and death from v2_recipes. Checks that every step points at real blocks and
real animations, so a typo shows up here and not on a server."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import anims, models, palette, roster

SELECTORS = {"", "all", "lit", "unlit", "detail", "trim", "vein", "plain"}


def tag(m):
    """Small pieces get a tag: "detail" for the tiniest (dropped first), "trim" for small thin plates."""
    for c in m.cubes:
        if c.get("g") or c.get("l"):
            continue
        w, h, d = (b - a for a, b in zip(c["f"], c["t"]))
        big, small, vol = max(w, h, d), min(w, h, d), w * h * d
        if big <= 1.6:
            c["g"] = "detail"
        elif vol <= 4 and small <= 0.6:
            c["g"] = "trim"
    # every model must lose something on low detail: tag its smallest untagged tenth
    if not any(c.get("g") in ("detail", "trim") for c in m.cubes):
        vol = lambda c: (c["t"][0] - c["f"][0]) * (c["t"][1] - c["f"][1]) * (c["t"][2] - c["f"][2])
        free = sorted((c for c in m.cubes if not c.get("g") and not c.get("l")), key=vol)
        for c in free[:max(1, len(free) // 10)]:
            c["g"] = "detail"


ABILITIES = ["lightning", "shockwave", "minions", "fire_ring", "pull", "leap", "poison", "blink", "frost", "volley", "darkness", "levitate",
             "heal", "quake", "detonate", "roar", "charge", "slam", "meteor", "sonic_boom", "skulls", "breath", "spikes", "orbs", "gifts",
             "sprinkles", "dive", "eggs"]
# a model names its attacks in its own words (hatchets, coal, hymn); each becomes the first fight ability it fits that the
# model does not already use, so every ability the boss casts plays its own move
ALIAS = {"vex": ["minions"], "beam": ["sonic_boom", "orbs"], "fangs": ["spikes"], "souls": ["skulls", "orbs"], "shards": ["volley", "spikes"],
         "shield": ["heal", "charge"], "vines": ["pull", "spikes"], "web": ["pull"], "venom": ["poison"], "wave": ["shockwave"],
         "curse": ["darkness"], "sand": ["spikes", "poison"], "chains": ["pull", "slam"], "fire": ["fire_ring", "breath"], "cannon": ["meteor"],
         "steam": ["darkness", "poison"], "coal": ["meteor", "volley"], "hook": ["pull", "charge"], "snowballs": ["volley"], "slide": ["charge"],
         "blizzard": ["frost", "levitate", "volley"], "freeze": ["frost", "levitate"], "spoon": ["slam"], "carrot": ["charge"], "peck": ["charge"], "caramel": ["orbs"],
         "seeds": ["volley"], "fork": ["charge"], "heads": ["meteor"], "hex": ["darkness"], "potions": ["orbs", "poison"],
         "hatchets": ["volley", "slam", "charge"], "coins": ["volley"], "bite": ["slam", "charge"], "flail": ["slam"], "roots": ["spikes"],
         "thorns": ["volley", "spikes"], "anchor": ["slam"], "hymn": ["darkness", "orbs"], "bell": ["shockwave", "slam"], "sonic": ["sonic_boom"],
         "claws": ["charge", "slam"], "blast": ["shockwave", "orbs"], "gust": ["shockwave", "levitate"], "charges": ["orbs"], "dash": ["charge"],
         "smash": ["slam"], "blade": ["charge"], "orb": ["orbs"], "crown": ["meteor"], "toss": ["slam", "shockwave"], "pounce": ["leap"],
         "sword": ["charge"], "spin": ["blink", "shockwave"], "sweep": ["shockwave", "slam"], "sting": ["poison", "charge"],
         "stomp": ["quake", "shockwave"], "spells": ["orbs", "darkness"], "summon": ["minions"], "magic": ["orbs", "levitate"], "bolt": ["lightning"], "shards2": ["volley"]}


def fight_attacks(m):
    out = {}
    for k, a in m.attacks.items():
        if k in ABILITIES and k not in out:
            out[k] = a
    for k, a in m.attacks.items():
        if k in ABILITIES:
            continue
        for t in ALIAS.get(k, []):
            if t not in out:
                out[t] = a
                break
        else:
            raise SystemExit(f"{m.id}: attack {k} has no fight ability to stand for")
    return out


def base(k):
    return k.split("[")[0]


def check(m, j, steps, what):
    rig = dict(anims.RIGS[m.rig], **(getattr(m, "anims", None) or {}))
    bones = [b["name"] for b in m.bones]
    blocks = {base(c["k"]) for c in m.cubes}
    problems = []
    for s in steps:
        only = s.get("only", "")
        sel = only[1:] if only.startswith("!") else only
        if sel not in SELECTORS and sel not in blocks and not any(b.startswith(sel) for b in bones):
            problems.append(f"{what} {s['op']}@{s['at']}: only={only} matches nothing")
        if s["op"] == "anim" and s.get("name") not in rig:
            problems.append(f"{what} anim {s.get('name')} is not in the {m.rig} rig")
    return problems


out = {"version": 2, "rigs": anims.RIGS, "models": {}}
used, problems = set(), []
SPAWN, DEATH = roster.recipes()
for id, fn in roster.builders().items():
    m = fn()
    if m.rig in ("biped", "float") and not getattr(m, "no_elbows", False):
        m.elbows(bend=getattr(m, "bend", -38), weapons=getattr(m, "hold", None))
    if m.rig in ("biped", "quad"): m.knees()
    m.zones()
    tag(m)
    m.attacks = fight_attacks(m)
    j = m.json()
    if m.id not in SPAWN or m.id not in DEATH:
        problems.append(f"{m.id}: no opening or death written")
        continue
    spawn = list(SPAWN[m.id])
    end = max(st["at"] + st.get("dur", 0) for st in spawn)
    spawn.append({"op": "pose", "at": end + 2, "dur": 4})   # whatever the opening did, it ends in the model's own shape
    j["spawn"], j["death"] = spawn, DEATH[m.id]
    problems += [f"{m.id}: {p}" for p in check(m, j, j["spawn"], "spawn") + check(m, j, j["death"], "death")]
    if not any(s["op"] == "flash" for s in j["death"]):
        problems.append(f"{m.id}: death has no flash")
    for a in set(m.attacks.values()) | ({m.melee} if m.melee else set()):
        if a not in anims.RIGS[m.rig] and a not in (getattr(m, "anims", None) or {}):
            problems.append(f"{m.id}: attack anim {a} not in {m.rig}")
    out["models"][m.id] = j
    used |= {base(c["k"]) for c in m.cubes}

missing = sorted(b for b in used if b not in palette.P)
if missing: print("no preview colour for", missing)
if problems:
    print("\n".join(problems))
    sys.exit(1)
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "../../src/main/resources/models.json")
json.dump(out, open(dest, "w"), separators=(",", ":"))
for id, m in out["models"].items():
    tags = sum(1 for c in m["cubes"] if c.get("g"))
    print(f"{id:20s} {len(m['cubes']):3d} cubes ({tags} small)  {m['height'] * m['scale'] / 16:.1f} blocks tall  {m['rig']}")
print(len(out["models"]), "models")
pv = {"rigs": anims.RIGS, "models": out["models"], "palette": {k: list(v) for k, v in palette.P.items()}}
pd = os.environ.get("PREVIEW_DATA", os.path.join(os.path.dirname(__file__), "../../build/preview-data.js"))
os.makedirs(os.path.dirname(pd), exist_ok=True)
open(pd, "w").write("const DATA=" + json.dumps(pv, separators=(",", ":")) + ";")
