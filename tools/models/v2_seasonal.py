"""Seasonal bosses, three per season: winter, summer, Easter and Halloween. Hand built with the kit,
each with its own joke and its own silhouette."""
import math
from models import model, biped, horn, mhorn, limb, mlimb, taper, quad
from build import Model
from kit import paint, crack, band, hem, tufts, spikes, plate, stack, mirror_rows, bevel

SPAWN, DEATH = {}, {}


def ring(m, bone, block, y, rad, n, size, x0=0, z0=0, light=False, tilt=0, phase=0):
    for k in range(n):
        a = math.radians(phase + k * 360 / n)
        m.c(bone, block, (x0 + rad * math.sin(a), y, z0 + rad * math.cos(a)), size, (tilt, math.degrees(a), 0), light=light)


def present(m, bone, box, ribbon, center, size, rot=(0, 0, 0)):
    """A wrapped present: box, two ribbons crossing over it and a bow on top."""
    x, y, z = center
    w, h, d = size
    m.c(bone, box, center, size, rot, center)
    m.c(bone, ribbon, center, (w + 0.2, h + 0.2, d * 0.22), rot, center)
    m.c(bone, ribbon, center, (w * 0.22, h + 0.2, d + 0.2), rot, center)
    m.c(bone, ribbon, (x, y + h / 2 + 0.5, z), (w * 0.5, 0.9, 0.9), (rot[0], rot[1] + 45, rot[2]), center)


# ================================================================================================== WINTER

