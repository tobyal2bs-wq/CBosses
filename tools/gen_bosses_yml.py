"""Writes src/main/resources/bosses.yml for the 52 bosses: 25 general bosses, 5 legends (the Warden, Wither,
Ender Dragon and Breeze bosses and the finale), 12 seasonal ones (3 each for winter, summer, spring/Easter and
Halloween) and a small boss after each of the 10 chapters.

Stats of bosses that already existed are read from the current bosses.yml so tuning done there is kept; new
bosses are defined below. Abilities start with the ones the model has its own attack move for (models.json),
then the extras listed here. Descriptions come from the model's own docstring, so the text matches the look.
Run: python3 tools/gen_bosses_yml.py   (after tools/models/gen_models.py)"""
import os, sys, json, yaml, importlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "models"))
import models as _m
for mod in ("v2_general", "v2_seasonal", "v2_chapters", "v2_legends"):
    importlib.import_module(mod)
DOCS = {f.__name__: " ".join((f.__doc__ or "").split()) for f in _m.MODELS}
MODELS = json.load(open(os.path.join(ROOT, "src/main/resources/models.json")))["models"]
YML = os.path.join(ROOT, "src/main/resources/bosses.yml")
OLD = yaml.safe_load(open(YML))["bosses"]

GENERAL = ["slagheart", "warlord_gruk", "grand_augur", "crimson_ronin", "thunderback", "gorehorn", "abyssal_eye", "overgrowth",
           "prism_sentinel", "tiki_warden", "hollow_king", "broodmother", "ironhide_behemoth", "fenrir", "tide_tyrant", "void_walker",
           "storm_herald", "pharaoh", "executioner", "ember_queen", "gravelord", "captain_brine", "keywarden", "bloodtusk", "king_gloop"]
LEGENDS = ["the_listener", "withered_tyrant", "ender_wyrm", "gale_sovereign", "the_unmaker"]
SEASONAL = {"winter": ["killer_claus", "frostbottom", "old_man_winter"], "summer": ["sunscorch", "admiral_pinchworth", "brain_freeze"],
            "spring": ["clucksworth", "killer_bunny", "cocoa_colossus"], "halloween": ["great_gourd", "headless_horseman", "hexmother"]}
CHAPTERS = ["brakka", "gate_shade", "oakheart", "vault_mimic", "crypt_knight", "iron_tusk", "reef_hulk", "ember_knight", "choirmaster", "sculk_herald"]

# extra abilities on top of the model's own attack moves (these use its melee swing)
EXTRA = {
 "slagheart": ["fire_ring", "shockwave"], "warlord_gruk": ["leap", "shockwave"], "grand_augur": ["levitate", "darkness"],
 "crimson_ronin": ["leap", "fire_ring"], "thunderback": ["leap", "shockwave"], "gorehorn": ["shockwave", "leap"],
 "abyssal_eye": ["frost", "shockwave"], "overgrowth": ["spikes", "poison"], "prism_sentinel": ["orbs", "shockwave"],
 "tiki_warden": ["fire_ring", "shockwave"], "hollow_king": ["darkness", "shockwave"], "broodmother": ["charge", "spikes"],
 "ironhide_behemoth": ["shockwave", "leap"], "fenrir": ["shockwave", "roar"], "tide_tyrant": ["frost", "minions"],
 "void_walker": ["sonic_boom", "levitate"], "storm_herald": ["meteor", "levitate"], "pharaoh": ["poison", "orbs"],
 "executioner": ["minions", "shockwave"], "ember_queen": ["breath", "orbs"], "gravelord": ["spikes", "shockwave"],
 "captain_brine": ["shockwave", "frost"], "keywarden": ["shockwave", "orbs"], "bloodtusk": ["minions", "shockwave"],
 "king_gloop": ["spikes", "shockwave"],
 "the_listener": ["shockwave", "pull", "charge"], "withered_tyrant": ["darkness", "meteor", "dive"],
 "ender_wyrm": ["dive", "orbs", "meteor", "levitate"], "gale_sovereign": ["levitate", "volley", "dive"],
 "the_unmaker": ["quake", "sonic_boom", "pull", "darkness", "lightning", "blink", "minions"],
 "killer_claus": ["gifts", "frost"], "frostbottom": ["gifts", "shockwave"], "old_man_winter": ["volley", "shockwave"],
 "sunscorch": ["meteor", "sprinkles"], "admiral_pinchworth": ["charge", "orbs"], "brain_freeze": ["orbs", "shockwave"],
 "clucksworth": ["leap", "shockwave"], "killer_bunny": ["shockwave", "slam"], "cocoa_colossus": ["eggs", "shockwave"],
 "great_gourd": ["meteor", "slam"], "headless_horseman": ["shockwave", "pull"], "hexmother": ["levitate", "heal"],
 "brakka": ["fire_ring"], "gate_shade": [], "oakheart": ["heal"], "vault_mimic": [], "crypt_knight": ["charge"],
 "iron_tusk": ["fire_ring"], "reef_hulk": [], "ember_knight": ["breath"], "choirmaster": ["sonic_boom"], "sculk_herald": ["pull"],
}

