"""CBosses' own legends: a Wither-like tyrant with three skulls, an Ender-Dragon-like wyrm that really
flies, Killer Claus for winter and the Brain Freeze ice cream for summer. Two new rigs (wither, wyrm)."""
import copy, math
from models import *
from seasonal import blob, ring
import anims
from anims import K, Z

# ================================================================================================ RIGS

WITHER = copy.deepcopy(anims.FLOAT)
WITHER["idle"]["bones"].update({
    "skullL": {"rot": K((0, (0, 10, 0)), (1.0, (-8, -6, 6)), (2.0, (4, 14, -4)), (3.0, (0, 10, 0)))},
    "skullR": {"rot": K((0, (0, -10, 0)), (1.3, (6, 8, -6)), (2.2, (-6, -14, 4)), (3.0, (0, -10, 0)))},
    "tail": {"rot": K((0, (10, 0, 0)), (1.5, (22, 0, 8)), (3.0, (10, 0, 0)))},
    "tail2": {"rot": K((0, (8, 0, 0)), (1.5, (18, 0, -10)), (3.0, (8, 0, 0)))},
})
WITHER["walk"]["bones"].update({"tail": {"rot": K((0, (30, 0, 0)), (1.5, (36, 0, 0)), (3.0, (30, 0, 0)))}})
# all three skulls snap forward one after another (the skull volley)
WITHER["volley"] = {"length": 1.2, "hit": 0.7, "bones": {
    "head": {"rot": K((0, Z), (0.3, (-25, 0, 0)), (0.45, (20, 0, 0)), (1.2, Z))},
    "skullL": {"rot": K((0, Z), (0.45, (-25, 0, 0)), (0.6, (20, 0, 0)), (1.2, Z))},
    "skullR": {"rot": K((0, Z), (0.6, (-25, 0, 0)), (0.75, (20, 0, 0)), (1.2, Z))},
    "core": {"rot": K((0, Z), (0.3, (-10, 0, 0)), (0.75, (12, 0, 0)), (1.2, Z))},
}}
# rears back and every skull screams at once
WITHER["scream"] = {"length": 1.6, "hit": 0.9, "bones": {
    "core": {"rot": K((0, Z), (0.6, (-30, 0, 0)), (0.9, (15, 0, 0)), (1.3, (12, 0, 0)), (1.6, Z)), "pos": K((0, Z), (0.6, (0, 6, 0)), (1.6, Z))},
    "head": {"rot": K((0, Z), (0.6, (-30, 0, 0)), (0.9, (10, 0, 0)), (1.6, Z))},
    "jaw": {"rot": K((0, Z), (0.6, (10, 0, 0)), (0.9, (40, 0, 0)), (1.3, (38, 0, 0)), (1.6, Z))},
    "skullL": {"rot": K((0, Z), (0.6, (-20, 30, 0)), (0.9, (10, -10, 0)), (1.6, Z))},
    "skullR": {"rot": K((0, Z), (0.6, (-20, -30, 0)), (0.9, (10, 10, 0)), (1.6, Z))},
    "tail": {"rot": K((0, Z), (0.6, (60, 0, 0)), (1.6, Z))},
}}
WITHER["hurt"] = copy.deepcopy(anims.FLOAT["hurt"])
WITHER["die_drop"] = copy.deepcopy(anims.FLOAT["die_drop"])
WITHER["die_drop"]["bones"].update({"skullL": {"rot": K((0, Z), (1.0, (50, 30, 20)))}, "skullR": {"rot": K((0, Z), (1.0, (50, -30, -20)))}})

