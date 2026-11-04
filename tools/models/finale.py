"""The finale: The Unmaker, the boss that wakes after the Withered Tyrant, the Ender Wyrm and The Listener
Below are all beaten. A floating four-armed titan of obsidian and end stone with a burning void heart,
one huge eye, a crown of shards that orbits its head and broken fins on its back. Its own rig (titan)."""
import copy, math
from models import *
from seasonal import blob
import anims
from anims import K, Z
from recipes import S, fx

# ================================================================================================ RIG

TITAN = copy.deepcopy(anims.FLOAT)
TITAN["idle"] = {"length": 4.0, "loop": True, "bones": {
    "core": {"pos": K((0, Z), (2.0, (0, 2.4, 0)), (4.0, Z)), "rot": K((0, (-2, 0, 0)), (2.0, (2, 0, 0)), (4.0, (-2, 0, 0)))},
    "chest": {"scl": K((0, (1, 1, 1)), (1.0, (1.03, 1.02, 1.04)), (2.0, (1, 1, 1)), (3.0, (1.03, 1.02, 1.04)), (4.0, (1, 1, 1)))},
    "heart": {"rot": K((0, Z), (2.0, (180, 90, 0)), (4.0, (360, 180, 0))), "scl": K((0, (1, 1, 1)), (0.25, (1.18, 1.18, 1.18)), (0.6, (1, 1, 1)), (2.0, (1, 1, 1)), (2.25, (1.18, 1.18, 1.18)), (2.6, (1, 1, 1)), (4.0, (1, 1, 1)))},
    "head": {"rot": K((0, (4, -10, 0)), (2.0, (-2, 10, 0)), (4.0, (4, -10, 0)))},
    "halo": {"rot": K((0, Z), (2.0, (0, 180, 0)), (4.0, (0, 360, 0))), "pos": K((0, Z), (1.0, (0, 0.8, 0)), (3.0, (0, -0.8, 0)), (4.0, Z))},
    "armL": {"rot": K((0, (8, 0, -14)), (2.0, (-4, 0, -20)), (4.0, (8, 0, -14)))},
    "armR": {"rot": K((0, (-4, 0, 20)), (2.0, (8, 0, 14)), (4.0, (-4, 0, 20)))},
    "arm2L": {"rot": K((0, (-20, 10, -24)), (2.0, (-12, 0, -30)), (4.0, (-20, 10, -24)))},
    "arm2R": {"rot": K((0, (-12, 0, 30)), (2.0, (-20, -10, 24)), (4.0, (-12, 0, 30)))},
    "finL": {"rot": K((0, (0, 12, 0)), (2.0, (0, 22, 6)), (4.0, (0, 12, 0)))},
    "finR": {"rot": K((0, (0, -12, 0)), (2.0, (0, -22, -6)), (4.0, (0, -12, 0)))},
    "tail": {"rot": K((0, (6, 0, 4)), (2.0, (12, 0, -4)), (4.0, (6, 0, 4)))},
    "ring1": {"rot": K((0, Z), (2.0, (0, 180, 0)), (4.0, (0, 360, 0)))},
    "ring2": {"rot": K((0, Z), (2.0, (0, -180, 0)), (4.0, (0, -360, 0)))},
    "ring3": {"rot": K((0, Z), (2.0, (0, 120, 0)), (4.0, (0, 240, 0)))},
}}
TITAN["walk"] = {"length": 3.0, "loop": True, "bones": {
    "core": {"rot": K((0, (10, 0, 0)), (1.5, (12, 0, 0)), (3.0, (10, 0, 0)))},
    "tail": {"rot": K((0, (24, 0, 6)), (1.5, (30, 0, -6)), (3.0, (24, 0, 6)))},
    "halo": {"rot": K((0, Z), (3.0, (0, 360, 0)))},
    "ring1": {"rot": K((0, Z), (1.5, (0, 180, 0)), (3.0, (0, 360, 0)))},
    "ring2": {"rot": K((0, Z), (1.5, (0, -180, 0)), (3.0, (0, -360, 0)))},
    "ring3": {"rot": K((0, Z), (1.5, (0, 180, 0)), (3.0, (0, 360, 0)))},
}}
# both great fists rise over the head and come down together
TITAN["smash"] = {"length": 1.8, "hit": 1.05, "bones": {
    "armL": {"rot": K((0, Z), (0.7, (-170, 0, -10)), (0.95, (-175, 0, -6)), (1.1, (-30, 0, -4)), (1.4, (-26, 0, -4)), (1.8, Z))},
    "armR": {"rot": K((0, Z), (0.7, (-170, 0, 10)), (0.95, (-175, 0, 6)), (1.1, (-30, 0, 4)), (1.4, (-26, 0, 4)), (1.8, Z))},
    "foreL": {"rot": K((0, Z), (0.7, (-40, 0, 0)), (1.1, (0, 0, 0)), (1.8, Z))},
    "foreR": {"rot": K((0, Z), (0.7, (-40, 0, 0)), (1.1, (0, 0, 0)), (1.8, Z))},
    "core": {"rot": K((0, Z), (0.7, (-16, 0, 0)), (1.1, (24, 0, 0)), (1.4, (22, 0, 0)), (1.8, Z)), "pos": K((0, Z), (0.7, (0, 6, 0)), (1.1, (0, -5, 4)), (1.8, Z))},
    "head": {"rot": K((0, Z), (0.7, (-20, 0, 0)), (1.1, (10, 0, 0)), (1.8, Z))},
    "arm2L": {"rot": K((0, Z), (0.7, (10, 0, -50)), (1.1, (-10, 0, -20)), (1.8, Z))},
    "arm2R": {"rot": K((0, Z), (0.7, (10, 0, 50)), (1.1, (-10, 0, 20)), (1.8, Z))},
}}
# the lower left arm sweeps the void blade in a wide arc, the body twists into it
TITAN["sweep"] = {"length": 1.3, "hit": 0.7, "bones": {
    "arm2L": {"rot": K((0, Z), (0.45, (-80, -70, -40)), (0.7, (-70, 80, -10)), (0.9, (-60, 90, -10)), (1.3, Z))},
    "core": {"rot": K((0, Z), (0.45, (0, 35, 0)), (0.7, (0, -40, 0)), (1.3, Z))},
    "halo": {"rot": K((0, Z), (0.7, (0, -180, 0)), (1.3, (0, -360, 0)))},
    "armL": {"rot": K((0, Z), (0.45, (-30, 0, -40)), (0.7, (10, 0, -20)), (1.3, Z))},
}}
# raises the orb in the lower right hand, the heart flares, the eye glares
TITAN["cast"] = {"length": 1.6, "hit": 0.95, "bones": {
    "arm2R": {"rot": K((0, Z), (0.6, (-150, 0, 20)), (1.2, (-150, 0, 20)), (1.6, Z))},
    "heart": {"scl": K((0, (1, 1, 1)), (0.6, (0.7, 0.7, 0.7)), (0.95, (1.6, 1.6, 1.6)), (1.3, (1, 1, 1)), (1.6, (1, 1, 1)))},
    "chest": {"rot": K((0, Z), (0.6, (-12, 0, 0)), (0.95, (6, 0, 0)), (1.6, Z))},
    "head": {"rot": K((0, Z), (0.6, (-24, 0, 0)), (0.95, (8, 0, 0)), (1.6, Z))},
    "halo": {"scl": K((0, (1, 1, 1)), (0.6, (0.7, 1, 0.7)), (0.95, (1.5, 1, 1.5)), (1.6, (1, 1, 1)))},
    "armL": {"rot": K((0, Z), (0.6, (-20, 0, -50)), (1.6, Z))}, "armR": {"rot": K((0, Z), (0.6, (-20, 0, 50)), (1.6, Z))},
}}
# throws all four arms wide and the shards of the crown fly out, then snap back
TITAN["roar"] = {"length": 2.0, "hit": 0.9, "bones": {
    "armL": {"rot": K((0, Z), (0.6, (-40, 0, -80)), (1.6, (-40, 0, -78)), (2.0, Z))},
    "armR": {"rot": K((0, Z), (0.6, (-40, 0, 80)), (1.6, (-40, 0, 78)), (2.0, Z))},
    "arm2L": {"rot": K((0, Z), (0.6, (20, 0, -70)), (1.6, (20, 0, -68)), (2.0, Z))},
    "arm2R": {"rot": K((0, Z), (0.6, (20, 0, 70)), (1.6, (20, 0, 68)), (2.0, Z))},
    "head": {"rot": K((0, Z), (0.6, (-30, 0, 0)), (1.0, (-30, 8, 0)), (1.4, (-30, -8, 0)), (2.0, Z))},
    "jaw": {"rot": K((0, Z), (0.6, (40, 0, 0)), (1.6, (38, 0, 0)), (2.0, Z))},
    "halo": {"scl": K((0, (1, 1, 1)), (0.6, (1.8, 1.2, 1.8)), (1.6, (1.8, 1.2, 1.8)), (2.0, (1, 1, 1)))},
    "finL": {"rot": K((0, Z), (0.6, (0, 40, 20)), (1.6, (0, 40, 20)), (2.0, Z))},
    "finR": {"rot": K((0, Z), (0.6, (0, -40, -20)), (1.6, (0, -40, -20)), (2.0, Z))},
    "core": {"rot": K((0, Z), (0.6, (-14, 0, 0)), (1.6, (-12, 0, 0)), (2.0, Z))},
}}
TITAN["swipe"] = {"length": 0.8, "hit": 0.4, "bones": {
    "armR": {"rot": K((0, Z), (0.25, (-120, 0, 40)), (0.4, (20, 0, -10)), (0.8, Z))},
    "foreR": {"rot": K((0, Z), (0.25, (-50, 0, 0)), (0.4, (0, 0, 0)), (0.8, Z))},
    "core": {"rot": K((0, Z), (0.25, (0, -22, 0)), (0.4, (0, 28, 0)), (0.8, Z))},
}}
TITAN["hurt"] = {"length": 0.35, "bones": {"core": {"rot": K((0, Z), (0.1, (-8, 0, 0)), (0.35, Z))}, "head": {"rot": K((0, Z), (0.1, (-14, 0, 0)), (0.35, Z))}}}
TITAN["die_drop"] = {"length": 2.2, "bones": {
    "root": {"pos": K((0, Z), (0.5, (0, 6, 0)), (1.8, (0, -14, 0)), (2.2, (0, -13, 0)))},
    "core": {"rot": K((0, Z), (0.5, (-20, 0, 0)), (1.8, (35, 0, 12)))},
    "head": {"rot": K((0, Z), (0.5, (-40, 0, 0)), (1.8, (40, 0, 10)))},
    "armL": {"rot": K((0, Z), (1.6, (50, 0, 40)))}, "armR": {"rot": K((0, Z), (1.6, (50, 0, -40)))},
    "arm2L": {"rot": K((0, Z), (1.6, (60, 0, 20)))}, "arm2R": {"rot": K((0, Z), (1.6, (60, 0, -20)))},
    "halo": {"pos": K((0, Z), (1.8, (0, -8, 0)))}, "ring1": {"pos": K((0, Z), (1.6, (0, -8, 0)))},
    "ring2": {"pos": K((0, Z), (1.6, (0, -14, 0)))}, "ring3": {"pos": K((0, Z), (1.6, (0, -20, 0)))}}}
