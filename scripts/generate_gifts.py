#!/usr/bin/env python3
"""Generate markdown files for each gift effect from the power system blob."""

import json
import os
import re

BLOB_PATH = "power_blob.json"
OUTPUT_DIR = "gifts"

VECTOR_NAMES = {
    "trap": "Trap",
    "direct": "Targeted",
    "passive": "Passive",
    "functional": "Functional",
    "at-will": "Activated",
}

MODALITY_NAMES = {
    "power": "Power",
    "signature-item-mod": "Legendary Artifact",
    "craftable-consumable": "Consumable Crafting",
    "craftable-artifact": "Artifact Crafting",
}

CATEGORY_DISPLAY = {
    "offensive": "Offensive",
    "defensive": "Defensive",
    "health": "Health",
    "mobility": "Mobility",
    "awareness": "Awareness",
    "communication": "Communication",
    "influence": "Influence",
    "material": "Material",
    "metamorphism": "Metamorphism",
    "extraordinary-object": "Extraordinary Object",
    "masteries": "Masteries",
}


def slugify_filename(name):
    """Convert an effect name to a safe filename."""
    s = name.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def format_status(required_status):
    """Format the required status for display."""
    if not required_status or required_status[0] == "ANY":
        return None
    return required_status[1]


def collect_modifiers_for_effect(blob, effect):
    """Collect all enhancements and drawbacks available for an effect,
    including vector-level and modality-level ones, respecting blacklists."""

    blacklist_enh = set(effect.get("blacklist_enhancements", []))
    blacklist_drw = set(effect.get("blacklist_drawbacks", []))

    # Effect-level enhancements/drawbacks
    enhancements = []
    for slug in effect.get("enhancements", []):
        if slug in blacklist_enh:
            continue
        enh = blob["enhancements"].get(slug)
        if enh:
            enhancements.append((enh, None))  # (modifier, vector_label)

    drawbacks = []
    for slug in effect.get("drawbacks", []):
        if slug in blacklist_drw:
            continue
        drw = blob["drawbacks"].get(slug)
        if drw:
            drawbacks.append((drw, None))

    # Vector-level enhancements/drawbacks
    available_vectors = effect.get("allowed_vectors", [])
    for vec_slug in available_vectors:
        vec = blob["vectors"].get(vec_slug)
        if not vec:
            continue
        vec_name = VECTOR_NAMES.get(vec_slug, vec.get("name", vec_slug))
        for enh_slug in vec.get("enhancements", []):
            if enh_slug in blacklist_enh:
                continue
            enh = blob["enhancements"].get(enh_slug)
            if enh:
                # Check if already added at effect level
                existing_slugs = {e[0]["slug"] for e in enhancements}
                if enh_slug not in existing_slugs:
                    enhancements.append((enh, vec_name))
                else:
                    # Already exists, but we might need to note the vector
                    for i, (e, label) in enumerate(enhancements):
                        if e["slug"] == enh_slug and label is not None:
                            # Append vector name
                            if vec_name not in label:
                                enhancements[i] = (e, f"{label}, {vec_name}")
                            break
        for drw_slug in vec.get("drawbacks", []):
            if drw_slug in blacklist_drw:
                continue
            drw = blob["drawbacks"].get(drw_slug)
            if drw:
                existing_slugs = {d[0]["slug"] for d in drawbacks}
                if drw_slug not in existing_slugs:
                    drawbacks.append((drw, vec_name))
                else:
                    for i, (d, label) in enumerate(drawbacks):
                        if d["slug"] == drw_slug and label is not None:
                            if vec_name not in label:
                                drawbacks[i] = (d, f"{label}, {vec_name}")
                            break

    # Modality-level enhancements/drawbacks
    available_modalities = effect.get("allowed_modalities", [])
    for mod_slug in available_modalities:
        mod = blob["modalities"].get(mod_slug)
        if not mod:
            continue
        mod_name = MODALITY_NAMES.get(mod_slug, mod.get("name", mod_slug))
        for enh_slug in mod.get("enhancements", []):
            if enh_slug in blacklist_enh:
                continue
            enh = blob["enhancements"].get(enh_slug)
            if enh:
                existing_slugs = {e[0]["slug"] for e in enhancements}
                if enh_slug not in existing_slugs:
                    enhancements.append((enh, mod_name))
        for drw_slug in mod.get("drawbacks", []):
            if drw_slug in blacklist_drw:
                continue
            drw = blob["drawbacks"].get(drw_slug)
            if drw:
                existing_slugs = {d[0]["slug"] for d in drawbacks}
                if drw_slug not in existing_slugs:
                    drawbacks.append((drw, mod_name))

    return enhancements, drawbacks


