#!/usr/bin/env python3
"""Reformat weapons-and-armor.md: remove rules content, convert tables to definition lists."""

import re
import os

SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                   "nightfall/stocks/01-weapons-and-armor.md")


def parse_table(lines, start_idx):
    """Parse a markdown table starting at start_idx. Returns (rows, end_idx).
    Each row is a list of cell values. First row is headers."""
    rows = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith('|'):
            break
        # Skip separator rows
        if re.match(r'^\|[\s:-]+\|', line):
            i += 1
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)
        i += 1
    return rows, i


def format_weapon(name, fields):
    """Format a single weapon/item entry as a definition list."""
    # Split name into primary name and examples if in parens
    # e.g. "Handgun (Glock-17s, M1911s)" -> name="Handgun", detail="Glock-17s, M1911s"
    match = re.match(r'^(.+?)\s*\((.+)\)\s*$', name)
    if match:
        primary = match.group(1).strip()
        detail = match.group(2).strip()
        out = [f"### {primary}", f"*{detail}*"]
    else:
        out = [f"### {name}"]

    for label, value in fields:
        if value and value.strip():
            out.append(f"- **{label}:** {value.strip()}")

    return "\n".join(out)


def build_firearms(rows):
    """Convert firearms table rows to definition lists."""
    # Headers: Weapon, Base Attack Difficulty, Weapon Damage & Handling, Effective Range, Reload After X Attacks
    entries = []
    for row in rows[1:]:  # skip header
        if len(row) < 5:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("Attack", row[1]),
            ("Weapon Damage", row[2]),
            ("Effective Range", row[3]),
            ("Reload", row[4]),
        ]))
    return "\n\n".join(entries)


def build_heavy_weapons(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 5:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("Attack", row[1]),
            ("Damage & Effect", row[2]),
            ("Effective Range", row[3]),
            ("Reload", row[4]),
        ]))
    return "\n\n".join(entries)


def build_explosives(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 4:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("Delay", row[1]),
            ("System", row[2]),
            ("Notes", row[3]),
        ]))
    return "\n\n".join(entries)


def build_grenades(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 2:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("System", row[1]),
        ]))
    return "\n\n".join(entries)


def build_melee(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 3:
            continue
        name = row[0]
        if not name.strip():
            continue
        fields = [
            ("Attack", row[1]),
            ("Weapon Damage", row[2]),
        ]
        if len(row) > 3 and row[3].strip():
            fields.append(("Notes", row[3]))
        entries.append(format_weapon(name, fields))
    return "\n\n".join(entries)


def build_other_weapons(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 4:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("Attack", row[1]),
            ("Weapon Damage", row[2]),
            ("Effective Range", row[3]),
        ]))
    return "\n\n".join(entries)


def build_nonlethal(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 4:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("Attack", row[1]),
            ("Maximum Range", row[2]),
            ("System", row[3]),
        ]))
    return "\n\n".join(entries)


