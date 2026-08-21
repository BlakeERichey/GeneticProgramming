import matplotlib.pyplot as plt
class Signal:
    def __init__(self, origin, velocity, emission_tick, stimulus):
        self.origin = origin # tower
        self.epicenter = self.origin.pos.copy() if origin else None #tower may move
        self.velocity = velocity
        self.emission_tick = emission_tick
        self.stimulus = stimulus
            
    def radius_at(self, tick):
        dt = tick - self.emission_tick
        return self.velocity * max(dt, 0) if dt >= 0 else 0
    
    def plot_wavefront(self, tick):
        radius = self.radius_at(tick)
        circle = plt.Circle(self.epicenter, radius, color='r', fill=False, lw=1, alpha=0.7)
        plt.gca().add_patch(circle)