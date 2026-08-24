from typing import List
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import logging
from tpcomp.inference.jitter import int_to_jitter
from tpcomp.constructs.node import Node
from tpcomp.constructs.signal import Signal
from collections import Counter

class Topology:
    def __init__(self, genome):
        self.genome = genome
        act_chrom = genome.actions
        obs_chrom = genome.observations
        self.lut = genome.lut
        self.action_space = 10

        self.obs_nodes = []
        for chrom in obs_chrom.values():
            pos = chrom.sequence[0] 
            decay = chrom.sequence[1]
            delay = chrom.sequence[2]
            sensitivity = chrom.sequence[3]
            fovs = []
            self.obs_nodes.append(
                Node(
                    pos,
                    decay,
                    delay,
                    sensitivity,
                    fovs
                )
            )

        self.act_nodes = []
        for chrom in act_chrom.values():
            pos = chrom.sequence[0] 
            decay = chrom.sequence[1]
            delay = chrom.sequence[2]
            sensitivity = chrom.sequence[3]
            fovs = [
                [chrom.sequence[4], chrom.sequence[5]],
                [chrom.sequence[6], chrom.sequence[7]]
            ]
            self.act_nodes.append(
                Node(
                    pos,
                    decay,
                    delay,
                    sensitivity,
                    fovs
                )
            )

        self.all_nodes = [*self.obs_nodes]
        self.all_nodes.extend(self.act_nodes)
        
        self.tick = 0
        self.signals = []
        self._energy_history = []
        self._abort = False # energy observation

    def reset(self,):
        Topology.__init__(self, self.genome)
        return self

    def __str__(self):
        return '\n'.join(list(map(str, [node for node in self.all_nodes])))

    def check_points_outside(self, center, radius, points):
        """
            Identifies if a wavefront has yet to reach a node
            Can be done more efficiently.
        """
        xc, yc = center.tolist()
        r_sq = radius ** 2
        
        for px, py in points:
            # Calculate squared distance
            dist_sq = (int(px) - xc)**2 + (int(py) - yc)**2     
            if dist_sq > r_sq:
                #logging.debug(f'Point {px, py, dist_sq} found outside wavefront {xc, yc, r_sq}')
                return True # Found a point outside
                
        return False # All nodes are inside or on the wavefront


    def prune_signals(self,):
        """
            Remove signals whose wavefront has encompassed all nodes
        """
        if len(self.signals):
            # actual practical limit is closer to D_max * 2 * len(all_nodes)
            # this value only emerges if each signal produces at least 2 more
            # They are emitting with higher frequency than being 
            # absorded by clamps.
            # Theoretical upper bounds < BigSigma(T_stasis) * len(all_nodes) <-> one new signal per node per timestep
            # = (T_stasis)(T_stasis + 1) / 2 * len(all_nodes)
            # Since stasis is topologically enforced, signals must dissapate within this limit and 
            # therefore signals cannot exceed this quantity.
            # Jitter enforces that not all nodes *can* emit a signal at each timestep, 
            # so the practical limit is much lower and mathematically constrainable.
            # for this example ~96k = len(all_nodes) * D_max is the practical limit.
            if len(self.signals)>4096:
                logging.error('Topology should be abandoned due to enumerable resources limit')
                self._abort = True

            #logging.debug(f'Checking Wavefronts @t={self.tick}')
            mask = []
            node_pos = [node.pos for node in self.all_nodes]
            for i, signal in enumerate(self.signals):
                #logging.debug(f'Wavefront: {signal.epicenter} @t={self.tick} -> {signal.radius_at(self.tick)}')
                if signal.epicenter is not None:
                    keep = self.check_points_outside(
                        signal.epicenter, 
                        signal.radius_at(self.tick), 
                        node_pos
                    )
                    if keep:
                        mask.append(i)
                    # else:
                    #     #logging.debug(f'All points within wavefront. Wavefront {signal} staged for pruning.')
            # if len(mask) < len(self.signals):
            #     #logging.debug(f'Pruning Signals {[self.signals[i] for i in range(len(self.signals)) if i not in mask]}')
            # else:
            #     #logging.debug(f'All Wavefronts Valid.')
            self.signals = [self.signals[i] for i in mask]

    def update_energy(self,):
        energy = 0
        for node in self.act_nodes:
            energy += node.stimulus
        self._energy_history.append(int(energy))

    def stage(self, stimulus: List[int]):
        for value in stimulus:
            signals = int_to_jitter(value, len(self.obs_nodes))
            #logging.debug(f'Stimulus Received: {value}')
            #logging.debug(f'Stimulus Processed: {signals}')
            for i, node in enumerate(self.obs_nodes):
                node.reflect()
                if not signals[i]:
                    incoming_signal = Signal(
                        None,
                        self.tick
                    ) 
                    node.stage(
                        incoming_signal,
                        self.tick
                    )

        new_signals = []
        for node in self.obs_nodes:
            node.commit()
            new_signal = node.response()
            node.record_history()
            if new_signal:
                new_signals.append(new_signal)

        self.signals.extend(new_signals)
        #logging.debug("Topology Staging Complete")
        # for i in range(len(self.obs_nodes)):
        #     #logging.debug(f"Obs_Node {i}: {self.obs_nodes[i]}")
        # #logging.debug(f"Topology {self.signals}")
        
    
    def response(self,):
        # while not in stasis - NON-HALTING, continue this loop, or only 1 tick
        
        logits = Counter()

        stasis = False
        self.update_energy()
        #Actual Hard Upper Bound = <= 255k + D_max, where D_max = maximum distance between 2 nodes.
        #(Max - Min) * k + sqrt((Max - Min) ** 2 + (Max - Min) ** 2)
        max_iter = (Node.MAX - Node.MIN) * (len(self.act_nodes))
        for i in range(max_iter):
            for node in self.act_nodes:
                node.reflect()
                for signal in self.signals:
                    node.stage(signal, self.tick)

            new_signals = []
            for node in self.act_nodes:
                node.commit()
                new_signal = node.response()
                node.record_history()
                if new_signal:
                    #logging.debug(f'Act_Node propagated new signal @t={self.tick}')
                    new_signals.append(new_signal)
            
            self.prune_signals() # before tick change
            self.signals.extend(new_signals)
            #logging.debug(f'Signal Count: {len(self.signals)}')
            self.tick += 1
            self.update_energy()
            stasis = self._energy_history[-1] == self._energy_history[-2]
            state = self.get_state()
            res = self.lut.lookup(state, self.action_space)
            if res is not None:
                logits.update([res])

            if len(self.signals) == 0 and stasis:
                #logging.debug(f"Stasis encountered at timestep {self.tick}. Terminating Early.")
                break

            if self._abort:
                #logging.debug('Aborting to avoid RuntimeOOMError.')
                break

        return logits
        
    def get_state(self,):
        """
            Retrieve which act_nodes are activated
        """
        return np.array([node.triggered for node in self.act_nodes])


    def plot(self,):
        # Stimulus over time
        plt.gca().set_aspect('equal')
        final_pos = np.array([node.pos for node in self.all_nodes])
        plt.xlim(final_pos.min() - 2, final_pos.max() + 2)
        plt.ylim(final_pos.min() - 2, final_pos.max() + 2)
        # plt.figure(figsize=(8,4))
        
        
        for i, t in enumerate(self.all_nodes):
            plt.plot([x for x in t.stimulus_history], label=f"Tower {i}")
        plt.legend()
        plt.xlabel('Tick')
        plt.ylabel('Stimulus Value')
        plt.title('Stimulus Value Over Time (Per Tower)')
        plt.show()

    def render(self,):
        final_stimuli = np.array([node.stimulus for node in self.all_nodes])
        final_pos = np.array([node.pos for node in self.all_nodes])
        clims = (final_stimuli.min(), final_stimuli.max() + 1e-6)
        # plt.figure(figsize=(8,7))
        plt.scatter(
            final_pos[:,0], 
            final_pos[:,1], 
            s=200, 
            c=final_stimuli, 
            cmap='hot', 
            edgecolor='k', 
            vmin=clims[0], 
            vmax=clims[1]
        )
        plt.colorbar(label='Stimulus')
        # FOVs
        for node in self.all_nodes:
            for fov in node.fovs:
                angle_deg = np.degrees(fov[0]) #center
                width_deg = np.degrees(fov[1]) #width
                wedge = mpatches.Wedge(
                    (node.pos[0], node.pos[1]), 
                    10,
                    angle_deg-width_deg/2, 
                    angle_deg+width_deg/2,
                    color='cyan', 
                    alpha=0.14, 
                    edgecolor='b', 
                    linewidth=1.0
                )
                plt.gca().add_patch(wedge)
        axes = plt.gca()
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)

        for signal in self.signals:
            signal.plot_wavefront(self.tick)
        plt.gca().set_aspect('equal')
        plt.show()