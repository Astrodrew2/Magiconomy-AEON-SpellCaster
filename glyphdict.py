# Glyph dictionary for spell calculator
#section is the parent domain 1 = END, 2 = DEATH, 3 = DARK SHAMAN, 4 = SHAMAN, 5 = DRUID, 6 = LEY
#range is the range: 1 = self, 2 = touch, 5 = 5ft, 10 = 10ft, 20 = 20ft and so on
#rt is the range type: 1 = self, 2 = touch, 3 = point, 4 = beam,  5 = cone, 6 = radial,
#chann means channeled if 1 = Yes, if 2 = No
# if EN is in the word name then you only add 1 AP due to the connection 
# if EN is in the word name and it has "over" = 1 then only add 1 charge rather than 1 AP
#if "vig":1 then  it is a vigor cost not charge (adds the < to the base AP
#if the vig keyword is = 1 and "fiver": 1 then it adds the > to the end of the base AP
# 2chann is the AP to channel (default 1)

words_dict = {
    #LEY
    #Novice
    "Light": {"level":1,"section":6,"AP":1, "range":10, "rt": 6, "comment": "instant, Emanate a light from your hand radially outward. It’s shine is almost calming", "chann":1 },
    "Charge D": {"level":2,"section":6,"AP":2, "range":2, "rt": 2, "comment": "Imbue a weapon with MD ✨ equal to 2 × INT. When the effect wears off, the weapon turns to ash. Duration 3 turns", "chann":2 },
    "Charge R": {"level":2,"section":6,"AP":2, "range":2, "rt": 2, "comment": "Imbue a piece of armor with MR 🪞 equal to 2 × INT. When the effect wears off, the armor turns to ash. Duration 3 turns", "chann":2 },
    #Adept
    "Freeze": {"level":1,"section":6,"AP":1, "range":10, "rt": 4, "comment": "The Ley winds caught within your cast halt almost to a stand still inflicting 4 Slow on targets within your range", "chann":1 },
    "Flame": {"level":1,"section":6,"AP":1, "range":10, "rt": 3, "comment": "Energize the Ley winds you cast upon making that which it touches burn. Causes Burn.", "chann":1 },
    "Socket": {"level":1,"section":6,"AP":2, "range":2, "rt": 2, "comment": "If a weapon or piece of armor has a slot for a magical item or gemstone, you may use the Ley winds to fuse them together so the weapon or armor gains the effects of the magical item. Duration: continuous", "chann":2 },
    "Heat": {"level":1,"section":6,"AP":1, "range":5, "rt": 4, "comment": "instant, pushes non-monsterous targets back 5ft", "chann":1 },
    "Chill": {"level":1,"section":6,"AP":1, "range":10, "rt": 5, "comment": "instant, The Ley winds caught within your cast slow down inflicting 1 Slow on targets within your range", "chann":2 },
    "Ice w=1": {"level":1,"section":6,"AP":1, "range":10, "rt": 3, "comment": "You take away all of the energy within the Ley winds creating a thing of ice before you with the density of the weight (w) of the cast,Duration: long-lasting", "chann":1 },
    "Ice w=2": {"level":1,"section":6,"AP":1, "range":10, "rt": 3, "comment": "You take away all of the energy within the Ley winds creating a thing of ice before you with the density of the weight (w) of the cast,Duration: long-lasting", "chann":1 },
    "Ice w=3": {"level":2,"section":6,"AP":1, "range":10, "rt": 3, "comment": "You take away all of the energy within the Ley winds creating a thing of ice before you with the density of the weight (w) of the cast,Duration: long-lasting", "chann":1 },
    "Ice w=4": {"level":2,"section":6,"AP":1, "range":10, "rt": 3, "comment": "You take away all of the energy within the Ley winds creating a thing of ice before you with the density of the weight (w) of the cast,Duration: long-lasting", "chann":1 },
    "Ice w=5": {"level":3,"section":6,"AP":1, "range":10, "rt": 3, "comment": "You take away all of the energy within the Ley winds creating a thing of ice before you with the density of the weight (w) of the cast,Duration: long-lasting", "chann":1 },
    "Shape Ice": {"level":1,"section":6,"AP":0, "range":2, "rt": 2, "comment": "You cut away at the Ley ice shaping it into your desired form as long as there is enough material to do so. Can only be added to Glyph of Ice. Duration: long-lasting", "chann":2 },
    #Master
    "Greater Flame": {"level":2,"section":6,"AP":1, "range":30, "rt": 4, "comment": "Energize the Ley winds you cast upon with far greater power and control making that which it touches burn and effect the natural world around it. Damage: If caught in flames, 2 x INT MD✨and Causes Burn.", "chann":1 },
    "Greater Chill": {"level":4,"section":6,"AP":1, "range":30, "rt": 5, "comment": "Instant, The Ley winds caught within your cast come to stop briefly inflicting Inflict 6 Slow on targets within your range", "chann":2 },
    #Enhancements: Novice
    "Brightness EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0, "comment": "adds stun effect to Glyph of Light", "chann":2 },
    #Enhancements: Adept
    "Vertical EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0, "comment": "Adds 6ft to the height of the channeled or long-lasting glyph attached (mass is increased as would be expected). Duration: long-lasting glyph", "chann":2 },
    "Impact EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0,"comment": "If spell makes contact, knock the enemy Prone. If makes contact with inanimate object, it will cause fracturing.", "chann":2, "over": 1 },
    "Shoot Ice EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0, "comment": "If the caster chooses to release the Ley ice as it pulls away from them during formation it shoots their Ley Ice up to the Glyph of Ice’s specified range (Unless modified with Shoot Ice1 or 2)", "chann":2 },
    #Enhancements: Master
    "Greater Vertical EN": {"level":2,"section":6,"AP":1, "range":0, "rt": 0, "comment": "Adds 10ft to the height of the channeled or long-lasting glyph attached", "chann":2 },

    
    #END
    #Novice
    "Noxious": {"level":1,"section":1,"AP":1, "range":15, "rt": 6, "comment": "instant, Turn the End winds around you into a cloud of noxious gas. Caster is immune to the effects. Entities in the cloud lose 60 Vigor. Triggers if an entity ends their turn in the Noxious Cloud.", "chann":2 },
    "Volatile": {"level":2,"section":1,"AP":1, "range":15, "rt": 6, "comment": "instant, Turn the End winds around you into a volatile cloud of gas. Caster is immune to the effects. Entities in the cloud lose 30 Vigor. Triggers if an entity ends their turn in the Volatile Cloud. The cloud can be ignited from an external source. Entities in the cloud upon ignition will be inflicted with Burn", "chann":2 },
    "Devour": {"level":2,"section":1,"AP":2, "range":2, "rt": 2, "comment": "Absorb the health of a target you are in contact with Deal 2 × INT MD ✨ and recover Injury Units equal to the ¼ final damage dealt. Fresh corpses have 5 injury units to steal.", "chann":1, "2chann":2},
    #Adept
    "Crystal": {"level":1,"section":1,"AP":1, "range":15, "rt": 3, "comment": "Condense the End winds into a hard blood red crystal before you (this is susceptible to gravity).", "chann":2},
    "Disenchant": {"level":1,"section":1,"AP":2, "range":2, "rt": 2, "comment": "Turn weapons and armor imbued with magic into their Primal Essence, pure magic in crystalline form. This destroys the weapon or armor. Disenchanting a weapon produces a Weapon Essence crystal with a stored magic value equal to the weapon’s MD. This cannot be used on Ice Weapons. Disenchanting a piece of armor produces one (1) Armor Essence crystal, unusable in combat", "chann":2},
    "Enchant": {"level":2,"section":1,"AP":2, "range":2, "rt": 2, "comment": "Use the power stored in a Weapon Essence crystal to enchant a weapon. This transfers the MD value stored in the Weapon Essence to the destination weapon. This can be done multiple times to the same weapon. If a single weapon is enchanted 2 times, it becomes Unstable, reducing it to 1 Strike and halving its durability. Attempting to use Disenchant on this weapon will now just turn it to dust. If a single weapon is enchanted 5 times, it becomes Draining. Every turn this weapon is wielded in combat, it inflicts 10 ✨ to the wielder's arm. ", "chann":2},
    "Bloodstone (Craft)": {"level":2,"section":1,"AP":2, "range":10, "rt": 3, "comment": "By combining the End within 3 Armor Essences you can craft a Bloodstone", "chann":2},
    "Endflame": {"level":1,"section":1,"AP":2, "range":20, "rt": 4, "comment": "Turn the End winds against a target, unleash a flaming bolt of End magic. Damage: INT + attack roll MD ✨", "chann":2},
    #Master
    "Demongate": {"level":5,"section":1,"AP":2, "range":5, "rt": 3, "comment": "Using the End winds open a rift to hell. The rift to hell seals in 2 seconds or after an End Pull whichever happens first unless stabilized.", "chann":2},
    "End Pull": {"level":3,"section":1,"AP":2, "range":10, "rt": 4, "comment": "Beckon End winds and the creatures of which it flows through towards you. Is easiest to cast in areas with concentrated End (e.g. Hell). If linked with with the Glyph of Demongate consult the Demongate table", "chann":2},
    #Enhancements: Novice
    #Enhancements: Adept
    "Shadowfire EN": {"level":1,"section":1,"AP":1, "range":0, "rt": 0, "comment": "This gives Ley Fire magic spells the additional Shadowfire effect, dealing 2 × INT MD ✨ to any limb instantly upon initial contact (if you are completely engulfed in Shadowfire this will afflict all targets you come in contact with). This includes contact with existing Walls of Flame and areas burning with the Shadowfire effect. You are a traitor of ley", "chann":2},
    "Crystal Growth EN": {"level":1,"section":1,"AP":2, "range":10, "rt": 3, "comment": "Grows the initial crystal from the Crystal Glyph far enough outward up to a total of 10ft away from you (This overwrites the default 15 ft). If hit by the point of a growing crystal while it grows (during the initial cast), you will take 40 (Piercing) PD ⚔️/7 PP. If range is increased increase the damage by that multiple (e.g. 30ft range = 3x40 → 120 PD ⚔️/7 PP.)", "chann":2},
    "Crystal Grove EN": {"level":1,"section":1,"AP":1, "range":10, "rt": 6, "comment": "Splits Glyph of Crystal into an area covering 10ft radial crystal shards", "chann":2 },
    #Enhancements: Master

    #DRUID:
    #Novice
    "Roots": {"level":2,"section":5,"AP":1, "range":20, "rt": 3, "comment": "Call upon the spark of life within the roots around a target and cause them to grow use them to wrap around the target, entangling them. Roots have 50 Vigor", "chann":2, "vig":1, "fiver":2},
    "Spirit Flame (Heal)": {"level":1,"section":5,"AP":1, "range":10, "rt": 4, "comment": "Cast green fire to restore the Vigor of a target at the cost of your own. Lose Spirit x 2 as Vigor and restore target’s Vigor by the same amount. Restore targets Injury Units equal to your Spi. (Requires Medium Spirit Check)", "chann":1, "vig":1, "fiver":2},
    "Spirit Flame (Damage)": {"level":1,"section":5,"AP":1, "range":10, "rt": 4, "comment": "Cast dark green fire to inflict MD ✨ on a target, Damage: SPI × 2 MD ✨", "chann":1, "vig":1, "fiver":2},
    "Barkskin": {"level":1,"section":5,"AP":1, "range":1, "rt": 1, "comment": "Instant. Duration: 3 turns. Harden your skin like tree bark, reinforcing your PR 🛡️. Bark skin acts as another layer of armor with 10 NR, 10 FR, and 1 PT for all sources of PD ⚔️. Dispelling the bark skin restores the Vigor used to cast it", "chann":2, "vig":1, "fiver":2},
    "Thorns": {"level":1,"section":5,"AP":1, "range":1, "rt": 1, "comment": "Instant. Duration: 3 turns. Grow bony thorns and spikes that protrude from all over your body. If an enemy comes into contact with an area of your body where you are wearing Light armor or less, they will take damage. If the enemy punches, kicks, or grapples you while they are wearing light armor or less in any area, they will take 10 (Piercing) ⚔️/1 PP. Dispelling the thorns restores the Vigor used to cast it", "chann":2, "vig":1, "fiver":2},
    
    #Adept
    "Claws": {"level":1,"section":5,"AP":1, "range":1, "rt": 1, "comment": "Flare your inner embers to Grow bony claws from your fingertips. Slash: 10 (Cutting) ⚔️/1 PP, Stab: 10 (Piercing) ⚔️/1 PP, Ambush Weapon. Dispelling Claws restores the Vigor used to cast it", "chann":2, "vig":1, "fiver":1},
    "Remediate": {"level":2,"section":5,"AP":1, "range":2, "rt": 2, "comment": "Cure yourself or a target of any poison, curses, or uncheck the Bleed Box.Cannot be performed during combat", "chann":2, "vig":1, "fiver":2},
    
    #Master
    "Fire of Life": {"level":3,"section":5,"AP":6, "range":2, "rt": 2, "comment": "Revert your Inner Fire to Inner Embers forever and in exchange you may resurrect one mortal entity at full Vigor and fully restoring their body, curing them of any ailments and healing any injuries (including missing limbs): Cost: Loss of Inner Fire forever", "chann":2, "vig":1, "fiver":2},
    
    #Enhancements: Novice
    #Enhancements: Adept
    "Shoot Thorns EN": {"level":1,"section":5,"AP":1, "range":0, "rt": 6, "comment": "Instant. Shoot Thorns in all directions (radial) for 5ft. If you are casting thorns from yourself you must be wearing Light armor or less on your torso. Damage: 10 (Piercing) PD ⚔️/2 PP", "chann":2, "vig":1, "fiver":2},
    "Venom EN": {"level":1,"section":5,"AP":1, "range":0, "rt": 1, "comment": "Instant. While Thorns is active, cause the thorns to secrete a poison. Inflicts 1 Poison on contact", "chann":2, "vig":1, "fiver":2},
    #Enhancements: Master

    #SHAMANISM:
    #Novice:
    "Earth (s=1)": {"level":1,"section":4,"AP":1, "range":10, "rt": 3, "comment": "Instant. Throw chunks of earth the size of a tennis ball from a source at a target up to 10ft away. Damage: d% +(10 x Focus) of 10 (Force)/1PP", "chann":2},
    "Water (s=1)": {"level":1,"section":4,"AP":1, "range":60, "rt": 4, "comment": "Instant. Shoot a thin tendril of water toward your target from a source 10ft away. Damage: d% +(10 x Focus) of 10 (Force)/0PP", "chann":2},
    "Fire (s=1)": {"level":1,"section":4,"AP":1, "range":60, "rt": 4, "comment": "Instant. Pull fire of a small size from a source up to 10 ft away and hurl it at enemies, extinguishing the same amount of fire. Damage: (d% + 10 × Focus) 30 MD, Causes Burn", "chann":2},
    "Air (s=1)": {"level":1,"section":4,"AP":1, "range":30, "rt": 3, "comment": "Pull the air from 1 vessel you target (vessel includes lungs).Damage: (d% + 10 × Focus) 60 Vigor, Inflicts 1 Stun buildup", "chann":2},
    
    #Adept:
    "Earth (s=2)": {"level":1,"section":4,"AP":1, "range":10, "rt": 3, "comment": "Shifts a chunk of earth the size of a basketball. This can either displace the chunk up as a new mound of the same size or hold it mid air for the action. IF THROWN: Damage: d% +(10 x Focus) of 150 (Force)/2PP", "chann":2},
    "Earth (s=3)": {"level":1,"section":4,"AP":2, "range":10, "rt": 3, "comment": "Pull up chunks of earth the size of a large yoga ball. This can either displace the chunk up as a new mound or hold it mid air for the action. IF THROWN: Damage: d% +(10 x Focus) of 300 (Force)/4PP", "chann":2},
    "Water (s=2)": {"level":1,"section":4,"AP":1, "range":60, "rt": 4, "comment": "Shoot a tendril of water toward your target from a source 10ft away. Damage: d% +(10 x Focus) of 20 (Force)/0PP", "chann":2},
    "Water (s=3)": {"level":2,"section":4,"AP":2, "range":30, "rt": 4, "comment": "Shoot a large tendril of water toward your target from a source 10ft away. Damage: d% +(10 x Focus) of 40 (Cutting)/0PP", "chann":2},
    "Fire (s=2)": {"level":2,"section":4,"AP":1, "range":60, "rt": 4, "comment": "Pull fire of a medium size from a source up to 10 ft away and hurl it at enemies, extinguishing the same amount of fire. Damage: (d% + 10 × Focus) 60 MD, Causes Burn", "chann":2},
    "Fire (s=3)": {"level":3,"section":4,"AP":2, "range":30, "rt": 4, "comment": "Pull fire of a medium size from a source up to 10 ft away and hurl it at enemies, extinguishing the same amount of fire. Damage: (d% + 10 × Focus) 90 MD, Causes Burn", "chann":2},
    "Air (s=2)": {"level":2,"section":4,"AP":1, "range":30, "rt": 6, "comment": "Pull the air from 2 vessel you target (vessel includes lungs).Damage: (d% + 10 × Focus) 60 Vigor, Inflicts 1 Stun buildup", "chann":2},
    "Air (s=3)": {"level":3,"section":4,"AP":2, "range":15, "rt": 6, "comment": "Pull the air from 5 vessels you target (vessel includes lungs).Damage: (d% + 10 × Focus) 60 Vigor, Inflicts 1 Stun buildup", "chann":2},
    
    #Master:
    "Earth (s=4)": {"level":5,"section":4,"AP":2, "range":10, "rt": 3, "comment": "Pull up chunks of earth the size of a refrigerator. This can either displace the chunk up as a new mound or hold it mid air for the action.IF THROWN: Damage: d% +(10 x Focus) of 1000 (Force)/6PP", "chann":2},
    "Water (s=4)": {"level":3,"section":4,"AP":2, "range":30, "rt": 4, "comment": "Shoot a tremendous tendril of water toward your target from a source 10ft away. Damage: d% +(10 x Focus) of 80 (Force)/0PP", "chann":2},
    "Fire (s=4)": {"level":4,"section":4,"AP":2, "range":30, "rt": 4, "comment": "Pull fire of a medium size from a source up to 10 ft away and hurl it at enemies, extinguishing the same amount of fire. Damage: (d% + 10 × Focus) 180 MD, Causes Burn 2", "chann":2},
    "Air (s=4)": {"level":5,"section":4,"AP":2, "range":15, "rt": 6, "comment": "Pull the air from 10 vessels you target (vessel includes lungs).Damage: (d% + 10 × Focus) 60 Vigor, Inflicts 1 Stun buildup", "chann":2},

    #Enhancements: Novice
    #Enhancements: Adept
    "Minor Throw Earth EN": {"level":1,"section":4,"AP":1, "range":0, "rt": 4, "comment": "Throw an object of earth that is loose or suspended with a medium or large size (such as with Glyph of Earth(s=2 or 3)) up to 20 ft away, dealing the specified thrown damage.", "chann":2,"over": 1 },
    "Water Grapple EN":{"level":2,"section":4,"AP":1, "range":0, "rt": 4, "comment": "A tendril of water this is applied to initiate a Grapple on its target (only if s = 2,3,or 4).Use 2 × SPI instead of STR for appropriate checks.", "chann":1},
    #Enhancements: Master
    "Major Throw Earth EN": {"level":1,"section":4,"AP":1, "range":0, "rt": 4, "comment": "Throw an object of earth that is loose or suspended with a tremendous size up to 10 ft away, dealing the specified thrown damage.", "chann":2,"over": 1 },
    
    #DARK SHAMANISM
    #Noice:
    "Demise": {"level":1,"section":3,"AP":5, "range":2, "rt": 2, "comment": "You alter your target soul’s longevity inflicting the “Curse of Demise” Status Effect. On Apply: Target will die in 25 days, reduced by 1 day for every point you exceed the target’s resistance roll by. E.g. You roll 15 and they roll 10. They will die in 20 days. While Active: The target will feel an increasing sense of dread as they rapidly approach their demise.", "chann":2 },
    "Pestulence": {"level":1,"section":3,"AP":1, "range":2, "rt": 2, "comment": "Instant. You cause the soul of your target to crack and leak applying the “Curse of Pestilence” Status Effect on a target. On Apply: Target will spread any curses they are currently afflicted with to nearby targets within 6ft + 1 for every point you exceed their resistance roll by. E.g. You roll 15 and they roll 10. The curses will spread to all targets within 11 feet of the initial target. While Active: Blisters will quickly form over the target’s body and burst leaving sickly green scabs.", "chann":2 },
    "Famine": {"level":1,"section":3,"AP":1, "range":2, "rt": 2, "comment": "Partially sever the connection between a targets soul and their fragments of Eyr, inflicting the “Curse of Famine” Status Effect on a target. While Active: Cannot naturally regenerate Vigor or Recovery Injuries. Target feels excessively fatigued and hungry during this time. Duration: 5 days.", "chann":2},
    "Rage": {"level":1,"section":3,"AP":1, "range":2, "rt": 2, "comment": "Duration: Buildup. Use the rage within a targets soul against them, inflicting the “Curse of War” on a target. On Apply/Reapply: Buildup = previous Buildup + the difference between your roll and target’s resistance roll. While Active: The target is overcome with destructive rage causing them to attack either the closest entity or another nearby entity that is currently and was most recently afflicted with Curse of War with murderous intent.", "chann": 2},
    #Adept:
    #Master:
    "Fragment": {"level":1,"section":3,"AP":1, "range":2, "rt": 2, "comment": "Locate the Fragments of Eyr within a living creature. The target cannot have been dead for more than 5 days and they cannot be posthumously disfigured beyond the ability to function (e.g. decapitation).", "chann":2},
    "anAtomy": {"level":2,"section":3,"AP":2, "range":2, "rt": 2, "comment": "Discern the immediate effect of whatever killed a target. The target cannot have been dead for more than 5 days and they cannot be posthumously disfigured beyond the ability to function (e.g. decapitation).", "chann":2},
    "spiriT": {"level":2,"section":3,"AP":3, "range":2, "rt": 2, "comment": "When combined with the Glyph of Fragment, discern exactly how long it has been since the target died.", "chann":2},
    "psychE": {"level":5,"section":3,"AP":4, "range":2, "rt": 2, "comment": "When combined with the Fragment, anAtomy, and spiriT Glyphs, change the fate of a dead target, reversing the immediate effect of whatever killed them. However, this does not cure any ailments nor mend any injuries, including lost limbs and Wound Table rolls. The target cannot have been dead for more than 5 days and they cannot be posthumously disfigured beyond the ability to function (e.g. decapitation).", "chann":2},
    
    #Enhancements: Novice
    "Virulence EN": {"level":1,"section":3,"AP":1, "range":2, "rt": 2, "comment": "When combined with the Glyph of Fragment, discern exactly how long it has been since the target died.", "chann":2, "over":5},
    "Chronic EN": {"level":1,"section":3,"AP":1, "range":2, "rt": 2, "comment": "Change the Duration of a curse to be Permanent. E.g. If the Duration was 5 days it now becomes Permanent.", "chann":2, "over":1},
    "Exacerbation EN": {"level":1,"section":3,"AP":2, "range":2, "rt": 2, "comment": "Instantly raise all Injury Levels to the next Level. (IE. Crippled is now Destroyed)", "chann":2},


    
    #Enhancements: Adept
    #Enhancements: Master
}
    
    
    


    
  
    
