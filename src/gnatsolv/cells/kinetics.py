# Lucas Swanson -- Ripon College '27
"""transcribed from Beloit_axon_propagation/kinetics_wholecell.hoc
Biophysical parameters in the form of key-value pairs are matched to different types of segment using standard python dictionarys.
see traubdict, traubdict_mod, jonasdict for more detail"""
#   original comments start with HOC's double-shash

traubdict = {
    "axon" : {
            "g_pas" : 1/1000,
            "Ra" :   100.0,
            #insert nafTraub
            "ena" : 50,
            "gbar_nafTraub" : 0.45,
            #insert kdrTraub
            "ek" : -95,
            "gbar_kdrTraub" :  0.45
    },
    "soma" : {
            "g_pas" : 1/50000,
            "Ra" : 250
    },
    "dendrite" : {
            "g_pas" : 1/50000,
            "Ra" : 250
    }
}
traubdict_mod = traubdict.copy()
traubdict_mod.update({
        "soma" : {
            "g_pas" : 2e-3, # // higher conductance makes up for currents not being modeled
            "Ra" : 250
        },
        "dendrite" : {
            "g_pas" : 1/50000,
            "Ra" : 250
        },
        "axon" : {
            "gbar_nafTraub" :   0.2,
            "gbar_kdrTraub" :   0.2
        }
})

jonasdict = {
    "axon" : {
            "g_pas" : 1/1000,
            "Ra" :  100.0,
            #insert nafTraub,
            "gbar_nafTraub" :   0.2,
            "ena" : 50,
            #insert kdrTraub,
            "gbar_kdrTraub" :   0.2,
            "ek" : -95
    },
    "soma" : {
        "g_pas" : 2e-3, # // higher conductance makes up for currents not being modeled
        # //1/50000
        "Ra" : 250
    },
    "dendrite" : {
        "g_pas" : 1/50000,
        "Ra" : 250
    }
}

def ins_Traub(sec, forsec):
    forsecdict = traubdict 
    assert(forsec in forsecdict)

    
    sec.insert("pas")
    if forsec == "axon":
        sec.insert("kdrTraub")
        sec.insert("nafTraub")
    attrdict = forsecdict[forsec]
    sec.e_pas = -70
    sec.cm = 0.9
    for k in attrdict:
        setattr(sec, k, attrdict[k])

def unins_Traub():
    print("uninsert_Traub: not implemented")

def inswho_Traub():
    print("uninsert_Traub: not implemented")

def insmod_Traub(sec, forsec): # legacy code declares tstpo=20 at the end.
    forsecdict = traubdict_mod
    assert(forsec in forsecdict)
    
    sec.insert("pas")
    if forsec == "axon":
        sec.insert("kdrTraub")
        sec.insert("nafTraub")
    attrdict = forsecdict[forsec]

    for k in attrdict:
        setattr(sec, k, attrdict[k])
    if sec.name == "IS": #this is to only set the first 40 micrometers of IS to the following gbars
        sec.gbar_nafTraub =   0.45
        sec.gbar_kdrTraub =   0.45
        # you dont need IS child.

            

def ins_Jonas(sec, forsec):
    print("ins_Jonas: not fully implemented (check kinetics_wholecell.hoc)")
    forsecdict = jonasdict 
    assert(forsec in forsecdict)

    sec.insert("pas")
    if forsec == "axon":
        sec.insert("kdrTraub")
        sec.insert("nafTraub")
    attrdict = forsecdict[forsec]
    sec.insert("pas")
    sec.e_pas = -70
    sec.cm = 0.9
    for k in attrdict:
        setattr(sec, k, attrdict[k])
