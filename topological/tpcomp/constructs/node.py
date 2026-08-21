import math
import numpy as np
from tpcomp.constructs.signal import Signal
from tpcomp.constructs.utils import truncate

class Node:
    def __init__(self, pos, 
                 decay, stim_amp, vel_amp, 
                 sensitivity, fovs):
        self.pos         = np.array(pos, dtype=float) # position (x, y)
        self.decay       = decay       # decay percentage of internal state per timestep
        self.stim_amp    = stim_amp    # multiplier for incoming stimulus -> outgoing stimulus = vel_amp * incoming 
        self.vel_amp     = vel_amp     # multiplier for incoming velocity -> outgoing velocity = vel_amp * incoming
        self.sensitivity = sensitivity # stimulus threshold to emit a signal
        self.fovs        = list(fovs)  # list of dicts: {'center':..., 'width':...}
        self.stimulus    = 0.0         # internal state
        self.pos_history = []
        self.stimulus_history = []
        self._incoming_signals = []    # current timestep signals, not yet processed
    
    def __str__(self,):
        t = self
        return f'f"Pos:{t.pos}\nstim:{t.stimulus:.1f}\nsens:{t.sensitivity:.1f}\ndec:{t.decay:.2f}\namp:{t.stim_amp:.2f}\nvamp:{t.vel_amp:.2f}\nFOV:{len(t.fovs)}"'

    def decay_stimulus(self):
        self.stimulus *= self.decay
        self.stimulus = truncate(self.stimulus, 6)

    def receive_signal(self, signal):
        accepted = False
        if not (signal.origin is self) \
        and not (signal in self._incoming_signals):
            accepted = True
            self._incoming_signals.append(signal)
        return accepted
    
    def process_incoming_signals(self,):
        for signal in self._incoming_signals:
            self.stimulus += math.log(
                max(0, signal.stimulus)
                +1
            )

    def resolve(self,):
        self._incoming_signals = []
    
    def can_see(self, signal, tick):
        # Check if vector from self to source is within ANY of my FoVs
        r1 = signal.radius_at(tick)
        r0 = signal.radius_at(tick-1)
        dist = np.linalg.norm(self.pos - signal.epicenter)
        in_range = (r0 < dist <= r1) # wasnt visible last tick, is now

        in_fov = False if self.fovs else True
        if in_range:
            vec = signal.epicenter - self.pos
            angle = np.arctan2(vec[1], vec[0]) % (2 * np.pi)
            for fov in self.fovs:
                c, w = fov[0], fov[1]
                lower, upper = (c - w/2) % (2*np.pi), (c + w/2) % (2*np.pi)
                in_fov = lower <= angle <= upper if lower < upper else (angle >= lower or angle <= upper)
                if in_fov: 
                    break
        return in_fov and in_range
    
    def check_and_emit(self, tick, velocity):
        # Only emit once; only if stimulus now exceeds sensitivity
        if self.stimulus >= self.sensitivity:
            # Velocity amplifier acts on base velocity=1
            out_stim = self.stimulus * self.stim_amp
            # out_vel = 1.0 * self.vel_amp
            out_vel = velocity * self.vel_amp
            return Signal(self, out_vel, tick, out_stim)  # emit 'this' tick
        return None
    
    def record_history(self):
        self.stimulus_history.append(self.stimulus)
        self.pos_history.append(self.pos.copy())