@model
def killer_claus():
    """Santa gone bad: a red coat with matted white fur, a beard stained grey at the tips, a crooked hat,
    glowing red eyes and a grin full of teeth. He drags a sack of stolen presents on his back, swings a
    giant candy-cane hook and keeps a burning lump of coal for the naughty."""
    m = Model("killer_claus", "biped", 1.8)
    biped(m, hip=14, legx=4, neck=34, shoulder=31.5, armx=10)
    m.bone("jaw", "head", (0, 34.6, 3))
    m.bone("sack", "body", (0, 30, -5))
    m.bone("cane", "armR", (-10, 12, 2))
    m.bone("coal", "armL", (10, 12, 2))
    m.hold = {"cane": 14}
    m.bend = -40
    RD, RD2, FU, FU2, BK, GD, SK = "red_concrete", "red_terracotta", "white_wool", "light_gray_wool", "black_concrete", "gold_block", "white_terracotta"
    # legs: red trousers tucked into black boots with fur cuffs and buckles
    for s, b in ((1, "legL"), (-1, "legR")):
        x = 4 * s
        bevel(m, b, RD, (x, 10.4, 0), (5, 7.6, 5), 0.6)
        bevel(m, b, BK, (x, 3.4, 0.6), (5.6, 6.8, 6.2), 0.6)
        m.c(b, BK, (x, 0.8, 3.6), (5, 1.6, 2))
        m.c(b, FU, (x, 7, 0.4), (6.2, 1.8, 6.6))
        m.c(b, GD, (x, 3.6, 3.75), (1.6, 1.4, 0.3))
        m.c(b, BK, (x, 3.6, 3.95), (0.8, 0.6, 0.2))
    # the coat skirt: it flares over the hips, fur hem stained grey in places
    stack(m, "hips", RD, 0, 9, 0, [(14, 3, 10), (13, 3, 9.4)])
    m.c("hips", FU, (0, 8.6, 0), (14.6, 1.8, 10.6))
    for k, x in enumerate((-5.4, -1.8, 1.8, 5.4)):
        m.c("hips", FU2, (x, 8.4, 5.4), (1.6, 1.4, 0.3))
    m.c("hips", FU, (0, 12, 5.05), (2.6, 6, 0.4))
    # body: a round belly in the red coat, a black belt with a gold buckle, a fur placket
    bevel(m, "body", RD, (0, 22.4, 0.4), (13, 13, 9), 1.2)
    bevel(m, "body", RD, (0, 20.4, 3.6), (10, 8, 4), 1.2)
    m.c("body", RD2, (0, 26, 4.75), (9, 0.6, 0.3))
    band(m, "body", BK, (0, 17.6, 1), (13.4, 2.2, 10.4))
    paint(m, "body", "front", (0, 17.6, 6.2), ["GGGGG", "G.K.G", "GGGGG"], {"G": GD, "K": BK}, px=0.8, depth=0.3)
    m.c("body", FU, (0, 24.8, 4.9), (2.6, 12, 0.6))
    for y in (21.2, 24.2, 27.2):
        m.c("body", BK, (0, y, 5.3), (0.8, 0.8, 0.3))
    # fur collar and a mantle over the shoulders
    bevel(m, "body", FU, (0, 30.4, 0), (14.4, 2.6, 9.6), 0.8)
    tufts(m, "body", FU, [(-6, 31.6, 3.6), (-2, 31.8, 4.6), (2, 31.8, 4.6), (6, 31.6, 3.6), (-6, 31.6, -3.6), (6, 31.6, -3.6)], 1.8, alt=FU2)
    # arms: red sleeves, fur cuffs, black gloves
    for s, a in ((1, "armL"), (-1, "armR")):
        x = 10 * s
        bevel(m, a, RD, (x, 27.6, 0), (5.4, 7, 5.6), 0.7)
        bevel(m, a, RD, (x, 20.4, 0.6), (5, 7.4, 5.2), 0.6)
        m.c(a, RD2, (x + 2.6 * s, 24, 0.3), (0.3, 1, 5))
        m.c(a, FU, (x, 16.2, 0.8), (6, 2.2, 6.2))
        bevel(m, a, BK, (x, 13, 1.4), (4.2, 4.4, 4.2), 0.6)
        m.c(a, BK, (x - 1.6 * s, 13.4, 3.4), (1.4, 2.6, 1.4))
    # head: pale skin, red glowing eyes under thick angry brows, a red nose, rosy cheeks
    bevel(m, "head", SK, (0, 38.4, 0.4), (8.2, 7.6, 8), 1.0)
    paint(m, "head", "front", (0, 39.8, 4.45), [
        "WWW...WWW",
        ".WWW.WWW.",
        "..R...R..",
        "...PPP...",
        ".C.PPP.C.",
    ], {"W": "white_concrete", "R": ("redstone_block", 0.4, True), "P": "pink_concrete", "C": "pink_terracotta"}, px=0.9, depth=0.3)
    # moustache that curls up at the ends, then a big beard that hides the jaw
    paint(m, "head", "front", (0, 35.8, 4.9), ["WW.....WW", ".WWW.WWW.", "..WWWWW.."], {"W": "white_concrete"}, px=1.0, depth=0.6)
    bevel(m, "jaw", FU, (0, 32.6, 3.2), (9.4, 6.6, 3.2), 0.9)
    bevel(m, "jaw", FU, (0, 28.8, 3.8), (7, 4.4, 2.6), 0.8)
    m.c("jaw", FU2, (0, 26, 4), (4, 2.4, 2))
    m.c("jaw", FU2, (0, 24.6, 4.2), (2, 1.6, 1.4))
    tufts(m, "jaw", FU, [(-4.6, 30.6, 3.6), (4.6, 30.6, 3.6), (-3, 27.4, 4), (3, 27.4, 4)], 1.8, alt=FU2)
    # a gap in the beard showing a grin of sharp teeth
    m.c("jaw", BK, (0, 33.4, 4.85), (5.4, 1.6, 0.2))
    paint(m, "jaw", "front", (0, 33.6, 5.0), ["W.W.W.W", ".W.W.W."], {"W": "white_concrete"}, px=0.75, depth=0.2)
    # the hat: a fur band, then a red cone that bends back and droops, with a grey bobble
    bevel(m, "head", FU, (0, 42.6, 0.2), (9.6, 2.4, 9.4), 0.7)
    m.c("head", RD, (0, 45, -0.2), (8, 2.6, 8))
    m.c("head", RD, (0.4, 47.2, -1.2), (6.2, 2.6, 6.2), (-14, 0, 6), (0.4, 46, -1.2))
    m.c("head", RD, (1, 48.6, -3.4), (4.6, 2.4, 4.6), (-42, 0, 10), (1, 48, -3.4))
    m.c("head", RD2, (1.4, 48.4, -5.8), (3.4, 2.6, 3.4), (-80, 0, 14), (1.4, 48.4, -5.8))
    m.c("head", FU2, (1.6, 46.8, -7.6), (2.8, 2.8, 2.8), (20, 20, 0))
    m.c("head", RD2, (-2.6, 44.6, 3.9), (1.4, 1.2, 0.4))
    # the sack: lumpy, patched, tied with rope, stolen presents spilling out of the top
    bevel(m, "sack", "brown_wool", (0, 24.6, -10.4), (13, 14, 9), 1.6)
    bevel(m, "sack", "brown_wool", (0, 31.6, -10), (9, 3, 7), 0.8)
    m.c("sack", "brown_terracotta", (0, 33.4, -9.6), (6, 1.4, 5))
    paint(m, "sack", "back", (3, 22, -14.95), ["PPP", "P.P", "PPP"], {"P": "green_terracotta"}, px=1.2, depth=0.2)
    m.c("sack", "brown_terracotta", (-4.6, 26, -14.95), (0.3, 4, 0.3), (0, 0, 30))
    m.c("sack", "brown_terracotta", (0, 31, -5.6), (1, 1, 10), (-30, 0, 0))
    m.c("sack", "brown_terracotta", (0, 28, -1.4), (13.6, 1, 1))
    present(m, "sack", "green_concrete", "red_concrete", (-2.6, 36.4, -9.4), (4, 4, 4), (0, 20, 10))
    present(m, "sack", "blue_concrete", GD, (2.6, 35.8, -10.8), (3.6, 3, 3.6), (10, -15, -12))
    m.c("sack", RD, (0.6, 38.6, -11.8), (0.8, 6, 0.8), (20, 0, -20))
    m.c("sack", FU, (1.4, 37, -11.6), (0.9, 0.9, 0.9), (20, 0, -20))
    m.c("sack", "yellow_concrete", (-3.6, 34.6, -12.6), (1.4, 3.4, 1.4), (-20, 0, 30))
    m.c("sack", BK, (-4.2, 36.4, -13.2), (1.6, 1, 1.6), (-20, 0, 30))
    # the candy-cane hook: red and white stripes, a curled hook, a cruel point on the end
    for k in range(10):
        m.c("cane", RD if k % 2 else "white_concrete", (-10, 8 + k * 2.4, 2), (1.8, 2.4, 1.8), (0, 0, 0))
    hk = [(-10, 33.2, 2.6, -20), (-10, 35, 4.4, -60), (-10, 35, 6.8, -110), (-10, 33.2, 8.4, -150), (-10, 30.8, 8.8, -180)]
    for k, (x, y, z, r) in enumerate(hk):
        m.c("cane", "white_concrete" if k % 2 else RD, (x, y, z), (1.8, 2.8, 1.8), (r, 0, 0), (x, y, z))
    m.c("cane", "iron_block", (-10, 28.6, 8.8), (0.9, 2.4, 0.9))
    m.c("cane", BK, (-10, 9, 2), (2.2, 3.4, 2.2))
    # a lump of coal burning in his other fist
    m.c("coal", "coal_block", (10, 9.4, 3.2), (3.4, 3, 3.4), (20, 30, 10), (10, 9.4, 3.2))
    for (u, v) in ((0, 0), (0.8, 1)):
        m.c("coal", "orange_concrete", (10 + u, 9.4 + v * 0.6, 4.95), (1.6, 0.4, 0.3), (0, 0, 30 - v * 60), light=True)
    m.c("coal", "magma_block", (10, 11.2, 3.2), (1.6, 1, 1.6), light=True)
    m.attacks = {"coal": "cast", "hook": "sweep", "minions": "roar", "quake": "stomp"}
    m.melee = "swipe"
    return m