NEW = {
 "slagheart": dict(name="<gradient:#3d3d3d:#ff6a00><bold>Slagheart</bold></gradient>", title="The Molten Colossus", entity="IRON_GOLEM",
     health=2000, damage=12, armor=10, bar="RED", theme="fire", minion="MAGMA_CUBE", minions=3, money=45000, top_money=140000,
     items=["IRON_BLOCK 3", "MAGMA_BLOCK 16", "DIAMOND 2"], top_items=["NETHERITE_SCRAP 1"]),
 "grand_augur": dict(name="<gradient:#4a5a8a:#ffd54f><bold>The Grand Augur</bold></gradient>", title="King of the Illagers", entity="EVOKER",
     health=1700, damage=11, armor=6, bar="BLUE", theme="witch", minion="VINDICATOR", minions=3, money=50000, top_money=150000,
     items=["EMERALD 24", "TOTEM_OF_UNDYING 1"], top_items=["DIAMOND 4"]),
 "crimson_ronin": dict(name="<gradient:#8b0000:#ff6b6b><bold>The Crimson Oni</bold></gradient>", title="Warlord of the Red Mountain", entity="VINDICATOR",
     health=1800, damage=13, armor=8, bar="RED", theme="blood", minion="VINDICATOR", minions=2, money=45000, top_money=140000,
     items=["IRON_INGOT 16", "GOLD_INGOT 8", "DIAMOND 2"], top_items=["ENCHANTED_GOLDEN_APPLE 1"]),
 "thunderback": dict(name="<gradient:#5d3a1a:#ffe14d><bold>Thunderback</bold></gradient>", title="The Storm Ape", entity="RAVAGER",
     health=2100, damage=12, armor=8, bar="YELLOW", theme="storm", minion=None, minions=0, money=45000, top_money=140000,
     items=["COPPER_BLOCK 8", "LIGHTNING_ROD 4", "DIAMOND 2"], top_items=["TRIDENT 1"]),
 "gorehorn": dict(name="<gradient:#3e2723:#ffcc80><bold>Gorehorn</bold></gradient>", title="Champion of the Pit", entity="RAVAGER",
     health=2000, damage=13, armor=8, bar="WHITE", theme="earth", minion=None, minions=0, money=45000, top_money=140000,
     items=["LEATHER 16", "IRON_INGOT 16", "DIAMOND 2"], top_items=["NETHERITE_SCRAP 1"]),
 "abyssal_eye": dict(name="<gradient:#003b46:#66fcf1><bold>The Abyssal Eye</bold></gradient>", title="Sentinel of the Drowned Temple", entity="BLAZE",
     health=1700, damage=11, armor=10, bar="BLUE", theme="water", movement="hover", fly_height=3, minion="DROWNED", minions=2,
     money=45000, top_money=140000, items=["PRISMARINE_SHARD 24", "SPONGE 4", "DIAMOND 2"], top_items=["HEART_OF_THE_SEA 1"]),
 "overgrowth": dict(name="<gradient:#2d6a4f:#d8a657><bold>Overgrowth</bold></gradient>", title="The Guardian the Jungle Took", entity="IRON_GOLEM",
     health=1900, damage=11, armor=10, bar="GREEN", theme="nature", minion="CAVE_SPIDER", minions=3, money=42000, top_money=130000,
     items=["MOSS_BLOCK 16", "GOLDEN_APPLE 3", "DIAMOND 2"], top_items=["ENCHANTED_GOLDEN_APPLE 1"]),
 "prism_sentinel": dict(name="<gradient:#7b2ff7:#4ef0ff><bold>The Prism Sentinel</bold></gradient>", title="Cut From the Heart of the Mountain", entity="IRON_GOLEM",
     health=1900, damage=11, armor=14, bar="PURPLE", theme="witch", minion=None, minions=0, money=50000, top_money=150000,
     items=["AMETHYST_SHARD 32", "DIAMOND 4"], top_items=["DIAMOND_BLOCK 1"]),
 "tiki_warden": dict(name="<gradient:#bf360c:#ffb300><bold>The Tiki Warden</bold></gradient>", title="Idol of the Burning Isle", entity="ZOMBIE",
     health=1800, damage=12, armor=8, bar="YELLOW", theme="fire", minion="BLAZE", minions=2, money=42000, top_money=130000,
     items=["GOLD_INGOT 12", "BLAZE_ROD 6", "DIAMOND 2"], top_items=["ENCHANTED_GOLDEN_APPLE 1"]),
 "gale_sovereign": dict(name="<gradient:#5fb3a8:#e0f7fa><bold>The Gale Sovereign</bold></gradient>", title="Lord of the Trial Winds", entity="BREEZE",
     health=2800, damage=13, armor=10, bar="WHITE", theme="wind", movement="hover", fly_height=3, minion="BREEZE", minions=2,
     phases=[0.7, 0.4, 0.15], ability_seconds=5, money=85000, top_money=280000,
     items=["BREEZE_ROD 8", "WIND_CHARGE 32", "DIAMOND 4"], top_items=["HEAVY_CORE 1"]),
 "cocoa_colossus": dict(name="<gradient:#4e2a1e:#ffcf6b><bold>The Cocoa Colossus</bold></gradient>", title="The Egg That Fought Back", entity="IRON_GOLEM",
     season="spring", health=1700, damage=11, armor=10, bar="YELLOW", theme="candy", minion="RABBIT", minions=3, money=50000, top_money=150000,
     items=["COCOA_BEANS 32", "COOKIE 32", "DIAMOND 2"], top_items=["ENCHANTED_GOLDEN_APPLE 1"]),
 "vault_mimic": dict(name="<gradient:#6d4c41:#ffd54f><bold>The Vault Mimic</bold></gradient>", title="The Fifth Key's Chest", entity="SPIDER",
     health=1200, damage=8, armor=8, bar="YELLOW", theme="gold", minion=None, minions=0, money=20000, top_money=0,
     items=["GOLD_INGOT 16", "EMERALD 8", "DIAMOND 1"], top_items=[]),
 "crypt_knight": dict(name="<gradient:#4a4e69:#9ad1ff><bold>The Crypt Knight</bold></gradient>", title="First to Answer the King", entity="ZOMBIE",
     health=1400, damage=9, armor=12, bar="BLUE", theme="soul", minion="SKELETON", minions=2, money=24000, top_money=0,
     items=["IRON_INGOT 16", "DIAMOND 2"], top_items=[]),
 "reef_hulk": dict(name="<gradient:#1b4965:#ff8fab><bold>The Reef Hulk</bold></gradient>", title="Where the Reef Grew", entity="DROWNED",
     health=1800, damage=10, armor=8, bar="BLUE", theme="water", minion="DROWNED", minions=2, money=34000, top_money=0,
     items=["PRISMARINE_SHARD 16", "DIAMOND 2", "NAUTILUS_SHELL 2"], top_items=[]),
 "ember_knight": dict(name="<gradient:#7f1d1d:#ffb703><bold>The Ember Knight</bold></gradient>", title="Champion of the Ember Court", entity="ZOMBIE",
     health=2000, damage=10, armor=10, bar="RED", theme="fire", minion="BLAZE", minions=1, money=40000, top_money=0,
     items=["BLAZE_ROD 8", "DIAMOND 3"], top_items=[]),
 "sculk_herald": dict(name="<gradient:#052e33:#29dfeb><bold>The Sculk Herald</bold></gradient>", title="It Wakes the Listener", entity="WITHER_SKELETON",
     health=2500, damage=11, armor=8, bar="BLUE", theme="sculk", movement="hover", fly_height=2, minion=None, minions=0, money=52000, top_money=0,
     items=["ECHO_SHARD 4", "SCULK_CATALYST 1", "DIAMOND 4"], top_items=[]),
}