# A dragon. Wings flap on z (+z lifts the left wing, -z the right), the neck and tail are chains.
WYRM = {
    "idle": {"length": 2.8, "loop": True, "bones": {
        "body": {"pos": K((0, Z), (1.4, (0, 1.2, 0)), (2.8, Z)), "rot": K((0, (-3, 0, 0)), (1.4, (2, 0, 0)), (2.8, (-3, 0, 0)))},
        "neck": {"rot": K((0, (-6, 0, 0)), (1.4, (4, 6, 0)), (2.8, (-6, 0, 0)))},
        "head": {"rot": K((0, (6, -8, 0)), (1.4, (-4, 8, 0)), (2.8, (6, -8, 0)))},
        "jaw": {"rot": K((0, Z), (1.4, (8, 0, 0)), (2.8, Z))},
        "wingL": {"rot": K((0, (0, 0, 8)), (1.4, (0, 0, 16)), (2.8, (0, 0, 8)))},
        "wingR": {"rot": K((0, (0, 0, -8)), (1.4, (0, 0, -16)), (2.8, (0, 0, -8)))},
        "tipL": {"rot": K((0, (0, 0, -30)), (1.4, (0, 0, -20)), (2.8, (0, 0, -30)))},
        "tipR": {"rot": K((0, (0, 0, 30)), (1.4, (0, 0, 20)), (2.8, (0, 0, 30)))},
        "tail": {"rot": K((0, (0, 10, 0)), (1.4, (0, -10, 0)), (2.8, (0, 10, 0)))},
        "tail2": {"rot": K((0, (0, 14, 0)), (1.4, (0, -14, 0)), (2.8, (0, 14, 0)))},
        "tail3": {"rot": K((0, (0, 18, 0)), (1.4, (0, -18, 0)), (2.8, (0, 18, 0)))},
    }},
    "fly": {"length": 1.3, "loop": True, "bones": {
        "body": {"pos": K((0, (0, 2, 0)), (0.35, (0, -2.5, 0)), (0.65, (0, -1, 0)), (1.0, (0, 3, 0)), (1.3, (0, 2, 0))),
                 "rot": K((0, (-4, 0, 0)), (0.65, (4, 0, 0)), (1.3, (-4, 0, 0)))},
        "wingL": {"rot": K((0, (0, 0, 42)), (0.45, (0, 8, -34)), (0.7, (0, 6, -30)), (1.3, (0, 0, 42)))},
        "wingR": {"rot": K((0, (0, 0, -42)), (0.45, (0, -8, 34)), (0.7, (0, -6, 30)), (1.3, (0, 0, -42)))},
        "tipL": {"rot": K((0, (0, 0, -12)), (0.45, (0, 0, -40)), (0.8, (0, 0, 10)), (1.3, (0, 0, -12)))},
        "tipR": {"rot": K((0, (0, 0, 12)), (0.45, (0, 0, 40)), (0.8, (0, 0, -10)), (1.3, (0, 0, 12)))},
        "legL": {"rot": K((0, (55, 0, 0)), (1.3, (55, 0, 0)))}, "legR": {"rot": K((0, (55, 0, 0)), (1.3, (55, 0, 0)))},
        "tail": {"rot": K((0, (-4, 0, 0)), (0.65, (6, 0, 0)), (1.3, (-4, 0, 0)))},
        "tail2": {"rot": K((0, (-6, 0, 0)), (0.65, (8, 0, 0)), (1.3, (-6, 0, 0)))},
        "tail3": {"rot": K((0, (-8, 0, 0)), (0.65, (10, 0, 0)), (1.3, (-8, 0, 0)))},
        "neck": {"rot": K((0, (4, 0, 0)), (0.65, (-4, 0, 0)), (1.3, (4, 0, 0)))},
    }},
    "walk": {"length": 1.3, "loop": True, "bones": {
        "wingL": {"rot": K((0, (0, 0, 30)), (0.65, (0, 0, -20)), (1.3, (0, 0, 30)))},
        "wingR": {"rot": K((0, (0, 0, -30)), (0.65, (0, 0, 20)), (1.3, (0, 0, -30)))},
        "legL": {"rot": K((0, (25, 0, 0)), (0.65, (-25, 0, 0)), (1.3, (25, 0, 0)))},
        "legR": {"rot": K((0, (-25, 0, 0)), (0.65, (25, 0, 0)), (1.3, (-25, 0, 0)))},
    }},
    "bite": {"length": 0.8, "hit": 0.4, "bones": {
        "neck": {"rot": K((0, Z), (0.25, (-30, 0, 0)), (0.4, (35, 0, 0)), (0.8, Z))},
        "head": {"rot": K((0, Z), (0.25, (-25, 0, 0)), (0.4, (20, 0, 0)), (0.8, Z))},
        "jaw": {"rot": K((0, Z), (0.25, (45, 0, 0)), (0.4, (0, 0, 0)), (0.8, Z))},
    }},
    # pulls the head back, the throat glows, then sweeps purple fire left to right
    "breath": {"length": 2.0, "hit": 0.9, "bones": {
        "neck": {"rot": K((0, Z), (0.6, (-40, 0, 0)), (0.9, (20, -30, 0)), (1.5, (20, 30, 0)), (2.0, Z))},
        "head": {"rot": K((0, Z), (0.6, (-20, 0, 0)), (0.9, (15, 0, 0)), (1.5, (15, 0, 0)), (2.0, Z))},
        "jaw": {"rot": K((0, Z), (0.6, (10, 0, 0)), (0.9, (50, 0, 0)), (1.5, (50, 0, 0)), (2.0, Z))},
        "body": {"rot": K((0, Z), (0.6, (-12, 0, 0)), (0.9, (6, 0, 0)), (2.0, Z))},
        "wingL": {"rot": K((0, Z), (0.6, (0, 0, 50)), (0.9, (0, 0, 10)), (2.0, Z))},
        "wingR": {"rot": K((0, Z), (0.6, (0, 0, -50)), (0.9, (0, 0, -10)), (2.0, Z))},
    }},
    # one huge wing beat that blows everyone back
    "gust": {"length": 1.4, "hit": 0.8, "bones": {
        "wingL": {"rot": K((0, Z), (0.6, (0, -20, 70)), (0.8, (0, 20, -45)), (1.0, (0, 10, -40)), (1.4, Z))},
        "wingR": {"rot": K((0, Z), (0.6, (0, 20, -70)), (0.8, (0, -20, 45)), (1.0, (0, -10, 40)), (1.4, Z))},
        "tipL": {"rot": K((0, Z), (0.6, (0, 0, 20)), (0.8, (0, 0, -50)), (1.4, Z))},
        "tipR": {"rot": K((0, Z), (0.6, (0, 0, -20)), (0.8, (0, 0, 50)), (1.4, Z))},
        "body": {"pos": K((0, Z), (0.6, (0, -3, 0)), (0.85, (0, 6, 0)), (1.4, Z)), "rot": K((0, Z), (0.6, (-20, 0, 0)), (0.85, (5, 0, 0)), (1.4, Z))},
    }},
    "dive": {"length": 1.2, "hit": 0.7, "bones": {
        "body": {"rot": K((0, Z), (0.4, (-20, 0, 0)), (0.7, (35, 0, 0)), (1.2, Z))},
        "wingL": {"rot": K((0, Z), (0.4, (0, -40, 30)), (0.7, (0, -60, 10)), (1.2, Z))},
        "wingR": {"rot": K((0, Z), (0.4, (0, 40, -30)), (0.7, (0, 60, -10)), (1.2, Z))},
        "jaw": {"rot": K((0, Z), (0.6, (40, 0, 0)), (1.2, Z))},
        "legL": {"rot": K((0, Z), (0.6, (-40, 0, 0)), (1.2, Z))}, "legR": {"rot": K((0, Z), (0.6, (-40, 0, 0)), (1.2, Z))},
    }},
    "roar": {"length": 1.8, "hit": 0.7, "bones": {
        "neck": {"rot": K((0, Z), (0.5, (-45, 0, 0)), (1.4, (-40, 0, 0)), (1.8, Z))},
        "head": {"rot": K((0, Z), (0.5, (-30, 0, 0)), (0.9, (-30, 10, 0)), (1.3, (-30, -10, 0)), (1.8, Z))},
        "jaw": {"rot": K((0, Z), (0.5, (55, 0, 0)), (1.4, (50, 0, 0)), (1.8, Z))},
        "wingL": {"rot": K((0, Z), (0.5, (0, 0, 60)), (1.4, (0, 0, 55)), (1.8, Z))},
        "wingR": {"rot": K((0, Z), (0.5, (0, 0, -60)), (1.4, (0, 0, -55)), (1.8, Z))},
    }},
    "hurt": {"length": 0.35, "bones": {"body": {"rot": K((0, Z), (0.1, (-8, 0, 0)), (0.35, Z))}, "neck": {"rot": K((0, Z), (0.1, (-14, 0, 0)), (0.35, Z))}}},
    "die_fall": {"length": 1.8, "bones": {
        "root": {"rot": K((0, Z), (0.6, (-15, 0, 10)), (1.6, (20, 0, 70)), (1.8, (18, 0, 66)))},
        "wingL": {"rot": K((0, Z), (1.2, (0, 0, -60)))}, "wingR": {"rot": K((0, Z), (1.2, (0, 0, 80)))},
        "neck": {"rot": K((0, Z), (0.6, (-50, 0, 0)), (1.6, (40, 0, 0)))}, "jaw": {"rot": K((0, Z), (1.6, (45, 0, 0)))},
        "tail": {"rot": K((0, Z), (1.6, (0, 40, 0)))},
    }},
}
anims.RIGS["wither"] = WITHER
anims.RIGS["wyrm"] = WYRM
anims.MELEE["wither"] = "swipe"
anims.MELEE["wyrm"] = "bite"

