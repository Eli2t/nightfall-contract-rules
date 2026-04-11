#!/usr/bin/env python3
"""Fix heading levels and structural issues across nightfall/ files.

This handles:
- Duplicate/redundant headers at file tops
- Heading level normalization (ensure proper hierarchy)
- Specific content fixes per file
"""

import os
import re

NIGHTFALL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nightfall")


def normalize_heading_levels(text):
    """Normalize heading levels so they don't skip (e.g. # -> #### becomes # -> ##).

    Strategy: Find the first heading, treat it as level 1. Then for each subsequent
    heading, ensure it doesn't skip more than one level from the previous heading.
    """
    lines = text.split('\n')
    result = []
    # Track the mapping from original level to normalized level
    level_stack = []  # stack of (original_level, normalized_level)

    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.*)', line)
        if match:
            hashes = match.group(1)
            content = match.group(2)
            orig_level = len(hashes)

            if not level_stack:
                # First heading is always level 1
                norm_level = 1
            else:
                prev_orig, prev_norm = level_stack[-1]

                if orig_level <= prev_orig:
                    # Going up or same level — find matching parent
                    while level_stack and level_stack[-1][0] >= orig_level:
                        level_stack.pop()
                    if level_stack:
                        norm_level = level_stack[-1][1] + 1
                    else:
                        norm_level = 1
                else:
                    # Going deeper — just one level deeper than parent
                    norm_level = prev_norm + 1

            # Cap at 6
            norm_level = min(norm_level, 6)
            level_stack.append((orig_level, norm_level))

            result.append('#' * norm_level + ' ' + content)
        else:
            result.append(line)

    return '\n'.join(result)


def fix_file(filepath, fixes):
    """Apply a list of (old, new) replacements to a file."""
    with open(filepath, 'r') as f:
        text = f.read()

    for old, new in fixes:
        text = text.replace(old, new, 1)

    # Normalize heading levels
    text = normalize_heading_levels(text)

    with open(filepath, 'w') as f:
        f.write(text)


