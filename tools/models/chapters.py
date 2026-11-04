"""Chapter bosses: one waits at the end of every CQuests chapter. Chapter 5 (the Hollow King) and
chapter 10 (the Listener, a Warden) are the big ones."""
import math
from models import *
from seasonal import blob, ring

def boots(m, s, b, x, block, cuff=None, sole="polished_blackstone", toe=True):
    m.c(b, block, (x, 2.2, 0.6), (5, 4.4, 6.4))
    m.c(b, sole, (x, 0.35, 1), (5.4, 0.7, 7.2))
    if toe: m.c(b, block, (x, 1.4, 4), (4.4, 2.6, 1.6))
    if cuff: m.c(b, cuff, (x, 4.6, 0.6), (5.6, 1.2, 6.8))

def belt(m, bone, y, w, d, strap="brown_terracotta", buckle="gold_block", z=0):
    m.c(bone, strap, (0, y, z), (w + 0.4, 1.8, d + 0.4))
    m.c(bone, buckle, (0, y, z + d / 2 + 0.3), (2.6, 2.2, 0.4))
    m.c(bone, strap, (0, y, z + d / 2 + 0.55), (1.2, 1, 0.2))

def eyes(m, bone, y, z, gap, block, glow=True, size=(1.6, 1.2)):
    m.m(bone, "black_concrete", (gap, y, z), (size[0] + 0.6, size[1] + 0.6, 0.2))
    m.m(bone, block, (gap, y, z + 0.12), (size[0], size[1], 0.2), light=glow)