# ================================================================================================ WITHER

@model
def withered_tyrant():
    """Three skulls on a cracked obsidian spine, ribs that leak black smoke, a whip tail, a crown on the middle skull."""
    m = Model("withered_tyrant", "wither", 1.9)
    m.bone("core", "root", (0, 22, 0))
    m.bone("head", "core", (0, 34, 0))
    m.bone("jaw", "head", (0, 35, 3))
    m.bone("skullL", "core", (11, 32, 0))
    m.bone("skullR", "core", (-11, 32, 0))
    m.bone("tail", "core", (0, 16, -1))
    m.bone("tail2", "tail", (0, 6, -5))
    for i in (1, 2, 3): m.bone(f"ring{i}", "root", (0, 0, 0))
    skull, dark, eye = "black_concrete", "blackstone", "red_concrete"
    # spine and the shoulders the side skulls sit on
    m.c("core", "polished_blackstone", (0, 25, -1), (3.4, 18, 3.4))
    m.c("core", "obsidian", (0, 31.5, -0.5), (26, 3.4, 4.6))
    for x in (-12.5, 12.5): m.c("core", "polished_blackstone_bricks", (x, 31, -0.5), (3.4, 4.4, 5.4))
    # three pairs of ribs that curl around a hollow chest with a wither rose heart
    for k, y in enumerate((28.2, 24.8, 21.4)):
        w = 7.2 - k * 1.0
        m.m("core", "polished_blackstone", (w, y, 1.4), (1.4, 1.4, 6), (0, -14, 0))
        m.m("core", "polished_blackstone", (w * 0.55, y, 4.5), (w * 0.7, 1.4, 1.4))
    m.c("core", "crimson_nylium", (0, 25, 1.5), (3.6, 3.6, 3.6), (45, 45, 0), light=True)
    m.c("core", "red_concrete", (0, 25, 1.5), (1.6, 1.6, 4.4), light=True)
    m.c("core", "netherrack", (0, 25, 1.5), (4.4, 1.6, 1.6), light=True)
    # the middle skull: big, crowned, glowing eye sockets and a jaw that drops when it screams
    blob(m, "head", skull, (0, 39, 0.4), (10, 9, 9.4), 1.4)
    m.c("head", dark, (0, 34.8, 0.4), (8.6, 1.4, 8.4))
    m.m("head", "black_concrete", (2.4, 39.8, 5.1), (2.6, 2.4, 0.4))
    m.m("head", eye, (2.4, 39.8, 5.25), (1.4, 1.2, 0.3), light=True)
    m.c("head", "polished_blackstone", (0, 37.8, 5.15), (1.2, 1.4, 0.3))
    m.c("jaw", skull, (0, 34, 1.8), (8, 2, 6.2))
    for x in (-2.7, -0.9, 0.9, 2.7):
        m.c("head", "white_concrete", (x, 35.6, 4.9), (1.1, 1.4, 0.6))
        m.c("jaw", "white_concrete", (x, 35.1, 4.6), (1.0, 1.2, 0.6))
    m.c("head", "gold_block", (0, 44, 0.4), (10.6, 1.4, 10))
    for x, h in ((-4.4, 2.6), (-2.2, 3.4), (0, 4.6), (2.2, 3.4), (4.4, 2.6)):
        m.c("head", "gold_block", (x, 45 + h / 2, 4.6), (1.2, h, 1.0))
    m.c("head", "crying_obsidian", (0, 46.2, 5.2), (1.6, 1.6, 0.6), (0, 0, 45), light=True)
    # cracks across the skull
    m.c("head", "gray_concrete", (2.6, 42.6, 5.06), (0.3, 2.6, 0.2), (0, 0, 30))
    m.c("head", "gray_concrete", (-3.4, 37.4, 5.06), (0.3, 1.8, 0.2), (0, 0, -20))
    # the side skulls, smaller, each with its own glowing eyes
    for s, b in ((1, "skullL"), (-1, "skullR")):
        x = 12.5 * s
        blob(m, b, skull, (x, 36.4, 0.6), (7, 6.4, 6.6), 1)
        for e in (-1.5, 1.5):
            m.c(b, eye, (x + e, 37, 3.95), (1.2, 1.1, 0.3), light=True)
        m.c(b, "white_concrete", (x, 34.2, 3.8), (4, 0.8, 0.5))
        m.c(b, dark, (x, 33.1, 0.6), (6, 0.9, 5.6))
    # the whip tail made of vertebrae, with a bony blade at the end
    for k in range(4):
        m.c("tail", "polished_blackstone", (0, 15 - k * 2.4, -1 - k * 1.6), (2.8 - k * 0.3, 2.2, 2.8 - k * 0.3), (25 + k * 6, 0, 0))
    for k in range(4):
        m.c("tail2", "blackstone", (0, 5 - k * 2.2, -6 - k * 2), (1.9 - k * 0.25, 2, 1.9 - k * 0.25), (40 + k * 6, 0, 0))
    m.c("tail2", "bone_block", (0, -3.6, -14), (0.8, 4, 2.6), (60, 0, 0))
    # three rings of black smoke stones orbiting the body
    for i, (y, r, n) in enumerate(((30, 15, 6), (22, 12, 5), (14, 9, 4))):
        for k in range(n):
            a = 360 * k / n + i * 20
            m.c(f"ring{i + 1}", "coal_block" if k % 2 else "blackstone", (r * math.cos(math.radians(a)), y, r * math.sin(math.radians(a))), (2, 2, 2), (45, a, 45))
    m.attacks = {"skulls": "volley", "darkness": "scream", "shockwave": "pulse", "minions": "raise", "levitate": "raise", "meteor": "scream", "dive": "dive"}
    m.melee = "swipe"
    return m

