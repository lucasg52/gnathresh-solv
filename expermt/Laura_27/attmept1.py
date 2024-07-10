from neuron import h, gui
import numpy as np
h.load_file("stdrun.hoc")

def abc_list(n):
    if n <= 0:
        return []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return list(alphabet[:n])

a_list = abc_list(5)


a, b, c, d, e = [h.Section(name=n) for n in a_list]
b.connect(a)
c.connect(b(1), 1) # connect the 1 end of c to the 1 end of b
d.connect(b)
e.connect(a(0)) # connect the 0 end of e to the 0 end of a
for sec in h.allsec():
    sec.nseg = 20
    sec.L = 100
    for seg in sec:
        seg.diam = np.interp(seg.x, [0, 1], [10, 40])

s = h.Shape()
s.show(False)
s.color(2, sec=a) # color section "a" red
h.topology()
h.finitialize(-65)
for sec in h.allsec():
    print(sec)
    for i in range(sec.n3d()):
        print('%d: (%g, %g, %g; %g)' % (i, sec.x3d(i), sec.y3d(i), sec.z3d(i), sec.diam3d(i)))
