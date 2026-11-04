"""Writes src/main/resources/bosses.yml: the 28 bosses from CQuests (with themes, movement, the new attacks and a
description each) plus the CBosses bosses. Run: python3 tools/gen_bosses_yml.py path/to/cquests/worldbosses.yml"""
import sys, os, yaml

src = yaml.safe_load(open(sys.argv[1]))["bosses"]

# id: (theme, movement, extra abilities, description)
OLD = {
 "gravelord": ("soul", "walk", ["skulls", "spikes"], "A lord of the restless dead in a tattered royal robe. Raises skeletons, blinds the arena and fires burning skulls."),
 "molten_colossus": ("fire", "walk", ["meteor", "slam"], "A walking forge of lava and iron plates. Its fists crater the ground and molten rocks rain from the sky."),
 "broodmother": ("toxic", "walk", ["spikes", "charge"], "A giant spider queen. Spits venom, drags you in with webs and sends her brood after you."),
 "frost_jarl": ("frost", "walk", ["slam", "spikes"], "A frost giant king in iron and fur. Freezes the ground, throws ice and calls his frozen guard."),
 "warlord_gruk": ("gold", "walk", ["charge", "slam"], "A piglin warlord dripping in gold. Charges, leaps and smashes, and his brutes never stop coming."),
 "tide_tyrant": ("water", "walk", ["orbs", "slam"], "A drowned king with a trident. Pulls you into the deep, freezes you with sea spray and raises the drowned."),
 "storm_herald": ("storm", "walk", ["orbs", "meteor"], "An evoker of storms. Calls lightning, throws players into the air and blinks around the arena."),
 "ironhide_behemoth": ("iron", "walk", ["charge", "slam"], "A huge armoured beast. Charges through everything and shakes the ground with every stomp."),
 "bloodtusk": ("blood", "walk", ["charge", "slam"], "A crimson boar of the Nether. Gores, charges and calls its herd."),
 "cinder_sovereign": ("fire", "hover", ["meteor", "orbs", "breath"], "A floating lord of embers in spinning rings of fire. Rains meteors and breathes flame."),
 "volatile_colossus": ("toxic", "walk", ["slam", "charge"], "A creeper the size of a house. It explodes, a lot, and never dies from it."),
 "king_gloop": ("toxic", "walk", ["slam", "spikes"], "The slime king. Bounces, quakes the arena and splits into a crowd of little slimes."),
 "executioner": ("blood", "walk", ["charge", "slam"], "A hooded executioner with a giant axe. Charges, cleaves and calls his vindicators."),
 "pharaoh": ("sand", "walk", ["spikes", "orbs"], "An ancient pharaoh. Curses the sun away, poisons with sand and raises husks from the dunes."),
 "ruinmaw": ("earth", "walk", ["charge", "spikes"], "A chained zoglin beast of the ruins. Breaks the ground into spikes and charges."),
 "hexmother": ("witch", "walk", ["orbs", "spikes"], "A witch queen. Curses, heals herself, throws potions and floats players up into the air."),
 "void_walker": ("void", "walk", ["orbs", "sonic_boom"], "A tall enderman from the void. Teleports, blinds and pulls players into its rift."),
 "fenrir": ("frost", "walk", ["charge", "slam"], "A giant frost wolf. Leaps, freezes and howls for its pack."),
 "tempest": ("storm", "hover", ["orbs", "dive"], "A living storm. Throws players around with wind and calls down lightning."),
 "pale_watcher": ("bone", "walk", ["spikes", "sonic_boom"], "A pale creaking tree that watches. Only moves when you look away... mostly."),
 "headless_horseman": ("pumpkin", "walk", ["charge", "meteor"], "Rides out every Halloween with a flaming pumpkin for a head. Throws fire and calls the dead."),
 "old_man_winter": ("frost", "walk", ["spikes", "gifts"], "A grumpy old winter wizard. Freezes the arena and throws snow and ice."),
 "killer_bunny": ("blood", "walk", ["charge", "eggs"], "A harmless little rabbit... that keeps growing, and bites."),
 "sunscorch": ("fire", "walk", ["meteor", "sprinkles"], "A grumpy sun on a pool float. Sets the arena on fire and cannonballs into players."),
 "great_gourd": ("pumpkin", "walk", ["meteor", "slam"], "A giant pumpkin giant with a lollipop club. Lobs burning pumpkins and smashes."),
 "frostbottom": ("frost", "walk", ["slam", "gifts"], "A huge snowman with a club. Throws snowballs, freezes and stomps."),
 "clucksworth": ("feather", "walk", ["eggs", "charge"], "Hatches out of a giant egg as the angriest chicken alive. Throws eggs that hatch, leaps and charges."),
 "admiral_pinchworth": ("water", "walk", ["charge", "orbs"], "A crab admiral. Pinches, scuttles sideways and pulls you in."),
}
MINION_SWAP = {}