# ================================================================================================ DRAGON

@model
def ender_wyrm():
    """The Ender Wyrm: a long black dragon with purple eyes, a spined neck, membrane wings and end crystal shards."""
    m = Model("ender_wyrm", "wyrm", 2.1)
    m.bone("body", "root", (0, 18, 0))
    m.bone("neck", "body", (0, 22, 13))
    m.bone("head", "neck", (0, 30, 26))
    m.bone("jaw", "head", (0, 29, 29))
    m.mbone("wingL", "body", (7, 25, 6))
    m.bone("tipL", "wingL", (30, 26, 6)); m.bone("tipR", "wingR", (-30, 26, 6))
    m.bone("tail", "body", (0, 18, -14))
    m.bone("tail2", "tail", (0, 16, -28))
    m.bone("tail3", "tail2", (0, 14, -40))
    m.mbone("legL", "body", (6, 14, -6))
    scale, belly, glow, horn = "black_concrete", "gray_concrete", "purple_concrete", "end_stone"
    # long body with belly plates and a ridge of spines
    blob(m, "body", scale, (0, 19, 0), (14, 11, 30), 2.4)
    for z in range(-12, 14, 4): m.c("body", belly, (0, 13.4, z), (9, 1.2, 3.4))
    for k, z in enumerate(range(-12, 14, 4)):
        m.c("body", "obsidian", (0, 25.6 + (k % 2) * 0.6, z), (1.2, 3 + (k % 2), 2.4), (-20, 0, 0))
    # end crystal shards growing out of its back, glowing (the weak spot)
    m.c("body", "pink_stained_glass", (0, 24.5, -3), (4.2, 4.2, 4.2), (45, 45, 0), light=True)
    m.c("body", "magenta_concrete", (0, 24.5, -3), (2, 2, 2), (45, 0, 45), light=True)
    m.c("body", "purpur_block", (0, 23, -3), (5, 1.2, 5))
    # the neck: four plated segments rising forward
    for k in range(5):
        t = k / 4
        m.c("neck", scale, (0, 22 + t * 7, 14 + t * 11), (7 - t * 1.6, 6.4 - t * 1.2, 4.6), (-32, 0, 0))
        m.c("neck", "obsidian", (0, 25.6 + t * 6.6, 13.4 + t * 11), (1, 2.4, 1.8), (-40, 0, 0))
        m.c("neck", belly, (0, 19.4 + t * 7, 15.4 + t * 11), (4.6, 1, 3.6), (-32, 0, 0))
    # long head with nostrils, glowing eyes, horns swept back
    m.c("head", scale, (0, 31, 29), (8, 5.4, 9))
    m.c("head", scale, (0, 30.6, 35.4), (6, 3.6, 5.6))
    m.m("head", "black_wool", (1.6, 32.6, 38.3), (1.2, 0.8, 0.3))
    m.m("head", glow, (3.3, 32.6, 31.6), (1.6, 1.0, 2.4), light=True)
    m.m("head", "magenta_concrete", (4.06, 32.6, 31.6), (0.2, 0.6, 1.4), light=True)
    m.m("head", "obsidian", (3, 34.1, 31), (2.6, 0.8, 3.6), (0, 0, -12))
    mhorn(m, "head", horn, (2.6, 33.4, 26.5), 4, (-110, 0, -18), (8, 0, -4), 1.5, 0.78)
    mhorn(m, "head", horn, (3.8, 31.6, 26), 3, (-120, 0, -50), (6, 0, 0), 1.0, 0.8)
    m.c("jaw", scale, (0, 28.2, 33.6), (5.6, 1.8, 10))
    for z in (30, 32.4, 34.8, 37.2):
        m.m("head", "white_concrete", (2.3, 28.8, z), (0.6, 1.2, 0.6))
        m.m("jaw", "white_concrete", (2.1, 29.4, z + 1.1), (0.6, 1.0, 0.6))
    m.c("jaw", glow, (0, 28.9, 33), (3.4, 0.3, 7), light=True)
    # the wings: a bony arm and finger struts with dark membrane panels between them
    for s, w, t in ((1, "wingL", "tipL"), (-1, "wingR", "tipR")):
        m.c(w, scale, (18.5 * s, 25.8, 6), (23, 2.2, 2.2))
        m.c(w, "obsidian", (30 * s, 26, 6), (2.6, 2.6, 2.6))
        for k in range(3):
            m.c(w, "black_wool", ((10 + k * 7) * s, 25, -1 - k * 0.4), (6.8, 0.5, 12 - k * 1.2))
        m.c(t, scale, (40 * s, 26.4, 4), (20, 1.6, 1.6), (0, -14 * s, 0))
        for k, (dz, ln) in enumerate(((-3, 16), (-8, 14), (-13, 10))):
            m.c(t, "polished_blackstone", ((33 + k * 3) * s, 25.4, dz), (1, 1, ln), (0, (30 + k * 18) * s, 0))
        m.c(t, "black_wool", (38 * s, 25.2, -4), (14, 0.5, 13))
        m.c(t, "purple_wool", (44 * s, 25.25, -6), (6, 0.5, 6), (0, 20 * s, 0))
        m.c(t, horn, (50 * s, 26.4, 1.6), (1.4, 1.4, 3), (0, -30 * s, 0))
    # tail in three chains with spines and a crystal tip
    for k in range(4):
        m.c("tail", scale, (0, 18 - k * 0.6, -16 - k * 3.4), (8 - k * 0.8, 7 - k * 0.6, 3.8))
        m.c("tail", "obsidian", (0, 22 - k * 0.8, -16 - k * 3.4), (1, 2.4, 1.6), (-20, 0, 0))
    for k in range(4):
        m.c("tail2", scale, (0, 15.6 - k * 0.5, -30 - k * 3), (4.8 - k * 0.6, 4.4 - k * 0.5, 3.4))
    for k in range(3):
        m.c("tail3", scale, (0, 13.6 - k * 0.4, -42 - k * 2.8), (2.6 - k * 0.5, 2.6 - k * 0.5, 3))
    m.c("tail3", "pink_stained_glass", (0, 13, -51), (2.2, 2.2, 2.2), (45, 45, 0), light=True)
    # back legs with claws (tucked up while flying)
    for s, b in ((1, "legL"), (-1, "legR")):
        m.c(b, scale, (6 * s, 11, -5), (4, 8, 5))
        m.c(b, scale, (6.6 * s, 5, -3.6), (2.6, 7, 2.6), (20, 0, 0))
        for k in (-1, 0, 1):
            m.c(b, "end_stone", (6.6 * s + k * 1.1, 1, -0.6), (0.7, 0.8, 2.4))
    m.attacks = {"breath": "breath", "dive": "dive", "shockwave": "gust", "meteor": "roar", "orbs": "breath", "levitate": "gust", "roar": "roar"}
    m.melee = "bite"
    return m

