#!/usr/bin/env python3
"""Replace thecontractrpg.com rule reference links with local file links."""

import os
import re
import glob

NIGHTFALL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nightfall")

# Mapping from URL fragments to local file paths (relative to nightfall/)
RULES_MAP = {
    # gameplay-basics/01-overview.md
    "#playgroups": "gameplay-basics/01-overview.md",
    "#setting": "gameplay-basics/01-overview.md",

    # gameplay-basics/02-rolling-dice.md
    "#rolling-dice": "gameplay-basics/02-rolling-dice.md",
    "#difficulty": "gameplay-basics/02-rolling-dice.md",
    "#contested-actions": "gameplay-basics/02-rolling-dice.md",

    # gameplay-basics/03-contractors.md
    "#contractors": "gameplay-basics/03-contractors.md",
    "#contractor": "gameplay-basics/03-contractors.md",
    "#character-creation": "gameplay-basics/03-contractors.md",
    "#the-character-sheet": "gameplay-basics/03-contractors.md",
    "#attributes": "gameplay-basics/03-contractors.md",
    "#abilities": "gameplay-basics/03-contractors.md",
    "#limits": "gameplay-basics/03-contractors.md",
    "#experience": "gameplay-basics/03-contractors.md",
    "#conditions-circumstances": "gameplay-basics/03-contractors.md",

    # gameplay-basics/04-contracts.md
    "#contracts": "gameplay-basics/04-contracts.md",
    "#scenarios": "gameplay-basics/04-contracts.md",
    "#harbingers": "gameplay-basics/04-contracts.md",
    "#journal": "gameplay-basics/04-contracts.md",
    "#journals": "gameplay-basics/04-contracts.md",
    "#questionnaire": "gameplay-basics/04-contracts.md",
    "#ringers": "01-situational-rules.md",
    "#visiting-other-playgroups": "01-situational-rules.md",

    # gameplay-basics/05-downtime.md
    "#downtime": "gameplay-basics/05-downtime.md",
    "#structured-downtimes": "gameplay-basics/05-downtime.md",
    "#making-moves": "gameplay-basics/05-downtime.md",
    "#loose-ends": "gameplay-basics/05-downtime.md",
    "#crafting": "gameplay-basics/05-downtime.md",
    "#rewards-advancement": "gameplay-basics/05-downtime.md",

    # gifts/
    "#gifts": "gifts/01-overview.md",
    "#gift-guide": "gifts/01-overview.md",
    "#building-gifts": "gifts/01-overview.md",
    "#gift-system-keywords": "gifts/01-overview.md",
    "#gifts-improvements": "gifts/01-overview.md",
    "#effects": "gifts/01-overview.md",
    "#equipment": "gifts/01-overview.md",

    # combat/01-overview.md
    "#combat": "combat/01-overview.md",
    "#initiative": "combat/01-overview.md",
    "#rounds": "combat/01-overview.md",

    # combat/02-actions.md
    "#actions": "combat/02-actions.md",
    "#action": "combat/02-actions.md",
    "#damage": "combat/02-actions.md",
    "#attack-difficulty-modifiers": "combat/05-hazards.md",
    "#supplemental-combat-rules": "combat/05-hazards.md",
    "#other-explosives": "combat/05-hazards.md",
    "#other-sources-damage": "combat/05-hazards.md",

    # combat/03-reactions.md
    "#reactions": "combat/03-reactions.md",
    "#dodging": "combat/03-reactions.md",
    "#defending": "combat/03-reactions.md",

    # combat/04-movement.md
    "#movement": "combat/04-movement.md",
    "#mobs": "combat/04-movement.md",

    # health/01-injuries.md
    "#injuries": "health/01-injuries.md",
    "#injures": "health/01-injuries.md",
    "#body": "health/01-injuries.md",
    "#stabilization": "health/01-injuries.md",
    "#battle-scars": "health/01-injuries.md",
    "#death": "health/01-injuries.md",

    # health/02-mind-and-exertion.md
    "#mind": "health/02-mind-and-exertion.md",
    "#trauma": "health/02-mind-and-exertion.md",
    "#exertion": "health/02-mind-and-exertion.md",
    "#stress": "health/02-mind-and-exertion.md",
    "#source": "health/02-mind-and-exertion.md",

    # stocks/01-weapons-and-armor.md
    "#armor": "stocks/01-weapons-and-armor.md",
    "#weapons": "stocks/01-weapons-and-armor.md",
    "#explosives": "stocks/01-weapons-and-armor.md",
    "#firearms": "stocks/01-weapons-and-armor.md",
}


def get_relative_path(from_file, to_file):
    """Get relative path from one file to another, both relative to NIGHTFALL_DIR."""
    from_dir = os.path.dirname(from_file)
    return os.path.relpath(to_file, from_dir)


def replace_links(filepath):
    rel_path = os.path.relpath(filepath, NIGHTFALL_DIR)

    with open(filepath, 'r') as f:
        text = f.read()

    original = text
    count = 0

    # Match markdown links: [text](url)
    def replacer(match):
        nonlocal count
        full = match.group(0)
        link_text = match.group(1)
        url = match.group(2)

        # Only process thecontractrpg.com/guide/rules/ or /rules/ links
        rules_match = re.match(
            r'https://www\.thecontractrpg\.com(?:/guide)?/rules/(#[\w-]+)', url)
        if not rules_match:
            return full

        fragment = rules_match.group(1)
        if fragment not in RULES_MAP:
            return full

        target = RULES_MAP[fragment]
        local_path = get_relative_path(rel_path, target)

        # Don't link to yourself
        if os.path.normpath(target) == os.path.normpath(rel_path):
            count += 1
            return link_text  # Just use the text, no link

        count += 1
        return f"[{link_text}]({local_path})"

    text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replacer, text)

    if text != original:
        with open(filepath, 'w') as f:
            f.write(text)

    return count


def main():
    files = sorted(glob.glob(os.path.join(NIGHTFALL_DIR, '**', '*.md'), recursive=True))
    total = 0
    for filepath in files:
        rel = os.path.relpath(filepath, NIGHTFALL_DIR)
        count = replace_links(filepath)
        if count > 0:
            print(f"  {rel}: {count} links replaced")
            total += count

    # Count remaining thecontractrpg links
    remaining = 0
    for filepath in files:
        with open(filepath, 'r') as f:
            text = f.read()
        remaining += len(re.findall(r'https://www\.thecontractrpg\.com', text))

    print(f"\n{total} rule reference links replaced")
    print(f"{remaining} thecontractrpg.com links remaining (website tool links)")


if __name__ == "__main__":
    main()