import math
import numpy as np
from tpcomp.constructs.signal import Signal
from tpcomp.constructs.utils import truncate

class Node:
    MIN = 0
    MAX = 255
    def __init__(self, pos, 
                 decay, delay, 
                 sensitivity, fovs):
        self.pos         = np.array(pos, dtype=np.uint8) # position (x, y)
        self.decay       = decay       # integer decay amount for internal state per timestep
        self.delay       = delay       # integer augmentation for incoming stimulus 
        self.sensitivity = sensitivity # stimulus threshold to emit a signal
        self.fovs        = list(fovs)  # list of dicts: {'center':..., 'width':...}
        self.stimulus    = 0           # internal state
        self.stimulus_history = []
        self._incoming_signals = []    # current timestep signals, not yet processed
    
    # def __str__(self,):
    #     t = self
    #     return f'f"Pos:{t.pos}\nstim:{t.stimulus:.1f}\nsens:{t.sensitivity:.1f}\ndec:{t.decay:.2f}\namp:{t.stim_amp:.2f}\nvamp:{t.vel_amp:.2f}\nFOV:{len(t.fovs)}"'
    
    @property
    def triggered(self,):
        return self.stimulus >= self.sensitivity

    def reflect(self):
        "Step 1 (disregard semantic inconsistencies, these steps are in correct numerical order)"
        self.stimulus = max(Node.MIN, self.stimulus - self.decay)

    def stage(self, signal, tick):
        "Step 2"
        accepted = False
        if not (signal.origin is self) \
        and not (signal in self._incoming_signals) \
        and not self.ignore(signal, tick):
            accepted = True
            self._incoming_signals.append(signal)
        return accepted
    
    def commit(self,):
        "Step 3"
        for signal in self._incoming_signals:
            self.stimulus = min(Node.MAX, self.stimulus + signal.stimulus)
        self._incoming_signals = []

    # response / feedback
    def response(self):
        "Step 4"
        if self.triggered:
            jitter = min(Node.MAX, self.stimulus + self.delay)
            return Signal(self, jitter)  # emit 'this' tick
    
    def ignore(self, signal, tick):
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
        return not (in_fov and in_range) #if in fov and in range, we listen
    
    def record_history(self):
        self.stimulus_history.append(self.stimulus)