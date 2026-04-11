# Nightfall Patch Notes

This document goes over the changes made for the nightfall contract playgroup.

---

## Progression

### Win Brackets — Granular Sub-Tiers

Nightfall uses ten sub-brackets instead of the official five tiers. Interaction
is limited to within two win-brackets of yourself.

- Newbie (0-3), Newbie-Novice (3-6), High Novice (6-9), Low Seasoned (9-12),
  Seasoned (12-15), High Seasoned (15-18), Vet Gate (19), Professional (20-23),
  Vet Test (24), Veteran (25+)

### Vet Gate / Vet Test Milestones

- Win 19 is a tailored solo "Vet Gate Game" — must engage with the Contractor's
  story in a meaningful way.
- Win 24 is a "Vet Test" — another tailored milestone game.
- Winning the Vet Gate and each game past it unlocks one Veteran Gift Slot per
  win.

### Rework Milestones

Contractors unlock a character Rework at certain win thresholds:

- Novice Rework at 4 wins
- Seasoned Rework at 10 wins
- Vet-Gate Rework at 20 wins
- Veteran Rework at 25 wins

### Maximum Gift Value Formula

- The maximum Gift Value a Contractor can have is (Wins * 2) + 1.
  - 0 wins = 3 (Free Gift Point, Gifted Asset, and Charon Coin)
  - 1 win = 4
  - 2 wins = 5
  - 3+ wins = (Wins * 2) + 1

### Newbie Concept Malleability

- Newbie Contractors' concepts are "malleable" and may change freely (e.g. a
  Police PC may become an FBI Agent, or a wizard might become a hermetic
  sorcerer).

### Seasoned From The Start

Contractors in nightfall are able to take seasoned enhancements equal to your
win count divided by 3. Eg:

- 0-2 Wins
  - 0
- 3-5 Wins
  - 1
- 6-8 Wins
  - 2
- 9 Wins
  - 3
- 10+ Wins
  - Seasoned as standard

Combat seasoned effects (Weapon Masteries, Artifact Weapons, and gifts under the
"Offensive" category [with the exception of environment control]), as well as a
few additional gifts (listed below) are excluded from this, and require 10 wins
as standard. The full list of excluded gifts are as follows:

- Weapon Masteries
  - Unarmed Mastery
  - Throwing Mastery
  - Archery Mastery
  - Firearm Mastery
  - Melee Mastery
- Artifact Weapons
  - Thrown Weapon
  - Special Firearm
  - Projectile Launcher
  - Melee Weapon
- Offensive Gifts
  - Traumatize
  - Spawn Minions
  - Injure
  - Blast
  - Afflict
- Other combat-related gifts
  - Armor
  - Pyromancy
  - Regeneration
  - Alternate Form

### Novice Gifts Change

- Novice gifts now require 4 wins as standard.

---

## Combat Mechanics

### Dice Rework

- The results of non-combat rolls are now hidden from players. Instead, the
  resulting outcome of the roll will be narrated by the GM.
- Rolling a 10 no longer provides +2 outcome. Instead, it adds an additional
  dice to your roll.

### Combat Secondaries Removed

- Combat secondaries (Ex. "pistols", "knives", "jiu-jitsu", "dodging", etc.) no
  longer provide a difficulty reduction in combat.

### Called Shots

- Called shot thresholds are now split by melee/ranged:
  - Small target: CO 3 ranged / CO 2 melee (official: flat CO 4)
  - Tiny target: CO 5 ranged / CO 4 melee (official: flat CO 6)
- Head/heart called shots deal +2 damage, bypassing the Severity 5 cap.
- Successful called shots to arms/legs deal a Battle Scar 1 level higher than
  usual.

### Aiming Rework

- Aiming now requires Concentration (Free Actions only, 1 Quick Action per
  Round, 10ft movement max).
- Stacking -X Difficulty reduction per round spent Aiming.
- +2 Difficulty to Perception rolls for non-target awareness while Aiming.
- Must specify a trigger; if target attacks, it becomes a Clash.

### Concentration

- +2 Difficulty to Perception rolls for non-target awareness while
  Concentrating.

### Weapon Handling Rules

- In order to use a Weapon without increased Difficulty, your Brawn must match
  its Weapon Damage. If not, you suffer a Difficulty increase equal to the
  difference.
- For Gift-enhanced weapons, use the higher of the base Weapon Damage or half
  the total Weapon Damage (rounded up).
- If the Buster Drawback is taken, use the full Weapon Damage for Handling.

### New Combat Maneuvers

**Disarms**

- Brawn/Dex + Melee as an Action or Clash. Target's contest floor = Brawn
  rating. Positive CO = take possession or launch item (CO * 5 feet). Can
  combine with a Quick Action to equip the disarmed item.

**Shoves, Trips & Pins**

- Brawn/Dex + Melee as an Action or Clash. Shove distance = CO * 2.5 feet. Can
  knock target prone (Quick Action to stand). Pinned (grappled + prone) = +2
  Difficulty to attack grappler.

**Throws**

- Lower of Brawn + Melee or Athletics. Throw distance = CO * 5 feet. Weapon
  Damage = half target's Brawn (rounded down). Thrown target also takes damage.

