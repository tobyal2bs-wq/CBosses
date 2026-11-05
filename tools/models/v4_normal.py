"""v4 normal bosses: real Minecraft mobs, grown huge and given a story, in the clean chunky style of the
Grand Augur. Each keeps the shape and colours you know the mob by and adds only what tells its story."""
import copy
import math
import anims
from models import model, biped, horn, limb, quad, dirof
from build import Model
from kit import paint, band, stack, bevel, crack
from v3_kit import grow, vines

SPAWN, DEATH = {}, {}

OMINOUS = [
    ".......",
    ".GGGGG.",
    ".G.K.G.",
    ".GGGGG.",
    "..KKK..",
    "...C...",
    "..CCC..",
    ".K.K.K.",
    "K.K.K.K",
    ".......",
]


@model
def pillager_captain():
    """Captain Crossfire, the raid captain: a big grey pillager head with the dark unibrow and long nose,
    the ominous banner worn on his head like every raid captain, a dark shirt under a leather vest with a
    bandolier of fireworks, and a heavy crossbow loaded with a rocket, held at the hip."""
    m = Model("pillager_captain", "biped", 2.0)
    biped(m, hip=8, legx=2.4, neck=19.5, shoulder=18, armx=6.6)
    m.bone("banner", "head", (0, 33, 0.5))
    m.bone("bow", "armR", (-6.6, 9, 0.4))
    m.hold = {"bow": 0}
    m.bend = -40
    SK, SK2, BR, SH, VS, LT, WD = ("light_gray_concrete", "polished_andesite", "gray_concrete", "gray_terracotta",
                                   "brown_terracotta", "brown_concrete", "dark_oak_planks")
    # legs: dark trousers, leather boots
    for s, b in ((1, "legL"), (-1, "legR")):
        x = 2.4 * s
        m.c(b, VS, (x, 5.4, 0), (3, 5.2, 3))
        m.c(b, LT, (x, 1.4, 0.4), (3.4, 2.8, 4))
        m.c(b, BR, (x, 3.0, 0.4), (3.6, 0.6, 4.2))
    # body: the dark shirt, an open brown vest, a belt, a bandolier of red fireworks across the chest
    stack(m, "hips", VS, 0, 7.4, 0, [(8.6, 1.6, 6)])
    bevel(m, "body", SH, (0, 13.8, 0), (8.6, 9, 6), 0.6)
    for s in (1, -1):
        m.c("body", VS, (3.1 * s, 13.8, 3.05), (2.4, 9, 0.3))
        m.c("body", VS, (4.35 * s, 13.8, 0), (0.2, 8.4, 5.4))
    band(m, "body", LT, (0, 10.2, 0), (8.8, 1.2, 6.2), studs=1, stud_block="iron_block")
    for k in range(5):
        x, y = -3.2 + k * 1.6, 17 - k * 1.5
        m.c("body", LT, (x, y, 3.3), (1.8, 1.0, 0.3), (0, 0, 40))
        m.c("body", "red_concrete", (x, y + 0.4, 3.55), (0.7, 1.6, 0.4))
    m.c("body", LT, (0, 13, -3.3), (2.4, 9, 0.6), (0, 0, -30))
    # a quiver of bolts on the back
    m.c("body", LT, (2.4, 14.6, -3.9), (2.6, 7, 2.2), (0, 0, -18))
    for dx in (-0.5, 0.5):
        m.c("body", "white_concrete", (3.6 + dx, 19, -3.9), (0.4, 2.4, 0.4), (0, 0, -18))
    # arms: dark sleeves, leather bracers, grey hands
    for s, a in ((1, "armL"), (-1, "armR")):
        x = 6.6 * s
        bevel(m, a, SH, (x, 15.4, 0), (3.4, 5.4, 3.6), 0.5)
        m.c(a, SH, (x, 11.2, 0.3), (3.2, 4.4, 3.4))
        m.c(a, LT, (x, 10, 0.3), (3.6, 1.6, 3.8))
        m.c(a, SK, (x, 8, 0.4), (2.6, 2.4, 2.6))
    # the crossbow: stock along the arm, a curved bow across the front, the string, a loaded rocket
    m.c("bow", WD, (-6.6, 9, 3.6), (1.4, 1.4, 10))
    m.c("bow", "iron_block", (-6.6, 9, 7.4), (1.8, 1.8, 1.2))
    for s in (1, -1):
        m.c("bow", WD, (-6.6 + 3 * s, 9, 8.2), (4.4, 1.0, 1.0), (0, 22 * s, 0))
        m.c("bow", WD, (-6.6 + 5.6 * s, 9, 6.8), (1.4, 1.0, 1.0), (0, 50 * s, 0))
    m.c("bow", "white_wool", (-6.6, 9, 6.0), (11, 0.25, 0.25))
    m.c("bow", "red_concrete", (-6.6, 9.9, 7.4), (0.9, 0.9, 4))
    m.c("bow", "white_concrete", (-6.6, 9.9, 9.6), (0.9, 0.9, 0.6))
    # head: the pillager face, big and grey: dark unibrow, small eyes, a long nose, a sour mouth
    bevel(m, "head", SK, (0, 26.4, 0.5), (13, 12.6, 12.4), 1.2)
    m.c("head", SK2, (0, 20.6, 0.5), (11, 1.4, 10.4))
    m.c("head", BR, (0, 28.8, 6.85), (11.4, 1.8, 0.4))
    for s in (1, -1):
        m.c("head", "white_concrete", (3.2 * s, 26.8, 6.8), (2.4, 1.6, 0.2))
        m.c("head", "black_concrete", (2.6 * s, 26.8, 6.95), (1.0, 1.6, 0.2))
        m.c("head", SK2, (5 * s, 24, 6.8), (2.2, 1.2, 0.2))
    m.c("head", "light_gray_terracotta", (0, 24, 8.2), (3, 7, 3))
    m.c("head", "light_gray_terracotta", (0, 20.8, 8.5), (2.4, 1, 2.4))
    m.c("head", BR, (0, 22.2, 6.8), (5, 0.6, 0.2))
    # the ominous banner worn on the head: a crossbar, a white cloth with the illager pattern both sides
    m.c("banner", "dark_oak_log", (0, 33.4, 0.5), (1, 1.2, 1))
    m.c("banner", "dark_oak_log", (0, 46.4, 0.5), (11, 1, 1))
    m.c("banner", "white_wool", (0, 39.6, 0.5), (10, 12.6, 0.6))
    for face, z in (("front", 0.8), ("back", 0.2)):
        paint(m, "banner", face, (0, 39.8, z), OMINOUS, {"G": "light_gray_concrete", "K": "black_concrete", "C": "cyan_concrete"}, px=1.3, depth=0.15)
    m.attacks = {"volley": "cast", "rocket": "roar", "kick": "stomp", "charge": "lunge"}
    m.melee = "swipe"
    return m