def main():
    # === combat/overview.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "combat/overview.md"), [
        ("# Combat Rules\n\n# Combat Rules and Reference\n\n# Overview",
         "# Combat Overview"),
    ])
    print("  fixed: combat/overview.md")

    # === combat/actions.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "combat/actions.md"), [
        ("# Actions, Reactions, and Movement",
         "# Actions"),
    ])
    print("  fixed: combat/actions.md")

    # === combat/reactions.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "combat/reactions.md"), [
        ("## Reactions",
         "# Reactions"),
    ])
    print("  fixed: combat/reactions.md")

    # === combat/movement.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "combat/movement.md"), [
        ("## Movement",
         "# Movement"),
    ])
    print("  fixed: combat/movement.md")

    # === combat/hazards.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "combat/hazards.md"), [])
    print("  fixed: combat/hazards.md")

    # === gifts/general-gift-rules.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gifts/general-gift-rules.md"), [
        ("# Gifts & Effects\n\n# Gifts & Effects Errata\n\n# General Overhauls / Reworks",
         "# General Gift Rules"),
    ])
    print("  fixed: gifts/general-gift-rules.md")

    # === gifts/gift-clarifications.md ===
    # Remove stray "# Stocks" at end if present
    fpath = os.path.join(NIGHTFALL_DIR, "gifts/gift-clarifications.md")
    with open(fpath, 'r') as f:
        text = f.read()
    text = re.sub(r'\n# Stocks\s*$', '', text.rstrip()) + '\n'
    with open(fpath, 'w') as f:
        f.write(text)
    fix_file(fpath, [])
    print("  fixed: gifts/gift-clarifications.md")

    # === gifts/assets-and-liabilities.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gifts/assets-and-liabilities.md"), [])
    print("  fixed: gifts/assets-and-liabilities.md")

    # === gifts/house-assets.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gifts/house-assets.md"), [])
    print("  fixed: gifts/house-assets.md")

    # === gifts/overview.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gifts/overview.md"), [])
    print("  fixed: gifts/overview.md")

    # === stocks/weapons-and-armor.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "stocks/weapons-and-armor.md"), [
        ("# Weapon Ref.\n\n# Quick Weapon reference",
         "# Quick Weapon Reference"),
    ])
    # Remove empty #### heading
    fpath = os.path.join(NIGHTFALL_DIR, "stocks/weapons-and-armor.md")
    with open(fpath, 'r') as f:
        text = f.read()
    text = re.sub(r'^#{1,6}\s*$\n', '', text, flags=re.MULTILINE)
    with open(fpath, 'w') as f:
        f.write(text)
    print("  fixed: stocks/weapons-and-armor.md")

    # === stocks/stat-blocks-people.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "stocks/stat-blocks-people.md"), [])
    print("  fixed: stocks/stat-blocks-people.md")

    # === stocks/stat-blocks-animals.md ===
    # Fix misplaced intro text
    fix_file(os.path.join(NIGHTFALL_DIR, "stocks/stat-blocks-animals.md"), [
        ("Covers mundane people; baseline Humans that possess no ability to channel Source\n(or Source at all, really), and wield typically mundane & ordinary weaponry and\nskills found / possessed by those in the real world.",
         "Stat blocks for terrestrial and aquatic predators."),
    ])
    print("  fixed: stocks/stat-blocks-animals.md")

    # === stocks/stat-blocks-vehicles.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "stocks/stat-blocks-vehicles.md"), [])
    print("  fixed: stocks/stat-blocks-vehicles.md")

    # === stocks/battle-scars.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "stocks/battle-scars.md"), [])
    print("  fixed: stocks/battle-scars.md")

    # === stocks/traumas-and-disorders.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "stocks/traumas-and-disorders.md"), [])
    print("  fixed: stocks/traumas-and-disorders.md")

    # === injuries.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "injuries.md"), [])
    print("  fixed: injuries.md")

    # === mind-and-exertion.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "mind-and-exertion.md"), [
        ("## Mind\n",
         "# Mind and Exertion\n\n## Mind\n"),
    ])
    print("  fixed: mind-and-exertion.md")

    # === lore.md ===
    fpath = os.path.join(NIGHTFALL_DIR, "lore.md")
    with open(fpath, 'r') as f:
        text = f.read()
    # Fix indented paragraphs
    lines = text.split('\n')
    fixed_lines = []
    for line in lines:
        if line.startswith('    ') and not line.strip().startswith('#'):
            fixed_lines.append(line.lstrip())
        else:
            fixed_lines.append(line)
    text = '\n'.join(fixed_lines)
    # Fix duplicate headers and broken link
    text = text.replace(
        "# Lore Overview\n\n# Detailed Lore Overview\n\n# Overview",
        "# Lore"
    )
    text = text.replace("[Lore Overview]()", "the lore section below")
    with open(fpath, 'w') as f:
        f.write(text)
    fix_file(fpath, [])
    print("  fixed: lore.md")

    # === situational-rules.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "situational-rules.md"), [])
    print("  fixed: situational-rules.md")

    # === gameplay-basics/rolling-dice.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gameplay-basics/rolling-dice.md"), [])
    print("  fixed: gameplay-basics/rolling-dice.md")

    # === gameplay-basics/downtime.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gameplay-basics/downtime.md"), [])
    print("  fixed: gameplay-basics/downtime.md")

    # === gameplay-basics/contracts.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gameplay-basics/contracts.md"), [])
    print("  fixed: gameplay-basics/contracts.md")

    # === gameplay-basics/overview.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gameplay-basics/overview.md"), [])
    print("  fixed: gameplay-basics/overview.md")

    # === gameplay-basics/contractors.md ===
    fix_file(os.path.join(NIGHTFALL_DIR, "gameplay-basics/contractors.md"), [])
    print("  fixed: gameplay-basics/contractors.md")

    print("\nDone!")


if __name__ == "__main__":
    main()