@model
def frostbottom():
    """A snow golem grown huge and grumpy: three packed snowballs, a cracked ice face with coal eyes that
    glow cold blue, a carrot nose, stick arms with twig fingers, a striped scarf, a dented bucket for a hat
    and icicles hanging off every ledge. It slides around on a patch of ice instead of walking."""
    m = Model("frostbottom", "float", 1.9)
    m.bone("core", "root", (0, 12, 0))
    m.bone("head", "core", (0, 30, 0))
    m.mbone("armL", "core", (9, 25, 0))
    m.bone("ring1", "core", (0, 2, 0))
    m.bone("ring2", "head", (0, 40, 0))
    m.no_elbows = True
    SN, SN2, IC, IC2, CO, ST = "snow_block", "white_concrete", "packed_ice", "blue_ice", "coal_block", "spruce_log"
    # the bottom ball (rounded with three crossed boxes and a sagging rim), the ice patch it slides on
    bevel(m, "core", SN, (0, 7, 0), (16, 14, 16), 3)
    m.c("core", SN, (0, 1.2, 0), (13, 2.4, 13))
    for (x, z) in ((5, 6), (-6, 4), (6, -5), (-4, -6)):
        m.c("core", SN2, (x, 10.4, z), (3, 1.4, 3), (0, 30, 0))
    m.c("ring1", IC, (0, 0.3, 0), (24, 0.6, 24))
    m.c("ring1", IC2, (0, 0.4, 0), (16, 0.6, 16), (0, 45, 0))
    for k in range(6):
        a = math.radians(k * 60 + 15)
        m.c("ring1", IC, (math.sin(a) * 12.4, 1.2, math.cos(a) * 12.4), (2.2, 2.4, 2.2), (0, k * 60, 20))
    # middle ball with coal buttons, bottom ball sits slightly forward
    bevel(m, "core", SN, (0, 19, 0.4), (13, 11, 12), 2.4)
    for y in (16.6, 19.6, 22.6):
        m.c("core", CO, (0, y, 6.6), (1.8, 1.8, 0.6))
    # ice crust on the shoulders, icicles hanging all the way round
    m.c("core", IC, (0, 24.4, 0.4), (13.6, 0.8, 12.4))
    for k, (x, z, h) in enumerate(((-6, 6.2, 3), (-3, 6.4, 2), (3.4, 6.4, 3.4), (6.4, 5.8, 2.2), (-6.6, -4, 3), (6.6, -3, 2.4), (0, -6.2, 3.6), (-4, -6.2, 2))):
        m.c("core", IC2 if k % 3 == 0 else IC, (x, 13.6 - h / 2 + 10, z), (1.2, h, 1.2))
    for k, (x, z, h) in enumerate(((-7, 7, 2.6), (2, 8.1, 3.4), (7.6, 5, 2), (-8, -5, 3), (5, -8, 2.4))):
        m.c("core", IC, (x, 13.4 - h / 2, z), (1.4, h, 1.4))
    # the scarf: red and green stripes wound round the neck, one end blowing out behind
    for k in range(6):
        a = math.radians(k * 60)
        m.c("core", "red_wool" if k % 2 else "green_wool", (math.sin(a) * 5.4, 26.2, math.cos(a) * 5.4 + 0.4), (5.8, 2.6, 1.6), (0, k * 60, 0))
    for k in range(4):
        m.c("core", "green_wool" if k % 2 else "red_wool", (3 + k * 0.6, 24.4 - k * 2.2, -6.4 - k * 0.9), (2.6, 2.4, 0.6), (-20, 0, -10))
    hem(m, "core", "white_wool", 3.4, 6.6, 15.8, -10, 0.6, 3, long=1.6, short=0.8)
    # the head: smaller ball, a cracked ice face, coal eyes lit blue, a carrot nose, a frown of coal
    bevel(m, "head", SN, (0, 34, 0.4), (10.6, 9.4, 10), 2)
    paint(m, "head", "front", (0, 35, 5.45), [
        "KK...KK",
        "KBK.KBK",
        ".KK.KK.",
        ".......",
        ".K...K.",
        "..KKK..",
    ], {"K": CO, "B": ("light_blue_concrete", 0.4, True)}, px=1.0, depth=0.35)
    crack(m, "head", "front", (0, 34, 5.45), [(-4.6, 4), (-3.4, 4), (-3.4, 2.4)], block=IC2, width=0.5)
    crack(m, "head", "left", (5.35, 34, 0.4), [(-3, 3), (-1, 3), (-1, -1), (1.6, -1)], block=IC2, width=0.5)
    m.c("head", "orange_concrete", (0, 34.6, 7.6), (1.6, 1.6, 4.4))
    m.c("head", "orange_concrete", (0, 34.4, 10.4), (1, 1, 2.2))
    m.c("head", "orange_terracotta", (0, 35.2, 6.2), (1.8, 0.4, 1.4))
    # a dented bucket hat, tipped back, with icicles on its rim and a sprig of holly
    m.c("head", "iron_block", (0, 40, -0.4), (8.6, 1, 8.6), (-10, 0, 6))
    m.c("head", "iron_block", (0, 42.6, -0.8), (7.4, 4.6, 7.4), (-10, 0, 6))
    m.c("head", "gray_concrete", (0, 41.4, 2.95), (7.6, 0.6, 0.3), (-10, 0, 6))
    m.c("head", "gray_concrete", (2.4, 43.6, 2.7), (1.6, 1.6, 0.3), (-10, 0, 6))
    m.c("head", "green_concrete", (-3, 44.4, 2.4), (2.2, 1, 0.4), (0, 0, 30))
    m.c("head", "green_concrete", (-1.8, 44.8, 2.4), (2.2, 1, 0.4), (0, 0, -30))
    m.c("head", "red_concrete", (-2.4, 44.2, 2.75), (0.8, 0.8, 0.4))
    for x in (-3.6, 0, 3.4):
        m.c("head", IC, (x, 38.8, 4.2), (0.8, 1.8, 0.8))
    # floating snowflakes circling the head
    for k in range(6):
        a = math.radians(k * 60)
        x, z = math.sin(a) * 10, math.cos(a) * 10
        m.c("ring2", "white_concrete", (x, 40 + (k % 2) * 3, z), (1.6, 0.4, 0.4), (0, k * 60, 45))
        m.c("ring2", "white_concrete", (x, 40 + (k % 2) * 3, z), (0.4, 1.6, 0.4), (0, k * 60, 45))
    # stick arms: a branch with a fork, three twig fingers, a snowball in each hand
    for s, a in ((1, "armL"), (-1, "armR")):
        tip = limb(m, a, ST, (6 * s, 25, 0), [(7, 1.4, (10, 0, -70 * s)), (6, 1.2, (-20, 0, -110 * s)), (3, 1, (-30, 0, -150 * s))])
        limb(m, a, ST, (11.4 * s, 27, 0), [(3.4, 0.8, (0, 0, -30 * s))])
        x, y, z = tip
        for k, r in enumerate((-30, 0, 30)):
            m.c(a, ST, (x + 0.6 * s, y - 1.4, z + k * 0.8 - 0.8), (0.6, 2.6, 0.6), (r, 0, 0))
        bevel(m, a, SN, (x, y - 3.6, z + 1), (3.4, 3.4, 3.4), 0.8)
    # frost patches on the snow, snow piled up round the base, a corncob pipe in its frown
    for (y, z, w) in ((5, 8.05, 4), (18, 6.45, 3)):
        m.c("core", "light_blue_concrete", (-3.6, y, z), (w, 1, 0.2))
        m.c("core", "light_blue_concrete", (-4.6, y - 1, z), (w * 0.6, 1, 0.2))
    for (x, z, w) in ((7.6, 4, 5), (-7.4, -3, 6), (3, -7.6, 5), (-4, 7.6, 4), (7, -6, 3), (-7.6, 6, 3)):
        m.c("core", SN, (x, 1.4, z), (w, 2.8, w * 0.8), (0, x * 5, 0))
        m.c("core", SN2, (x, 3.2, z), (w * 0.6, 1, w * 0.5), (0, x * 5, 0))
    m.c("head", "yellow_terracotta", (2.4, 31.8, 6.4), (1.6, 2.2, 1.6))
    m.c("head", "brown_terracotta", (1.4, 31.4, 5.8), (2.4, 0.6, 0.6))
    m.c("head", "white_stained_glass", (2.4, 34, 6.4), (1, 1, 1), (45, 45, 0))
    m.c("head", "white_stained_glass", (2.9, 35.6, 6.4), (0.7, 0.7, 0.7), (45, 45, 0))
    # pebbles and rough lumps on the balls
    for (x, y, z) in ((7.8, 8, 2), (-7.8, 6, -1), (6.4, 20, 2), (-6.4, 18, -2), (0, 9, -8), (0, 20, -6.2), (5, 36, 3.6), (-5, 33, -2)):
        b = "head" if y > 30 else "core"
        m.c(b, SN2, (x, y, z), (1.8, 1.8, 1.8), (20, 30, 10))
    # a ridge of ice spikes growing up its back
    for k, (y, h) in enumerate(((10, 3), (15, 4), (20, 4.4), (24, 3.4))):
        m.c("core", IC2 if k % 2 else IC, (0, y, -7.6 + (k == 3) * 1.4), (1.6, h, 1.6), (-35, 0, 0))
    m.c("core", "light_blue_concrete", (0, 26.2, 7.4), (2, 2, 0.8), (0, 0, 45), light=True)
    for s_ in (1, -1):
        m.c("head", "pink_concrete", (3.8 * s_, 33.4, 5.5), (1.6, 0.8, 0.2))
    m.attacks = {"snowballs": "spin", "frost": "pulse", "slide": "dive", "minions": "raise"}
    m.melee = "swipe"
    return m