NEW = {
 # ---------------------------------------------------------------- legends
 "withered_tyrant": dict(name="<gradient:#2b2b2b:#8b0000><bold>The Withered Tyrant</bold></gradient>", title="Three Skulls, One Hunger",
     entity="WITHER_SKELETON", health=2600, damage=14, armor=12, bar="PURPLE", theme="wither", movement="hover", fly_height=5,
     minion="WITHER_SKELETON", minions=3, abilities=["skulls", "darkness", "shockwave", "meteor", "minions", "dive"], ability_seconds=6,
     phases=[0.66, 0.33], money=80000, top_money=250000, items=["NETHER_STAR 1", "GOLDEN_APPLE 6"], top_items=["ENCHANTED_GOLDEN_APPLE 2"],
     description="A three-headed wither. Floats above the arena firing volleys of wither skulls from all three heads, screams the light away and dives at you."),
 "ender_wyrm": dict(name="<gradient:#1a0033:#d14bff><bold>Vorthax the Ender Wyrm</bold></gradient>", title="Dragon of the Outer Dark",
     entity="PHANTOM", health=3000, damage=13, armor=8, bar="PINK", theme="dragon", movement="fly", fly_height=9,
     minion="ENDERMITE", minions=4, abilities=["breath", "dive", "orbs", "meteor", "shockwave", "levitate"], ability_seconds=6,
     phases=[0.7, 0.4, 0.15], money=90000, top_money=300000, items=["DRAGON_BREATH 4", "ENDER_PEARL 8", "SHULKER_SHELL 2"], top_items=["ELYTRA 1"],
     description="A real flying dragon. Circles the arena, dives through it, breathes purple fire across the floor and calls down end crystals."),
 "killer_claus": dict(name="<gradient:#b30000:#ffffff><bold>Killer Claus</bold></gradient>", title="He Knows If You've Been Bad",
     entity="ZOMBIE", health=2000, damage=12, armor=6, bar="RED", theme="holiday", movement="walk", season="winter",
     minion="STRAY", minions=4, abilities=["gifts", "frost", "charge", "minions", "leap", "volley"], ability_seconds=6,
     phases=[0.6, 0.3], money=60000, top_money=180000, items=["COOKIE 32", "DIAMOND 3"], top_items=["ENCHANTED_GOLDEN_APPLE 1"],
     description="Santa gone very wrong, with a candy cane scythe and a sack of presents that explode. Climbs out of the sack laughing."),
 "brain_freeze": dict(name="<gradient:#ff8fc8:#9fffd0><bold>Brain Freeze</bold></gradient>", title="The Sundae Supreme",
     entity="ZOMBIE", health=1800, damage=10, armor=4, bar="PINK", theme="candy", movement="walk", season="summer",
     minion="SLIME", minions=4, abilities=["sprinkles", "frost", "orbs", "shockwave", "minions", "levitate"], ability_seconds=6,
     phases=[0.5], money=55000, top_money=160000, items=["COOKIE 16", "MELON_SLICE 32", "DIAMOND 2"], top_items=["ENCHANTED_GOLDEN_APPLE 1"],
     description="A three-scoop ice cream monster on a waffle cone. Rains sprinkles, freezes you solid and splats scoops across the arena."),
 # ---------------------------------------------------------------- chapter bosses
 "brakka": dict(name="<gradient:#ff7b00:#ffd27a><bold>Brakka the Torchbearer</bold></gradient>", title="Burner of the Wanderers' Camp",
     entity="VINDICATOR", health=500, damage=7, armor=4, bar="YELLOW", theme="fire", chapter=1,
     minion="PILLAGER", minions=2, abilities=["fire_ring", "charge", "minions", "breath"], ability_seconds=8,
     phases=[0.5], money=8000, top_money=0, items=["IRON_INGOT 8", "BREAD 8"], top_items=[],
     description="Chapter 1. The bandit chief who burned the Wanderers' Camp, with a torch in one hand and a cleaver in the other."),
 "gate_shade": dict(name="<gradient:#22223b:#8ecae6><bold>The Gate Shade</bold></gradient>", title="What Waits at the Gate",
     entity="WITHER_SKELETON", health=700, damage=7, armor=2, bar="BLUE", theme="soul", chapter=2, movement="hover", fly_height=3,
     minion="SKELETON", minions=2, abilities=["darkness", "blink", "pull", "orbs"], ability_seconds=8,
     phases=[0.5], money=12000, top_money=0, items=["IRON_INGOT 12", "GOLDEN_APPLE 1"], top_items=[],
     description="Chapter 2. A chained, hooded shadow that hangs in the broken gate. Pulls you into the dark and blinks around you."),
 "oakheart": dict(name="<gradient:#3a5a40:#a3b18a><bold>Sir Oakheart</bold></gradient>", title="The Elder's Champion",
     entity="ZOMBIE", health=900, damage=8, armor=8, bar="GREEN", theme="nature", chapter=3,
     minion=None, minions=0, abilities=["spikes", "heal", "pull", "charge", "shockwave"], ability_seconds=8,
     phases=[0.5], money=16000, top_money=0, items=["GOLD_INGOT 8", "GOLDEN_APPLE 2"], top_items=[],
     description="Chapter 3. The Elder's champion: a knight grown from an old oak. Roots burst from the ground and he heals in the sun."),
 "keywarden": dict(name="<gradient:#b8860b:#fff3b0><bold>The Keywarden</bold></gradient>", title="Guardian of the Five Keys",
     entity="IRON_GOLEM", health=1200, damage=9, armor=12, bar="YELLOW", theme="gold", chapter=4,
     minion=None, minions=0, abilities=["slam", "shockwave", "pull", "quake", "orbs"], ability_seconds=7,
     phases=[0.5], money=20000, top_money=0, items=["GOLD_INGOT 16", "DIAMOND 1"], top_items=[],
     description="Chapter 4. A giant walking padlock with five glowing keyholes, swinging a key the size of a tree."),
 "hollow_king": dict(name="<gradient:#1b263b:#7fd1ff><bold>THE HOLLOW KING</bold></gradient>", title="The King Wakes",
     entity="WITHER_SKELETON", health=2400, damage=13, armor=12, bar="BLUE", theme="soul", chapter=5,
     minion="WITHER_SKELETON", minions=3, abilities=["slam", "minions", "darkness", "shockwave", "meteor", "charge", "spikes"], ability_seconds=6,
     phases=[0.7, 0.4, 0.15], money=60000, top_money=0, items=["DIAMOND 4", "GOLDEN_APPLE 4", "NETHERITE_SCRAP 1"], top_items=[],
     description="Chapter 5, the first great boss. The ancient king rises from his tomb, nine blocks tall in rusted royal armour, a crown of soul fire on an empty helm."),
 "iron_tusk": dict(name="<gradient:#5c5c5c:#ff9e40><bold>Iron Tusk</bold></gradient>", title="The War Boar",
     entity="HOGLIN", health=1600, damage=10, armor=12, bar="WHITE", theme="iron", chapter=6,
     minion="HOGLIN", minions=2, abilities=["charge", "quake", "shockwave", "fire_ring", "slam"], ability_seconds=7,
     phases=[0.5], money=28000, top_money=0, items=["IRON_BLOCK 4", "DIAMOND 2"], top_items=[],
     description="Chapter 6. A war boar in riveted iron plates with a furnace burning in its chest. It charges, and it does not stop."),
 "captain_brine": dict(name="<gradient:#005f73:#94d2bd><bold>Captain Brine</bold></gradient>", title="Captain of the Drowned",
     entity="DROWNED", health=1900, damage=10, armor=8, bar="BLUE", theme="water", chapter=7,
     minion="DROWNED", minions=3, abilities=["pull", "slam", "frost", "minions", "orbs", "shockwave"], ability_seconds=7,
     phases=[0.5], money=34000, top_money=0, items=["PRISMARINE_SHARD 16", "DIAMOND 2", "HEART_OF_THE_SEA 1"], top_items=[],
     description="Chapter 7. A drowned sea captain with a coral beard who swings a rusted anchor on a chain and drags you under."),
 "ember_queen": dict(name="<gradient:#9d0208:#ffba08><bold>The Ember Queen</bold></gradient>", title="Queen of the Ember Court",
     entity="BLAZE", health=2200, damage=11, armor=8, bar="RED", theme="fire", chapter=8, movement="hover", fly_height=3,
     minion="BLAZE", minions=2, abilities=["fire_ring", "meteor", "breath", "orbs", "blink", "minions"], ability_seconds=6,
     phases=[0.6, 0.3], money=40000, top_money=0, items=["BLAZE_ROD 8", "DIAMOND 3"], top_items=[],
     description="Chapter 8. A queen of blackstone and fire who steps out of a lava pillar. Rains meteors and breathes fire."),
 "choirmaster": dict(name="<gradient:#e9e3c9:#6c757d><bold>The Choirmaster</bold></gradient>", title="Conductor of the Bone Choir",
     entity="WITHER_SKELETON", health=2500, damage=11, armor=8, bar="WHITE", theme="bone", chapter=9, movement="hover", fly_height=3,
     minion="SKELETON", minions=4, abilities=["minions", "skulls", "shockwave", "darkness", "sonic_boom", "orbs"], ability_seconds=6,
     phases=[0.6, 0.3], money=48000, top_money=0, items=["BONE_BLOCK 8", "DIAMOND 4"], top_items=[],
     description="Chapter 9. A skeleton conductor floating inside a ring of singing skulls. Every chord is an attack."),
 "the_listener": dict(name="<gradient:#052e33:#4ae3e3><bold>THE LISTENER BELOW</bold></gradient>", title="It Hears Your Heartbeat",
     entity="IRON_GOLEM", health=3600, damage=15, armor=14, bar="BLUE", theme="sculk", chapter=10,
     minion=None, minions=0, abilities=["sonic_boom", "darkness", "slam", "shockwave", "quake", "pull", "charge"], ability_seconds=5,
     phases=[0.75, 0.5, 0.25], money=100000, top_money=0, items=["DIAMOND 8", "NETHERITE_INGOT 1", "ECHO_SHARD 4"], top_items=[],
     description="Chapter 10, the last great boss. A Warden from the deep dark, nine blocks tall and eyeless. Its ribcage of souls lights up when it hears you, and its sonic boom goes through walls."),
  "the_unmaker": dict(name="<gradient:#2a0845:#ff4fd8:#2a0845><bold>THE UNMAKER</bold></gradient>", title="Heart of the Void",
     entity="IRON_GOLEM", health=6000, damage=17, armor=16, bar="PINK", theme="void", movement="hover", fly_height=4,
     minion="ENDERMAN", minions=3, abilities=["quake", "sonic_boom", "meteor", "orbs", "pull", "darkness", "lightning", "blink", "charge", "minions"], ability_seconds=4,
     phases=[0.8, 0.6, 0.4, 0.2], money=250000, top_money=250000, items=["NETHERITE_INGOT 2", "DIAMOND_BLOCK 2", "ENCHANTED_GOLDEN_APPLE 1"], top_items=["NETHER_STAR 1"],
     description="The finale. Wakes once the Withered Tyrant, the Ender Wyrm and The Listener Below have all been beaten. A four-armed titan of obsidian around a burning void heart, ten blocks tall, with one great eye and a crown of orbiting shards. Smashes with both fists, sweeps a blade of the void and casts from an orb."),
}

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
#             blood, toxic, void, witch, sand, bone, sculk, wither, dragon, holiday, candy, pumpkin, feather, iron.
# abilities:  picked at random every ability-seconds (faster in later phases):
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
    w(f"    movement: {d.get('movement', 'walk')}")
    if d.get("fly_height"): w(f"    fly-height: {d['fly_height']}")
    w(f"    phases: [{', '.join(str(p) for p in d.get('phases', [0.5]))}]")
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

