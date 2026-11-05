"""Which bosses ship, by group. Every model module registers its bosses; a later module's version of an id
replaces an earlier one, and only the ids listed here are built."""
import importlib
import models

MODULES = ["v2_general", "v2_seasonal", "v2_chapters", "v2_legends", "v3_general", "v3_mythic", "v3_seasonal",
           "v4_normal", "v4_chapters", "v4_seasonal"]

NORMAL = ["grand_augur", "king_gloop", "grave_marshal", "mayor_grumble", "old_ironroot", "siegebreaker", "old_tusker",
          "elder_eye", "queen_bee", "pillager_captain", "pale_watcher", "weeping_ghast", "elder_sniffer", "cinderheart",
          "shulker_matriarch", "frostmaw", "bogmaw", "ramthunder", "gale_sovereign", "bogged_hunter"]
MYTHIC = ["the_listener", "withered_tyrant", "ender_wyrm"]
FINALE = ["the_unmaker"]
SEASONAL = {"winter": ["killer_claus", "frostbottom", "old_man_winter"], "summer": ["sunscorch", "admiral_pinchworth", "brain_freeze"],
            "spring": ["clucksworth", "killer_bunny", "cocoa_colossus"], "halloween": ["great_gourd", "headless_horseman", "hexmother"]}
CHAPTERS = ["brakka", "nightwing", "oakheart", "vault_mimic", "crypt_knight", "iron_tusk", "deep_mother", "ember_knight",
            "bellwarden", "the_shrieker"]
ALL = NORMAL + MYTHIC + FINALE + [b for s in SEASONAL.values() for b in s] + CHAPTERS


def builders():
    """id -> the function that builds it (the last module to define an id wins)."""
    for mod in MODULES:
        importlib.import_module(mod)
    by_id = {}
    for fn in models.MODELS:
        by_id[fn.__name__] = fn
    missing = [i for i in ALL if i not in by_id]
    if missing:
        raise SystemExit("no model for " + ", ".join(missing))
    return {i: by_id[i] for i in ALL}


def recipes():
    import v2_recipes, v4_recipes
    spawn, death = dict(v2_recipes.SPAWN), dict(v2_recipes.DEATH)
    spawn.update(v4_recipes.SPAWN)
    death.update(v4_recipes.DEATH)
    return spawn, death