def format_modifier_entry(mod, source_label):
    """Format a single enhancement or drawback entry."""
    lines = []
    name = mod["name"]
    status = format_status(mod.get("required_status"))
    detail_label = mod.get("detail_field_label")
    multiplicity = mod.get("multiplicity_allowed", False)

    # Build the header line with tags
    tags = []
    if source_label:
        tags.append(source_label)
    if status:
        tags.append(status)
    if multiplicity:
        tags.append("Stackable")

    if tags:
        tag_str = " | ".join(tags)
        lines.append(f"- **{name}** [{tag_str}]")
    else:
        lines.append(f"- **{name}**")

    # Description
    desc = mod.get("description", "").strip()
    if desc:
        lines.append(f"  {desc}")

    # Eratta
    eratta = mod.get("eratta", "").strip()
    if eratta:
        lines.append(f"  *Errata: {eratta}*")

    # Detail field
    if detail_label:
        lines.append(f"  Detail required: {detail_label}")

    # Required enhancements/drawbacks
    req_enh = mod.get("required_enhancements", [])
    req_drw = mod.get("required_drawbacks", [])
    if req_enh or req_drw:
        reqs = []
        if req_enh:
            reqs.append(f"enhancements: {', '.join(req_enh)}")
        if req_drw:
            reqs.append(f"drawbacks: {', '.join(req_drw)}")
        lines.append(f"  Requires: {'; '.join(reqs)}")

    return "\n".join(lines)


def generate_markdown(blob, effect_slug, effect):
    """Generate the full markdown content for one effect."""
    lines = []

    name = effect["name"]
    summary = effect.get("summary", "").strip()
    description = effect.get("description", "").strip()
    category = CATEGORY_DISPLAY.get(effect.get("category", ""), effect.get("category", ""))
    eratta = effect.get("eratta", "").strip()
    required_status = format_status(effect.get("required_status"))

    # Title
    lines.append(f"# {name}")
    lines.append("")

    # Summary / metadata
    lines.append(f"*{summary}*")
    lines.append("")
    meta = [f"**Category:** {category}"]
    if required_status:
        meta.append(f"**Required Status:** {required_status}")
    lines.append(" | ".join(meta))
    lines.append("")

    # Vectors
    available_vectors = effect.get("allowed_vectors", [])
    if available_vectors:
        vec_names = [VECTOR_NAMES.get(v, v) for v in available_vectors]
        lines.append(f"**Vectors:** {', '.join(vec_names)}")
        lines.append("")

    # Modalities
    available_modalities = effect.get("allowed_modalities", [])
    if available_modalities:
        mod_names = [MODALITY_NAMES.get(m, m) for m in available_modalities]
        lines.append(f"**Modalities:** {', '.join(mod_names)}")
        lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    lines.append(description)
    lines.append("")

    # Eratta
    if eratta:
        lines.append("## Errata")
        lines.append("")
        lines.append(eratta)
        lines.append("")

    # Collect all modifiers
    enhancements, drawbacks = collect_modifiers_for_effect(blob, effect)

    # Enhancements
    lines.append("## Enhancements")
    lines.append("")
    if enhancements:
        for enh, source_label in sorted(enhancements, key=lambda x: x[0]["name"]):
            lines.append(format_modifier_entry(enh, source_label))
            lines.append("")
    else:
        lines.append("*No enhancements available.*")
        lines.append("")

    # Drawbacks
    lines.append("## Drawbacks")
    lines.append("")
    if drawbacks:
        for drw, source_label in sorted(drawbacks, key=lambda x: x[0]["name"]):
            lines.append(format_modifier_entry(drw, source_label))
            lines.append("")
    else:
        lines.append("*No drawbacks available.*")
        lines.append("")

    return "\n".join(lines)


def main():
    with open(BLOB_PATH) as f:
        blob = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    effects = blob["effects"]
    # Sort effects alphabetically by name
    sorted_effects = sorted(effects.items(), key=lambda x: x[1]["name"])

    for slug, effect in sorted_effects:
        filename = slugify_filename(effect["name"]) + ".md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        content = generate_markdown(blob, slug, effect)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  {filename}")

    print(f"\nGenerated {len(sorted_effects)} gift files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