@model
def old_man_winter():
    """The spirit of winter as an old giant: an ice-blue robe embroidered with snowflakes, a mantle of
    white fur, a beard of icicles that reaches his belt, a crown of ice spikes and frozen breath. He leans
    on a frozen staff topped by a huge blue crystal and a lantern of cold light."""
    m = Model("old_man_winter", "biped", 1.95)
    biped(m, hip=14, legx=3.8, neck=35, shoulder=32.5, armx=9.6)
    m.bone("jaw", "head", (0, 35.6, 3))
    m.bone("cape", "body", (0, 33, -4))
    m.bone("staff", "armR", (-9.6, 12, 2))
    m.hold = {"staff": 0}
    m.bend = -46
    RB, RB2, TR, FU, IC, IC2, SK, SN = "light_blue_concrete", "blue_concrete", "white_concrete", "white_wool", "packed_ice", "blue_ice", "white_terracotta", "snow_block"
    # a long robe that hides the legs, widening to the ground with a fur hem and snowflake embroidery
    for s, b in ((1, "legL"), (-1, "legR")):
        bevel(m, b, RB2, (3.8 * s, 1.2, 1.6), (4.6, 2.4, 6), 0.5)
    stack(m, "hips", RB, 0, 1.4, 0, [(14, 3, 11), (13, 3, 10), (12, 3, 9.4), (11, 3, 8.8), (10.6, 2, 8.4)])
    m.c("hips", FU, (0, 1.6, 0), (14.6, 2, 11.6))
    m.c("hips", RB2, (0, 7.6, 5.05), (3, 12, 0.4))
    for y in (10, 6):
        paint(m, "hips", "front", (-4.4, y, 5.0 - (10 - y) * 0.05), [".T.", "TTT", ".T."], {"T": TR}, px=0.8, depth=0.2)
        paint(m, "hips", "front", (4.4, y, 5.0 - (10 - y) * 0.05), [".T.", "TTT", ".T."], {"T": TR}, px=0.8, depth=0.2)
    paint(m, "hips", "back", (0, 8, -5.05), ["T.T.T", ".TTT.", "TTTTT", ".TTT.", "T.T.T"], {"T": TR}, px=1.0, depth=0.2)
    # upper robe, a silver belt with an ice gem, and a heavy fur mantle
    bevel(m, "body", RB, (0, 23.6, 0), (11.4, 14, 7.6), 1.0)
    band(m, "body", "iron_block", (0, 17.6, 0), (11.8, 1.6, 8))
    m.c("body", IC2, (0, 17.6, 4.15), (2, 2, 0.6), (0, 0, 45), light=True)
    bevel(m, "body", FU, (0, 30.8, 0), (15, 3.6, 9.4), 1.0)
    tufts(m, "body", FU, [(-6.6, 29, 4), (-3.6, 28.6, 4.6), (3.6, 28.6, 4.6), (6.6, 29, 4), (-6.6, 29, -4), (0, 29, -4.6), (6.6, 29, -4)], 2, alt="light_gray_wool")
    # arms: wide sleeves with fur cuffs, old bony hands
    for s, a in ((1, "armL"), (-1, "armR")):
        x = 9.6 * s
        bevel(m, a, RB, (x, 27.4, 0), (4.6, 7, 5), 0.6)
        bevel(m, a, RB, (x, 19.8, 0.8), (5.6, 8, 5.8), 0.7)
        m.c(a, RB2, (x, 16.4, 0.8), (5.8, 1, 6))
        m.c(a, FU, (x, 15.4, 0.8), (6, 1.4, 6.2))
        m.c(a, SK, (x, 13, 1.4), (3, 3.4, 3))
        paint(m, a, "left" if s > 0 else "right", (x + 2.95 * s, 22, 0.8), [".T.", "TTT", ".T."], {"T": TR}, px=0.8, depth=0.2)
    m.c("armL", SK, (10.6, 11.2, 3.2), (0.8, 2, 0.8))
    # the face: deep-set pale eyes that glow, frosted brows, a long nose, wrinkles
    bevel(m, "head", SK, (0, 39.2, 0.6), (7.8, 8.4, 7.8), 1.0)
    paint(m, "head", "front", (0, 40.4, 4.55), [
        "WWW.WWW",
        "WWW.WWW",
        ".B...B.",
        "...N...",
        ".K.N.K.",
    ], {"W": TR, "B": ("light_blue_concrete", 0.4, True), "N": SK, "K": "brown_terracotta"}, px=0.9, depth=0.3)
    m.c("head", SK, (0, 38.4, 5.2), (1.4, 2.6, 1.6))
    # the beard: a moustache that sweeps out, then layered icicles down to the belt
    paint(m, "head", "front", (0, 37, 5.0), ["WWW...WWW", ".WWWWWWW."], {"W": TR}, px=1.0, depth=0.6)
    bevel(m, "jaw", FU, (0, 33.4, 3.6), (8.4, 5, 2.6), 0.8)
    for k, (x, y, h, w) in enumerate(((-3.2, 29.4, 6, 1.8), (-1.2, 27.4, 10, 2.2), (1.2, 28, 9, 2.0), (3.2, 30, 5, 1.6), (0, 25, 12, 1.6), (-2.2, 28, 5, 1.2), (2.2, 27, 6, 1.2))):
        m.c("jaw", IC if k % 2 else FU, (x, y, 3.8 + (k % 3) * 0.3), (w, h, w), (0, 0, x * 2))
    m.c("jaw", IC2, (0, 18.8, 4), (0.8, 2, 0.8))
    # long white hair falling down the back and sides of the head
    m.c("head", TR, (0, 38.6, -3.6), (8.6, 8, 1.6))
    m.c("head", FU, (0, 34.4, -3.8), (7.6, 3.4, 1.4))
    for s_ in (1, -1):
        m.c("head", TR, (4.15 * s_, 38.6, -0.6), (0.8, 7, 5))
        m.c("head", FU, (4.3 * s_, 34.6, -1.2), (1, 4, 3.6))
    m.c("head", TR, (0, 42.8, 0.6), (8, 0.8, 8))
    # a crown of ice spikes, tallest at the front, set in a silver band
    band(m, "head", "iron_block", (0, 43.6, 0.6), (8.6, 1.4, 8.6))
    for k in range(8):
        a = math.radians(k * 45)
        h = (6.4 if k == 0 else 4.6 if k in (1, 7) else 3.4)
        x, z = math.sin(a) * 4, math.cos(a) * 4 + 0.6
        m.c("head", IC if k % 2 else IC2, (x, 44.2 + h / 2, z), (1.4, h, 1.4), (math.cos(a) * 12, 0, -math.sin(a) * 12), (x, 44.2, z), light=k == 0)
    # cape: a long fur-trimmed blue cloak with a frost pattern, torn into icicles at the bottom
    m.c("cape", RB2, (0, 18.6, -4.8), (13, 28, 0.8))
    m.c("cape", FU, (0, 32.4, -5), (14, 1.6, 1.2))
    hem(m, "cape", RB2, -6.5, 6.5, 4.6, -4.8, 0.8, 7, long=3, short=1.2)
    hem(m, "cape", IC, -6, 6, 5.6, -5.4, 0.4, 4, long=3.4, short=1.6, seed=2)
    paint(m, "cape", "back", (0, 20, -5.3), [
        "...T...",
        "T..T..T",
        ".T.T.T.",
        "..TTT..",
        "TTTTTTT",
        "..TTT..",
        ".T.T.T.",
        "T..T..T",
        "...T...",
    ], {"T": TR}, px=1.1, depth=0.2)
    # the staff: frozen wood wrapped in ice, a great crystal and a cold lantern hanging under it
    for k in range(4):
        m.c("staff", "stripped_spruce_log", (-9.6, 5 + k * 7, 2), (1.4, 7, 1.4))
        m.c("staff", IC, (-9.6, 8 + k * 7, 2), (1.8, 1.2, 1.8), (0, 45, 0))
    bevel(m, "staff", IC2, (-9.6, 37.6, 2), (3.4, 6.4, 3.4), 0.7, light=True)
    m.c("staff", IC, (-9.6, 37.6, 2), (4.6, 2.2, 4.6), (0, 45, 0))
    for s in (1, -1):
        m.c("staff", IC, (-9.6 + 2.4 * s, 36, 2), (1.4, 4, 1.4), (0, 0, 24 * s))
    m.c("staff", "white_stained_glass", (-9.6, 42, 2), (1.2, 2.4, 1.2), light=True)
    m.c("staff", "chain", (-11.8, 31.4, 2), (0.6, 3, 0.6))
    m.c("staff", "soul_lantern", (-11.8, 28.6, 2), (2.2, 2.6, 2.2), light=True)
    m.attacks = {"blizzard": "cast", "frost": "roar", "spikes": "slam", "minions": "double"}
    m.melee = "swipe"
    return m