# ================================================================================================ KILLER CLAUS

@model
def killer_claus():
    """Santa gone very wrong: torn red suit, bloodied beard, glowing eyes, a candy cane scythe and a sack of
    presents that tick."""
    m = Model("killer_claus", "biped", 1.95)
    biped(m, hip=15, legx=4.2, neck=33, shoulder=31, armx=10.5)
    m.bone("jaw", "head", (0, 36, 4))
    m.bone("sack", "body", (0, 30, -6))
    m.bone("scythe", "armR", (-11, 14, 2))
    red, red2, fur, belt, boot = "red_wool", "red_concrete", "white_wool", "black_concrete", "black_terracotta"
    # boots with buckles and fur cuffs, trousers
    for s, b in ((1, "legL"), (-1, "legR")):
        m.c(b, boot, (4.2 * s, 2.2, 0.8), (5.2, 4.4, 7))
        m.c(b, boot, (4.2 * s, 0.6, 3.8), (4.8, 1.2, 2))
        m.c(b, "gold_block", (4.2 * s, 3.2, 4.4), (2, 1.2, 0.3))
        m.c(b, fur, (4.2 * s, 5, 0.4), (5.8, 1.6, 6.2))
        m.c(b, red, (4.2 * s, 10.2, 0), (4.8, 9, 5))
        m.c(b, "red_terracotta", (4.2 * s + 1.4 * s, 8, 2.6), (1.2, 2.4, 0.2), (0, 0, 20))
    # a round belly in a coat that has seen things, with a heavy belt and a cracked gold buckle
    blob(m, "body", red, (0, 24, 0.6), (17, 15, 13), 3)
    m.c("body", red2, (0, 23, 6.9), (5, 13, 0.6))
    m.c("body", fur, (0, 23, 7.25), (2.8, 13.4, 0.6))
    for y in (27, 23, 19): m.c("body", "black_concrete", (0, y, 7.6), (1, 1, 0.3))
    m.c("body", belt, (0, 18.6, 0.6), (17.6, 2.4, 13.6))
    m.c("body", "gold_block", (0, 18.6, 7.5), (4.2, 3.2, 0.5))
    m.c("body", belt, (0, 18.6, 7.8), (2, 1.4, 0.4))
    m.c("body", fur, (0, 16.6, 0.6), (17.8, 1.8, 13.8))
    # rips and stains
    for x, y, r in ((-5.4, 26.4, 30), (6, 21, -20), (-6.8, 21.4, 10)):
        m.c("body", "black_wool", (x, y, 7.12), (2.4, 0.5, 0.2), (0, 0, r))
    m.c("body", "red_terracotta", (4.6, 27.6, 7.12), (2.4, 2.2, 0.2), (0, 0, 15))
    # fur collar
    m.c("body", fur, (0, 31.4, 0.4), (15, 2.6, 11))
    # arms: big sleeves with fur cuffs, black gloves
    for s, a in ((1, "armL"), (-1, "armR")):
        blob(m, a, red, (10.5 * s, 27, 0), (5.2, 8, 5.6), 1.2)
        m.c(a, red, (10.5 * s, 20, 0.6), (4.6, 7, 4.8))
        m.c(a, fur, (10.5 * s, 16.4, 0.6), (5.4, 1.8, 5.6))
        m.c(a, "black_concrete", (10.5 * s, 13.8, 1), (3.8, 3.4, 3.8))
    # the head: rosy face, a grin full of crooked teeth, glowing red eyes under bushy brows
    m.c("head", "pink_terracotta", (0, 38.6, 0.8), (8.4, 7.4, 7.6))
    m.m("head", "black_concrete", (2.1, 40, 4.66), (1.8, 1.4, 0.2))
    m.m("head", "red_concrete", (2.1, 40, 4.78), (0.9, 0.8, 0.2), light=True)
    m.m("head", fur, (2.3, 41.4, 4.8), (3.2, 1, 0.8), (0, 0, -18))
    m.c("head", "pink_concrete", (0, 38.6, 5.1), (1.8, 1.8, 1.4))
    # beard (stained), moustache that curls up, grin
    m.c("jaw", fur, (0, 34.4, 3.4), (9.4, 4.4, 4))
    m.c("jaw", fur, (0, 31.6, 3.8), (7.4, 2.4, 3.2))
    m.c("jaw", fur, (0, 29.8, 3.9), (4.4, 1.6, 2.6))
    m.c("jaw", "red_terracotta", (1.6, 32.2, 5.45), (2, 1.6, 0.2))
    m.m("head", fur, (2.6, 37.3, 5.0), (4.2, 1.4, 1.2), (0, 0, 16))
    m.c("head", "black_concrete", (0, 36, 4.7), (5.2, 1.2, 0.3))
    for x in (-2, -0.6, 0.8, 2.1): m.c("head", "white_concrete", (x, 36.2, 4.86), (0.8, 1.0 if x != 0.8 else 1.4, 0.2), (0, 0, x * 4))
    # floppy hat with a fur rim and a bobble that glows
    m.c("head", fur, (0, 42.8, 0.8), (9.6, 2, 8.8))
    m.c("head", red, (0, 45.4, 0), (8, 3.4, 7.4))
    m.c("head", red, (0, 47.6, -1.4), (5.6, 3, 5.4), (-20, 0, 0))
    m.c("head", red, (0, 48.6, -4.6), (3.6, 2.6, 4.4), (-60, 0, 0))
    blob(m, "head", fur, (0, 46.6, -7.6), (3, 3, 3), 0.6, light=True)
    # the sack of presents slung over the back: wrapped boxes, one with a lit fuse
    blob(m, "sack", "brown_wool", (0, 27, -11), (13, 14, 8), 2.4)
    m.c("sack", "brown_terracotta", (0, 34.4, -9.6), (4, 2, 3))
    for x, y, c, rib in ((-4, 36, "lime_concrete", "red_concrete"), (2.6, 36.8, "light_blue_concrete", "yellow_concrete"), (-0.6, 38.4, "red_concrete", "white_concrete")):
        m.c("sack", c, (x, y, -11), (4, 3.6, 4), (0, 20, 8))
        m.c("sack", rib, (x, y, -11), (4.2, 0.8, 4.2), (0, 20, 8))
        m.c("sack", rib, (x, y + 1.9, -11), (1.6, 0.8, 1.6), (45, 20, 0))
    m.c("sack", "tnt", (4.6, 32, -11.6), (3.4, 3.4, 3.4), (0, 30, 0))
    m.c("sack", "redstone_block", (4.6, 34.4, -11.6), (0.4, 1.6, 0.4), light=True)
    m.c("sack", "brown_wool", (0, 31, -4.8), (13, 1.2, 1.2), (0, 0, -35))
    # the candy cane scythe: striped shaft and a long dark blade
    for k in range(11):
        m.c("scythe", "white_concrete" if k % 2 else "red_concrete", (-11, 2 + k * 3.4, 2.4), (1.8, 3.4, 1.8))
    for k in range(5):
        a = k * 36
        m.c("scythe", "white_concrete" if k % 2 else "red_concrete", (-11 + 2.4 * math.sin(math.radians(a)), 39.4 + 2.4 * math.cos(math.radians(a)) - 2.4 + 2.4, 2.4 + 2.4 * (1 - math.cos(math.radians(a)))),
            (1.8, 2.2, 1.8), (a, 0, 0))
    m.c("scythe", "polished_blackstone", (-11, 41.4, 10), (0.6, 3.4, 14), (12, 0, 0))
    m.c("scythe", "iron_block", (-11, 39.6, 11), (0.4, 1.4, 13), (14, 0, 0))
    m.c("scythe", "redstone_block", (-11, 38.4, 16.4), (0.5, 1, 2.6), (30, 0, 0), light=True)
    m.hold = {"scythe": 20}
    m.attacks = {"gifts": "double", "frost": "cast", "volley": "cast", "minions": "roar", "leap": "slam", "charge": "lunge", "sprinkles": "cast"}
    m.melee = "sweep"
    return m