def build_armor(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 4:
            continue
        name = row[0]
        if not name.strip():
            continue
        fields = [
            ("Armor Value", row[1]),
            ("Penalty", row[2]),
        ]
        if row[3].strip():
            fields.append(("Notes", row[3]))
        entries.append(format_weapon(name, fields))
    return "\n\n".join(entries)


def build_shields(rows):
    entries = []
    for row in rows[1:]:
        if len(row) < 4:
            continue
        name = row[0]
        if not name.strip():
            continue
        entries.append(format_weapon(name, [
            ("Armor Bonus", row[1]),
            ("Weight", row[2]),
            ("Penalty", row[3]),
        ]))
    return "\n\n".join(entries)


def main():
    with open(SRC, 'r') as f:
        lines = f.readlines()

    # Find all table start positions and their section context
    table_sections = []
    i = 0
    current_section = ""
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#'):
            current_section = line.lstrip('#').strip()
        if line.startswith('|') and i + 1 < len(lines) and lines[i+1].strip().startswith('|'):
            rows, end_i = parse_table(lines, i)
            table_sections.append((current_section, i, end_i, rows))
            i = end_i
        else:
            i += 1

    # Map section names to builder functions
    builders = {
        "Firearms List": build_firearms,
        "Heavy Weapons List": build_heavy_weapons,
        "Explosives List": build_explosives,
        "Grenades List": build_grenades,
        "Melee Weapons List": build_melee,
        "Other Weapons List": build_other_weapons,
        "Non-Lethal Weapons List": build_nonlethal,
        "Armor List": build_armor,
        "Shields List": build_shields,
    }

    # Build the new file content
    out = []

    out.append("# Weapons and Armor\n")

    # Firearms
    out.append("## Firearms\n")
    out.append("Firearms are quite powerful, but they can be difficult to transport and obtain.\n")
    out.append("The effective range listed below is not a maximum range. Guns may be fired at")
    out.append("targets beyond that, with the Difficulty increasing by +1 for each additional")
    out.append("increment.\n")
    out.append("Attacks made at all are \"All-Out Attacks\"--for Firearms, this means that the")
    out.append("amount of rounds expended during an Attack is abstracted.\n")
    out.append("For \"single-shot\" / ammunition-saving fire modes outside of the abstracted")
    out.append("Attack: halve Weapon Damage and round down.\n")
    out.append("Reloading is always at least an Action, some Firearms may require multiple")
    out.append("Actions to reload (such as box / belt-fed Machine Guns, or heavy duty explosive")
    out.append("weapons).\n")

    for section, start, end, rows in table_sections:
        if section == "Firearms List":
            out.append(build_firearms(rows))
            break

    # Notes after firearms
    out.append("")
    out.append("**Note:** \"Proper Support\" refers to things like a bipod, a tripod, a vehicle")
    out.append("fixture, structure fixture, prone on stable ground, etc.")
    out.append("The two quick actions are an abstraction for deploying the bipod, and then")
    out.append("supporting the weapon with–and other combinations. GMs may call for making a")
    out.append("roll on \"unstable fixtures\" or \"unstable terrain\" at their discretion.\n")
    out.append("Heavy weaponry mounted onto vehicles, typically, hand waves any Handling Rules.\n")
    out.append("Note that tracking reloads and ammo is an optional rule at the GM's discretion.")
    out.append("The \"reload after X attacks\" rating above reflects that Contractors likely fire")
    out.append("more than once during a given all-out attack.\n")

    # Heavy Support Weapons
    out.append("## Heavy Support Weapons\n")
    out.append("Heavy Support Weapons are weapons that utilize similar rules to firearms but")
    out.append("fire, instead of a traditional round / bullet, an explosive ordnance such as a")
    out.append("rocket, missile or grenade.\n")

    for section, start, end, rows in table_sections:
        if section == "Heavy Weapons List":
            out.append(build_heavy_weapons(rows))
            break

    # Explosives
    out.append("\n## Explosives\n")
    out.append("**GM Tip:**\n")
    out.append("GMs should always give Contractors a roll to detect explosive traps, no matter")
    out.append("how well-hidden they are. Dying in one shot to an undetectable trap is never a")
    out.append("good experience.\n")

    for section, start, end, rows in table_sections:
        if section == "Explosives List":
            out.append(build_explosives(rows))
            break

    out.append("")
    out.append("If the above doesn't provide enough detail for you, check out")
    out.append("[Other Explosives](https://www.thecontractrpg.com/guide/rules/#other-explosives)")
    out.append("for a generalized system.\n")

    # Grenades
    out.append("## Grenades\n")
    out.append("All grenades have a delay of 2 Rounds, meaning they explode on your turn the")
    out.append("Round after you throw them. They have an effective throwing range of 100 feet.")
    out.append("Grenades weigh 2 pounds.\n")

    for section, start, end, rows in table_sections:
        if section == "Grenades List":
            out.append(build_grenades(rows))
            break

    out.append("")
    out.append("**Cooking off Grenades:**")
    out.append("You may \"cook off\" a grenade by holding it for a Round and then throwing with a")
    out.append("Perception + Athletics roll, Difficulty 8. Failure or partial success")
    out.append("indicates a dangerous throw. If you do so, it goes off the Round you throw it.")
    out.append("Fully cooked-off grenades may still be Reacted to.\n")

    # Melee Weapons
    out.append("## Melee Weapons\n")
    out.append("The stats for a given class of melee weapon are as follows:\n")

    for section, start, end, rows in table_sections:
        if section == "Melee Weapons List":
            out.append(build_melee(rows))
            break

    # Other Weapons
    out.append("\n## Other Weapons\n")
    out.append("Stats for thrown weapons and projectile launchers are as follows. Effective")
    out.append("Range works as per Firearms.\n")

    for section, start, end, rows in table_sections:
        if section == "Other Weapons List":
            out.append(build_other_weapons(rows))
            break

    # Non-Lethal Weapons
    out.append("\n## Non-Lethal Weapons\n")

    for section, start, end, rows in table_sections:
        if section == "Non-Lethal Weapons List":
            out.append(build_nonlethal(rows))
            break

    # Armor
    out.append("\n## Worn Armor\n")
    out.append("Armor reduces incoming Damage from most sources.\n")
    out.append("Armor from multiple sources cannot stack. Instead, the highest Armor Value is")
    out.append("used.\n")
    out.append("While bulkier Armors provide more protection, they also levy a dice penalty on")
    out.append("any physical actions attempted by their wearer. Note that dice penalties from")
    out.append("all sources stack.\n")

    for section, start, end, rows in table_sections:
        if section == "Armor List":
            out.append(build_armor(rows))
            break

    out.append("")
    out.append("**Note:** Slashing / Piercing Weapons does not include Firearms.\n")

    # Shields
    out.append("## Shields\n")
    out.append("Shields increase your Armor, stacking with the highest rating of any other Armor")
    out.append("you are wearing. However they incur a dice penalty to all physical Actions other")
    out.append("than Defending. All shields use up one hand, meaning you cannot use two-handed")
    out.append("weapons like rifles or greatswords with them.\n")
    out.append("Some shields are mobile (wheeled or mechanized), allowing them to move up to")
    out.append("10ft a Round while still providing Armor to their users, with no Penalty.\n")

    for section, start, end, rows in table_sections:
        if section == "Shields List":
            out.append(build_shields(rows))
            break

    out.append("")
    out.append("Non-transparent shields may increase the Difficulty of Perception rolls.\n")
    out.append("Bucklers and armored wristbands do not provide extra Armor or take up a hand,")
    out.append("but they allow you to use Brawl to Defend against Melee Attacks.\n")

    # Write
    with open(SRC, 'w') as f:
        f.write("\n".join(out))

    print("Done! Reformatted weapons-and-armor.md")
    print(f"  Converted {len(table_sections)} tables to definition lists")


if __name__ == "__main__":
    main()