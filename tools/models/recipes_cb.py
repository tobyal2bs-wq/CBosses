"""Entrances and deaths for the CBosses bosses, plus the pass that makes every older death hit harder
(a white flash and a shudder first, the last pieces shatter into flying shards instead of shrinking)."""
from recipes import S, fx, SPAWN, DEATH, SPAWN_TEXT, DEATH_TEXT

NEW_SPAWN = {
 # three skulls light up one at a time in black smoke, then the spine and ribs knit together between them
 "withered_tyrant": [S("shrink", 0, s=0), fx(1, "LARGE_SMOKE", 80, "ENTITY_WITHER_AMBIENT", 0.5, y=0.6, spread=2.5, ring=4),
     S("pose", 6, 6, only="skullL"), fx(6, "SOUL", 30, "ENTITY_WITHER_SKELETON_AMBIENT", 0.5, y=0.8), S("flash", 6, 4, only="skullL"),
     S("pose", 16, 6, only="skullR"), fx(16, "SOUL", 30, "ENTITY_WITHER_SKELETON_AMBIENT", 0.6, y=0.8), S("flash", 16, 4, only="skullR"),
     S("pose", 26, 6, only="head"), fx(26, "SOUL", 40, "ENTITY_WITHER_SKELETON_AMBIENT", 0.4, y=0.9), S("flash", 26, 5, only="head"),
     S("pose", 34, 22, order="up", stagger=18), fx(36, "SMOKE", 60, "BLOCK_BASALT_PLACE", 0.5, y=0.4, spread=1.5),
     S("shake", 56, 16), fx(58, "EXPLOSION_EMITTER", 2, "ENTITY_WITHER_SPAWN", 0.8, y=0.5), S("anim", 60, 32, name="scream")],
 # dives in from high above and behind, pulls up, flares the wings and roars
 "ender_wyrm": [S("move", 0, v=[0, 34, -40]), S("tilt", 0, deg=40, axis="x") if False else S("spin", 0, deg=0),
     fx(1, "END_ROD", 60, "ENTITY_ENDER_DRAGON_FLAP", 0.6, y=3, spread=4), S("pose", 2, 34),
     fx(14, "DRAGON_BREATH", 40, "ENTITY_ENDER_DRAGON_FLAP", 0.7, y=1.5, spread=3), fx(26, "DRAGON_BREATH", 60, "ENTITY_ENDER_DRAGON_FLAP", 0.8, y=1, spread=3),
     fx(36, "REVERSE_PORTAL", 120, "ENTITY_ENDER_DRAGON_GROWL", 0.7, y=0, spread=5, ring=6), S("shake", 36, 10),
     S("anim", 38, 36, name="roar"), fx(44, "END_ROD", 80, "ENTITY_ENDER_DRAGON_AMBIENT", 0.6, y=1.2, spread=3)],
 # a sack drops down out of the sky, rustles, ticks... and Claus climbs out of it, piece by piece, laughing
 "killer_claus": [S("shrink", 0, s=0, only="!sack"), S("move", 0, v=[0, 22, 0], only="sack"), fx(1, "SNOWFLAKE", 80, "BLOCK_BELL_USE", 0.5, y=3, spread=3),
     S("move", 2, 10, v=[0, -22, 0], only="sack"), fx(12, "BLOCK", 60, "BLOCK_SNOW_FALL", 0.6, y=0, spread=2, block="SNOW_BLOCK"),
     S("shake", 16, 12, only="sack", amp=0.12), fx(16, sound="BLOCK_NOTE_BLOCK_HAT", pitch=1.6), fx(20, sound="BLOCK_NOTE_BLOCK_HAT", pitch=1.6),
     fx(24, sound="ENTITY_TNT_PRIMED", pitch=0.7), S("shake", 28, 12, only="sack", amp=0.2),
     S("flash", 40, 4, block="red_concrete"), S("pose", 40, 4, order="up", stagger=22), fx(40, "FIREWORK", 60, "ENTITY_FIREWORK_ROCKET_BLAST", 0.7, y=0.6),
     fx(50, sound="ENTITY_WITCH_CELEBRATE", pitch=0.5), fx(58, "SNOWFLAKE", 60, "BLOCK_BELL_RESONATE", 0.6, y=1), S("anim", 64, 28, name="roar"),
     fx(66, sound="ENTITY_EVOKER_CELEBRATE", pitch=0.5)],
 # the cone pokes up out of the ground, then three scoops drop on top one after another and squish into place
 "brain_freeze": [S("shrink", 0, s=0, only="!core"), S("move", 0, vh=[0, -1, 0], only="core"), fx(1, "ITEM_SNOWBALL", 40, "BLOCK_POWDER_SNOW_STEP", 0.6, y=0, spread=2),
     S("move", 2, 14, vh=[0, 1, 0], only="core"), S("pose", 16, 2, only="core"), fx(10, "SNOWFLAKE", 30, "BLOCK_SNOW_BREAK", 0.6, y=0.3),
     S("pose", 20, 1, only="head"), S("move", 20, 1, v=[0, 16, 0], only="head"), S("move", 21, 10, v=[0, -16, 0], only="head"),
     S("scale", 31, 3, s=[1.3, 0.7, 1.3], only="head"), S("pose", 34, 5, only="head"), fx(31, "ITEM_SLIME", 40, "BLOCK_HONEY_BLOCK_PLACE", 0.6, y=0.8),
     fx(31, sound="ENTITY_SLIME_SQUISH", pitch=0.7), S("shake", 32, 8, amp=0.1),
     S("pose", 42, 8, only="ring"), S("pose", 42, 8, only="arm"), S("pose", 42, 8, only="spoon"), S("pose", 42, 8, only="fore"),
     fx(44, "SNOWFLAKE", 60, "ENTITY_PLAYER_HURT_FREEZE", 1.2, y=1, spread=2), S("pose", 48, 4), S("anim", 52, 26, name="spin"), fx(52, sound="ENTITY_WANDERING_TRADER_YES", pitch=0.6)],
 # walks out of a wall of fire, black with soot; the colours come back as the flames die down
 "brakka": [S("swap", 0, block="black_concrete"), S("move", 0, v=[0, 0, -7]), fx(1, "FLAME", 80, "ITEM_FIRECHARGE_USE", 0.5, y=0.4, spread=2.5, ring=3),
     S("pose", 2, 26), fx(8, "LAVA", 20, "BLOCK_FIRE_AMBIENT", 0.8, y=0.4, spread=1.5), fx(18, "FLAME", 40, "ENTITY_BLAZE_BURN", 0.6, y=0.5),
     S("swap", 28, block="", order="up", stagger=20), fx(30, "SMOKE", 60, "BLOCK_FIRE_EXTINGUISH", 0.6, y=0.6),
     S("anim", 48, 28, name="roar"), fx(50, sound="ENTITY_VINDICATOR_CELEBRATE", pitch=0.6), S("shake", 50, 10)],
 # a thin shadow flat on the ground stands up, the chains pull taut, the eyes open last
 "gate_shade": [S("scale", 0, s=[1, 0.02, 1]), S("swap", 0, block="black_concrete"), fx(1, "SQUID_INK", 60, "AMBIENT_CAVE", 0.6, y=0, spread=2.5, ring=3),
     S("pose", 8, 24), fx(12, "SOUL", 40, "ENTITY_WARDEN_AMBIENT", 1.4, y=0.4), S("swap", 32, block="", order="up", stagger=12),
     fx(34, sound="BLOCK_CHAIN_PLACE", pitch=0.5), fx(38, sound="BLOCK_CHAIN_PLACE", pitch=0.7), S("shake", 36, 8, only="core"),
     S("flash", 46, 5, only="lit", block="light_blue_concrete"), fx(46, "SCULK_SOUL", 30, "ENTITY_VEX_CHARGE", 0.5, y=0.9), S("anim", 50, 28, name="raise")],
 # grows out of a sapling: small, then bigger in jumps with leaves bursting each time, armour bark sets last
 "oakheart": [S("scale", 0, s=[0.12, 0.12, 0.12]), S("swap", 0, block="oak_leaves", only="!lit"), fx(1, "HAPPY_VILLAGER", 30, "BLOCK_GRASS_PLACE", 0.6, y=0),
     S("scale", 6, 6, s=[3.33, 3.33, 3.33]), fx(8, "CHERRY_LEAVES", 40, "BLOCK_AZALEA_LEAVES_PLACE", 0.6, y=0.3), S("shake", 12, 4),
     S("scale", 18, 6, s=[1.875, 1.875, 1.875]), fx(20, "CHERRY_LEAVES", 60, "BLOCK_AZALEA_LEAVES_PLACE", 0.5, y=0.5), S("shake", 24, 4),
     S("pose", 30, 8), fx(32, "COMPOSTER", 60, "BLOCK_ROOTED_DIRT_PLACE", 0.5, y=0.2, spread=2.5, ring=3),
     S("swap", 40, block="", order="down", stagger=16), fx(42, sound="BLOCK_WOOD_PLACE", pitch=0.6), S("flash", 56, 4, only="lit", block="yellow_concrete"),
     S("anim", 58, 26, name="roar"), fx(60, sound="ENTITY_IRON_GOLEM_REPAIR", pitch=0.7)],
 # five glowing keyholes fly in from all around first, then the lock body unfolds around them and the shackle snaps shut
 "keywarden": [S("shrink", 0, s=0, only="unlit"), S("burst", 0, power=9, up=4, tilt=360, rand=3, only="lit"),
     fx(1, "WAX_ON", 40, "BLOCK_IRON_TRAPDOOR_OPEN", 0.5, y=0.6, spread=4), S("pose", 4, 16, order="random", stagger=20, only="lit"),
     fx(20, sound="BLOCK_TRIAL_SPAWNER_OPEN" if False else "BLOCK_VAULT_OPEN_SHUTTER", pitch=0.8), S("pose", 26, 6, order="out", stagger=22, only="unlit"),
     fx(26, "ELECTRIC_SPARK", 60, "BLOCK_IRON_DOOR_CLOSE", 0.6, y=0.6), fx(48, sound="BLOCK_ANVIL_PLACE", pitch=0.6), S("shake", 48, 8),
     S("flash", 48, 4, block="yellow_concrete"), S("anim", 54, 28, name="stomp")],
 # BIG: the ground cracks for a long time, then the king rises slowly out of his tomb, armour from the boots up,
 # the soul crown lights last and the sky goes dark with lightning
 "hollow_king": [S("move", 0, vh=[0, -1.08, 0]), fx(1, "SOUL", 80, "ENTITY_WARDEN_DIG", 0.5, y=0, spread=3, ring=5),
     fx(10, "BLOCK", 80, "BLOCK_DEEPSLATE_BREAK", 0.5, y=0, spread=3.5, block="DEEPSLATE"), fx(20, sound="ENTITY_ELDER_GUARDIAN_CURSE", pitch=0.5),
     S("move", 24, 50, vh=[0, 1.08, 0]), S("shake", 24, 50, amp=0.05), S("pose", 24, 50),
     fx(30, "SOUL_FIRE_FLAME", 60, "BLOCK_SCULK_SHRIEKER_SHRIEK", 0.5, y=0.3, spread=2), fx(50, "SOUL", 60, "ENTITY_WITHER_AMBIENT", 0.5, y=0.6, spread=2),
     S("swap", 24, block="soul_soil", order="down", stagger=1), S("swap", 40, block="", order="up", stagger=34),
     fx(76, "EXPLOSION_EMITTER", 3, "ENTITY_LIGHTNING_BOLT_THUNDER", 0.6, y=0.5, lightning=True), S("flash", 76, 6),
     fx(78, "SOUL_FIRE_FLAME", 120, "ENTITY_WITHER_SPAWN", 0.6, y=1, spread=1.2), S("anim", 80, 34, name="roar"), fx(86, "SOUL", 80, "ENTITY_RAVAGER_ROAR", 0.4, y=0.6, spread=4, ring=7)],
 # charges in from far away, skids to a stop in a cloud of dirt, the furnace roars to life
 "iron_tusk": [S("move", 0, v=[0, 0, -26]), fx(1, sound="ENTITY_HOGLIN_ANGRY", pitch=0.5), S("pose", 2, 14),
     fx(6, "BLOCK", 30, "ENTITY_RAVAGER_STEP", 0.6, y=0, spread=1.5, block="DIRT"), fx(12, "BLOCK", 40, "ENTITY_RAVAGER_STEP", 0.6, y=0, spread=2, block="DIRT"),
     S("tilt", 16, 4, deg=-12) if False else S("shake", 16, 8, amp=0.12), fx(16, "CAMPFIRE_COSY_SMOKE", 30, "BLOCK_GRAVEL_BREAK", 0.5, y=0, spread=2.5),
     S("flash", 24, 4, only="lit", block="orange_concrete"), fx(24, "FLAME", 50, "BLOCK_BLASTFURNACE_FIRE_CRACKLE", 0.6, y=0.4), S("anim", 26, 30, name="howl"),
     fx(28, sound="ENTITY_HOGLIN_ANGRY", pitch=0.4)],
 # rises out of a whirl of water, dripping, the lantern eyes open
 "captain_brine": [S("move", 0, vh=[0, -1.05, 0]), S("swap", 0, block="prismarine"), fx(1, "SPLASH", 120, "ENTITY_GENERIC_SPLASH", 0.6, y=0, spread=3, ring=4),
     S("move", 4, 32, vh=[0, 1.05, 0]), S("spin", 4, 32, deg=180), S("pose", 36, 4), fx(10, "BUBBLE_POP", 60, "BLOCK_BUBBLE_COLUMN_UPWARDS_AMBIENT", 0.6, y=0.3, spread=2),
     S("swap", 30, block="", order="up", stagger=18), fx(36, "DRIPPING_WATER", 60, "ENTITY_DROWNED_AMBIENT", 0.5, y=0.8, spread=1),
     S("flash", 46, 4, only="lit", block="sea_lantern"), S("anim", 48, 28, name="roar"), fx(50, sound="ENTITY_ELDER_GUARDIAN_AMBIENT", pitch=0.6)],
 # a pillar of lava erupts and she steps out of it as it falls back, the fan of fire opening behind her
 "ember_queen": [S("scale", 0, s=[0.25, 1.5, 0.25]), S("swap", 0, block="magma_block"), S("light", 0, on=True),
     fx(1, "LAVA", 40, "ENTITY_GENERIC_EXPLODE", 0.5, y=0, spread=1.5), fx(2, "FLAME", 80, "ITEM_FIRECHARGE_USE", 0.6, y=0.5, spread=0.6),
     S("pose", 10, 16), S("swap", 22, block="", order="up", stagger=16), S("light", 40, on=False),
     S("scale", 26, 1, s=[0.05, 0.05, 0.05], only="fan"), S("pose", 30, 10, only="fan"), fx(30, "FLAME", 60, "ENTITY_BLAZE_SHOOT", 0.6, y=0.8, spread=1.5),
     S("flash", 40, 4, block="orange_concrete"), S("anim", 44, 30, name="raise"), fx(46, sound="ENTITY_BLAZE_AMBIENT", pitch=0.5)],
 # the skull choir appears first and sings a rising chord; the conductor is put together note by note
 "choirmaster": [S("shrink", 0, s=0, only="!ring"), fx(1, "NOTE", 20, "BLOCK_NOTE_BLOCK_CHIME", 0.5, y=1, spread=2),
     fx(8, "NOTE", 20, "BLOCK_NOTE_BLOCK_CHIME", 0.6, y=1, spread=2), fx(16, "NOTE", 20, "BLOCK_NOTE_BLOCK_CHIME", 0.75, y=1, spread=2),
     fx(24, "NOTE", 20, "BLOCK_NOTE_BLOCK_CHIME", 0.9, y=1, spread=2), S("pose", 8, 3, order="up", stagger=30, only="!ring"),
     fx(32, "NOTE", 40, "BLOCK_NOTE_BLOCK_BELL", 1.0, y=1, spread=2), fx(38, sound="BLOCK_NOTE_BLOCK_BELL", pitch=1.2),
     S("flash", 40, 4, only="lit", block="yellow_concrete"), fx(42, "SOUL", 60, "ENTITY_SKELETON_AMBIENT", 0.5, y=0.6), S("anim", 44, 28, name="raise")],
 # BIG: the Warden digs its way up. Long rumble, sculk spreads, it claws out of the ground, sniffs, then roars
 "the_listener": [S("move", 0, vh=[0, -1.1, 0]), fx(1, "SCULK_CHARGE_POP", 60, "ENTITY_WARDEN_HEARTBEAT", 0.8, y=0, spread=3, ring=5),
     fx(12, sound="ENTITY_WARDEN_HEARTBEAT", pitch=0.8), fx(22, sound="ENTITY_WARDEN_HEARTBEAT", pitch=0.9),
     fx(24, "BLOCK", 120, "ENTITY_WARDEN_EMERGE", 0.8, y=0, spread=3.5, block="SCULK"), S("shake", 24, 60, amp=0.05),
     S("move", 26, 56, vh=[0, 1.1, 0]), S("pose", 26, 56), S("swap", 26, block="sculk", order="down", stagger=1), S("swap", 46, block="", order="up", stagger=34),
     fx(40, "SCULK_SOUL", 40, "BLOCK_SCULK_SPREAD", 0.6, y=0.3, spread=2), fx(60, "SCULK_SOUL", 60, "BLOCK_SCULK_CATALYST_BLOOM", 0.6, y=0.5, spread=2),
     fx(84, sound="ENTITY_WARDEN_SNIFF", pitch=0.8), S("flash", 92, 5, only="lit", block="light_blue_concrete"),
     S("anim", 94, 34, name="roar"), fx(96, "SONIC_BOOM", 1, "ENTITY_WARDEN_ROAR", 0.8, y=0.7), fx(98, "SCULK_SOUL", 80, None, 1, y=0.6, spread=4, ring=7)],
 # clucksworth: hatches out of a real giant egg. It wobbles, cracks, and the shell shatters off him
 "clucksworth": [S("shrink", 0, s=0, only="!shell"), fx(1, "CLOUD", 30, "ENTITY_CHICKEN_EGG", 0.5, y=0.2),
     S("shake", 8, 6, only="shell", amp=0.18), fx(10, sound="ENTITY_TURTLE_EGG_CRACK", pitch=0.7),
     S("shake", 22, 6, only="shell", amp=0.24), fx(24, sound="ENTITY_TURTLE_EGG_CRACK", pitch=0.6), S("swap", 24, block="white_concrete_powder", only="shell", order="random", stagger=6),
     S("shake", 34, 8, only="shell", amp=0.3), fx(36, sound="ENTITY_TURTLE_EGG_CRACK", pitch=0.5),
     S("flash", 44, 3, only="shell"), S("shatter", 46, 10, only="shell", order="out", stagger=4, pieces=3, power=4, up=3),
     fx(46, "POOF", 80, "ENTITY_TURTLE_EGG_HATCH", 0.6, y=0.5, spread=1.6), S("pose", 46, 6, only="!shell"),
     S("scale", 46, 1, s=[0.7, 0.7, 0.7], only="!shell"), S("pose", 47, 6, only="!shell"),
     S("anim", 54, 30, name="roar"), fx(56, "CLOUD", 40, "ENTITY_CHICKEN_AMBIENT", 0.5, y=0.8), fx(66, sound="ENTITY_CHICKEN_AMBIENT", pitch=0.6)],
}