### Combat Actions and Reactions

**Counter**

- Added reaction "Counter".
- Counter acts as a "riposte" or "parry" mechanic, dealing contested outcome
  from a defense.
  - Ex: If you roll an 8 on a counter roll and your attacker rolls a 6, deal 2
    damage plus your weapon damage to your attacker
- Counter is rolled at difficulty 7.
- The "Riposte" enhancement for melee mastery reduces the difficulty to 6.

**Evade**

- The evade action now lets you apply the full outcome of your roll to any
  attacks made against you that round, but is now rolled at difficulty 7.
- Mob bonuses do not apply on attacks against you while Evading.
- "Bullet time" on mythic dex now allows you to exert your mind to evade as an
  action or reaction at difficulty 6.

**Dodge**

- The dodge reaction now allows you to move half of your free movement (rounded
  down) as a part of the reaction.

### Limit Roll Clarification

- A one success is no longer sufficient to pass a mind roll, they now use the
  following system:
  - Botch: 1 Mind damage and you receive a new trauma
  - 0-2: You receive 1 mind damage
  - 3+: You are unaffected

---

## Health & Recovery

### Injuries — Severity 4+ Default to Battle Scar

- Injuries of Severity 4+ default to causing a Battle Scar. Equipment
  destruction requires a separate GM-initiated coin flip (official rules treat
  them as equal alternatives).

### Source — Full at Start of Events

- You begin every Contract, Move, and Hustle with full Source.

### Mind — Full Reset at Contract/Downtime Start

- Full Mind reset at the start of each Contract and the first Move of Downtime.
- Mind does not recover to full at the start of each Move, only the first.

### Will to Survive — Extended to Downtimes

- Will to Survive can be used once per Contract AND once per Downtime.

### Exertion — Source Replaces Mind for All Exertion

- Source can replace Mind for any Exertion, not just Gift activation.
- Exceptions: cannot substitute Source for Mind Damage from Effects, failed
  Trauma rolls, or overriding Traumas/Disorders.

### Exertion — Override Traumas/Disorders

- You may Exert Mind (not Source) on a failure (but not a botch) to instantly
  succeed any Trauma or Disorder roll.

### Disorders

- Disorders are a new category distinct from Traumas, with unique interaction
  rules. They represent long-lasting permanent conditions for how a person's Mind
  operates.

---

## Gift and Drawback Changes

### Drawback Changes

- Disfiguring is now major battle scars only
- Traumas (eg. phobias, compulsions, etc.) need to be likely to appear in a
  contract
- Fuels/Focus need to have two levels of specification i.e gun > revolver, must
  require some form of significant interaction and be problematic to transport.

### Resistible / Easily Resistible Rework

- Targets of Easily Resistible Effects may always make a Resistance Roll at
  Difficulty 6 (or higher if the Effect originally required a higher Difficulty).
- Compelling a target to choose not to resist does not deny them their roll.

### Signature Item Rework

- Signature item now prevents artifacts from being denied through non-gameplay
  or non-interactive means. Artifacts with this gift can still be stolen,
  however doing so requires at minimum a roll from a physically present
  character.
- Signature item is limited to a single artifact and cannot be taken multiple
  times or crafted onto multiple artifacts.
- Artifacts with this gift cannot exceed a maximum of 4 gift cost, including the
  signature item gift.
  - This is increased to 5 upon hitting seasoned.
- A few examples where an artifact with this gift cannot be deprived:
  - Fade-to-black "you wake up with nothing" situations
  - Unresistable/unreactable incapacitation
  - The harbingers arbitrarily denying artifacts
- For a general rule of thumb, a contestable roll by a physically present
  character is required to deny/steal an artifact with this gift.

### Samson Nerf

- When using Will to Survive on an attack, roll high or low. If the high or low
  fails, your samson gets destroyed and you lose all benefits for the next 2
  months. This may either be a replacement to the battlescar you would've taken,
  or in addition, at gm discretion and depending on severity.

### Hail Storm Rework

- Instead of exerting your mind to attack all targets in a 120 degree arc, it
  now simply allows bows to make a full-auto sweep against targets in a 120
  degree arc. (Attack @ 8, no longer requires an exertion)

---

## Hazards

### Poisons/Toxins

- New subsystem with 3 lethality tiers (Deadly, Dangerous, Mild), dosing
  mechanics, onset time, Body resistance at Difficulty 8, persistent agents,
  medical treatment, and irritant rules.

### Drugs

- New subsystem with addiction/dependence mechanics, onset times by delivery
  method (IV, snorted/injected, ingested), dosage levels, and specific
  subsystems for recreational drugs, stimulants, painkillers/sedatives, and
  truth serums.

---

## Equipment

### Stock Armor Nerfs

- Reinforced clothing ("bulletproof hoodies" or "bulletproof suits") now have -1
  armor against melee
- Kevlar vests reduced to 2 armor
- Plate carriers reduced to 3 armor and now have 1 dice penalty

---

## Admin

### Artifact Storage Change

- From now on, if artifacts are lost or stolen, send them to John Artifact. This
  ensures fairness across all situations.