# ------------------------------------------------------------------------------------- chapter 1
@model
def brakka():
    """Brakka the Torchbearer: the bandit chief who burned the Wanderers' Camp. Leather and fur, a war-painted
    face, a burning torch in one hand and a cleaver in the other."""
    m = Model("brakka", "biped", 1.6)
    biped(m, hip=15, legx=3.6, neck=33, shoulder=31, armx=9)
    m.bone("jaw", "head", (0, 36, 3))
    m.bone("cleaver", "armR", (-9.5, 14, 2))
    m.bone("torch", "armL", (9.5, 14, 2))
    m.bone("cape", "body", (0, 32, -4))
    leather, leather2, fur, skin = "brown_terracotta", "spruce_planks", "light_gray_wool", "orange_terracotta"
    for s, b in ((1, "legL"), (-1, "legR")):
        boots(m, s, b, 3.6 * s, "dark_oak_planks", fur)
        m.c(b, leather, (3.6 * s, 10.4, 0), (4.4, 9, 4.6))
        m.c(b, "iron_block", (3.6 * s, 9, 2.5), (3.2, 2.4, 0.6))
        for y in (7.4, 12.6): m.c(b, "brown_wool", (3.6 * s, y, 0), (4.8, 0.8, 5))
    m.c("body", leather, (0, 23, 0), (14, 14, 8))
    m.c("body", leather2, (0, 25, 4.2), (10, 9, 0.6))
    for y in (22, 25, 28): m.c("body", "iron_block", (-3.6, y, 4.6), (1, 1, 0.3))
    belt(m, "body", 17.2, 14, 8)
    for k, (x, c) in enumerate(((-5, "red_concrete"), (5, "bone_block"))):
        m.c("body", c, (x, 15.4, 4.4), (1.6, 2.2, 0.6))
    m.c("body", "brown_wool", (0, 26, 0), (14.4, 1, 8.4), (0, 0, 35))
    m.c("body", fur, (0, 31, -0.4), (16, 3, 9.4))
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, fur, (9.4 * s, 31.4, 0), (5.6, 3, 6))
        m.c(a, skin, (9 * s, 26.5, 0), (4, 6.4, 4))
        m.c(a, "red_concrete", (9 * s, 26, 2.05), (2.4, 0.6, 0.2))
        m.c(a, leather, (9 * s, 20.4, 0.5), (4.4, 6, 4.4))
        m.c(a, skin, (9 * s, 15.6, 1), (3.6, 3.4, 3.6))
    m.c("head", skin, (0, 38.4, 0.4), (7.6, 7.6, 7.4))
    m.c("head", "red_concrete", (0, 39.6, 4.15), (7.8, 1.2, 0.2))
    eyes(m, "head", 39.6, 4.3, 1.8, "yellow_concrete", glow=False, size=(1.2, 0.9))
    m.c("head", "black_wool", (0, 42.6, -0.4), (8, 1.4, 8))
    for k in range(5): m.c("head", "black_wool", (0, 43.6 + k * 0.2, -3 + k * 1.4), (1.6, 2.4, 1.4), (-20, 0, 0))
    m.c("jaw", "brown_wool", (0, 34.6, 3.2), (6.4, 2.6, 2.6))
    m.c("jaw", "white_concrete", (0, 35.8, 4.4), (3, 0.6, 0.3))
    m.c("head", "orange_terracotta", (0, 38, 4.6), (1.4, 2, 1))
    for z, h in ((0.5, 3), (-2.2, 3.4)): m.m("head", "bone_block", (4.2, 39, z), (0.8, h, 0.8), (0, 0, -15))
    m.c("cape", fur, (0, 22, -4.8), (13, 20, 0.8), (6, 0, 0), (0, 32, -4.4))
    for x in (-4.4, -1.4, 1.6, 4.6): m.c("cape", fur, (x, 11.4, -6), (2.4, 2, 0.8), (6, 0, 0), (0, 32, -4.4))
    # cleaver
    m.c("cleaver", "dark_oak_log", (-9.5, 14, 6), (1.4, 1.4, 6))
    m.c("cleaver", "iron_block", (-9.5, 15.4, 14), (0.6, 6.4, 10))
    m.c("cleaver", "polished_andesite", (-9.5, 12.4, 14), (0.65, 0.8, 10))
    m.c("cleaver", "redstone_block", (-9.5, 16.8, 17), (0.7, 1.2, 1.4))
    # torch with real fire
    m.c("torch", "spruce_log", (9.5, 18, 2.6), (1.6, 14, 1.6))
    m.c("torch", "brown_wool", (9.5, 24.6, 2.6), (2.4, 2.2, 2.4))
    m.c("torch", "shroomlight", (9.5, 27, 2.6), (2.4, 2.8, 2.4), light=True)
    m.c("torch", "orange_stained_glass", (9.5, 29, 2.6), (1.8, 2.4, 1.8), (0, 45, 0), light=True)
    m.c("torch", "yellow_stained_glass", (9.5, 30.6, 2.6), (1, 1.6, 1), (0, 45, 0), light=True)
    m.hold = {"cleaver": 40, "torch": 0}
    m.attacks = {"fire_ring": "sweep", "charge": "lunge", "minions": "roar", "slam": "slam", "breath": "cast"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 2
@model
def gate_shade():
    """The Gate Shade: a hooded shadow that hangs in the broken gate, chained, with a lantern and hands of smoke."""
    m = Model("gate_shade", "float", 1.8)
    m.bone("core", "root", (0, 20, 0))
    m.bone("head", "core", (0, 34, 0))
    m.mbone("armL", "core", (9, 31, 0))
    for i in (1, 2, 3): m.bone(f"ring{i}", "root", (0, 0, 0))
    m.bone("lantern", "armL", (11, 16, 2))
    robe, robe2 = "black_wool", "gray_wool"
    # a robe that tapers into wisps instead of legs
    for k, (w, d) in enumerate(((13, 9), (12, 8.4), (10.6, 7.6), (9, 6.6), (7, 5.4), (5, 4))):
        m.c("core", robe if k % 2 == 0 else "black_concrete", (0, 30 - k * 3.6, 0), (w, 3.6, d))
    for x, z, h in ((-3, 1, 5), (2.4, -1, 7), (0.6, 2, 4), (-1.4, -1.6, 6)):
        m.c("core", "black_stained_glass", (x, 8 - h / 2, z), (1.4, h, 1.4))
    m.c("core", robe2, (0, 31, 0), (14, 1.2, 9.6))
    # chains wrapped around the body
    for y, r in ((26, 20), (20, -25)):
        m.c("core", "chain", (0, y, 0), (13.6, 1, 9.2), (0, 0, r))
    m.c("core", "iron_block", (0, 23, 4.8), (2.6, 2.6, 1), light=False)
    # its glowing soul heart (weak spot) seen through a tear in the robe
    m.c("core", "soul_lantern", (0, 27, 3.8), (3.4, 3.4, 2), light=True)
    # hood with nothing inside but two eyes
    m.c("head", robe, (0, 39, -0.6), (10, 10, 9.4))
    m.c("head", robe, (0, 43.6, -3.6), (6, 4, 5), (-30, 0, 0))
    m.c("head", "black_concrete", (0, 38.6, 4.2), (7, 7.4, 0.4))
    eyes(m, "head", 39.4, 4.45, 1.8, "light_blue_concrete", size=(1.4, 0.8))
    m.c("head", robe2, (0, 34.6, 3.6), (10.2, 1, 2))
    # long sleeves ending in smoky claws
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, robe, (10.4 * s, 25, 0), (4.6, 12, 4.6), (0, 0, 10 * s))
        m.c(a, robe2, (11.4 * s, 18.6, 0.4), (5, 1, 5))
        for k in (-1, 0, 1):
            m.c(a, "black_stained_glass", (11.4 * s + k * 1.2, 15.6, 1.4), (0.6, 4, 0.6), (20, 0, k * 10))
    m.c("lantern", "chain", (11, 13, 2), (0.6, 4, 0.6))
    m.c("lantern", "soul_lantern", (11, 9.4, 2), (3.4, 4, 3.4), light=True)
    for k in range(6):
        a = k * 60
        m.c("ring1", "chain", (12 * math.cos(math.radians(a)), 26, 12 * math.sin(math.radians(a))), (0.8, 3, 0.8), (0, a, 60))
    for k in range(4):
        a = k * 90 + 20
        m.c("ring2", "soul_lantern", (14 * math.cos(math.radians(a)), 34, 14 * math.sin(math.radians(a))), (1.4, 1.8, 1.4), (0, a, 0), light=True)
    m.hold = {"lantern": 0}
    m.attacks = {"darkness": "raise", "blink": "dive", "pull": "pulse", "orbs": "spin", "minions": "raise"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 3
@model
def oakheart():
    """Sir Oakheart: the Elder's champion, a knight grown from an old oak, bark armour, mossy shoulders,
    a living-wood shield and a sword of polished root."""
    m = Model("oakheart", "biped", 1.8)
    biped(m, hip=16, legx=4, neck=34, shoulder=32, armx=10)
    m.bone("sword", "armR", (-10.5, 14, 2))
    m.bone("shield", "armL", (12, 22, 2))
    bark, wood, moss, leaf = "oak_log", "stripped_oak_log", "moss_block", "flowering_azalea_leaves"
    for s, b in ((1, "legL"), (-1, "legR")):
        m.c(b, bark, (4 * s, 3, 0.4), (5.4, 6, 6.4))
        for k in (-1.6, 0, 1.6): m.c(b, wood, (4 * s + k, 0.8, 4), (1.2, 1.4, 2.6), (0, k * 10, 0))
        m.c(b, bark, (4 * s, 11, 0), (4.6, 10, 5))
        m.c(b, moss, (4 * s, 9, 2.6), (3, 3.4, 0.6))
    m.c("body", bark, (0, 25, 0), (14, 15, 8.4))
    m.c("body", wood, (0, 25.6, 4.4), (8, 11, 0.6))
    # the heart of the oak: a glowing amber knot in the chest
    m.c("body", "ochre_froglight", (0, 26, 4.8), (3.6, 3.6, 0.8), light=True)
    m.c("body", "honeycomb_block", (0, 26, 4.6), (5.4, 5.4, 0.4))
    belt(m, "body", 18.2, 14, 8.4, strap="dark_oak_log", buckle="moss_block")
    for x, y in ((-5.4, 30.4), (5.8, 21.4), (-6.4, 20)): m.c("body", leaf, (x, y, 4.4), (2, 2, 1.2))
    for s, a in ((1, "armL"), (-1, "armR")):
        blob(m, a, moss, (10.6 * s, 32.6, 0), (6.4, 3.6, 7), 1.2)
        m.c(a, leaf, (11.4 * s, 34.6, -1), (2.8, 1.6, 3))
        m.c(a, bark, (10 * s, 26, 0), (4.4, 8, 4.6))
        m.c(a, bark, (10 * s, 19, 0.6), (4, 6, 4.2))
        m.c(a, wood, (10 * s, 15, 1), (3.6, 3, 3.6))
    m.c("head", bark, (0, 39.4, 0.2), (8.4, 8.6, 8))
    m.c("head", wood, (0, 39, 4.25), (6.4, 6, 0.2))
    m.c("head", "black_concrete", (0, 40.6, 4.4), (6, 1, 0.2))
    m.m("head", "lime_concrete", (1.8, 40.6, 4.5), (1.2, 0.6, 0.2), light=True)
    m.c("head", "dark_oak_log", (0, 38, 4.4), (1, 3.6, 0.2))
    # antler branches and a crown of leaves
    mhorn(m, "head", "oak_log", (3, 43.4, 0), 3, (0, 0, -30), (-10, 0, -10), 1.4, 0.8)
    mhorn(m, "head", "oak_log", (3.6, 44.6, -1), 2, (-20, 0, -60), (0, 0, 20), 1, 0.8)
    for x, z in ((-2.6, -2), (2.4, 1.6), (0, -0.4), (-1, 2.6)): m.c("head", leaf, (x, 44.6, z), (2.6, 2, 2.6))
    m.c("head", "pink_concrete", (3.4, 45.4, 0.6), (0.8, 0.8, 0.8), light=True)
    # sword of root wood, with a gold guard
    m.c("sword", "dark_oak_log", (-10.5, 14, 4), (1.4, 1.4, 4))
    m.c("sword", "gold_block", (-10.5, 14, 6.6), (4.6, 1.2, 1.2))
    m.c("sword", "stripped_dark_oak_log", (-10.5, 14, 15), (1.2, 2.4, 16))
    m.c("sword", "verdant_froglight", (-10.5, 14, 15), (1.25, 0.5, 14), light=True)
    # round shield of a tree slice
    m.c("shield", "oak_log", (13.2, 22, 2), (1.2, 11, 11))
    m.c("shield", "stripped_oak_log", (13.85, 22, 2), (0.2, 8, 8))
    m.c("shield", "moss_block", (13.95, 22, 2), (0.2, 3, 3))
    m.hold = {"sword": 40}
    m.attacks = {"spikes": "slam", "heal": "cast", "pull": "sweep", "charge": "lunge", "shockwave": "stomp"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 4
@model
def keywarden():
    """The Keywarden: a giant lock with legs, guarding the Five Keys. A padlock body, five glowing keyholes,
    chain arms and a key the size of a tree as its weapon."""
    m = Model("keywarden", "biped", 1.85)
    biped(m, hip=14, legx=5, neck=34, shoulder=31, armx=11)
    m.bone("key", "armR", (-11.5, 13, 2))
    for s, b in ((1, "legL"), (-1, "legR")):
        boots(m, s, b, 5 * s, "iron_block", "gold_block", sole="polished_deepslate")
        m.c(b, "chain", (5 * s, 9.6, 0), (2.4, 9, 2.4))
        m.c(b, "iron_block", (5 * s, 13.4, 0), (4.4, 2, 4.4))
    # padlock body: a heavy gold case with iron rivets and the shackle arching over the head
    blob(m, "body", "gold_block", (0, 24, 0), (18, 18, 10), 1.6)
    for x in (-7.6, 7.6):
        for y in (17, 24, 31): m.c("body", "iron_block", (x, y, 5.1), (1.2, 1.2, 0.4))
    m.c("body", "raw_gold_block", (0, 15, 0), (18.6, 1.4, 10.6))
    # the five keyholes glow, the middle one brightest (weak spot)
    for k, (x, y) in enumerate(((0, 25), (-5, 28.4), (5, 28.4), (-5, 20), (5, 20))):
        sz = 1.6 if k else 2.6
        m.c("body", "black_concrete", (x, y, 5.05), (sz * 1.4, sz * 1.4, 0.3))
        m.c("body", ("pearlescent_froglight" if k == 0 else ("lime_concrete", "light_blue_concrete", "red_concrete", "magenta_concrete")[k - 1]), (x, y + sz * 0.2, 5.2), (sz * 0.8, sz * 0.8, 0.3), light=True)
        m.c("body", "black_concrete", (x, y - sz * 0.6, 5.1), (sz * 0.4, sz * 0.8, 0.3))
    for s in (1, -1):
        m.c("body", "iron_block", (5.6 * s, 37, 0), (2.4, 6, 2.4))
    m.c("body", "iron_block", (0, 41, 0), (13.6, 2.4, 2.4))
    # chain arms ending in iron gauntlets
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, "iron_block", (11.4 * s, 30.6, 0), (5, 4, 5))
        m.c(a, "chain", (11.4 * s, 23.6, 0), (2.4, 10, 2.4))
        m.c(a, "iron_block", (11.4 * s, 16, 1), (4.4, 4.6, 4.4))
    # the head is a small cut key bow with two eyes
    m.c("head", "gold_block", (0, 37, 1.4), (6, 5, 3))
    eyes(m, "head", 37.4, 3, 1.4, "yellow_concrete", size=(1, 1))
    # the key weapon
    m.c("key", "gold_block", (-11.5, 13, 18), (1.6, 1.6, 26))
    blob(m, "key", "gold_block", (-11.5, 13, 4.4), (1.6, 6, 6), 1)
    m.c("key", "black_concrete", (-11.5, 13, 4.4), (1.7, 2.4, 2.4))
    for z, h in ((26, 4), (29, 6), (31.4, 3)): m.c("key", "gold_block", (-11.5, 13 - h / 2, z), (1.6, h, 1.8))
    m.hold = {"key": 40}
    m.attacks = {"slam": "slam", "shockwave": "stomp", "pull": "sweep", "quake": "slam", "orbs": "cast"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 5 (BIG)
@model
def hollow_king():
    """The Hollow King: the ancient king who wakes at the end of chapter 5. Twice as tall as the others,
    rusted royal armour over nothing, a soul fire crown, a torn royal cape and a greatsword."""
    m = Model("hollow_king", "biped", 2.8)
    biped(m, hip=17, legx=4.2, neck=36, shoulder=34, armx=10.5)
    m.bone("jaw", "head", (0, 39, 3))
    m.bone("cape", "body", (0, 35, -4.5))
    m.bone("blade", "armR", (-11, 14, 2))
    plate, plate2, trim, cloth = "netherite_block", "polished_deepslate", "gold_block", "purple_wool"
    for s, b in ((1, "legL"), (-1, "legR")):
        boots(m, s, b, 4.2 * s, plate, trim)
        m.c(b, plate2, (4.2 * s, 9.6, 0), (4.8, 6, 5))
        m.c(b, plate, (4.2 * s, 9.6, 2.7), (3.6, 3, 0.6))
        m.c(b, trim, (4.2 * s, 11.2, 2.9), (3.6, 0.6, 0.4))
        m.c(b, plate, (4.2 * s, 14.6, 0), (5, 4, 5.4))
    # skirt of armour plates (tassets)
    for x in (-4.6, -1.6, 1.6, 4.6):
        m.c("hips", plate2, (x, 15.4, 4.6), (2.8, 5, 0.8), (-8, 0, 0))
        m.c("hips", trim, (x, 13.2, 5), (2.8, 0.6, 0.6), (-8, 0, 0))
    m.c("hips", cloth, (0, 12, 4.8), (4, 10, 0.6))
    m.c("hips", trim, (0, 7.4, 5.1), (4.4, 0.8, 0.4))
    # breastplate over a hollow chest: soul fire burns where the heart should be (weak spot)
    m.c("body", plate, (0, 27, 0), (15, 15, 9))
    m.c("body", plate2, (0, 28, 4.6), (11, 10, 0.6))
    m.c("body", trim, (0, 33.4, 4.7), (13, 0.8, 0.6))
    m.c("body", trim, (0, 20.4, 4.7), (13, 0.8, 0.6))
    m.c("body", "black_concrete", (0, 28, 4.9), (5.4, 6.4, 0.5))
    m.c("body", "soul_lantern", (0, 28, 4.4), (4.2, 4.6, 1.6), light=True)
    for y in (26, 28, 30): m.m("body", "bone_block", (1.9, y, 5.1), (1.4, 0.7, 0.3))
    belt(m, "body", 19.6, 15, 9, strap="black_wool", buckle="gold_block")
    # huge layered pauldrons with gold rims and spikes
    for s, a in ((1, "armL"), (-1, "armR")):
        blob(m, a, plate, (11.4 * s, 35, 0), (7.6, 4.6, 8.6), 1.4)
        m.c(a, plate2, (12 * s, 32.6, 0), (7, 2.4, 8.2), (0, 0, -15 * s))
        m.c(a, trim, (12.4 * s, 31.4, 0), (7.2, 0.6, 8.4), (0, 0, -15 * s))
        horn(m, a, "gold_block", (12.4 * s, 37, 0), 2, (0, 0, -25 * s), (0, 0, -10 * s), 1.2)
        m.c(a, plate2, (10.5 * s, 27.4, 0), (4.4, 7, 4.6))
        m.c(a, plate, (10.5 * s, 20.6, 0.6), (4.8, 6, 5))
        m.c(a, trim, (10.5 * s, 18, 0.6), (5, 0.8, 5.2))
        m.c(a, plate2, (10.5 * s, 15.6, 1), (4, 3.4, 4))
    # the head: a closed great helm, empty but for soul light in the visor, a crown of soul fire
    m.c("head", plate, (0, 41.4, 0.4), (9, 9.4, 9))
    m.c("head", plate2, (0, 41, 5), (7.6, 7, 0.4))
    m.c("head", "black_concrete", (0, 42, 5.25), (6.4, 1.2, 0.2))
    m.m("head", "light_blue_concrete", (1.8, 42, 5.35), (1.4, 0.6, 0.2), light=True)
    for x in (-2.4, -0.8, 0.8, 2.4): m.c("head", "black_concrete", (x, 39.2, 5.25), (0.5, 2.6, 0.2))
    m.c("jaw", plate2, (0, 37.2, 2.6), (7.6, 1.6, 5))
    m.c("head", trim, (0, 46.6, 0.4), (10, 1.4, 9.6))
    for k in range(8):
        a = k * 45
        h = 3.6 if k % 2 == 0 else 2.2
        m.c("head", trim, (4.6 * math.sin(math.radians(a)), 47.4 + h / 2, 0.4 + 4.4 * math.cos(math.radians(a))), (1.2, h, 1.2), (0, a, 0))
    for k in range(4):
        a = k * 90 + 45
        m.c("head", "soul_lantern", (3.4 * math.sin(math.radians(a)), 49.6, 0.4 + 3.4 * math.cos(math.radians(a))), (1.2, 1.6, 1.2), (0, a, 0), light=True)
    m.c("head", "crying_obsidian", (0, 48.6, 5.1), (1.8, 1.8, 0.6), (0, 0, 45), light=True)
    # torn royal cape with a fur collar
    m.c("cape", "white_wool", (0, 35.6, -1), (16, 2.6, 10))
    for k in range(4): m.c("cape", "black_wool", (-5.4 + k * 3.6, 35.8, 4.1), (0.8, 1, 0.3))
    m.c("cape", cloth, (0, 21, -5.6), (15, 28, 0.8), (7, 0, 0), (0, 35, -5))
    m.c("cape", trim, (0, 21, -6.1), (1.4, 28, 0.4), (7, 0, 0), (0, 35, -5))
    for i, x in enumerate((-6, -3, 0, 3, 6)):
        m.c("cape", cloth, (x, 5.4 - (i % 2) * 1.4, -7.6), (2.6, 2.8 + (i % 2) * 1.6, 0.8), (7, 0, 0), (0, 35, -5))
    # greatsword with a glowing fuller
    m.c("blade", "black_concrete", (-11, 14, 3), (1.6, 1.6, 5))
    m.c("blade", trim, (-11, 14, 6.6), (6, 1.4, 1.4))
    m.c("blade", "crying_obsidian", (-11, 14, 6.6), (1.4, 1.5, 1.5), (0, 0, 45), light=True)
    m.c("blade", "iron_block", (-11, 14, 20), (1, 3.4, 25))
    m.c("blade", "light_blue_concrete", (-11, 14, 19), (1.05, 0.8, 21), light=True)
    m.c("blade", "iron_block", (-11, 14, 33.4), (1, 1.8, 2), (45, 0, 0))
    m.hold = {"blade": 40}
    m.attacks = {"slam": "slam", "minions": "roar", "darkness": "cast", "shockwave": "stomp", "meteor": "cast", "charge": "lunge", "spikes": "slam"}
    m.melee = "sweep"
    return m

# ------------------------------------------------------------------------------------- chapter 6
@model
def iron_tusk():
    """Iron Tusk: a war boar in riveted iron plates with a furnace in its chest and two huge tusks."""
    m = Model("iron_tusk", "quad", 1.9)
    quad(m, body_y=16, legx=6, legz_front=9, legz_back=-9, neck_y=18, neck_z=13)
    hide, plate, rivet = "brown_terracotta", "iron_block", "polished_andesite"
    blob(m, "body", hide, (0, 17, 0), (15, 13, 26), 2.4)
    for z in (-8, -1, 6):
        m.c("body", plate, (0, 23.4, z), (14, 1.4, 6.4))
        m.m("body", plate, (7.4, 18.6, z), (1, 8, 6.4))
        for x in (-6, 0, 6): m.c("body", rivet, (x, 24.2, z + 2.6), (0.7, 0.4, 0.7))
    # a furnace grill on its chest (weak spot) with fire showing
    m.c("body", "blast_furnace", (0, 15.4, 13.4), (6, 6, 1.2))
    m.c("body", "orange_concrete", (0, 14.4, 14.05), (4, 2, 0.2), light=True)
    m.c("body", "magma_block", (0, 15.4, 13), (5, 5, 0.6), light=True)
    # bristles of iron bars along the spine and a smoking exhaust
    for z in range(-10, 12, 3): m.c("body", "iron_bars", (0, 26, z), (0.6, 3, 2.4), (-25, 0, 0))
    m.c("body", "blackstone", (4, 26.6, -7), (2, 4, 2))
    for s, (b, z) in ((s, x) for s in (1, -1) for x in (("legFL" if s > 0 else "legFR", 9), ("legBL" if s > 0 else "legBR", -9))):
        m.c(b, hide, (6 * s, 9.4, z), (4.6, 8, 4.6))
        m.c(b, plate, (6 * s, 5, z), (4.8, 4, 4.8))
        m.c(b, "black_concrete", (6 * s, 0.8, z + 0.8), (4.4, 1.6, 4.6))
    blob(m, "head", hide, (0, 17, 19), (11, 10, 9), 1.6)
    m.c("head", "pink_terracotta", (0, 15.6, 24), (6, 4.4, 1.4))
    m.m("head", "black_concrete", (1.4, 15.6, 24.75), (1, 1.6, 0.2))
    m.c("head", plate, (0, 21.2, 19), (11.6, 1.6, 9))
    m.m("head", "red_concrete", (4.1, 18.6, 23.4), (1.2, 1.2, 0.3), light=True)
    m.m("head", hide, (5.6, 21.6, 16), (2, 3, 1), (0, 0, -30))
    m.c("jaw", hide, (0, 12.6, 20.4), (8, 2, 6))
    mhorn(m, "jaw", "bone_block", (3.6, 13.6, 22.6), 4, (-20, 0, -12), (-22, 0, -4), 1.6, 0.82)
    m.c("tail", hide, (0, 19, -15.4), (1, 1, 3), (40, 0, 0))
    m.attacks = {"charge": "charge", "quake": "rear", "shockwave": "rear", "fire_ring": "howl", "slam": "rear", "minions": "howl"}
    m.melee = "bite"
    return m

# ------------------------------------------------------------------------------------- chapter 7
@model
def captain_brine():
    """Captain Brine of the Drowned: a soaked sea captain with a coral beard, a barnacled coat,
    a lantern of glowing kelp and a rusted anchor on a chain."""
    m = Model("captain_brine", "biped", 1.8)
    biped(m, hip=15, legx=3.8, neck=33, shoulder=31, armx=10)
    m.bone("jaw", "head", (0, 36, 3))
    m.bone("anchor", "armR", (-10.5, 14, 2))
    m.bone("cape", "body", (0, 32, -4))
    coat, coat2, skin = "cyan_terracotta", "blue_terracotta", "dark_prismarine"
    for s, b in ((1, "legL"), (-1, "legR")):
        boots(m, s, b, 3.8 * s, "black_terracotta", "brown_terracotta")
        m.c(b, "light_gray_terracotta", (3.8 * s, 10.6, 0), (4.4, 9, 4.6))
    m.c("legR", "dark_oak_log", (-3.8, 3.6, 0.6), (2.2, 6, 2.2))
    m.c("body", coat, (0, 23, 0), (14, 14, 8))
    m.c("body", "white_wool", (0, 26, 4.2), (5, 8, 0.4))
    for y in (28, 24, 20):
        m.m("body", "gold_block", (3.6, y, 4.25), (1, 1, 0.3))
    belt(m, "body", 17.6, 14, 8, strap="black_terracotta")
    for x, y, c in ((-5, 22, "tube_coral_block"), (5.4, 27, "brain_coral_block"), (-4, 29.6, "fire_coral_block"), (6, 19.4, "horn_coral_block")):
        m.c("body", c, (x, y, 4.3), (1.8, 1.6, 0.8))
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, coat2, (10.3 * s, 31.6, 0), (5.6, 2.6, 6))
        for k in (-1.6, 0, 1.6): m.c(a, "gold_block", (12.6 * s, 30.6, k), (0.4, 1.6, 0.6))
        m.c(a, coat, (10 * s, 25.6, 0), (4.4, 8, 4.6))
        m.c(a, coat, (10 * s, 19, 0.6), (4.2, 6, 4.4))
        m.c(a, "gold_block", (10 * s, 16.6, 0.6), (4.6, 0.8, 4.8))
        m.c(a, skin, (10 * s, 14.6, 1), (3.4, 3, 3.4))
    m.c("cape", coat, (0, 18, -4.6), (14, 26, 0.6), (5, 0, 0), (0, 32, -4.4))
    for x in (-4, 0, 4): m.c("cape", coat2, (x, 4.8, -5.8), (3, 2, 0.6), (5, 0, 0), (0, 32, -4.4))
    m.c("head", skin, (0, 38.4, 0.4), (7.6, 7.6, 7.4))
    eyes(m, "head", 39.4, 4.25, 1.8, "sea_lantern", size=(1.4, 1))
    m.c("jaw", "fire_coral_block", (0, 34.2, 3.2), (6.6, 3.6, 2.2))
    for x in (-2, 0, 2): m.c("jaw", "fire_coral_block", (x, 31.6, 3.6), (1.4, 2.6, 1.2), (0, 0, x * 8))
    # tricorne hat
    m.c("head", "black_wool", (0, 42.6, 0.4), (12, 1, 10))
    m.c("head", "black_wool", (0, 44.4, 0.4), (8, 3, 7.4))
    m.c("head", "gold_block", (0, 43.2, 5.4), (8, 0.6, 0.4))
    m.c("head", "white_concrete", (0, 44.4, 4.3), (1.6, 1.6, 0.2))
    m.c("head", "kelp_block" if False else "dried_kelp_block", (3.6, 41, -3.4), (1, 4, 1), (20, 0, -30))
    # anchor
    m.c("anchor", "chain", (-10.5, 9, 2.6), (0.8, 10, 0.8))
    m.c("anchor", "oxidized_copper", (-10.5, 2, 2.6), (1.6, 12, 1.6))
    m.c("anchor", "oxidized_copper", (-10.5, 7, 2.6), (6, 1.4, 1.4))
    for s in (1, -1):
        m.c("anchor", "oxidized_copper", (-10.5 + 3.2 * s, -3, 2.6), (1.4, 6, 1.4), (0, 0, -40 * s))
        m.c("anchor", "weathered_copper", (-10.5 + 5.4 * s, -1, 2.6), (1.8, 1.8, 1.8), (0, 0, 45))
    m.hold = {"anchor": 0}
    m.attacks = {"pull": "sweep", "slam": "slam", "frost": "cast", "minions": "roar", "orbs": "cast", "shockwave": "stomp"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 8
@model
def ember_queen():
    """The Ember Queen of the Ember Court: a tall queen of blackstone and fire, a gown of lava folds,
    a crown of flames and a fan of fire feathers behind her."""
    m = Model("ember_queen", "float", 1.85)
    m.bone("core", "root", (0, 18, 0))
    m.bone("head", "core", (0, 37, 0))
    m.mbone("armL", "core", (7.5, 34, 0))
    for i in (1, 2, 3): m.bone(f"ring{i}", "root", (0, 0, 0))
    m.bone("fan", "core", (0, 34, -4))
    gown, gown2, skin = "red_nether_bricks", "nether_bricks", "polished_blackstone"
    for k, (w, d) in enumerate(((16, 14), (14.4, 12), (12.6, 10.4), (10.6, 9), (9, 7.4), (8, 6.4))):
        m.c("core", gown if k % 2 else gown2, (0, 8 + k * 3.6, 0), (w, 3.6, d))
        if k < 3: m.c("core", "magma_block", (0, 8 + k * 3.6 - 1.4, d / 2), (w * 0.6, 0.8, 0.4), light=True)
    m.c("core", skin, (0, 32, 0), (8.6, 7, 5.6))
    m.c("core", "gold_block", (0, 29, 0), (9, 1, 6))
    m.c("core", "shroomlight", (0, 32, 2.9), (2.6, 2.6, 0.4), light=True)
    m.c("core", "gold_block", (0, 35.6, 0), (10, 1.6, 6.4))
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, skin, (8.6 * s, 29.6, 0), (2.4, 9, 2.4), (0, 0, 8 * s))
        m.c(a, "gold_block", (9.2 * s, 25.6, 0), (2.8, 0.8, 2.8))
        m.c(a, skin, (9.4 * s, 22.4, 0.6), (2.2, 5.4, 2.2))
        m.c(a, "orange_stained_glass", (9.4 * s, 19, 1), (1.6, 2, 1.6), light=True)
    m.c("head", skin, (0, 40.4, 0.2), (6.4, 6.8, 6.2))
    eyes(m, "head", 41, 3.35, 1.4, "yellow_concrete", size=(1.2, 0.6))
    m.c("head", "red_concrete", (0, 38.8, 3.4), (2, 0.5, 0.2))
    for k in range(7):
        a = (k - 3) * 22
        h = 6 - abs(k - 3) * 0.9
        m.c("head", "gold_block", (3.4 * math.sin(math.radians(a)), 44.4 + h / 2 - 1, 3.4 * math.cos(math.radians(a)) - 1), (1, h, 1), (0, a, 0))
        m.c("head", "orange_stained_glass", (3.4 * math.sin(math.radians(a)), 44.6 + h, 3.4 * math.cos(math.radians(a)) - 1), (1.2, 1.8, 1.2), (0, a, 0), light=True)
    m.c("head", skin, (0, 42, -3.4), (5, 6, 2))
    for k in range(9):
        a = (k - 4) * 18
        m.c("fan", "orange_concrete" if k % 2 else "red_concrete", (9 * math.sin(math.radians(a)), 36 + 9 * math.cos(math.radians(a)) - 2, -6), (1.8, 12, 0.6), (0, 0, -a), (0, 34, -6), light=k % 2 == 0)
    for k in range(6):
        a = k * 60
        m.c("ring1", "magma_block", (12 * math.cos(math.radians(a)), 22, 12 * math.sin(math.radians(a))), (1.8, 1.8, 1.8), (45, a, 45), light=True)
    m.attacks = {"fire_ring": "spin", "meteor": "raise", "breath": "pulse", "orbs": "raise", "blink": "dive", "minions": "raise"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 9
@model
def choirmaster():
    """The Choirmaster of the Bone Choir: a skeleton conductor floating in a ring of singing skulls, with an
    organ-pipe spine and a femur baton."""
    m = Model("choirmaster", "float", 1.8)
    m.bone("core", "root", (0, 20, 0))
    m.bone("head", "core", (0, 35, 0))
    m.bone("jaw", "head", (0, 36, 3))
    m.mbone("armL", "core", (8, 32, 0))
    for i in (1, 2, 3): m.bone(f"ring{i}", "root", (0, 0, 0))
    m.bone("baton", "armR", (-10, 16, 2))
    bone, robe = "bone_block", "black_wool"
    # a choir robe over bare bones, with a white collar
    for k, (w, d) in enumerate(((12, 9), (11, 8.4), (10, 7.6), (9, 7))):
        m.c("core", robe, (0, 12 + k * 4, 0), (w, 4, d))
    m.c("core", "white_wool", (0, 31.6, 0), (12, 1.6, 8.6))
    m.c("core", "red_wool", (0, 30, 4.4), (2, 3, 0.4))
    # organ pipes rising from its back
    for k, h in enumerate((10, 14, 18, 14, 10)):
        m.c("core", "gold_block", ((k - 2) * 2, 26 + h / 2, -5), (1.6, h, 1.6))
        m.c("core", "black_concrete", ((k - 2) * 2, 26 + h * 0.7, -4.15), (0.8, 0.6, 0.2))
    # ribs showing through a tear, the bell heart rings (weak spot)
    for y in (27, 25, 23): m.m("core", bone, (2.4, y, 4.2), (3, 0.8, 0.6))
    m.c("core", "gold_block", (0, 25, 3.6), (2.4, 2.6, 1.4), light=True)
    for s, a in ((1, "armL"), (-1, "armR")):
        m.c(a, robe, (9 * s, 29, 0), (4, 6, 4))
        m.c(a, bone, (9.4 * s, 22.4, 0.6), (1.6, 7, 1.6))
        m.c(a, "white_wool", (9.4 * s, 25.6, 0.6), (3.6, 1, 3.6))
        for k in (-0.7, 0, 0.7): m.c(a, bone, (9.4 * s + k, 18, 1.2), (0.5, 2, 0.5), (15, 0, 0))
    blob(m, "head", "calcite", (0, 39.4, 0.4), (7.6, 7, 7.2), 1.2)
    m.m("head", "black_concrete", (1.8, 40, 4.05), (2, 2, 0.2))
    m.m("head", "light_blue_concrete", (1.8, 40, 4.15), (0.7, 0.7, 0.2), light=True)
    m.c("head", "black_concrete", (0, 38.2, 4.05), (0.8, 1, 0.2))
    m.c("jaw", "calcite", (0, 35.4, 1.8), (6, 1.6, 5))
    for x in (-2, -0.7, 0.7, 2): m.c("jaw", "white_concrete", (x, 36.4, 4.2), (0.7, 0.8, 0.4))
    m.c("baton", bone, (-10, 16, 8), (1, 1, 12))
    m.c("baton", "calcite", (-10, 16, 14.4), (1.8, 1.8, 1.8))
    # the choir: skulls with open mouths circling, each a different size
    for k in range(6):
        a = k * 60
        x, z = 15 * math.cos(math.radians(a)), 15 * math.sin(math.radians(a))
        y = 30 + (k % 2) * 4
        m.c("ring1", "calcite", (x, y, z), (3.4, 3.4, 3.4), (0, -a + 90, 0))
        m.c("ring1", "black_concrete", (x + 1.75 * math.cos(math.radians(a)), y - 0.6, z + 1.75 * math.sin(math.radians(a))), (1, 1.4, 0.2), (0, -a + 90, 0))
    for k in range(8):
        a = k * 45 + 22
        m.c("ring2", "bone_block", (11 * math.cos(math.radians(a)), 16, 11 * math.sin(math.radians(a))), (0.8, 3, 0.8), (0, -a, 40))
    m.hold = {"baton": 25}
    m.attacks = {"minions": "raise", "skulls": "spin", "shockwave": "pulse", "darkness": "raise", "sonic_boom": "pulse", "orbs": "spin"}
    m.melee = "swipe"
    return m

# ------------------------------------------------------------------------------------- chapter 10 (BIG)
@model
def the_listener():
    """The Listener Below: a Warden from the deep dark, the last boss of the story. Huge, eyeless, a ribcage
    of souls that light up when it hears you, sculk tendrils on its head that twitch."""
    m = Model("the_listener", "biped", 2.7)
    biped(m, hip=15, legx=4.6, neck=34, shoulder=32, armx=11.5)
    m.bone("jaw", "head", (0, 37, 4))
    m.mbone("tendrilL", "head", (5, 44, 0))
    hide, hide2, sculk, soul = "warped_wart_block", "cyan_terracotta", "sculk", "soul_lantern"
    hide, hide2 = "dark_prismarine", "cyan_terracotta"
    for s, b in ((1, "legL"), (-1, "legR")):
        m.c(b, hide, (4.6 * s, 7.6, 0), (5.4, 15, 6))
        m.c(b, sculk, (4.6 * s, 2.4, 0.6), (5.8, 4.8, 6.8))
        for k in (-1.6, 0, 1.6): m.c(b, hide2, (4.6 * s + k, 0.6, 4.2), (1.2, 1.2, 1.6))
        m.c(b, "sculk_catalyst", (4.6 * s, 11, 3.05), (2.4, 2.4, 0.2), light=True)
    # the chest: a massive slab of hide with an open ribcage full of trapped souls (weak spot)
    m.c("body", hide, (0, 25, -1), (20, 18, 10))
    m.c("body", "black_concrete", (0, 26, 4.1), (11, 10, 0.4))
    m.c("body", soul, (0, 26, 3.2), (7, 7, 2), light=True)
    m.c("body", "light_blue_stained_glass", (0, 26, 3.9), (9, 8, 0.4), light=True)
    for y in (22.4, 25, 27.6, 30.2):
        m.m("body", hide2, (3.6, y, 4.4), (5.2, 1.2, 0.8), (0, 0, -6))
    m.c("body", hide2, (0, 26, 4.4), (1.4, 10, 0.8))
    for x, y in ((-7.6, 20), (7, 31.6), (-6.4, 32.6), (8.4, 19)): m.c("body", sculk, (x, y, 4.1), (3, 2.4, 0.5))
    m.c("body", hide, (0, 34, -1.6), (17, 2.6, 8.6))
    # long heavy arms
    for s, a in ((1, "armL"), (-1, "armR")):
        blob(m, a, hide, (12 * s, 29, -0.6), (6.4, 9, 6.6), 1.4)
        m.c(a, hide, (12 * s, 20, 0), (5.6, 10, 5.6))
        m.c(a, sculk, (12 * s, 16.6, 0.4), (6, 2.4, 6))
        m.c(a, hide, (12 * s, 12.4, 0.8), (5.4, 5, 5.4))
        for k in (-1.6, 0, 1.6): m.c(a, hide2, (12 * s + k, 9.4, 2.4), (1.2, 2, 1.2))
    # the head: wide, eyeless, a huge jaw full of teeth, the tendrils
    m.c("head", hide, (0, 41, 0.4), (14, 10, 10))
    m.c("head", hide2, (0, 44.4, 5.45), (10, 1.6, 0.2))
    m.c("head", "black_concrete", (0, 39.2, 5.45), (10, 3, 0.2))
    for x in (-4, -2, 0, 2, 4): m.c("head", "white_concrete", (x, 39.8, 5.5), (0.8, 1.6, 0.2))
    m.c("jaw", hide, (0, 36.6, 2), (12, 2.6, 7.6))
    for x in (-3.4, -1.2, 1.2, 3.4): m.c("jaw", "white_concrete", (x, 38.4, 5.4), (0.8, 1.4, 0.4))
    m.m("head", soul, (3.6, 42, 5.5), (1.4, 1.4, 0.2), light=True)
    for s, t in ((1, "tendrilL"), (-1, "tendrilR")):
        for k in range(3):
            m.c(t, "sculk_sensor" if False else "cyan_concrete", (5 * s + s * k * 1.6, 46 + k * 2.6, -k * 0.6), (1.6, 3, 1.6), (0, 0, -25 * s - k * 8 * s), light=True)
        m.c(t, "light_blue_concrete", (5 * s + s * 5, 54, -2), (1.8, 1.8, 1.8), (45, 45, 0), light=True)
    m.attacks = {"sonic_boom": "roar", "darkness": "cast", "slam": "slam", "shockwave": "stomp", "quake": "slam", "pull": "sweep", "charge": "lunge", "minions": "roar"}
    m.melee = "swipe"
    return m