@model
def pale_watcher():
    """The Pale Watcher, a creaking that grew for a thousand years in the pale garden: a tall, thin body of
    grey pale oak bark, long arms ending in twig fingers, a narrow head with two burning orange eyes, its
    creaking heart beating orange in an open chest, resin oozing at the joints, pale moss hanging off it
    and branches growing out of its shoulders and head."""
    m = Model("pale_watcher", "biped", 2.2)
    biped(m, hip=20, legx=2.6, neck=38, shoulder=37, armx=6.4)
    m.bone("heart", "body", (0, 30, 1))
    m.bend = -14
    BK, BK2, MS, RS, EY, HT = "pale_oak_log", "gray_terracotta", "pale_moss_block", "resin_block", "orange_concrete", "creaking_heart"
    # legs: long thin bark pillars, knotted knees, root feet splayed on the ground
    for s, b in ((1, "legL"), (-1, "legR")):
        x = 2.6 * s
        m.c(b, BK, (x, 14.6, 0), (3.4, 11, 3.4))
        m.c(b, BK2, (x, 9.2, 0.2), (4, 2, 4))
        m.c(b, BK, (x, 4.6, 0.2), (3, 8, 3))
        for dz, ry in ((2.2, 0), (-1.6, 180), (0.4, 90 * s)):
            m.c(b, BK2, (x + (1.8 * s if ry == 90 * s else 0), 0.6, dz), (1.4, 1.2, 3), (0, ry, 0))
        m.c(b, RS, (x + 1.4 * s, 9.6, 1.6), (1, 1.4, 1), light=True)
    # body: a narrow torso, the bark split open on the chest round the heart
    m.c("hips", BK2, (0, 21, 0), (7, 2.4, 4))
    m.c("body", BK, (0, 25.6, 0), (6, 7, 4))
    bevel(m, "body", BK, (0, 33, 0), (9, 8, 5), 0.6)
    m.c("body", "black_concrete", (0, 30.4, 2.3), (4, 5, 0.6))
    for s in (1, -1):
        m.c("body", BK2, (2.6 * s, 30.4, 2.6), (1, 6.4, 0.8), (0, 0, 6 * s))
    m.c("heart", HT, (0, 30.4, 1.6), (3, 3.6, 2.4), light=True)
    m.c("heart", EY, (0, 30.4, 2.85), (1, 1.6, 0.2), light=True)
    m.c("body", RS, (-3.6, 27, 2.1), (1.4, 2.2, 1), light=True)
    m.c("body", RS, (3.2, 35.4, 2.4), (1.6, 1.2, 0.8), light=True)
    # pale moss hanging from the shoulders, front and back
    for (x, z, L) in ((-3.4, 2.6, 5), (3.8, 2.6, 3.2), (-1.6, -2.6, 6), (2.4, -2.6, 4.4)):
        m.c("body", MS, (x, 36.6 - L / 2, z), (1.6, L, 0.4))
    # arms: long and thin, a knotted elbow, twig fingers spread
    for s, a in ((1, "armL"), (-1, "armR")):
        x = 6.4 * s
        m.c(a, BK, (x, 32, 0), (2.8, 10, 2.8))
        m.c(a, BK2, (x, 26.6, 0), (3.4, 1.8, 3.4))
        m.c(a, BK, (x, 20.6, 0.2), (2.4, 10, 2.4))
        for k, (dx, dz) in enumerate(((-0.8, 0.8), (0.4, 1.0), (1.0, -0.4))):
            m.c(a, BK2, (x + dx * s, 13.8, dz), (0.7, 4.4, 0.7), (dz * 10, 0, -dx * 12 * s))
        m.c(a, MS, (x + 1.5 * s, 21, 0), (0.4, 6, 1.6))
    # branches out of the shoulders: crooked, tipped with pale moss
    for s in (1, -1):
        tip = limb(m, "body", BK, (4 * s, 37, -0.6), [(4, 1.4, (-10, 0, -40 * s)), (3.6, 1.0, (-20, 0, -10 * s)), (2.6, 0.8, (-30, 0, -50 * s))])
        m.c("body", MS, tip, (2.4, 1.6, 2.4))
    # head: tall and narrow, twigs crowning it, two burning orange eye slits and a dark mouth crack
    bevel(m, "head", BK, (0, 44, 0), (7, 12, 6), 0.6)
    for s in (1, -1):
        m.c("head", EY, (1.7 * s, 45.6, 3.05), (1.2, 2.6, 0.2), light=True)
        m.c("head", "yellow_concrete", (1.7 * s, 46.2, 3.15), (0.5, 0.8, 0.1), light=True)
    m.c("head", "black_concrete", (0, 40.6, 3.05), (3.4, 0.8, 0.2))
    m.c("head", "black_concrete", (0.6, 41.3, 3.05), (0.8, 0.8, 0.2))
    for (x, rz, L) in ((-2.6, 30, 6), (-0.6, 8, 8), (1.6, -18, 5), (2.8, -40, 6.4)):
        tip = limb(m, "head", BK2, (x, 50, 0), [(L * 0.6, 1.0, (0, 0, rz)), (L * 0.4, 0.7, (-20, 0, rz * 1.6))])
    m.c("head", MS, (0, 50.4, -1.6), (6, 1.0, 3))
    m.c("head", MS, (-2.4, 47, -3.1), (1.6, 6, 0.4))
    m.attacks = {"roots": "slam", "freeze": "roar", "grab": "lunge", "swarm": "cast"}
    m.melee = "swipe"
    return m