NEW_DEATH = {
 "withered_tyrant": [S("anim", 0, 26, name="die_drop"), fx(0, "SOUL", 60, "ENTITY_WITHER_HURT", 0.5),
     S("fling", 16, 30, only="skullL", power=5, up=4, tilt=200), S("fling", 22, 30, only="skullR", power=5, up=4, tilt=200), fx(16, sound="ENTITY_WITHER_SHOOT", pitch=0.6),
     fx(30, "EXPLOSION_EMITTER", 2, "ENTITY_WITHER_DEATH", 0.7), S("shatter", 32, 12, only="head", pieces=3, power=3, up=3),
     S("shatter", 40, 12, order="random", stagger=20, pieces=2, power=2.5, up=2), fx(44, "LARGE_SMOKE", 120, "BLOCK_BASALT_BREAK", 0.5, y=0.3, spread=3)],
 "ender_wyrm": [S("anim", 0, 36, name="die_fall"), fx(0, "DRAGON_BREATH", 80, "ENTITY_ENDER_DRAGON_HURT", 0.5, spread=3), S("light", 10, on=True),
     fx(20, "END_ROD", 120, "ENTITY_ENDER_DRAGON_DEATH", 0.8, y=1, spread=4), S("swap", 20, block="purpur_block", order="out", stagger=30),
     S("move", 30, 30, v=[0, 3, 0], order="random", stagger=10), fx(40, "REVERSE_PORTAL", 200, "BLOCK_END_PORTAL_SPAWN", 0.7, y=1, spread=5),
     S("flash", 58, 5, block="magenta_concrete"), S("shatter", 62, 14, order="out", stagger=18, pieces=2, power=4, up=3), fx(62, "FLASH", 3, "ENTITY_GENERIC_EXPLODE", 0.7, y=1)],
 "killer_claus": [S("anim", 0, 24, name="die_back"), fx(0, sound="ENTITY_EVOKER_DEATH", pitch=0.5), fx(6, sound="ENTITY_TNT_PRIMED", pitch=0.8),
     S("shake", 6, 16, only="sack", amp=0.2), S("shatter", 22, 10, only="sack", pieces=3, power=5, up=4), fx(22, "EXPLOSION_EMITTER", 2, "ENTITY_GENERIC_EXPLODE", 0.9, y=0.4),
     fx(22, "FIREWORK", 100, "ENTITY_FIREWORK_ROCKET_TWINKLE", 0.8, y=0.6, spread=2), S("fling", 26, 30, only="scythe", power=4, up=5, tilt=400),
     S("swap", 30, block="coal_block", order="up", stagger=20), fx(36, "SNOWFLAKE", 100, "BLOCK_BELL_USE", 0.4, y=0.6, spread=2),
     S("drop", 46, 14, tilt=90, rand=1.5, order="down", stagger=16), S("shatter", 66, 10, order="random", stagger=14, pieces=2, power=1.5, up=1.5)],
 "brain_freeze": [S("anim", 0, 22, name="die_drop"), fx(0, sound="ENTITY_PLAYER_HURT_FREEZE", pitch=0.6),
     S("scale", 16, 30, s=[1.5, 0.25, 1.5], order="down", stagger=20), fx(20, "ITEM_SLIME", 60, "BLOCK_HONEY_BLOCK_SLIDE", 0.5, y=0.2, spread=2),
     S("swap", 20, block="pink_concrete_powder", only="pink_concrete"), fx(30, "FALLING_WATER", 80, "BLOCK_POWDER_SNOW_BREAK", 0.6, y=0.2, spread=2.5),
     S("fling", 30, 28, only="red_concrete", power=3, up=6, tilt=200), fx(30, sound="ENTITY_ITEM_PICKUP", pitch=0.5),
     S("shatter", 50, 12, only="core", pieces=2, power=2, up=1.5, order="random", stagger=14), S("shrink", 60, 14, s=0, order="random", stagger=10)],
 "brakka": [S("anim", 0, 26, name="die_front"), fx(0, sound="ENTITY_VINDICATOR_DEATH", pitch=0.6), S("fling", 10, 26, only="cleaver", power=4, up=3, tilt=500),
     S("fling", 10, 26, only="torch", power=3, up=4, tilt=300), fx(14, "FLAME", 80, "ITEM_FIRECHARGE_USE", 0.6, y=0.3, spread=2),
     S("swap", 26, block="black_concrete", order="up", stagger=16), fx(30, "SMOKE", 100, "BLOCK_FIRE_EXTINGUISH", 0.5, y=0.3, spread=2),
     S("shatter", 46, 12, order="random", stagger=16, pieces=2, power=1.2, up=1.5)],
 "gate_shade": [S("anim", 0, 22, name="die_drop"), fx(0, "SOUL", 60, "ENTITY_VEX_DEATH", 0.5), S("fling", 10, 28, only="lantern", power=2, up=4, tilt=200),
     S("swap", 16, block="black_stained_glass", order="down", stagger=16), S("scale", 30, 20, s=[1.4, 0.02, 1.4], order="down", stagger=10),
     fx(30, "SQUID_INK", 100, "BLOCK_CHAIN_BREAK", 0.5, y=0, spread=2.5), fx(46, "SCULK_SOUL", 40, "ENTITY_WARDEN_DEATH", 1.6, y=0.1), S("shrink", 52, 8, s=0)],
 "oakheart": [S("anim", 0, 28, name="die_kneel"), fx(0, sound="BLOCK_WOOD_BREAK", pitch=0.5), S("light", 8, on=False),
     S("swap", 18, block="dead_bush" if False else "brown_terracotta", only="leaves"), fx(18, "CHERRY_LEAVES", 120, "BLOCK_AZALEA_LEAVES_BREAK", 0.5, y=0.6, spread=2.5),
     S("fling", 24, 26, only="sword", power=3, up=3, tilt=200), S("fling", 24, 26, only="shield", power=3, up=2, tilt=160),
     S("drop", 34, 14, tilt=60, rand=1.5, order="down", stagger=14), fx(40, "COMPOSTER", 80, "BLOCK_ROOTED_DIRT_BREAK", 0.5, y=0, spread=2.5),
     S("shatter", 60, 12, order="random", stagger=14, pieces=2, power=1, up=1.2)],
 "keywarden": [S("anim", 0, 20, name="die_back"), fx(0, sound="BLOCK_IRON_DOOR_OPEN", pitch=0.5), S("shake", 8, 14, amp=0.12),
     S("burst", 20, 18, power=7, up=5, tilt=360, rand=2, only="lit"), fx(20, "WAX_OFF", 60, "BLOCK_VAULT_EJECT_ITEM" if False else "BLOCK_CHAIN_BREAK", 0.6, y=0.6, spread=2),
     S("fling", 22, 30, only="key", power=3, up=4, tilt=250), S("drop", 26, 14, tilt=110, rand=2, only="unlit", order="out", stagger=14),
     fx(32, sound="BLOCK_ANVIL_LAND", pitch=0.6), S("shatter", 56, 12, order="random", stagger=12, pieces=2, power=1.5, up=1.5)],
 "hollow_king": [S("anim", 0, 32, name="die_kneel"), fx(0, "SOUL", 80, "ENTITY_WITHER_DEATH", 0.5, spread=2), S("shake", 0, 30, amp=0.06),
     fx(14, sound="ENTITY_LIGHTNING_BOLT_THUNDER", pitch=0.6, lightning=True), S("fling", 20, 34, only="blade", power=2, up=2, tilt=120),
     S("move", 30, 30, v=[0, 6, 0], only="lit"), fx(36, "SOUL_FIRE_FLAME", 120, "BLOCK_SOUL_SAND_BREAK", 0.5, y=1, spread=1),
     S("swap", 30, block="rust" if False else "oxidized_copper", only="netherite_block", order="up", stagger=20),
     S("drop", 44, 16, tilt=100, rand=1.6, only="!lit", order="down", stagger=24), S("flash", 60, 6, only="lit", block="light_blue_concrete"),
     S("shatter", 66, 10, only="lit", pieces=4, power=6, up=5), fx(66, "EXPLOSION_EMITTER", 3, "ENTITY_GENERIC_EXPLODE", 0.6, y=1.2),
     fx(70, "SOUL", 200, "ENTITY_ALLAY_DEATH", 0.5, y=1.2, spread=3), S("shatter", 90, 12, order="random", stagger=20, pieces=2, power=1.5, up=1.5)],
 "iron_tusk": [S("anim", 0, 30, name="die_side"), fx(0, sound="ENTITY_HOGLIN_DEATH", pitch=0.5), S("light", 16, on=False),
     fx(20, "LARGE_SMOKE", 60, "BLOCK_FIRE_EXTINGUISH", 0.5, y=0.4, spread=1.5), S("burst", 30, 18, power=5, up=3, tilt=240, rand=1.5, only="iron_block"),
     fx(30, sound="BLOCK_ANVIL_LAND", pitch=0.5), fx(32, "EXPLOSION", 4, "ENTITY_GENERIC_EXPLODE", 0.8, y=0.4),
     S("shatter", 56, 12, order="random", stagger=14, pieces=2, power=1.2, up=1.5)],
 "captain_brine": [S("anim", 0, 26, name="die_back"), fx(0, sound="ENTITY_DROWNED_DEATH", pitch=0.5), S("fling", 12, 30, only="anchor", power=2, up=2, tilt=100),
     S("swap", 20, block="prismarine", order="down", stagger=20), fx(24, "BUBBLE_COLUMN_UP", 100, "ENTITY_GENERIC_SPLASH", 0.5, y=0, spread=2.5),
     S("move", 40, 30, v=[0, -4, 0]), fx(46, "SPLASH", 140, "BLOCK_BUBBLE_COLUMN_WHIRLPOOL_INSIDE", 0.6, y=0, spread=3), S("shrink", 66, 6, s=0)],
 "ember_queen": [S("anim", 0, 22, name="die_drop"), fx(0, sound="ENTITY_BLAZE_DEATH", pitch=0.5), S("light", 0, on=True),
     S("swap", 10, block="magma_block", order="up", stagger=20), fx(14, "LAVA", 60, "BLOCK_LAVA_POP", 0.6, y=0.4, spread=2),
     S("swap", 30, block="obsidian", order="up", stagger=20), S("light", 40, on=False), fx(40, "LARGE_SMOKE", 100, "BLOCK_LAVA_EXTINGUISH", 0.5, y=0.6, spread=2),
     S("flash", 54, 4, block="orange_concrete"), S("shatter", 56, 12, order="out", stagger=16, pieces=2, power=3, up=3), fx(56, "FLAME", 120, "ENTITY_GENERIC_EXPLODE", 0.9, y=0.6, spread=2)],
 "choirmaster": [S("anim", 0, 22, name="die_drop"), fx(0, "NOTE", 20, "BLOCK_NOTE_BLOCK_CHIME", 1.4), fx(6, sound="BLOCK_NOTE_BLOCK_CHIME", pitch=1.0),
     fx(12, sound="BLOCK_NOTE_BLOCK_CHIME", pitch=0.7), fx(18, sound="BLOCK_NOTE_BLOCK_CHIME", pitch=0.5),
     S("fling", 20, 30, only="ring1", power=4, up=3, tilt=300), S("fling", 20, 30, only="baton", power=2, up=3, tilt=300),
     S("drop", 26, 14, tilt=90, rand=1.5, only="!ring", order="down", stagger=18), fx(30, "SOUL", 60, "ENTITY_SKELETON_DEATH", 0.5, y=0.3),
     S("shatter", 56, 12, order="random", stagger=14, pieces=2, power=1, up=1.2)],
 "the_listener": [S("anim", 0, 34, name="die_kneel"), fx(0, sound="ENTITY_WARDEN_DEATH", pitch=0.7), S("shake", 0, 40, amp=0.07),
     S("flash", 10, 4, only="lit", block="light_blue_concrete"), fx(10, "SCULK_SOUL", 60, "ENTITY_WARDEN_HEARTBEAT", 0.6, y=0.6),
     S("flash", 22, 4, only="lit", block="light_blue_concrete"), fx(22, "SCULK_SOUL", 60, "ENTITY_WARDEN_HEARTBEAT", 0.5, y=0.6),
     S("swap", 30, block="sculk", order="down", stagger=24), fx(36, "SCULK_CHARGE_POP", 200, "BLOCK_SCULK_SPREAD", 0.5, y=0.4, spread=3),
     S("move", 40, 24, v=[0, 5, 0], only="lit", order="random", stagger=10), fx(50, "SONIC_BOOM", 1, "ENTITY_WARDEN_SONIC_BOOM", 0.6, y=1.2),
     S("shatter", 58, 10, only="lit", pieces=3, power=5, up=4), S("move", 60, 40, v=[0, -4, 0], only="!lit"),
     fx(70, "SCULK_SOUL", 200, "BLOCK_SCULK_CATALYST_BLOOM", 0.5, y=0.3, spread=4, ring=6), S("shrink", 96, 10, s=0, order="random", stagger=10)],
}

