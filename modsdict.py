# Modifier dictionary for spell calculator
#shape is the addition to the afflicted glyph

mod_dict = {
    #Ley
     "Shoot Ice1": {"shape":"square","size":2, "appto":["Shoot Ice EN"], "AP":1, "energy":0, "comment": "Ice deals d6 × 2 (Piercing) PD ⚔️/2 PP,(Foe rolls 1 medium AGI checks, if from point or beam, 2 medium AGI checks if cone, and 3 medium AGI checks if radial Glyph of Ice), Add 1 AP Requirement: 20 ft range, 16 INT, and Master (If not, DEATH)"},
    "Shoot Ice2": {"shape":"double_square", "size":2, "appto":["Shoot Ice EN"], "AP":3, "energy":0, "comment": "Ice deals 100 (Piercing) ⚔️/6 PP Add 3 AP, Requirement: Ice with weight >=3, 10 ft range, 16 INT, and Master (If not ALL, DEATH)"},
     "Ley Fire Burn": {"shape":"circle","size":1,"appto":["Flame","Greater Flame"], "AP":5, "energy":0, "comment": "Burn + d12 x INT MD✨ (Force), Add 5 AP.Requirement: 16 INT and Master (If not, DEATH) "},
    #End 
    "Crystal Proj": {"shape":"diamond","size":2, "appto":["Crystal"], "AP":0, "energy":1, "comment": "Crystal or shards send toward target (if character this hits all limbs), shooting D4 projectiles (only 1 if single Crystal) dealing d10 (Piercing) ⚔️/1 PP (for shards) or dealing d10 (Force)⚔️"}

}