@model
def weeping_ghast():
    """The Weeping Matron, the oldest ghast of the Nether: the vanilla ghast as a giant white cube, its eyes
    shut with grey tears running down, nine tentacles hanging under it that sway on their own, old
    scorch marks and cracks on its skin, and tears of soul fire that glow and fall when it cries."""
    m = Model("weeping_ghast", "float", 3.0)
    m.bone("core", "root", (0, 22, 0))
    m.bone("head", "core", (0, 22, 0))
    WH, WH2, GR, DK, SL = "white_concrete", "smooth_stone", "light_gray_concrete", "gray_concrete", "light_blue_concrete"
    # the body: the white cube, softened at the edges, a few grey scorch marks and a crack
    bevel(m, "head", WH, (0, 22, 0), (16, 16, 16), 0.8)
    paint(m, "head", "front", (0, 22, 8), [
        "................",
        "................",
        "................",
        "..GGGG....GGGG..",
        "..DDDD....DDDD..",
        "...T........T...",
        "...T........T...",
        "...S........S...",
        "...T........T...",
        "...S...DDDD.S...",
        ".......DDDD.....",
        "...S........S...",
        "................",
        "................",
        "................",
        "................",
    ], {"G": GR, "D": DK, "T": GR, "S": (SL, 0.3, True)}, px=1, depth=0.3)
    for side in ("left", "right"):
        paint(m, "head", side, ((8 if side == "left" else -8), 22, 0), [
            "................", ".....G..........", "....GG......G...", "...........GG...", "................",
            "..G.............", "..GG............", "........G.......", ".......GG.......", "................",
        ], {"G": GR}, px=1.6, depth=0.25)
    paint(m, "head", "top", (0, 30, 0), ["......", ".G..G.", "..GG..", "......"], {"G": GR}, px=2.6, depth=0.25)
    # tentacles: nine, in a three by three grid, each its own bone so each one sways on its own
    lens = [9, 13, 10, 12, 8, 14, 11, 9, 12]
    for i in range(9):
        x, z = (i % 3 - 1) * 5, (i // 3 - 1) * 5
        b = "tent%d" % i
        m.bone(b, "head", (x, 14, z))
        L = lens[i]
        m.c(b, WH, (x, 14 - L * 0.32, z), (2.2, L * 0.64, 2.2))
        m.c(b, WH2, (x, 14 - L * 0.82, z), (1.8, L * 0.36, 1.8))
    idle = copy.deepcopy(anims.RIGS["float"]["idle"])
    for i in range(9):
        a, b = 10 + (i % 3) * 4, -8 - (i % 2) * 5
        sg = 1 if i % 2 == 0 else -1
        idle["bones"]["tent%d" % i] = {"rot": anims.K((0, (a * sg, 0, b * sg)), (1.5, (-a * sg, 0, -b * sg)), (3.0, (a * sg, 0, b * sg)))}
    m.anims = {"idle": idle}
    m.no_elbows = True
    m.attacks = {"fireball": "pulse", "wail": "raise", "tears": "spin", "dive": "dive"}
    m.melee = "pulse"
    return m


@model
def elder_sniffer():
    """The Elder Sniffer, the last of the ancient sniffers: the vanilla sniffer's rust-red fur and green
    moss back, its big flat nose and six short legs, so old that a whole garden grows on its back:
    torchflowers, a pitcher plant, mossy stones and a sapling."""
    m = Model("elder_sniffer", "quad", 2.2)
    quad(m, body_y=13, legx=8, legz_front=10, legz_back=-10, neck_y=16, neck_z=16)
    FR, FR2, MS, MS2, NS, DK = "red_terracotta", "terracotta", "moss_block", "green_concrete", "lime_terracotta", "black_concrete"
    # six short legs: the four of the rig and a middle pair on the body
    for s, (b, z) in ((1, ("legFL", 10)), (-1, ("legFR", 10)), (1, ("legBL", -10)), (-1, ("legBR", -10))):
        x = 8 * s
        bevel(m, b, FR, (x, 6, z), (5, 8, 5), 0.6)
        m.c(b, FR2, (x, 1.2, z + 0.4), (5.4, 2.4, 6))
    for s in (1, -1):
        bevel(m, "body", FR, (8 * s, 6, 0), (5, 8, 5), 0.6)
        m.c("body", FR2, (8 * s, 1.2, 0.4), (5.4, 2.4, 6))
    # body: long and low, rust-red fur, a deep green moss blanket over the back
    bevel(m, "body", FR, (0, 15, 0), (20, 12, 30), 1.6)
    m.c("body", MS, (0, 21.4, 0), (20.4, 1.6, 30.4))
    for s in (1, -1):
        m.c("body", MS, (10.3 * s, 18.4, 0), (0.6, 5, 30.2))
        for k in range(6):
            z = -12.6 + k * 5
            L = 2.2 + (k * 7 % 3) * 0.9
            m.c("body", MS2, (10.5 * s, 15.9 - L / 2 + 1, z), (0.4, L, 2.6))
    m.c("body", FR2, (0, 9.2, 0), (17, 0.6, 26))
    # the garden on its back: mossy stones, two torchflowers, a pitcher plant, a sapling
    m.c("body", "mossy_cobblestone", (-5, 23.4, -8), (5, 2.6, 4), (0, 20, 0))
    m.c("body", "mossy_cobblestone", (6, 23, 6), (3.4, 2, 3.4), (0, -15, 0))
    for (x, z) in ((4, -6), (-6, 7)):
        m.c("body", MS2, (x, 24.4, z), (0.5, 4, 0.5))
        for dx, dz in ((0.9, 0), (-0.9, 0), (0, 0.9), (0, -0.9)):
            m.c("body", "orange_concrete", (x + dx, 26.4, z + dz), (1, 1.4, 1))
        m.c("body", "yellow_concrete", (x, 26.6, z), (0.8, 1, 0.8), light=True)
    m.c("body", "lime_concrete", (0, 24.6, -2), (1.4, 5, 1.4))
    for dx in (-1.2, 1.2):
        m.c("body", "light_blue_concrete", (dx, 27.4, -2), (1, 2.6, 1.6), (0, 0, dx * 20))
    m.c("body", "oak_log", (-6, 25.6, 1), (1.4, 7, 1.4))
    m.c("body", "oak_leaves", (-6, 30, 1), (6, 4, 6))
    m.c("body", "oak_leaves", (-6, 32.6, 1), (3.6, 2, 3.6))
    # tail: a short mossy tuft
    m.c("tail", MS, (0, 17, -15.6), (4, 3, 2))
    # head: a big boxy head with a long flat nose, small dark eyes under a fringe of moss
    bevel(m, "head", FR, (0, 16.4, 19), (14, 11, 8), 1.0)
    m.c("head", MS, (0, 22.3, 18.6), (14.4, 1.4, 8.4))
    for s in (1, -1):
        m.c("head", MS2, (5 * s, 21, 23.1), (3, 1.4, 0.3))
        m.c("head", DK, (4 * s, 19.2, 23.1), (1.6, 1.6, 0.2))
        m.c("head", "white_concrete", (4.4 * s, 19.6, 23.2), (0.6, 0.6, 0.1))
    bevel(m, "jaw", NS, (0, 12.4, 25.4), (11, 4, 7), 0.6)
    m.c("jaw", "lime_terracotta", (0, 14.45, 26), (9, 0.2, 5))
    for s in (1, -1):
        m.c("jaw", DK, (2.4 * s, 14.6, 27.2), (1.6, 0.2, 1.0))
    m.attacks = {"sniff": "howl", "dig": "rear", "charge": "charge", "spores": "toss"}
    m.melee = "bite"
    return m
