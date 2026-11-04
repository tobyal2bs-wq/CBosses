"""Writes README.md from bosses.yml and the images in docs/images. Run from the repo root."""
import re, yaml, os

VIEWER = "https://claude.ai/artifact/NbYXjJCKyRwZ2oTmETby7k"
b = yaml.safe_load(open("src/main/resources/bosses.yml"))["bosses"]

def plain(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()

def nice(s):
    return " ".join(w.capitalize() for w in s.replace("_", " ").split())

def card(i, v):
    img = f"docs/images/{i}.jpg"
    pic = f'<img src="{img}" width="260" alt="{plain(v["name"])}">' if os.path.exists(img) else ""
    abil = ", ".join(nice(a) for a in v.get("abilities", []))
    move = {"walk": "Walks", "hover": "Hovers", "fly": "Flies"}.get(v.get("movement", "walk"), "Walks")
    phases = len(v.get("phases", [])) + 1
    return (f'<td valign="top" width="33%">{pic}<br><b>{plain(v["name"])}</b><br><i>{plain(v.get("title"))}</i><br>'
            f'<sub><code>{i}</code> · {v["health"]} HP · {phases} phases · {move}</sub><br><br>'
            f'{v.get("description","")}<br><br><sub><b>Attacks:</b> {abil}</sub></td>')

def table(items):
    rows = []
    for k in range(0, len(items), 3):
        rows.append("<tr>" + "".join(card(i, v) for i, v in items[k:k+3]) + "</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>\n"

chapter = sorted([(i, v) for i, v in b.items() if v.get("chapter")], key=lambda x: x[1]["chapter"])
legends = [(i, b[i]) for i in ("withered_tyrant", "ender_wyrm") if i in b]
finale = [(i, b[i]) for i in ("the_unmaker",) if i in b]
season = [(i, v) for i, v in b.items() if v.get("season")]
world = [(i, v) for i, v in b.items() if not v.get("chapter") and not v.get("season") and i not in ("withered_tyrant", "ender_wyrm", "the_unmaker")]
counts = sorted(len(m["cubes"]) for m in __import__("json").load(open("src/main/resources/models.json"))["models"].values())

def chapter_rows():
    out = ["| Chapter | Boss | Health | Size |", "|---|---|---|---|"]
    for i, v in chapter:
        big = " **(big)**" if v["chapter"] in (5, 10) else ""
        out.append(f'| {v["chapter"]}{big} | {plain(v["name"])} | {v["health"]} | {v.get("scale", 1)}x |')
    return "\n".join(out)

hero = "docs/images/hero.jpg"
md = f"""# CBosses

<p align="center"><img src="{hero}" alt="CBosses bosses" width="100%"></p>

**CBosses** adds {len(b)} animated block-model bosses to Paper and Folia servers. Every boss is built from {counts[0]} to
{counts[-1]} display blocks, has its own entrance, its own attacks and its own death, and runs on a schedule, on a
season, right after a player finishes a CQuests chapter, or as the finale once the three legends have fallen. It
works on its own and alongside **CQuests**, and it has full **WorldGuard** support.

### [Open the 3D boss viewer]({VIEWER})

Spin every boss around, play its entrance, each attack and its death, right in your browser. A copy of the viewer is
also in this repo at [`docs/viewer.html`](docs/viewer.html) (download and open it locally).

## Highlights

- **Hand-finished models.** Every boss has at least 120 blocks: layered shoulder plates, knee guards, chest badges,
  spines, torn hems, rivets, shading patches and glowing veins on top of its own design. Turn the fine detail down
  with `effects.model-detail` on a busy server.
- **A different entrance for every boss.** Omens, ground cracks and a themed build-up first, then the boss climbs out of the
  earth, falls from the sky, assembles block by block, or, for Clucksworth, hatches out of a giant egg.
- **A different death for every boss.** Each death has a flash, a camera shake and a custom sequence: the veins go dark,
  the armour plates are thrown off, and most end with the model shattering into physics shards.
- **The finale.** Beat the Withered Tyrant, the Ender Wyrm and The Listener Below and **The Unmaker** wakes: a ten block
  tall, four-armed titan with a void heart, one great eye and a crown of orbiting shards.
- **Private chapter bosses.** A chapter boss appears where the player finished their quest and only exists for them:
  nobody else sees it, hears it, bumps into it or gets attacked. No boss ever breaks or places blocks.
- **Every word is yours.** All chat lines, titles, action bars, menus and the defeat broadcast are in `messages.yml`;
  boss names, titles and descriptions are in `bosses.yml`.
- **Attacks you can read.** Every ability has its own wind-up pose, effects and impact: slams, charges, dives, beams, meteors,
  spikes, sonic booms, minion waves and more. Flying bosses swoop and dive instead of jumping.
- **Chapter bosses.** A boss after every CQuests chapter (1 to 10), with two big set pieces after chapters 5 and 10.
- **Legend bosses.** The Withered Tyrant (a three-headed wither), the Ender Wyrm (a flying dragon) and The Listener Below
  (a warden-like horror) are the biggest fights in the plugin.
- **Seasonal bosses.** Halloween, Winterfest, Spring and Summer bosses, including Killer Claus, Brain Freeze and Clucksworth.
- **Built to stay light.** Models only update near players, movement uses client-side interpolation, particles and flying
  blocks have hard caps, and every cost can be tuned in `effects:`. Region schedulers make it Folia-safe.
- **Tested on real servers.** CI starts Paper 1.21.4, Paper 26.x and Folia, spawns every boss, runs each attack and plays
  each death, and fails on any error.

## Chapter bosses

When a player finishes a chapter in CQuests, CBosses counts down on their screen and their chapter boss appears in a
circle at their quest spot. It is their own private fight: other players do not see it, hear it or get hit by it,
and its minions only go after that player. If they lose or leave, it waits for `/cbosses chapter retry`. Pick a different boss per chapter under `chapter-bosses.bosses` in `config.yml`.

{chapter_rows()}

{table(chapter)}

## The finale

When the Withered Tyrant, the Ender Wyrm and The Listener Below have all been beaten (in any order, by anyone),
the whole server is warned and The Unmaker wakes at the main arena a minute later. `/cbosses finale` shows how far
the server is, `/cbosses finale wake` starts it now and `/cbosses finale reset` starts over. Change the bosses, the
delay and the arena under `finale:` in `config.yml`.

{table(finale)}

<p align="center"><img src="docs/images/unmaker_heart.jpg" width="32%"> <img src="docs/images/unmaker_arms.jpg" width="32%"> <img src="docs/images/unmaker_death.jpg" width="32%"></p>
<p align="center"><sub>The void heart lights alone in the air, the four arms swing in, and the end: the arms torn away before it bursts.</sub></p>

## Legend bosses

{table(legends)}

## World bosses

These take turns as the weekly public boss at your arena.

{table(world)}

## Seasonal bosses

A seasonal boss takes the weekly slot while its season is on. Seasons switch on by date, by command, or by following
the season CQuests has on.

{table(season)}

<p align="center"><img src="docs/images/clucksworth_egg.jpg" width="32%"> <img src="docs/images/clucksworth_hatch.jpg" width="32%"> <img src="docs/images/killer_claus_death.jpg" width="32%"></p>
<p align="center"><sub>Clucksworth's egg, the hatch, and Killer Claus breaking apart.</sub></p>

## Install

1. Put `CBosses-x.y.z.jar` in `plugins/` (Paper or Folia 1.21.4 and newer, Java 21).
2. Optional: WorldGuard, PlaceholderAPI, CQuests.
3. Start the server, then set up an arena:
   ```
   /cbosses arena setspawn main
   /cbosses arena region main <worldguard-region>   (or /cbosses arena wand main, or /cbosses arena radius main 40)
   ```
4. Try a boss with `/cbosses test the_listener`, or open the menu with `/cbosses`.

## Commands

All commands need `cbosses.admin` except `/cbosses next`. Aliases: `/cb`, `/bosses`.

| Command | What it does |
|---|---|
| `/cbosses` or `/cbosses menu` | Boss menu. Left-click tests a boss on you, right-click spawns it at the arena. |
| `/cbosses list` | Every boss, with which ones are alive. |
| `/cbosses spawn <boss> [arena]` | Spawn a public boss at an arena. |
| `/cbosses test <boss>` / `test phase` / `test stop` | A private test fight next to you, skip a phase, or end it. |
| `/cbosses stop [boss]` | Remove live bosses. |
| `/cbosses selftest` | Spawn every boss, run every attack and death, and report. |
| `/cbosses arena setspawn\\|wand\\|show\\|region\\|radius\\|clear\\|delete\\|list` | Set up arenas and their borders. |
| `/cbosses schedule on\\|off` | Turn the weekly boss on or off. |
| `/cbosses chapter <player> <n>` / `reset` / `retry` | Start, reset or retry a player's chapter boss. |
| `/cbosses season <id> <on\\|off\\|auto>` | Switch a season. |
| `/cbosses finale [wake\\|reset]` | Finale progress, wake it now, or start over. |
| `/cbosses next` | When the next boss wakes. |
| `/cbosses reload` | Reload every file. |

## Configuration

- **`config.yml`** has the sections `effects` (quality and lag), `schedule` (weekly boss days, times, time zone, order),
  `arenas`, `fight` (health and damage multipliers, idle and max time, minion caps), `chapter-bosses`, `rewards`,
  `announcements`, `worldguard` and `seasons`. Every option has a comment.
- **`bosses.yml`** has every boss: name, title, health, scale, damage, armor, boss bar color, movement, abilities, ability
  timing, phases, minions and rewards (money, items and commands, plus extra rewards for the top damage dealer).
  New bosses from an update are added to your file without touching your changes.
- **`messages.yml`** has every line the plugin shows, in MiniMessage: chat, titles, action bars, the menu, command
  replies and the broadcasts. Words in angle brackets like `<boss>` and `<player>` are filled in. New lines from an
  update are added to your file by themselves.
- **`arenas.yml`** is written by the arena commands.

### Lag settings

`effects.model-detail` (high, medium, low) drops the fine pieces from every model (about 15% fewer blocks on
medium, about 25% fewer on low). `effects.quality` (low, medium, high, ultra) and `particle-multiplier` scale every particle. `flying-blocks`,
`max-flying-blocks` and `max-shards-per-death` cap block effects. `model-update-ticks` (3 by default) and
`model-view-distance` control how often and how far models animate. `intro: false` skips the omens.

## WorldGuard

- **Flags:** `cbosses-spawn` (deny to stop bosses appearing in a region) and `cbosses-fight` (deny to stop players hurting
  bosses there).
- **Region arenas:** `/cbosses arena region <arena> <region>` uses a region's shape as the arena border.
- **Spawn protection:** `worldguard.bypass-spawn-blocking: true` keeps WorldGuard's `mob-spawning deny` from blocking
  bosses and their minions. Only CBosses' own entities are let through.

## CQuests

With CQuests installed, chapter completions start chapter bosses, and seasons can follow CQuests' seasons. Both are
optional and CBosses runs fine without CQuests. CQuests ships the same models for its own world bosses, and when both
plugins are installed CQuests leaves the world bosses to CBosses so there are never two at once.

## PlaceholderAPI

`%cbosses_next%`, `%cbosses_next_boss%`, `%cbosses_alive%`, `%cbosses_alive_bool%`, `%cbosses_count%`,
`%cbosses_chapter_<n>%` (beaten or not for the player) and `%cbosses_name_<boss>%`.

## Developer API

```java
CBossesAPI api = CBossesAPI.get();
api.spawn("the_listener", "main");
api.chapterBoss(player, 5);
```

Events: `BossSpawnEvent` (cancellable) and `BossDefeatEvent`.

## Building

```
./gradlew build
```

The jar is in `build/libs/`. GitHub Actions builds every push and runs the server tests. Boss models are generated by
the scripts in `tools/models/` (`python3 tools/models/gen_models.py`), the viewer by `tools/viewer/build_viewer.py`,
and this README by `tools/gen_readme.py`.
"""
open("README.md", "w").write(md)
print("README.md", len(md))
