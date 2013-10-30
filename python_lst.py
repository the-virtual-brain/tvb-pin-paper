from tvb.simulator.lab import *

sim = simulator.Simulator(
    model        = models.Generic2dOscillator(), 
    connectivity = connectivity.Connectivity(),
    coupling     = coupling.Linear(a=1e-2),
    integrator   = integrators.HeunDeterministic(),
    monitors     = (
        monitors.TemporalAverage(), 
    )
)

sim.configure()

ys = array([y for ((t, y),) 
	      in  sim(simulation_length=3e2)])

# Other example
# eeg, mri = [], []
# for (t_eeg, y_eeg), (t_mri, y_mri) in sim(3e2):
#     if y_eeg is not None:
# 	eeg.append(y_eeg)
    ...
plot(ys[:, 0, :, 0], 'k', alpha=0.1)
