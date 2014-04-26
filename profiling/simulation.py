import sys
from time import time

if len(sys.argv) < 3:
    print 'usage: python simulation.py outfile_prefix id'
    sys.exit()

# simulation id from command line, use to determine parameters
sid = int(sys.argv[2])

# log activity by time to annotate Valgrind's output
log_t0 = time()
fd = open('%s-%d.txt' % (sys.argv[1], sid,), 'w')
def LOG(msg, *args):
    msg_ = "%.3f\t%s\n" % (time() - log_t0, msg % args)
    sys.stderr.write(msg_)
    fd.write(msg_)


use_surface = sid & 4
use_jr      = sid & 2
use_slow_vc = sid & 1

LOG('sid=%d use_surf=%s use_jr=%s use_slow_vc=%s', 
        sid, use_surface, use_jr, use_slow_vc)

LOG('import simulator')
from tvb.simulator.lab import (
        coupling, integrators, noise, monitors, connectivity, 
        models, surfaces, simulator, array, nan
    )

LOG('common components')
components = {
    'coupling' : coupling.Linear(a=0.0043), #0.0066
    'integrator' : integrators.HeunStochastic(
        dt=2.0**-4, 
        noise=noise.Additive(nsig = array([2.0**-10,]))
        ), 
    'monitors' : ( monitors.TemporalAverage(period=1000.0/512.0),),
}

LOG('connectivity')
components['connectivity'] = \
        connectivity.Connectivity(speed=2.0 if use_slow_vc else 20.0)

LOG('model')
components['model'] = \
        (models.JRFast if use_jr else models.Generic2dOscillator)()

if use_surface:
    LOG('surface')
    components['surface'] = \
            surfaces.Cortex(coupling_strength=array([0.1835]))

LOG('simulator')
sim = simulator.Simulator(**components)

LOG('configure')
sim.configure()

LOG('create generator')
gen = sim(1e2 if use_surface else 1e3)

LOG('first step')
_ = next(gen)

LOG('begin integration loop')
while True:

    try:
        (t0, surf), = next(gen)
    except Exception as e:
        break

    if (surf==nan).any():
        LOG ('found nan, breaking')
        break

LOG(repr(e))

fd.close()