NEW_SPAWN_TEXT = {
 "withered_tyrant": "Three skulls light up one by one in black smoke, then the spine and ribs knit together between them.",
 "ender_wyrm": "Dives in from high above, pulls up, flares its wings and roars.",
 "killer_claus": "A sack falls out of the sky, rustles and ticks... and Claus climbs out of it, laughing.",
 "brain_freeze": "A waffle cone pokes out of the ground, then the scoops drop on top and squish into place.",
 "brakka": "Walks out of a wall of fire black with soot; the colours come back as the flames die.",
 "gate_shade": "A flat shadow on the ground stands up, the chains pull tight, the eyes open last.",
 "oakheart": "Grows from a sapling in jumps, leaves bursting each time, the bark armour sets last.",
 "keywarden": "Five glowing keyholes fly in first, the lock body unfolds around them and snaps shut.",
 "hollow_king": "The tomb cracks for a long time, the king rises slowly, the soul crown lights in a thunderclap.",
 "iron_tusk": "Charges in from far away and skids to a stop; the furnace roars to life.",
 "captain_brine": "Rises out of a whirl of water turning slowly, dripping, the lantern eyes open.",
 "ember_queen": "A pillar of lava erupts; she steps out as it falls and her fan of fire opens.",
 "choirmaster": "The skull choir sings a rising chord while the conductor is assembled note by note.",
 "the_listener": "A long heartbeat, sculk spreads, the Warden claws its way out of the ground, sniffs and roars.",
 "clucksworth": "A giant egg wobbles, cracks three times and shatters, and an extremely angry chicken hatches out.",
}
NEW_DEATH_TEXT = {
 "withered_tyrant": "The side skulls are flung away, the crowned skull shatters, the body crumbles in smoke.",
 "ender_wyrm": "Falls out of the sky, glows, its scales lift off and burst into shards of the End.",
 "killer_claus": "The sack of presents explodes, the scythe spins away, he turns to coal and falls apart.",
 "brain_freeze": "Melts into a puddle from the top down; the cherry pops off, the cone cracks.",
 "brakka": "Falls on his face, torch and cleaver fly, and he burns down to ash.",
 "gate_shade": "Sinks into a flat shadow on the ground and the lantern rolls away.",
 "oakheart": "Kneels, the leaves wither and fall, sword and shield fly, the bark crumbles.",
 "keywarden": "The keyholes burst out of it, the key spins away, the lock falls open in pieces.",
 "hollow_king": "Kneels in a thunderclap, armour rusts and falls, the soul crown rises and explodes.",
 "iron_tusk": "Rolls onto its side, the furnace goes out, the iron plates burst off.",
 "captain_brine": "Falls back into the water, the anchor drags him down through a whirlpool.",
 "ember_queen": "Turns to magma, then to cooling obsidian, then cracks apart in a burst of flame.",
 "choirmaster": "The choir's chord falls flat, the skulls fly apart and the conductor collapses.",
 "the_listener": "Kneels, its heart of souls flashes twice, the souls escape upward and it sinks back into the sculk.",
}

def enhance(model_id, death):
    """Every death starts with a white flash and a shudder, and its last vanish shatters into shards."""
    steps = [dict(s) for s in death]
    if not any(s["op"] == "flash" for s in steps): steps.insert(0, S("flash", 0, 4))
    if not any(s["op"] == "shake" for s in steps): steps.insert(1, S("shake", 0, 14))
    if not any(s["op"] == "shatter" for s in steps):
        for s in reversed(steps):
            if s["op"] == "shrink" and s.get("s") == 0 and not s.get("only"):
                s["op"] = "shatter"; s.pop("s", None); s["pieces"] = 2; s["power"] = 1.4; s["up"] = 1.4
                break
    return steps

SPAWN.update(NEW_SPAWN)
DEATH.update(NEW_DEATH)
SPAWN_TEXT.update(NEW_SPAWN_TEXT)
DEATH_TEXT.update(NEW_DEATH_TEXT)
for k in list(DEATH): DEATH[k] = enhance(k, DEATH[k])