def blob(m, bone, block, center, size, r=1.5, rot=None, origin=None, light=False):
    bevel(m, bone, block, center, size, r, rot, origin, light)


# ================================================================================================== SUMMER

@model
def sunscorch():
    m = Model("sunscorch", "slime", 1.9)
    m.bone("body", "root", (0, 0, 0))
    m.bone("inner", "body", (0, 14, 0))
    m.bone("mouth", "body", (0, 10, 14))
    # a melting little sun, far too hot, on holiday: a glowing orange jelly with a yellow core
    sh, sh2 = "orange_stained_glass", "yellow_stained_glass"
    blob(m, "body", sh, (0, 13, 0), (28, 24, 28), 5)
    m.c("body", sh, (0, 1.2, 0), (32, 2.4, 32))
    blob(m, "inner", "yellow_concrete", (0, 14, 0), (14, 13, 14), 3, light=True)
    m.c("inner", "orange_concrete", (0, 14, 0), (8, 8, 14.4), light=True)
    # sun rays poking up round the top like a crown of flames
    for k in range(10):
        a = math.radians(k * 36 + 18)
        h = 6 if k % 2 else 4.4
        x, z = 11.4 * math.cos(a), 11.4 * math.sin(a)
        m.c("body", sh2, (x, 25 + h / 2, z), (2.6, h, 2.6), (math.degrees(math.sin(a)) * 0.4, -k * 36 - 18, -math.degrees(math.cos(a)) * 0.4), light=True)
    # melting: drips sliding down, a puddle spreading round its base
    for x, z, h in ((-9, 14.6, 6), (5, 14.6, 4), (14.6, 7, 5), (-14.6, -4, 7), (9, -14.6, 4)):
        m.c("body", sh2, (x, 3.4 + h / 2, z), (1.8, h, 1.8), light=True)
        m.c("body", sh2, (x, 3, z), (2.6, 1.6, 2.6), light=True)
    m.c("body", "orange_stained_glass", (0, 0.2, 0), (34, 0.4, 32))
    # sweat drops flying off its forehead
    for x, y in ((-12.6, 24), (13.4, 22), (-14.6, 20)):
        m.c("body", "light_blue_stained_glass", (x, y, 9), (1.4, 2.2, 1.4), (0, 0, 20 if x > 0 else -20))
    # face: huge sunglasses with a pink rim, sunscreen smeared on the nose, a melting grin, tongue out
    for s in (1, -1):
        m.c("body", "black_stained_glass", (5 * s, 17.6, 14.4), (7.4, 4.6, 0.6))
        m.c("body", "magenta_concrete", (5 * s, 20.2, 14.6), (8, 0.8, 0.8))
        m.c("body", "white_concrete", (6.6 * s, 18.6, 14.8), (1.4, 0.8, 0.2), (0, 0, 30))
        m.c("body", "magenta_concrete", (12.4 * s, 18.6, 9), (0.6, 0.6, 12))
        m.c("body", "pink_concrete", (9.6 * s, 13, 14.2), (3, 1.4, 0.4))
    m.c("body", "magenta_concrete", (0, 18.4, 14.6), (2.6, 0.8, 0.8))
    m.c("body", "white_concrete", (0, 15, 14.6), (3.4, 2.4, 1.2))
    m.c("body", "white_concrete", (0, 15.6, 15.4), (1.2, 1, 0.6))
    m.c("mouth", "black_concrete", (0, 9.6, 14.3), (12, 3, 0.4))
    for x in (-4.6, -1.6, 1.6, 4.6):
        m.c("mouth", "white_concrete", (x, 10.8, 14.5), (1.6, 0.9, 0.3))
    m.c("mouth", "red_concrete", (2.4, 7.4, 15.2), (3.6, 4, 1.4), (20, 0, -8))
    m.c("mouth", "pink_concrete", (2.4, 6, 16), (2.6, 1.6, 0.8), (20, 0, -8))
    # a rubber duck float ring round its middle, the duck head grinning back at you
    for k in range(16):
        a = k * 22.5
        x, z = 16.6 * math.cos(math.radians(a)), 16.6 * math.sin(math.radians(a))
        c = "yellow_concrete" if (k // 2) % 2 else "white_concrete"
        m.c("body", c, (x, 7.4, z), (4.6, 4.2, 7), (0, -a, 0))
    m.c("body", "yellow_concrete", (-11, 12.6, 14), (5, 5, 5), (0, -30, 0))
    m.c("body", "orange_concrete", (-12.2, 12, 16.8), (3, 1.2, 2.4), (0, -30, 0))
    m.m("body", "black_concrete", (-9.6 + 0, 13.8, 16.2), (0.8, 0.8, 0.2), (0, -30, 0))
    m.c("body", "black_concrete", (-12.6, 13.8, 14.2), (0.8, 0.8, 0.2), (0, -30, 0))
    # a cocktail umbrella stuck in its head, and a straw
    m.c("body", "white_concrete", (5, 31, -3), (0.6, 12, 0.6), (0, 0, -12))
    m.c("body", "lime_concrete", (6.4, 37, -3), (12, 0.8, 12), (0, 45, -12))
    m.c("body", "pink_concrete", (6.6, 37.8, -3), (8, 0.8, 8), (0, 45, -12))
    m.c("body", "yellow_concrete", (6.8, 38.6, -3), (3, 0.8, 3), (0, 45, -12))
    m.c("body", "red_concrete", (-5, 30, 2), (0.8, 10, 0.8), (14, 0, 20))
    m.c("body", "red_concrete", (-7, 34.8, 3.2), (0.8, 3, 0.8), (40, 0, 70))
    # a lei of flowers round its middle, above the duck ring
    for k in range(14):
        an = math.radians(k * 360 / 14)
        c = ("pink_concrete", "white_concrete", "magenta_concrete", "yellow_concrete")[k % 4]
        m.c("body", c, (math.sin(an) * 14.6, 11.6 + (k % 2) * 0.6, math.cos(an) * 14.6), (2.4, 2.4, 1), (0, math.degrees(an), 45))
    for k in range(7):
        an = math.radians(k * 360 / 7 + 13)
        m.c("body", "lime_concrete", (math.sin(an) * 14.3, 11, math.cos(an) * 14.3), (1.6, 0.6, 0.6), (0, math.degrees(an), 0))
    # a second ring of short flames between the rays, all lit
    for k in range(10):
        an = math.radians(k * 36)
        x, z = 10.6 * math.cos(an), 10.6 * math.sin(an)
        m.c("body", "orange_concrete", (x, 25.6, z), (2, 2.6, 2), (0, -k * 36, 0), light=True)
    # its beach spot: a striped towel under it, a beach ball, flip-flops left in front, a coconut drink
    m.c("body", "light_blue_wool", (-4, 0.1, 2), (40, 0.2, 22), (0, 15, 0))
    for k in range(4):
        m.c("body", "white_wool", (-4 + (k - 1.5) * 8 * math.cos(math.radians(15)), 0.22, 2 + (k - 1.5) * 8 * math.sin(math.radians(-15)) * -1), (2.4, 0.2, 21.6), (0, 15, 0))
    for k, c in enumerate(("red_concrete", "white_concrete", "blue_concrete", "yellow_concrete")):
        m.c("body", c, (-19, 3.2, 8), (6, 6, 6), (0, k * 22.5, 0), (-19, 3.2, 8)) if k == 0 else m.c("body", c, (-19, 3.2, 8 + (k - 2) * 0.01), (6.2, 4.4 - k * 0.6, 4.4 - k * 0.6) if k % 2 else (4.4, 6.2, 4.4), (0, k * 30, 0))
    for x in (-3, 3):
        m.c("body", "lime_concrete", (x, 0.5, 20), (2.4, 0.6, 5), (0, x * 3, 0))
        m.c("body", "pink_concrete", (x, 1.1, 19), (0.4, 0.8, 2.6), (0, x * 3, 0))
    m.c("body", "brown_terracotta", (10, 2, 18.6), (3.6, 3.6, 3.6))
    m.c("body", "white_concrete", (10, 3.9, 18.6), (2.6, 0.3, 2.6))
    m.c("body", "pink_concrete", (10.6, 5.6, 18.6), (0.4, 3.6, 0.4), (0, 0, -15))
    # the hot heart: shroomlight flares inside the core
    for (x, y, z) in ((4, 18, 3), (-4, 11, -3), (3, 9, -4), (-3, 19, 4)):
        m.c("inner", "shroomlight", (x, y, z), (3, 3, 3), (45, 0, 45), light=True)
    # angry brows over the shades, peeling sunburn, a sunscreen bottle stuck in its side, a beach spade
    for s_ in (1, -1):
        m.c("body", "orange_concrete", (5 * s_, 21.8, 14.6), (6, 1, 0.6), (0, 0, 14 * s_), light=True)
        m.c("body", "white_terracotta", (10 * s_, 22, 13.4), (1.6, 1, 0.3))
        m.c("body", "white_terracotta", (11.4 * s_, 16, 14.2), (1, 1.4, 0.3))
    m.c("body", "white_concrete", (15.4, 17, -3), (2.6, 5, 2.6), (0, 0, -30))
    m.c("body", "blue_concrete", (16.8, 19.8, -3), (1.6, 1.4, 1.6), (0, 0, -30))
    m.c("body", "light_blue_concrete", (15.3, 16.6, -1.65), (2, 2, 0.2), (0, 0, -30))
    m.c("body", "red_concrete", (-12, 6, -14.6), (0.6, 8, 0.6), (30, 0, 10))
    m.c("body", "red_concrete", (-12.6, 11.4, -16.6), (2.4, 3, 0.4), (30, 0, 10))
    m.c("body", "yellow_concrete", (12, 4.4, -14), (4, 4, 4))
    m.c("body", "orange_concrete", (12, 6.6, -14), (4.4, 0.6, 4.4))
    m.c("body", "sand", (12, 7.2, -14), (3.4, 0.6, 3.4))
    m.c("body", "white_concrete", (0, 23.6, 14.4), (2, 0.6, 0.3))
    # more drips, heavier on the sunny side
    for x, z, h in ((-3, 14.7, 7), (11, 11.4, 5), (-12, 10, 3), (14.7, -9, 6), (0, -14.7, 5)):
        m.c("body", "yellow_stained_glass", (x, 3.4 + h / 2, z), (1.4, h, 1.4), light=True)
    m.attacks = {"leap": "slam", "quake": "hop", "fire_ring": "burst", "volley": "spit"}
    m.melee = "hop"
    return m


@model
def admiral_pinchworth():
    m = Model("admiral_pinchworth", "spider", 1.7)
    m.bone("body", "root", (0, 12, 0))
    m.bone("abdomen", "body", (0, 16, -4))
    m.bone("head", "body", (0, 14, 9))
    m.bone("fangL", "head", (10, 14, 10))
    m.bone("fangR", "head", (-10, 14, 10))
    sh, sh2, leg, belly = "red_concrete", "red_terracotta", "orange_terracotta", "white_terracotta"
    # a wide flat crab shell, bumpy rim, pale belly
    blob(m, "body", sh, (0, 14, 0), (26, 8, 20), 2.4)
    m.c("body", sh2, (0, 18.4, 0), (18, 1.4, 12))
    for x in (-10, -5, 0, 5, 10):
        m.c("body", sh2, (x, 15, 10.4), (2.4, 2, 1), (0, 0, 45))
    for x, z in ((-7, 3), (7, 3), (-4, -4), (4, -4), (0, 1)):
        m.c("body", sh, (x, 19.2, z), (2.2, 1.2, 2.2))
    m.c("body", belly, (0, 10, 0), (20, 1, 15))
    # a whole sandcastle built on its back, with a little flag and a starfish
    m.c("abdomen", "sandstone", (0, 22, -4), (12, 6, 10))
    for x, z in ((-5, -8), (5, -8), (-5, 0), (5, 0)):
        m.c("abdomen", "sandstone", (x, 27, z), (3.4, 5, 3.4))
        m.c("abdomen", "smooth_sandstone", (x, 30, z), (4, 1, 4))
    m.c("abdomen", "smooth_sandstone", (0, 25.6, -4), (13, 1, 11))
    m.c("abdomen", "sandstone", (0, 28, -4), (5, 6, 5))
    m.c("abdomen", "black_concrete", (0, 23, 1.05), (2, 3, 0.2))
    # its weak spot: the treasure it hides in the castle, a glowing pearl in the gate
    m.c("abdomen", "sea_lantern", (0, 22.6, 1.4), (3.4, 3.4, 3.4), light=True)
    m.c("abdomen", "spruce_log", (0, 34, -4), (0.5, 6, 0.5))
    m.c("abdomen", "blue_concrete", (1.6, 36, -4), (3, 2, 0.2))
    m.c("abdomen", "orange_concrete", (-6.6, 20.6, 1.4), (3.6, 0.8, 0.8), (0, 0, 36))
    m.c("abdomen", "orange_concrete", (-6.6, 20.6, 1.4), (3.6, 0.8, 0.8), (0, 0, -36))
    m.c("abdomen", "orange_concrete", (-6.6, 20.6, 1.4), (0.8, 3.6, 0.8))
    # googly eyes on stalks, a twirled moustache, a tiny admiral's bicorne
    m.c("head", sh, (0, 14, 10.6), (14, 5, 3))
    for s in (1, -1):
        m.c("head", sh2, (3 * s, 19, 10.6), (1.2, 7, 1.2), (0, 0, -10 * s))
        m.c("head", "white_concrete", (3.6 * s, 22.8, 10.6), (3.4, 3.4, 3.4))
        m.c("head", "black_concrete", (3.6 * s + 0.4 * s, 22.2, 12.35), (1.4, 1.4, 0.2))
        m.c("head", "black_concrete", (4.4 * s, 14.8, 12.2), (4, 0.9, 0.6), (0, 0, -20 * s))
        m.c("head", "black_concrete", (6.4 * s, 15.8, 12.2), (1, 1, 0.6))
    m.c("head", "black_concrete", (0, 12.2, 12.15), (4, 0.8, 0.2))
    m.c("head", "blue_terracotta", (0, 26, 9.6), (11, 2.6, 2), (0, 0, 0))
    m.c("head", "blue_terracotta", (0, 27.4, 9.6), (7, 2, 1.8))
    m.c("head", "gold_block", (0, 25, 10.7), (11.2, 0.6, 0.2))
    m.c("head", "white_concrete", (0, 27.4, 10.6), (1.6, 1.6, 0.2))
    # big lopsided claws: the left one is massive and keeps snapping
    for s, b, k in ((1, "fangL", 1.4), (-1, "fangR", 1.0)):
        limb(m, b, leg, (10 * s, 14, 10), [(6, 2.2, (-60, 0, -30 * s)), (5, 2, (-90, 0, 10 * s))])
        cx, cy, cz = 13 * s, 14.6, 20
        m.c(b, sh, (cx, cy, cz), (5 * k, 4.4 * k, 6 * k))
        m.c(b, sh, (cx + 1 * s, cy + 0.4, cz + 5.4 * k), (3 * k, 2.4 * k, 6 * k), (-8, 0, 0))
        m.c(b, sh2, (cx - 1.4 * s, cy - 1.8 * k, cz + 4.8 * k), (2.2 * k, 1.6 * k, 5 * k), (14, 0, 0))
        m.c(b, "white_terracotta", (cx + 1 * s, cy + 0.4, cz + 8.6 * k), (2.4 * k, 1.6 * k, 0.6))
    # eight legs splayed sideways, with pointed tips
    zs = {1: 5, 2: 2, 3: -1.5, 4: -5}
    fan = {1: 30, 2: 10, 3: -10, 4: -30}
    for i in (1, 2, 3, 4):
        m.bone(f"legL{i}", "body", (11, 13, zs[i]))
        m.bone(f"legR{i}", "body", (-11, 13, zs[i]))
        a = fan[i]
        mlimb(m, f"legL{i}", leg, (11, 13, zs[i]), [(8, 1.8, (a, 0, -60)), (13, 1.5, (a * 0.5, 0, -160), sh2), (5, 0.9, (a * 0.3, 0, -178), "white_terracotta")])
    # admiral's dress on the shell: gold epaulettes with fringe, a sash and medals across the front
    for s_ in (1, -1):
        m.c("body", "gold_block", (11 * s_, 18.6, 3), (5, 0.8, 4.4))
        for k in range(4):
            m.c("body", "gold_block", (13.4 * s_, 17.6, 1.4 + k * 1.1), (0.4, 1.6, 0.4))
    m.c("body", "blue_concrete", (0, 15.6, 10.8), (16, 1.6, 0.6), (0, 0, -12))
    for k, c in enumerate(("gold_block", "lapis_block", "gold_block", "emerald_block")):
        m.c("body", c, (-5 + k * 2.2, 13.6, 10.9), (1.2, 1.4, 0.4))
        m.c("body", "red_concrete", (-5 + k * 2.2, 15, 10.85), (0.8, 0.8, 0.3))
    # barnacles and darker spots on the shell, a frill of seaweed caught on the back
    for (x, z) in ((-9, -4), (9, -6), (-5, -8), (6, 6), (-10, 4), (2, -8)):
        m.c("body", "white_terracotta", (x, 18.4, z), (1.6, 1.2, 1.6))
        m.c("body", "light_gray_concrete", (x, 19, z), (0.6, 0.4, 0.6))
    for (x, z) in ((-3, 5), (3, -2), (-7, 0), (8, 1)):
        m.c("body", "red_terracotta", (x, 18.2, z), (2.4, 0.4, 2.4))
    for k, x in enumerate((-8, -4, 3, 8)):
        m.c("body", "green_terracotta" if k % 2 else "lime_terracotta", (x, 13.4, -10.4), (1.6, 6 - k % 2 * 2, 0.4), (10, 0, 6 - k * 4))
    # claw teeth along the pincers, joints on the claws
    for s_, b, k in ((1, "fangL", 1.4), (-1, "fangR", 1.0)):
        cx, cy, cz = 13 * s_, 14.6, 20
        for t in range(3):
            m.c(b, "white_terracotta", (cx - 1.4 * s_, cy - 0.4 * k, cz + (3 + t * 1.6) * k), (0.8 * k, 1.2 * k, 0.8 * k), (45, 0, 0))
        m.c(b, "red_terracotta", (cx, cy, cz - 3 * k), (3.6 * k, 3.6 * k, 1.4))
    # the sandcastle grows two more turrets with flags and a shell door
    for x, c in ((-7, "red_concrete"), (7, "yellow_concrete")):
        m.c("abdomen", "sandstone", (x, 24, -9), (3, 4, 3))
        m.c("abdomen", "smooth_sandstone", (x, 26.4, -9), (3.6, 0.8, 3.6))
        m.c("abdomen", "spruce_log", (x, 28.6, -9), (0.4, 3.6, 0.4))
        m.c("abdomen", c, (x + 1.2, 29.6, -9), (2, 1.4, 0.2))
    for k in range(4):
        m.c("abdomen", "smooth_sandstone", (-4.5 + k * 3, 32.2, -4), (1.6, 1.4, 1.6))
    m.c("abdomen", "pink_terracotta", (0, 25.6, 1.15), (2.6, 1.6, 0.3))
    m.c("head", "white_concrete", (0, 26, 10.7), (11.2, 0.4, 0.2))
    # eye-stalk rings and a pipe
    for s_ in (1, -1):
        m.c("head", "orange_terracotta", (3.2 * s_, 20.6, 10.6), (1.8, 0.6, 1.8))
    m.c("head", "brown_terracotta", (-3, 11.6, 13), (0.6, 0.6, 3))
    m.c("head", "brown_terracotta", (-3, 12.8, 14.4), (1.4, 1.8, 1.4))
    m.attacks = {"leap": "leap", "minions": "drum", "pull": "rearup", "volley": "spit"}
    m.melee = "fang"
    return m