# bosses that used to close a chapter and now join the weekly rotation get general boss health
PROMOTED = {"keywarden": 1800, "hollow_king": 2200, "captain_brine": 1900, "ember_queen": 2000}
# minions for bosses whose model has a summon move
MINION = {"keywarden": "SILVERFISH", "hexmother": "VEX", "oakheart": "SPIDER", "vault_mimic": "SILVERFISH", "sculk_herald": "SILVERFISH"}
CHAPTER_HEALTH = [500, 700, 900, 1200, 1400, 1600, 1800, 2000, 2200, 2500]


def describe(id):
    d = DOCS.get(id, "")
    if d.startswith("Chapter") or d.startswith("THE UNMAKER"):
        return d
    return d[0].upper() + d[1:] if d else OLD.get(id, {}).get("description", "")


def entry(id, kind, season=None, chapter=None):
    o = OLD.get(id)
    if o:
        r = o.get("rewards", {})
        d = dict(name=o["name"], title=o.get("title", ""), entity=o["entity"], health=o["health"], scale=o.get("scale"), damage=o["damage"],
                 speed=o.get("speed"), armor=o.get("armor", 0), bar=o.get("bar", "RED"), theme=o.get("theme", "soul"),
                 movement=o.get("movement", "walk"), fly_height=o.get("fly-height"), phases=o.get("phases", [0.66, 0.33]),
                 equipment=o.get("equipment"), minion=o.get("minion"), minions=o.get("minions", 3), ability_seconds=o.get("ability-seconds", 7),
                 hpp=o.get("health-per-player", 0.25), money=r.get("money", 0), top_money=r.get("top-money", 0), items=r.get("items", []),
                 top_items=r.get("top-items", []), commands=r.get("commands", []), top_commands=r.get("top-commands", []))
    else:
        d = dict(NEW[id])
    d.update(NEW.get(id, {}) if o else {})
    d["season"], d["chapter"] = season, chapter
    if chapter:
        d["health"] = CHAPTER_HEALTH[chapter - 1]
        d["top_money"] = 0
    elif id in PROMOTED:
        d["health"] = PROMOTED[id]
    if not chapter and not d.get("top_money"):
        d["top_money"] = d.get("money", 0) * 3
    if id == "gale_sovereign":
        d["theme"] = "wind"
    if id == "the_unmaker":
        d["description"] = describe(id).replace("THE UNMAKER, the finale.", "The finale. Wakes once the Withered Tyrant, the Ender Wyrm, the Gale Sovereign and The Listener Below have all been beaten.")
    else:
        d["description"] = describe(id)
    if id in MINION and not d.get("minion"):
        d["minion"], d["minions"] = MINION[id], 2 if chapter else 3
    own = list(MODELS[id]["attacks"])
    d["abilities"] = list(dict.fromkeys(own + EXTRA.get(id, [])))
    return d