# ================================================================================================ ICE CREAM

@model
def brain_freeze():
    """A three-scoop sundae monster on a waffle cone: strawberry, mint and chocolate scoops with sprinkles,
    a cherry on top, waffle arms and a giant spoon."""
    m = Model("brain_freeze", "float", 1.9)
    m.bone("core", "root", (0, 22, 0))
    m.bone("head", "core", (0, 34, 0))
    m.mbone("armL", "core", (8, 30, 0))
    for i in (1, 2, 3): m.bone(f"ring{i}", "root", (0, 0, 0))
    m.bone("spoon", "armR", (-12, 18, 2))
    cone, cone2 = "orange_terracotta", "yellow_terracotta"
    # the waffle cone, stacked and narrowing to a point, with a criss-cross pattern
    for k, w in enumerate((11, 9.6, 8, 6.4, 4.8, 3.2, 1.8)):
        y = 28 - k * 3
        m.c("core", cone if k % 2 == 0 else cone2, (0, y, 0), (w, 3, w))
        if w > 4:
            for a in (0, 90):
                m.c("core", "brown_terracotta", (0, y, 0), (w + 0.1, 0.4, w * 0.2), (0, a + 45, 0))
    m.c("core", "white_terracotta", (0, 30, 0), (12.6, 1.4, 12.6))
    # a scoop sits on the cone and melts over the rim
    blob(m, "core", "pink_concrete", (0, 32.6, 0), (13.4, 6, 13.4), 2)
    for x, z, h in ((5.6, 4.2, 3.4), (-4.8, 5, 2.4), (6, -3, 2.8), (-5.8, -4.4, 4), (0.6, 6.6, 3)):
        m.c("core", "pink_concrete", (x, 30 - h / 2, z), (2, h, 2))
    # the cherry heart in the middle scoop is the weak spot
    m.c("core", "red_concrete", (0, 33.4, 6.7), (3, 3, 1.4), light=True)
    # the head: the mint scoop with chocolate chips and a face, the chocolate scoop on top
    blob(m, "head", "lime_concrete", (0, 38.8, 0), (12, 7, 12), 2)
    for x, y, z in ((3.4, 41, 5.6), (-4.6, 37.6, 4.8), (5.4, 37.4, -3), (-2.4, 41.2, -5.6), (0.4, 36.4, 5.9)):
        m.c("head", "brown_concrete", (x, y, z), (1, 0.8, 0.6), (0, 0, 30))
    m.m("head", "black_concrete", (2.4, 39.6, 6.06), (1.8, 2.2, 0.2))
    m.m("head", "white_concrete", (2.7, 40.3, 6.16), (0.6, 0.6, 0.1))
    m.c("head", "black_concrete", (0, 37.4, 6.06), (4.4, 1, 0.2))
    m.c("head", "pink_concrete", (0, 36.8, 6.1), (2.2, 0.8, 0.2))
    m.m("head", "light_blue_concrete", (4.4, 38.4, 6.04), (1.2, 0.5, 0.2))
    blob(m, "head", "brown_concrete", (0, 45, 0), (10, 6, 10), 1.8)
    # whipped cream, sprinkles and the cherry with its stalk
    blob(m, "head", "white_concrete", (0, 48.6, 0), (6, 2.4, 6), 0.8)
    m.c("head", "white_concrete", (0, 50.2, 0), (3, 1.6, 3))
    for k, c in enumerate(("red_concrete", "yellow_concrete", "lime_concrete", "light_blue_concrete", "pink_concrete", "white_concrete", "orange_concrete", "magenta_concrete")):
        a = k * 45
        m.c("head", c, (4.6 * math.cos(math.radians(a)), 47.4, 4.6 * math.sin(math.radians(a))), (1.6, 0.4, 0.4), (0, a + 30, 0))
    blob(m, "head", "red_concrete", (0, 52.6, 0), (3.2, 3.2, 3.2), 0.6, light=True)
    m.c("head", "green_concrete", (0.6, 55.2, 0), (0.4, 2.6, 0.4), (0, 0, -20))
    # wafer arms with dripping fudge, and the giant spoon
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, cone2, (11 * s, 27, 0), (2.4, 7, 2.4), (0, 0, 20 * s))
        m.c(a, cone, (12 * s, 21, 0.6), (2.2, 6, 2.2))
        m.c(a, "brown_concrete", (12 * s, 18, 1), (2.8, 2, 2.8))
    m.c("spoon", "iron_block", (-12, 16, 2), (1, 22, 1))
    m.c("spoon", "iron_block", (-12, 29, 2), (4, 1, 6))
    m.c("spoon", "pink_concrete", (-12, 29.8, 2), (3, 1, 4))
    # a ring of orbiting sprinkles and two of floating wafer sticks
    for k in range(8):
        a = k * 45
        m.c("ring1", ("red_concrete", "yellow_concrete", "lime_concrete", "light_blue_concrete")[k % 4], (13 * math.cos(math.radians(a)), 34, 13 * math.sin(math.radians(a))), (1.6, 0.5, 0.5), (0, a, 30))
    for k in range(4):
        a = k * 90 + 45
        m.c("ring2", cone2, (10 * math.cos(math.radians(a)), 22, 10 * math.sin(math.radians(a))), (0.8, 4, 0.8), (20, a, 0))
    m.hold = {"spoon": 0}
    m.attacks = {"sprinkles": "spin", "frost": "pulse", "orbs": "raise", "shockwave": "dive", "minions": "raise", "levitate": "pulse"}
    m.melee = "swipe"
    return m
