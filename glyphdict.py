# Glyph dictionary for spell calculator
#section is the parent domain 1 = END, 2 = DEATH, 3 = DARK SHAMAN, 4 = SHAMAN, 5 = DRUID, 6 = LEY
#range is the range: 1 = self, 2 = touch, 5 = 5ft, 10 = 10ft, 20 = 20ft and so on
#rt is the range type: 1 = self, 2 = touch, 3 = point, 4 = beam,  5 = cone, 6 = radial,
#chann means channeled if 1 = Yes, if 2 = No
# if EN is in the word name then you only add 1 AP due to the connection 
# if EN is in the word name and it has "over" = 1 then only add 1 charge rather than 1 AP

words_dict = {
    #LEY
    #Novice
    "Light": {"level":1,"section":6,"AP":1, "range":10, "rt": 6, "comment": "instant", "chann":1 },
    "Detect Magic": {"level":1,"section":6,"AP":1, "range":40, "rt": 6, "comment": "none", "chann":1 },
    "Charge D": {"level":2,"section":6,"AP":2, "range":2, "rt": 2, "comment": "duration 3 turns", "chann":2 },
    "Charge R": {"level":2,"section":6,"AP":2, "range":2, "rt": 2, "comment": "duration 3 turns", "chann":2 },
    #Adept
    "Freeze": {"level":1,"section":6,"AP":1, "range":10, "rt": 4, "comment": "cause slow 1", "chann":1 },
    "Flame": {"level":1,"section":6,"AP":1, "range":10, "rt": 3, "comment": "cause burn", "chann":1 },
    "Socket": {"level":1,"section":6,"AP":2, "range":2, "rt": 2, "comment": "permanent", "chann":2 },
    "Heat": {"level":1,"section":6,"AP":1, "range":5, "rt": 4, "comment": "instant, pushes non-monsterous targets back 5ft", "chann":1 },
    "Chill": {"level":1,"section":6,"AP":1, "range":10, "rt": 5, "comment": "instant", "chann":2 },
    "Ice w=1": {"level":1,"section":6,"AP":1, "range":10, "rt": 3, "comment": "long-lasting, w = weight of object and is 2x defualt charge value", "chann":1 },
    "Ice w=2": {"level":1,"section":6,"AP":1, "range":10, "rt": 3, "comment": "long-lasting, w = weight of object and is 2x defualt charge value", "chann":1 },
    "Ice w=3": {"level":2,"section":6,"AP":1, "range":10, "rt": 3, "comment": "long-lasting, w = weight of object and is 2x defualt charge value", "chann":1 },
    "Ice w=4": {"level":2,"section":6,"AP":1, "range":10, "rt": 3, "comment": "long-lasting, w = weight of object and is 2x defualt charge value", "chann":1 },
    "Ice w=5": {"level":3,"section":6,"AP":1, "range":10, "rt": 3, "comment": "long-lasting, w = weight of object and is 2x defualt charge value", "chann":1 },
    "Shape Ice": {"level":1,"section":6,"AP":0, "range":2, "rt": 2, "comment": "long-lasting, can only be added to Glyph of Ice", "chann":2 },
    #Master
    "Greater Flame": {"level":2,"section":6,"AP":1, "range":30, "rt": 4, "comment": "cause burn and 2x INT MD", "chann":1 },
    "Greater Chill": {"level":4,"section":6,"AP":1, "range":30, "rt": 5, "comment": "Instant, adds Slow 4", "chann":2 },
    #Enhancements: Novice
    "Brightness EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0, "comment": "adds stun effect to Glyph of Light", "chann":2 },
    #Enhancements: Adept
    "Vertical EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0, "comment": "adds 6ft to height of channeled / long-lasting glyph", "chann":2 },
    "Impact EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0,"comment": "knocks enemy Prone, causes fracturing on inanimate object", "chann":2, "over": 1 },
    "Shoot Ice EN": {"level":1,"section":6,"AP":1, "range":0, "rt": 0, "comment": "shoots ley ice up to specified range", "chann":2 },
    #Enhancements: Master
    "Greater Vertical EN": {"level":2,"section":6,"AP":1, "range":0, "rt": 0, "comment": "adds 10ft to height of channeled / long-lasting glyph", "chann":2 },

    
    #END
    #Novice
    "Volatile": {"level":2,"section":1,"AP":1, "range":15, "rt": 6, "comment": "instant", "chann":2 },
    "Devour": {"level":2,"section":1,"AP":2, "range":2, "rt": 2, "comment": "none", "chann":1, "2chann":2},
    #Adept
    "Crystal": {"level":1,"section":1,"AP":1, "range":15, "rt": 3, "comment": "none", "chann":2},
    "Disenchant": {"level":1,"section":1,"AP":2, "range":2, "rt": 2, "comment": "unusable in combat", "chann":2},
    "Enchant": {"level":2,"section":1,"AP":2, "range":2, "rt": 2, "comment": "none", "chann":2},
    "Bloodstone (Craft)": {"level":2,"section":1,"AP":2, "range":10, "rt": 3, "comment": "none", "chann":2},
    "Endflame": {"level":1,"section":1,"AP":2, "range":20, "rt": 4, "comment": "none", "chann":2},
    #Master
    "Demongate": {"level":5,"section":1,"AP":2, "range":5, "rt": 3, "comment": "Rift seals in 2 seconds or after an End Pull whichever happens first", "chann":2},
    "End Pull": {"level":3,"section":1,"AP":2, "range":10, "rt": 4, "comment": "Beckon End winds and the creatures of which it flows through towards you. Is easiest to cast in areas with concentrated End (e.g. Hell). If linked with with the Glyph of Demongate consult the Demongate table", "chann":2},
    #Enhancements: Novice
    #Enhancements: Adept
    "Shadowfire EN": {"level":1,"section":1,"AP":1, "range":0, "rt": 0, "comment": "shadowfire effect, traitor of ley", "chann":2},
    "Crystal Growth EN": {"level":1,"section":1,"AP":2, "range":10, "rt": 3, "comment": "range overwrites crystal, edit", "chann":2},
    "Crystal Grove EN": {"level":1,"section":1,"AP":1, "range":10, "rt": 6, "comment": "Splits Glyph of Crystal into an area covering 10ft radial crystal shards", "chann":2 },
    #Enhancements: Master
    #MODIFIERES
    #Range Increase:
    "Shadowfire EN": {"level":1,"section":1,"AP":1, "range":0, "rt": 0, "comment": "shadowfire effect, traitor of ley", "chann":2},
    #TESTS:
    "Test EN": {"level":1,"section":1,"AP":2, "range":0, "rt": 0, "comment": "TEST EN", "chann":2},
    "TestCh EN": {"level":1,"section":1,"AP":2, "range":0, "rt": 0, "comment": "TESTCh EN", "chann":1},
    "Test": {"level":1,"section":6,"AP":1, "range":10, "rt": 5, "comment": "TEST", "chann":1},
    "Test1": {"level":1,"section":1,"AP":1, "range":10, "rt": 5, "comment": "TEST1", "chann":2},
    "Test2": {"level":1,"section":6,"AP":2, "range":10, "rt": 5, "comment": "TEST2", "chann":2},
    "Test3": {"level":2,"section":1,"AP":3, "range":10, "rt": 5, "comment": "TEST3", "chann":2},
    "Test4": {"level":2,"section":6,"AP":4, "range":10, "rt": 5, "comment": "TEST4", "chann":2},
    "TestCh": {"level":2,"section":6,"AP":2, "range":10, "rt": 5, "comment": "TESTCh", "chann":1},
    "TestCh2": {"level":2,"section":1,"AP":2, "range":10, "rt": 5, "comment": "TESTCh2", "chann":1,"2chann":2}
    
    

    
    
}
    
    
    


    
  
    
