# Modifier dictionary for spell calculator
#shape is the addition to the afflicted glyph

mod_dict = {
    #Ley
    "Shape Ice1": {"shape":"triangle","size":1,"appto":["Ice w=1","Ice w=2"],"AP":0, "energy":1,"comment": "You cut away at the Ley ice shaping it into your desired form as long as there is enough material to do so." },
    "Shape Ice2": {"shape":"triangle","size":1,"appto":["Ice w=3","Ice w=4"],"AP":0, "energy":2,"comment": "You cut away at the Ley ice shaping it into your desired form as long as there is enough material to do so." },
    "Shape Ice3": {"shape":"triangle","size":1,"appto":["Ice w=5"],"AP":0, "energy":1, "comment": "You cut away at the Ley ice shaping it into your desired form as long as there is enough material to do so." },
     "Shoot Ice1": {"shape":"square","size":1, "appto":["Shoot Ice EN"], "AP":1, "energy":0, "comment": "Ice deals d6 × 2 (Piercing) PD ⚔️/2 PP,(Foe rolls 1 medium AGI checks, if from point or beam, 2 medium AGI checks if cone, and 3 medium AGI checks if radial Glyph of Ice), Add 1 AP Requirement: <=20 ft range, 16 INT, and Master (If not, DEATH)"},
    "Shoot Ice2": {"shape":"double_square", "size":2, "appto":["Shoot Ice EN"], "AP":3, "energy":0, "comment": "Ice deals 100 (Piercing) ⚔️/6 PP Add 3 AP, Requirement: <=10 ft range, 16 INT, and Master (If not ALL, DEATH)"},
     "Ley Fire Damage": {"shape":"circle","size":1,"appto":["Flame","Greater Flame"], "AP":5, "energy":0, "comment": "Burn + d12 x INT MD✨ (Force), Add 5 AP.Requirement: 16 INT and Master (If not, DEATH) "},
    #End 
    "Crystal Projectile": {"shape":"diamond","size":2, "appto":["Crystal"], "AP":1, "energy":0, "comment": "Crystal or shards shoot toward a target. For shards this shoots D4 projectiles (this hits all limbs) dealing d10 (Piercing) ⚔️/1 PP. For a single crystal it deals d10 (Force)⚔️, to one limb"},
    "Crystal Growth": {"shape":"double_diamond","size":2,"appto":["Crystal"],"AP":2, "energy":0, "comment": "Requires: Glyph of Crystal with beam range type Grows the initial crystal from the Crystal Glyph far enough outward up to the total range of the Glyph of Crystal away from you. If hit by the point of a growing crystal while it grows (during the initial cast), you will take 60 (Piercing) PD ⚔️/7 PP per 15ft of growth. If range is increased increase the damage by that multiple (e.g. 30ft range = 2x60 → 120 PD ⚔️/7 PP.). Add 2 Charge and 2 AP"},

}
