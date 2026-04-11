#!/usr/bin/env python3
"""Split the Nightfall Rules Reference into structured markdown files."""

import os

SRC = "Nightfall Rules Reference.md"
OUT = "nightfall"

def read_lines():
    with open(SRC, "r") as f:
        return f.readlines()

def extract(lines, start, end):
    """Extract lines[start-1:end] (1-indexed, inclusive)."""
    return "".join(lines[start - 1 : end])

def write_file(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content.strip() + "\n")
    print(f"  {path}")

def main():
    lines = read_lines()

    # ── gameplay-basics/ ──

    write_file("gameplay-basics/overview.md",
        extract(lines, 1, 97) + "\n" + extract(lines, 662, 751))

    write_file("gameplay-basics/rolling-dice.md",
        extract(lines, 752, 1020))

    write_file("gameplay-basics/contractors.md",
        extract(lines, 98, 376) + "\n" + extract(lines, 1021, 1218))

    write_file("gameplay-basics/contracts.md",
        extract(lines, 377, 534))

    write_file("gameplay-basics/downtime.md",
        extract(lines, 594, 661) + "\n" + extract(lines, 1219, 1457) + "\n" + extract(lines, 1458, 1544))

    # ── combat/ ──

    write_file("combat/overview.md",
        extract(lines, 1676, 1874))

    # actions: attacking through holding actions + aiming
    write_file("combat/actions.md",
        extract(lines, 1875, 1907) + "\n" +  # Actions, Reactions, and Movement intro
        extract(lines, 1908, 2220) + "\n" +   # Attacking through disarms/shoves/throws
        extract(lines, 2221, 2307))            # Quick actions, mental actions, holding actions, aiming

    # reactions: desperate defense through clashing
    write_file("combat/reactions.md",
        extract(lines, 2308, 2404))

    # movement + vehicles
    write_file("combat/movement.md",
        extract(lines, 2405, 2601) + "\n" + extract(lines, 4047, 4311))

    # hazards: attack difficulty modifiers, other damage, poisons
    write_file("combat/hazards.md",
        extract(lines, 3794, 4046) + "\n" + extract(lines, 4312, 4500))

    # ── gifts/ ──

    write_file("gifts/overview.md",
        extract(lines, 535, 593))

    # general gift rules: overhauls, seasoned from start, disfigurings, crafting softcap, focus/fuel
    write_file("gifts/general-gift-rules.md",
        extract(lines, 5815, 6066))

    # specific gift clarifications: per-gift errata
    write_file("gifts/gift-clarifications.md",
        extract(lines, 6067, 6670))

    # assets-and-liabilities: core rules, reworks, changing, how to implement
    write_file("gifts/assets-and-liabilities.md",
        extract(lines, 4583, 4880))

    # house assets: the 4/8/14/22-point house assets + FAQ
    write_file("gifts/house-assets.md",
        extract(lines, 4881, 5813))

    # ── stocks/ ──

    # weapons and armor lists + quick reference
    write_file("stocks/weapons-and-armor.md",
        extract(lines, 2602, 2942) + "\n" + extract(lines, 4501, 4582))

    # stat blocks - people (civilians, criminals, law enforcement, military)
    write_file("stocks/stat-blocks-people.md",
        extract(lines, 7225, 7954))

    # stat blocks - animals
    write_file("stocks/stat-blocks-animals.md",
        extract(lines, 7955, 8322))

    # stat blocks - vehicles
    write_file("stocks/stat-blocks-vehicles.md",
        extract(lines, 8323, 9136))

    # battle scars
    write_file("stocks/battle-scars.md",
        extract(lines, 6674, 6881))

    # traumas and disorders (delusions, compulsions, phobias, disorders)
    write_file("stocks/traumas-and-disorders.md",
        extract(lines, 6882, 7224))

    # ── standalone files ──

    # injuries: body, injuries, stabilization, battle scars, death
    write_file("injuries.md",
        extract(lines, 3139, 3418))

    # mind and exertion: mind damage, traumas, exertion, stress, source, recovery
    write_file("mind-and-exertion.md",
        extract(lines, 3419, 3793))

    write_file("situational-rules.md",
        extract(lines, 1545, 1675))

    write_file("lore.md",
        extract(lines, 78, 97) + "\n" + extract(lines, 9137, 9190))

    print(f"\nDone! Files written to {OUT}/")


if __name__ == "__main__":
    main()