def q(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


def lst(v):
    return "[" + ", ".join(q(x) for x in v) + "]"


out = []
w = out.append
w("""# CBosses bosses. Every boss is a block model (models.json) drawn over an invisible mob that gives it its AI
# and hitbox. Add your own, change any number, or set enabled: false to turn one off. /cbosses reload applies it.
#
# kind:       world (the weekly boss rotation), seasonal (needs season:) or chapter (needs chapter:).
#             It is worked out for you from season: and chapter: when left out.
# chapter:    the CQuests chapter after which this boss comes for the player (chapter bosses are one-on-one).
# season:     halloween, winter, spring or summer. Seasonal bosses take the weekly slot while their season is on.
# entity:     the invisible mob underneath (its AI and hitbox). Any mob works.
# movement:   walk, fly (circles and dives), hover (floats above the ground) or still.
# fly-height: blocks above the ground for fly and hover bosses (2 to 20).
# theme:      colours, particles and sounds of every attack: soul, fire, frost, nature, gold, water, storm, earth,
#             blood, toxic, void, witch, sand, bone, sculk, wither, dragon, holiday, candy, pumpkin, feather, iron, wind.
# abilities:  picked at random every ability-seconds (faster in later phases). The first ones listed are the
#             attacks the model has its own move for; the rest use its normal swing.
#             lightning, shockwave, minions, fire_ring, pull, leap, poison, blink, frost, volley, darkness, levitate,
#             heal, quake, detonate, roar, charge, slam, meteor, sonic_boom, skulls, breath, spikes, orbs, gifts,
#             sprinkles, dive, eggs
# phases:     health fractions where it gets angrier: faster attacks, more minions, its last ability right away.
# health-per-player: extra health for each extra player near when it wakes (0.25 = +25% each).
# rewards:    everyone who did at least rewards.min-damage-percent (config.yml) gets money, items and commands;
#             the top 3 get top-money (split 1, 1/2, 1/3) and top-items, the best gets top-commands too.
#             %player% and %place% work in commands. Chapter bosses pay the player who beat it.
# model:      the model in models.json (defaults to the id), or none for the plain mob with its equipment.
# description: shown in /cbosses menu and the README.
bosses:
""")


def emit(id, d):
    w(f"  {id}:")
    for k in ("name", "title"):
        w(f"    {k}: {q(d[k])}")
    if d.get("chapter"): w(f"    chapter: {d['chapter']}")
    if d.get("season"): w(f"    season: {d['season']}")
    w(f"    entity: {d['entity']}")
    w(f"    health: {d['health']}")
    if d.get("scale"): w(f"    scale: {d['scale']}")
    w(f"    damage: {d['damage']}")
    if d.get("speed"): w(f"    speed: {d['speed']}")
    w(f"    armor: {d.get('armor', 0)}")
    w(f"    bar: {d['bar']}")
    w(f"    theme: {d['theme']}")
    w(f"    movement: {d.get('movement') or 'walk'}")
    if d.get("fly_height"): w(f"    fly-height: {d['fly_height']}")
    w(f"    phases: [{', '.join(str(p) for p in d.get('phases') or [0.5])}]")
    if d.get("equipment"):
        w("    equipment:")
        for slot, item in d["equipment"].items(): w(f"      {slot}: {item}")
    if d.get("minion"):
        w(f"    minion: {d['minion']}")
        w(f"    minions: {d.get('minions', 3)}")
    w(f"    ability-seconds: {d.get('ability_seconds', 7)}")
    w(f"    abilities: [{', '.join(d['abilities'])}]")
    w(f"    health-per-player: {d.get('hpp', 0.25)}")
    w("    rewards:")
    w(f"      money: {d.get('money', 0)}")
    w(f"      top-money: {d.get('top_money', 0)}")
    w(f"      items: {lst(d.get('items', []))}")
    w(f"      top-items: {lst(d.get('top_items', []))}")
    w(f"      commands: {lst(d.get('commands', []))}")
    w(f"      top-commands: {lst(d.get('top_commands', []))}")
    w(f"    description: {q(d['description'])}")


w("  # ------------------------------------------------------------ the 25 general bosses (weekly rotation)")
for id in GENERAL: emit(id, entry(id, "world"))
w("  # ------------------------------------------------------------ legends: Warden, Wither, Ender Dragon, Breeze and the finale")
for id in LEGENDS: emit(id, entry(id, "world"))
for season, ids in SEASONAL.items():
    w(f"  # ------------------------------------------------------------ {season}")
    for id in ids: emit(id, entry(id, "seasonal", season=season))
w("  # ------------------------------------------------------------ chapter bosses, one after every CQuests chapter")
for n, id in enumerate(CHAPTERS, 1): emit(id, entry(id, "chapter", chapter=n))

all_ids = GENERAL + LEGENDS + sum(SEASONAL.values(), []) + CHAPTERS
assert len(all_ids) == 52 and len(set(all_ids)) == 52 and set(all_ids) == set(MODELS), set(MODELS) ^ set(all_ids)
open(YML, "w").write("\n".join(out) + "\n")
print("wrote", YML, len(all_ids), "bosses")