anims.RIGS["titan"] = TITAN
anims.MELEE["titan"] = "swipe"

# ================================================================================================ MODEL

OBS, CRY, END, ENDB, GOLD, DEEP, PUR, AME = ("obsidian", "crying_obsidian", "end_stone", "end_stone_bricks", "gold_block",
                                             "reinforced_deepslate", "purpur_block", "amethyst_block")


def crack(m, bone, pts, th=0.55, z=None, block="purple_concrete"):
    """A glowing crack: straight runs between points on a front face (x, y) at depth z."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        lo_x, hi_x = sorted((x0, x1)); lo_y, hi_y = sorted((y0, y1))
        m.box(bone, block, (lo_x - th / 2, lo_y - th / 2, z - 0.05), (hi_x + th / 2, hi_y + th / 2, z + 0.25), light=True)


@model
def the_unmaker():
    """THE UNMAKER: four arms, a void heart, one eye, a crown of orbiting shards. Wakes after the three legends."""
    m = Model("the_unmaker", "titan", 3.0)
    m.bone("core", "root", (0, 18, 0))
    m.bone("tail", "core", (0, 14, 0))
    m.bone("chest", "core", (0, 24, 0))
    m.bone("heart", "chest", (0, 29, 7))
    m.bone("head", "chest", (0, 38, 0.5))
    m.bone("jaw", "head", (0, 39.5, 4))
    m.bone("halo", "head", (0, 47, 0.5))
    m.mbone("armL", "chest", (12, 36, 0))
    m.mbone("foreL", "armL", (17, 26, 0.5))
    m.mbone("arm2L", "chest", (9.5, 27, 1))
    m.mbone("finL", "chest", (5, 34, -6))
    for i in (1, 2, 3): m.bone(f"ring{i}", "root", (0, 0, 0))

    # --- the lower body: broken pillars tapering into a trail of floating rubble
    m.c("core", OBS, (0, 19.5, 0), (13, 6, 9))
    m.c("core", DEEP, (0, 22.6, 0), (14.4, 1.4, 10.2))
    for k, (x, z) in enumerate(((-4.5, 3.2), (4.5, 3.2), (-4.5, -3.2), (4.5, -3.2))):
        m.c("core", OBS if k % 2 else "crying_obsidian", (x, 16, z), (3.6, 4.4, 3.2), (6 * (1 if z > 0 else -1), 0, 8 * (1 if x > 0 else -1)), light=k % 2 == 0)
    crack(m, "core", [(-3, 21.8), (-3, 19.4), (-0.6, 19.4), (-0.6, 17.2)], z=4.5)
    crack(m, "core", [(3.6, 21.6), (3.6, 18.6), (1.8, 18.6)], z=4.5)
    for k in range(4):
        y = 13 - k * 3.2
        w = 8 - k * 1.7
        m.c("tail", OBS if k % 2 == 0 else ENDB, (0.4 * (-1) ** k, y, -0.4 * k), (w, 2.6, w * 0.75), (8 * k, 20 * k, 6 * (-1) ** k))
        m.c("tail", CRY, (0.8 * (-1) ** k, y - 1.3, -0.4 * k), (w * 0.45, 0.8, w * 0.4), (8 * k, 20 * k, 0), light=True)
    for k in range(6):
        a = math.radians(60 * k + 15)
        m.c("tail", END if k % 2 else OBS, (math.cos(a) * 5.5, 5 + (k % 3) * 1.6, math.sin(a) * 5.5), (1.8, 1.8, 1.8), (40, 60 * k, 30))

    # --- the chest: layered plates over a hollow ribcage holding the heart
    m.c("chest", DEEP, (0, 30, -1), (19, 13, 10))
    m.c("chest", OBS, (0, 30.5, 3.9), (16, 11, 0.8))
    m.c("chest", "black_concrete", (0, 29, 4.35), (8, 7, 0.4))
    for k, y in enumerate((33.6, 31.4, 29.2, 27)):
        w = 7.4 - k * 0.6
        m.m("chest", ENDB, (w * 0.62, y, 4.6), (w * 0.62, 1.1, 1.2))
        m.m("chest", GOLD, (w * 0.62 + w * 0.33, y, 4.7), (0.6, 1.3, 1.3))
    m.c("chest", GOLD, (0, 25.2, 4.2), (17, 1.2, 1.6))
    m.c("chest", GOLD, (0, 36.2, 3.6), (19.6, 1.2, 2.2))
    m.c("chest", OBS, (0, 37.6, -1), (16, 2.6, 9))
    for x in (-7.5, 7.5):
        m.c("chest", ENDB, (x, 30, 4.25), (2.6, 10, 0.6))
        m.c("chest", GOLD, (x, 34.4, 4.6), (2.2, 1.4, 0.6))
    crack(m, "chest", [(-8.6, 34.6), (-8.6, 31.6), (-6.6, 31.6), (-6.6, 27.4)], z=4.55)
    crack(m, "chest", [(8.6, 33.2), (8.6, 29.4), (6.6, 29.4), (6.6, 26.2)], z=4.55)
    # the back: a gold spine with plates down it
    for k in range(5):
        m.c("chest", GOLD if k % 2 == 0 else OBS, (0, 35 - k * 2.4, -6.3), (2.4, 1.8, 0.8))
    # the void heart: a spinning crystal inside a cage, the weak spot
    m.c("heart", "magenta_concrete", (0, 29, 7), (3.6, 3.6, 3.6), light=True)
    m.c("heart", "purple_stained_glass", (0, 29, 7), (5.2, 5.2, 5.2), (45, 45, 0), light=True)
    m.c("heart", "beacon", (0, 29, 7), (1.8, 1.8, 1.8), (45, 0, 45), light=True)
    for a in range(4):
        r = math.radians(90 * a + 45)
        m.c("heart", AME, (math.cos(r) * 3.4, 29 + math.sin(r) * 3.4, 7), (1.0, 1.0, 1.0), (0, 0, 90 * a + 45))

    # --- the head: a heavy helm with one great eye, a hinged jaw full of teeth
    m.c("head", OBS, (0, 42.5, 0.5), (9.4, 8, 8.4))
    m.c("head", DEEP, (0, 46.8, 0.5), (10.2, 1.4, 9.2))
    m.c("head", GOLD, (0, 46.2, 4.8), (10.4, 1, 0.6))
    m.m("head", OBS, (5.4, 42.5, 0.5), (1.6, 6.6, 7.4))
    m.m("head", GOLD, (5.8, 43.5, 3.4), (1.0, 1.0, 1.6))
    # brow ridges and the eye
    m.m("head", "black_concrete", (2.6, 45.2, 4.8), (3.4, 1.2, 0.5), (0, 0, -16))
    m.c("head", "black_concrete", (0, 43, 4.75), (6.4, 4.2, 0.4))
    m.c("head", "pearlescent_froglight", (0, 43, 4.95), (5.4, 3.4, 0.4), light=True)
    m.c("head", "pink_concrete", (0, 43, 5.12), (3.6, 2.2, 0.3), light=True)
    m.c("head", "black_concrete", (0, 43, 5.3), (1.2, 2.4, 0.3))
    m.c("head", "white_concrete", (-1.5, 43.9, 5.3), (0.6, 0.6, 0.25), light=True)
    m.c("jaw", OBS, (0, 38.6, 2.4), (8.4, 2.4, 6))
    m.c("jaw", GOLD, (0, 37.6, 5.2), (8.6, 0.6, 0.6))
    for x in (-3.3, -1.6, 0, 1.6, 3.3):
        m.c("head", "white_concrete", (x, 39.4, 4.6), (0.8, 1.4, 0.6))
        m.c("jaw", "white_concrete", (x + 0.8, 40.0, 5.0), (0.7, 1.2, 0.6))
    # horns sweeping back from the helm
    mhorn(m, "head", "end_stone", (4.4, 46, -1), 4, (-30, 0, -40), (-14, 0, 10), 1.6, 0.8)
    # the crown: eight shards that orbit above the head, alternating gold and amethyst
    for k in range(8):
        a = math.radians(45 * k)
        m.c("halo", GOLD if k % 2 else AME, (math.cos(a) * 7, 48 + (k % 2) * 1.2, 0.5 + math.sin(a) * 7), (1.2, 3.4 + (k % 2), 1.2), (0, -45 * k, 12), light=k % 2 == 0)
    m.c("halo", "end_rod", (0, 51, 0.5), (0.8, 3, 0.8), light=True)

    # --- the great arms: huge pauldrons, gold bands, fists with glowing knuckles
    for s, arm, fore in ((1, "armL", "foreL"), (-1, "armR", "foreR")):
        x = 15 * s
        m.c(arm, DEEP, (x, 31, 0.5), (5.4, 10, 5.4))
        m.c(arm, OBS, (x + 0.4 * s, 37, 0.5), (9, 4.4, 8.4))
        m.c(arm, GOLD, (x + 0.6 * s, 39.4, 0.5), (8, 1, 7.4))
        m.c(arm, OBS, (x + 2.6 * s, 34, 0.5), (4.6, 3, 7.8))
        m.c(arm, GOLD, (x + 4.6 * s, 33, 0.5), (0.8, 2.2, 7.8))
        horn(m, arm, END, (x + 2 * s, 41, 0.5), 3, (0, 0, -30 * s), (0, 0, -12 * s), 1.6, 0.75)
        m.c(arm, GOLD, (x, 27.2, 0.5), (6, 1.2, 6))
        fx_ = 17 * s
        m.c(fore, OBS, (fx_, 22, 1), (6, 8, 6))
        m.c(fore, GOLD, (fx_, 24.6, 1), (6.6, 1.2, 6.6))
        m.c(fore, ENDB, (fx_ + 3.1 * s, 22, 1), (0.6, 6, 4.4))
        crack(m, fore, [(fx_ - 1.6, 25.6), (fx_ - 1.6, 22.4), (fx_ + 0.8, 22.4), (fx_ + 0.8, 19.6)], z=4.05)
        # the fist and its knuckles
        m.c(fore, DEEP, (fx_, 15.6, 1.4), (7, 5.6, 7))
        for k in range(4):
            m.c(fore, CRY, (fx_ - 2.4 + k * 1.6, 17.4, 5.1), (1.2, 1.4, 0.6), light=True)
            m.c(fore, GOLD, (fx_ - 2.4 + k * 1.6, 14.6, 5.0), (1.3, 1.6, 0.6))
        m.c(fore, DEEP, (fx_ - 3.6 * s, 16.4, 3.4), (1.6, 3.2, 2.4))
    # --- the lower arms: thin, jointed, one holds a blade of the void, the other an orb
    for s, arm in ((1, "arm2L"), (-1, "arm2R")):
        x = 11.5 * s
        m.c(arm, OBS, (x, 24.2, 1.5), (3, 6.4, 3))
        m.c(arm, GOLD, (x, 26.6, 1.5), (3.4, 0.8, 3.4))
        m.c(arm, ENDB, (x + 0.6 * s, 19.6, 3.4), (2.6, 2.6, 6))
        m.c(arm, OBS, (x + 0.6 * s, 19.6, 7.2), (3, 3, 2.6))
    # blade: a long amethyst edge on an obsidian hilt, glowing core line
    m.c("arm2L", GOLD, (12.1, 19.6, 9.2), (5, 0.9, 1.2))
    m.c("arm2L", OBS, (12.1, 19.6, 10.4), (1.4, 1.4, 1.6))
    m.c("arm2L", AME, (12.1, 19.6, 18.4), (0.9, 2.6, 14), light=True)
    m.c("arm2L", "magenta_concrete", (12.1, 19.6, 18.4), (1.05, 0.6, 13.6), light=True)
    m.c("arm2L", AME, (12.1, 19.6, 26.2), (0.9, 1.6, 2), (45, 0, 0), light=True)
    # orb: a beacon in a gold cage
    m.c("arm2R", "beacon", (-12.1, 19.6, 9.8), (2.6, 2.6, 2.6), light=True)
    m.c("arm2R", "purple_stained_glass", (-12.1, 19.6, 9.8), (3.6, 3.6, 3.6), (45, 45, 0), light=True)
    for k in range(4):
        a = math.radians(90 * k)
        m.c("arm2R", GOLD, (-12.1 + math.cos(a) * 2.2, 19.6, 9.8 + math.sin(a) * 2.2), (0.5, 4.2, 0.5))
    # --- broken fins on the back
    for s, fin in ((1, "finL"), (-1, "finR")):
        for k in range(3):
            m.c(fin, OBS if k != 1 else CRY, (s * (5 + k * 2.6), 37 + k * 2.4, -7.4 - k * 1.6), (1.2, 8 - k * 1.6, 4 - k * 0.6), (-25 - k * 10, 0, (-22 - k * 10) * s), light=k == 1)
        m.c(fin, GOLD, (5 * s, 33.6, -6.8), (2.4, 1.2, 2.4))
    # --- three rings of floating debris round the body
    for i, (y, r, n) in enumerate(((34, 21, 8), (24, 17, 7), (12, 12, 6))):
        for k in range(n):
            a = 360 * k / n + i * 17
            blk = (OBS, END, CRY, PUR)[(k + i) % 4]
            m.c(f"ring{i + 1}", blk, (r * math.cos(math.radians(a)), y + (k % 2) * 1.4, r * math.sin(math.radians(a))), (2.2 - 0.2 * (k % 3), 2.2, 2.2), (30 + k * 20, a, 45), light=blk == CRY)
    m.attacks = {"quake": "smash", "shockwave": "smash", "spikes": "smash", "meteor": "cast", "sonic_boom": "cast", "orbs": "cast",
                 "lightning": "cast", "pull": "roar", "darkness": "roar", "minions": "roar", "levitate": "cast", "blink": "spin",
                 "charge": "sweep", "dive": "dive", "skulls": "cast"}
    m.melee = "sweep"
    return m


SPAWN = [
    # the sky goes dark and the three legends' colours burn in a ring on the floor
    S("shrink", 0, s=0), fx(1, "REVERSE_PORTAL", 160, "ENTITY_ENDER_DRAGON_GROWL", 0.4, y=0, spread=6, ring=8),
    fx(4, "SCULK_SOUL", 60, "ENTITY_WARDEN_HEARTBEAT", 0.5, y=0, spread=4, ring=6), fx(8, "SOUL", 60, "ENTITY_WITHER_AMBIENT", 0.4, y=0, spread=5, ring=7),
    fx(14, sound="AMBIENT_SOUL_SAND_VALLEY_MOOD", pitch=0.5, lightning=True),
    # rubble rises from the ground and circles, the lower body forms from the trail upward
    S("move", 0, v=[0, -6, 0], only="ring"), S("pose", 16, 26, order="random", stagger=20, only="ring"),
    fx(18, "BLOCK", 120, "BLOCK_DEEPSLATE_BREAK", 0.5, y=0, spread=5, block="OBSIDIAN"),
    S("burst", 20, power=8, up=6, tilt=360, rand=3, only="tail"), S("pose", 22, 18, order="up", stagger=14, only="tail"),
    S("burst", 26, power=7, up=4, tilt=360, rand=2, only="core"), S("pose", 28, 16, order="up", stagger=12, only="core"),
    # the heart lights up alone in the air
    S("pose", 46, 4, only="heart"), S("flash", 46, 6, only="heart", block="white_concrete"),
    fx(46, "END_ROD", 80, "BLOCK_BEACON_ACTIVATE", 0.5, y=0.55, spread=1), fx(50, sound="ENTITY_WARDEN_HEARTBEAT", pitch=0.4),
    fx(56, sound="ENTITY_WARDEN_HEARTBEAT", pitch=0.4),
    # the chest plates fold in around the heart from the bottom up
    S("toward", 50, k=1, y=0.55, only="chest"), S("pose", 54, 16, order="up", stagger=14, only="chest"),
    fx(56, "SMOKE", 60, "BLOCK_RESPAWN_ANCHOR_CHARGE", 0.6, y=0.6, spread=2),
    # the great arms swing in from behind, then the lower arms with blade and orb
    S("move", 66, v=[0, 4, -10], only="arm"), S("pose", 68, 14, only="armL"), S("pose", 70, 14, only="armR"),
    S("pose", 68, 14, only="fore"), fx(78, sound="BLOCK_ANVIL_PLACE", pitch=0.5), S("shake", 80, 8),
    S("move", 80, v=[0, -3, -6], only="arm2"), S("pose", 82, 12, only="arm2"), S("pose", 80, 14, only="fin"),
    fx(90, "WITCH", 60, "ITEM_TRIDENT_RETURN", 0.5, y=0.5, spread=2.5),
    # the head comes down onto the shoulders with its crown, the eye opens last
    S("move", 92, v=[0, 10, 0], only="head"), S("move", 92, v=[0, 10, 0], only="jaw"), S("move", 92, v=[0, 10, 0], only="halo"),
    S("pose", 94, 14, only="head"), S("pose", 94, 14, only="jaw"), S("pose", 96, 16, order="random", stagger=10, only="halo"),
    S("swap", 94, block="black_concrete", only="pearlescent_froglight"), S("swap", 94, block="black_concrete", only="pink_concrete"),
    fx(108, sound="BLOCK_IRON_DOOR_CLOSE", pitch=0.5), S("shake", 108, 6),
    S("swap", 116, block="", only="pearlescent_froglight"), S("swap", 116, block="", only="pink_concrete"),
    S("flash", 116, 5, only="lit", block="magenta_concrete"), fx(116, "END_ROD", 60, "ENTITY_ELDER_GUARDIAN_CURSE", 0.5, y=0.85),
    # the veins burn on, it roars and the shockwave rolls out
    S("flash", 118, 3, only="vein", block="white_concrete", order="up", stagger=10),
    S("pose", 120, 2), S("anim", 122, 40, name="roar"), S("shake", 124, 20, amp=0.18),
    fx(124, "EXPLOSION_EMITTER", 3, "ENTITY_WITHER_SPAWN", 0.5, y=0.4, ring=8),
    fx(126, "SONIC_BOOM", 3, "ENTITY_WARDEN_SONIC_BOOM", 0.6, y=0.6), fx(128, "DRAGON_BREATH", 120, "ENTITY_ENDER_DRAGON_GROWL", 0.5, y=0.2, spread=6, ring=9),
]

DEATH = [
    # the heart stutters: three white flashes, each one harder
    S("flash", 0, 4), fx(0, sound="ENTITY_WARDEN_HEARTBEAT", pitch=0.4), S("shake", 0, 60, amp=0.12),
    S("flash", 10, 4, only="heart"), fx(10, "END_ROD", 40, "BLOCK_BEACON_DEACTIVATE", 0.5, y=0.55, spread=1),
    S("flash", 18, 5, only="lit", block="white_concrete"), fx(18, sound="ENTITY_WARDEN_HEARTBEAT", pitch=0.35),
    # every vein goes dark from the bottom up
    S("swap", 22, block="black_concrete", only="vein", order="up", stagger=18), fx(24, "LARGE_SMOKE", 60, "BLOCK_FIRE_EXTINGUISH", 0.4, y=0.5, spread=3),
    # the crown shards scatter, the debris rings fall
    S("burst", 26, 12, power=9, up=6, tilt=360, rand=2, only="halo"), S("drop", 28, 14, tilt=180, rand=2, only="ring", order="random", stagger=12),
    fx(30, "BLOCK", 80, "BLOCK_GLASS_BREAK", 0.6, y=0.9, spread=3, block="AMETHYST_BLOCK"),
    # the arms are torn away one after another and land in heaps
    S("anim", 30, 44, name="die_drop"),
    S("fling", 36, 18, power=7, up=4, tilt=160, only="arm2L"), S("fling", 40, 18, power=7, up=4, tilt=160, only="arm2R"),
    fx(36, sound="BLOCK_AMETHYST_CLUSTER_BREAK", pitch=0.6), fx(40, sound="BLOCK_BEACON_DEACTIVATE", pitch=0.6),
    S("fling", 46, 20, power=6, up=5, tilt=140, only="armL"), S("fling", 50, 20, power=6, up=5, tilt=140, only="armR"),
    S("fling", 46, 20, power=6, up=5, tilt=140, only="foreL"), S("fling", 50, 20, power=6, up=5, tilt=140, only="foreR"),
    fx(48, "EXPLOSION", 6, "ENTITY_GENERIC_EXPLODE", 0.6, y=0.5, spread=2), fx(52, "EXPLOSION", 6, "ENTITY_GENERIC_EXPLODE", 0.5, y=0.5, spread=2),
    # the plates pop off, the body falls in on the heart
    S("burst", 56, 10, power=4, up=3, tilt=200, rand=2, only="trim"), S("toward", 60, 18, k=0.85, y=0.55, only="!heart"),
    fx(60, "REVERSE_PORTAL", 160, "BLOCK_END_PORTAL_SPAWN", 0.6, y=0.55, spread=1.5),
    # the heart flares and it all breaks apart
    S("scale", 74, 6, s=[1.8, 1.8, 1.8], only="heart"), S("flash", 78, 6, block="white_concrete"),
    S("shatter", 80, 18, pieces=3, power=6, up=4, order="out", stagger=16),
    fx(80, "EXPLOSION_EMITTER", 4, "ENTITY_GENERIC_EXPLODE", 0.4, y=0.5, ring=8), fx(82, "END_ROD", 200, "ENTITY_ENDER_DRAGON_DEATH", 0.6, y=0.6, spread=6),
    fx(90, "FIREWORK", 120, "UI_TOAST_CHALLENGE_COMPLETE", 1.0, y=0.6, spread=5),
]
SPAWN_TEXT = "The three legends' colours burn in a ring, rubble rises and circles, the body forms around a lone void heart, four arms swing in, the crowned head descends and the eye opens."
DEATH_TEXT = "The heart stutters, the veins go dark, the crown scatters, all four arms are torn away and the body falls in on the heart before it bursts."

import recipes as _r
_r.SPAWN["the_unmaker"] = SPAWN
_r.DEATH["the_unmaker"] = DEATH
_r.SPAWN_TEXT["the_unmaker"] = SPAWN_TEXT
_r.DEATH_TEXT["the_unmaker"] = DEATH_TEXT
