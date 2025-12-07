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
    
    
    #Adept
    
    #Master
    
    #Enhancements: Novice
    
    #Enhancements: Adept
    
    #Enhancements: Master
    
    
    
}
    
    
    


    
  
    
