# Lucas Swanson 6/6/2024
# transcribed from Beloit_axon_propagation/kinetics.hoc
# original comments start with HOC's double-shash

from neuron import h
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

    attrdict = forsecdict[forsec]
    if forsec == "axon":
        sec.insert("kdrTraub")
        sec.insert("nafTraub")
    for seg in sec:
        seg.insert("pas")
        seg.e_pas = -70
        seg.cm = 0.9
        for k in attrdict:
            setattr(seg, k, attrdict[k])

def unins_Traub():
    print("uninsert_Traub: not implemented")

def inswho_Traub():
    pass


def ins_Jonas(sec, forsec):
    forsecdict = jonasdict 
    assert(forsec in forsecdict)

    attrdict = forsecdict[forsec]
    if forsec == "axon":
        sec.insert("kdrTraub")
        sec.insert("nafTraub")
    for seg in sec:
        seg.insert("pas")
        seg.e_pas = -70
        seg.cm = 0.9
        for k in attrdict:
            setattr(seg, k, attrdict[k])
