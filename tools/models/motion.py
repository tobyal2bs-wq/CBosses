"""A choreography pass on every entrance and death, using the craft pass's tagged pieces:

entrance  once the body has formed, the armour plates and trims spring out a little and click back into
          place one after another from the feet up (with an armour sound), then the glowing veins light
          from the bottom up just before the boss's own roar or pose
death     the veins go dark at random, the armour plates are thrown off in arcs before the boss's own death
          plays out, so every boss sheds its armour before it falls"""
from recipes import S, fx


def _end(s):
    return s["at"] + s.get("dur", 0) + s.get("stagger", 0)


def spawn(steps, has_trim, has_vein):
    steps = [dict(s) for s in steps]
    full = [s for s in steps if s["op"] == "pose" and not s.get("only")]
    anim = [s for s in steps if s["op"] == "anim"]
    if not full: return steps
    last = max(full, key=_end)
    t = _end(last) + 1
    if anim: t = min(t, max(0, anim[-1]["at"] - 2))
    t = max(t, last["at"] + 2)
    if has_trim:
        steps.append(S("burst", t, power=1.6, up=1.0, tilt=60, rand=0.6, only="trim"))
        steps.append(S("pose", t + 1, 6, order="up", stagger=12, only="trim"))
        steps.append(fx(t + 2, sound="ITEM_ARMOR_EQUIP_NETHERITE", pitch=0.7, y=0.4))
        steps.append(fx(t + 9, sound="ITEM_ARMOR_EQUIP_IRON", pitch=0.6, y=0.8))
    if has_vein:
        steps.append(S("flash", t + 4, 3, order="up", stagger=14, only="vein", block="white_concrete"))
        steps.append(fx(t + 6, sound="BLOCK_RESPAWN_ANCHOR_CHARGE", pitch=1.4, y=0.5))
    steps.sort(key=lambda s: s["at"])
    return steps


def death(steps, has_trim, has_vein):
    steps = [dict(s) for s in steps]
    if has_vein:
        steps.append(S("swap", 3, block="black_concrete", order="random", stagger=18, only="vein"))
        steps.append(fx(4, sound="BLOCK_RESPAWN_ANCHOR_DEPLETE", pitch=0.7, y=0.5))
    if has_trim and not any(s.get("only") == "trim" for s in steps):
        steps.append(S("fling", 6, 16, power=3.2, up=2.6, tilt=170, order="random", stagger=12, only="trim"))
        steps.append(fx(7, sound="ITEM_SHIELD_BREAK", pitch=0.6, y=0.6))
        steps.append(fx(12, sound="BLOCK_CHAIN_BREAK", pitch=0.6, y=0.4))
    steps.sort(key=lambda s: s["at"])
    return steps