for id, b in src.items():
    theme, movement, extra, desc = OLD[id]
    ab = list(dict.fromkeys(b.get("abilities", []) + extra))
    if id == "clucksworth": ab = [a for a in ab if a != "volley"] + []
    r = b.get("rewards", {})
    d = dict(name=b["name"], title=b.get("title", ""), entity=b["entity"], health=b.get("health", 800), scale=b.get("scale"),
             damage=b.get("damage", 8), speed=b.get("speed"), armor=b.get("armor", 0), bar=b.get("bar", "RED"), theme=theme,
             movement=movement, fly_height=3 if movement == "hover" else None, season=b.get("season"), phases=b.get("phases", [0.66, 0.33]),
             equipment=b.get("equipment"), minion=MINION_SWAP.get(id, b.get("minion")), minions=b.get("minions", 3), ability_seconds=b.get("ability-seconds", 7),
             abilities=ab, money=r.get("money", 0), top_money=r.get("top-money", 0), items=r.get("items", []), top_items=r.get("top-items", []),
             commands=r.get("commands", []), top_commands=r.get("top-commands", []), description=desc)
    emit(id, d)
w("")
w("  # ------------------------------------------------------------------ CBosses legends")
for id in ("withered_tyrant", "ender_wyrm", "killer_claus", "brain_freeze"): emit(id, NEW[id])
w("")
w("  # ------------------------------------------------------------------ the finale (after the three legends)")
emit("the_unmaker", NEW["the_unmaker"])
w("")
w("  # ------------------------------------------------------------------ chapter bosses (one after every CQuests chapter)")
for id in ("brakka", "gate_shade", "oakheart", "keywarden", "hollow_king", "iron_tusk", "captain_brine", "ember_queen", "choirmaster", "the_listener"):
    emit(id, NEW[id])
dest = os.path.join(os.path.dirname(__file__), "../src/main/resources/bosses.yml")
open(dest, "w").write("\n".join(out) + "\n")
# check it parses and every ability is known
ALL = set("lightning shockwave minions fire_ring pull leap poison blink frost volley darkness levitate heal quake detonate roar charge slam meteor sonic_boom skulls breath spikes orbs gifts sprinkles dive eggs".split())
data = yaml.safe_load(open(dest))["bosses"]
for id, b in data.items():
    bad = set(b["abilities"]) - ALL
    assert not bad, (id, bad)
print(len(data), "bosses written to", dest)
