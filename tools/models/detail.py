"""A finishing pass that adds small craft details to the humanoid ("people") bosses: boot soles and toe caps,
a belt with a buckle, and bands on the forearms. Runs after the elbows and hands are made."""

PEOPLE = {
    # id: (sole block, belt block, buckle block, band block)
    "gravelord": ("polished_blackstone", None, None, "gold_block"),
    "frost_jarl": ("spruce_planks", "brown_terracotta", "iron_block", "iron_block"),
    "warlord_gruk": ("polished_blackstone", None, None, "gold_block"),
    "tide_tyrant": ("dark_prismarine", "prismarine_bricks", "gold_block", "gold_block"),
    "storm_herald": ("polished_deepslate", "blue_terracotta", "gold_block", "gold_block"),
    "executioner": ("black_terracotta", None, None, "iron_block"),
    "pharaoh": ("cut_sandstone", None, None, "gold_block"),
    "hexmother": ("black_terracotta", None, None, "gold_block"),
    "old_man_winter": ("spruce_planks", None, None, "light_blue_concrete"),
}

def _box(c):
    return c["f"], c["t"]

def enrich(m):
    spec = PEOPLE.get(m.id)
    if not spec or m.rig != "biped": return
    sole, strap, buckle, band = spec
    added = 0
    # soles: under the lowest piece of each leg, if it reaches the ground and is not rotated
    for leg in ("legL", "legR"):
        mine = [c for c in m.cubes if c["b"] == leg and "r" not in c]
        if not mine: continue
        low = min(mine, key=lambda c: c["f"][1])
        f, t = _box(low)
        if f[1] > 1.2 or t[0] - f[0] < 2: continue
        m.box(leg, sole, (f[0] - 0.25, 0, f[2] - 0.3), (t[0] + 0.25, 0.55, t[2] + 0.5))
        m.box(leg, sole, (f[0] + 0.2, 0.5, t[2] - 0.2), (t[0] - 0.2, 1.4, t[2] + 0.5))
        added += 2
    # a belt around the waist, when the body has a clear waist and there is no belt yet
    hips = next(b for b in m.bones if b["name"] == "hips")["pivot"][1]
    if strap:
        y = hips + 2
        around = [c for c in m.cubes if c["b"] in ("body", "hips") and "r" not in c and c["f"][1] <= y <= c["t"][1]]
        if around:
            x0 = min(c["f"][0] for c in around); x1 = max(c["t"][0] for c in around)
            z0 = min(c["f"][2] for c in around); z1 = max(c["t"][2] for c in around)
            m.box("body", strap, (x0 - 0.3, y - 0.8, z0 - 0.3), (x1 + 0.3, y + 0.8, z1 + 0.3))
            m.c("body", buckle, ((x0 + x1) / 2, y, z1 + 0.45), (2.6, 2.2, 0.4))
            m.c("body", strap, ((x0 + x1) / 2, y, z1 + 0.7), (1.2, 1.0, 0.2))
            added += 3
    # a band at the top of each forearm
    if band:
        for fore in ("foreL", "foreR"):
            mine = [c for c in m.cubes if c["b"] == fore and "r" not in c]
            if len(mine) < 2: continue
            top = max(mine, key=lambda c: c["t"][1])
            f, t = _box(top)
            if t[0] - f[0] < 1.6: continue
            m.box(fore, band, (f[0] - 0.25, t[1] - 1.0, f[2] - 0.25), (t[0] + 0.25, t[1] - 0.2, t[2] + 0.25))
            added += 1
    m.detail_added = added
