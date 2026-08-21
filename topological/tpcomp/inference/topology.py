from typing import List, Int
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import logging
from tpcomp.inference.jitter import int_to_jitter
from tpcomp.constructs.node import Node
from tpcomp.constructs.signal import Signal

class Topology:
    def __init__(self, genome):
        self.genome = genome
        act_chrom = genome.sequence.get('actions')
        obs_chrom = genome.sequence.get('observations')

        self.obs_nodes = []
        for chrom in obs_chrom.values():
            pos = chrom.sequence[0] 
            decay = chrom.sequence[1]
            stim_amp = chrom.sequence[2]
            vel_amp = chrom.sequence[3]
            sensitivity = chrom.sequence[4]
            fovs = []
            self.obs_nodes.append(
                Node(
                    pos,
                    decay,
                    stim_amp,
                    vel_amp,
                    sensitivity,
                    fovs
                )
            )

        self.act_nodes = []
        for chrom in act_chrom.values():
            pos = chrom.sequence[0]
            decay = chrom.sequence[1]
            stim_amp = chrom.sequence[2]
            vel_amp = chrom.sequence[3]
            sensitivity = chrom.sequence[4]
            fovs = [
                [chrom.sequence[5], chrom.sequence[6]],
                [chrom.sequence[7], chrom.sequence[8]]
            ]
            self.act_nodes.append(
                Node(
                    pos,
                    decay,
                    stim_amp,
                    vel_amp,
                    sensitivity,
                    fovs
                )
            )

        self.all_nodes = [*self.obs_nodes]
        self.all_nodes.extend(self.act_nodes)
        
        self.velocity = 1
        self.tick = 0
        self.signals = []
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
        xc, yc = center
        r_sq = radius ** 2
        
        for px, py in points:
            # Calculate squared distance
            dist_sq = (px - xc)**2 + (py - yc)**2
            if dist_sq > r_sq:
                return True # Found a point outside
                
        return False # All nodes are inside or on the wavefront


    def prune_signals(self,):
        """
            Remove signals whose wavefront has encompassed all nodes
        """
        if len(self.signals)>999:
            logging.error('Topology abandoned due to enumerable resources limit')
            self._abort = True

        mask = []
        node_pos = [node.pos for node in self.all_nodes]
        for i, signal in enumerate(self.signals):
            if signal.epicenter is not None:
                keep = self.check_points_outside(
                    signal.epicenter, 
                    signal.radius_at(self.tick), 
                    node_pos
                )
                if keep:
                    mask.append(i)
        
        self.signals = [self.signals[i] for i in mask]


    def stage(self, stimulus: List[Int]):
        for value in stimulus:
            signals = int_to_jitter(value)
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
        
    
    def response(self,):
        # while not in stasis - NON-HALTING
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
                new_signals.append(new_signal)
        
        self.prune_signals() # before tick change
        self.signals.extend(new_signals)
        self.tick += 1

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

    

            










# -------------------------------------------------


    # def possible_states(self,):
    #     # arr = [i for i in range(len(self.synapses))]
    #     # n = len(arr)
    #     # res = []

    #     # # Loop through all possible subsets
    #     # for i in range(1 << n):
    #     #     subset = []

    #     #     # Loop through all elements
    #     #     for j in range(n):
            
    #     #         # Check if jth bit is set
    #     #         if i & (1 << j):
    #     #             subset.append(arr[j])

    #     #     # Add subset to result
    #     #     res.append(subset)

    #     # return res
    #     s = list(range(len(self.synapses)))
    #     return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    # def state_action_mapping(self, n_actions):
    #     # states = list(self.possible_states())
    #     # mapping = {i: [] for i in range(n_actions)}
    #     # for action, state in enumerate(states):
    #     #     mapping[action%n_actions].append(state)

    #     states = list(self.possible_states())
    #     mapping = {}
    #     for action, state in enumerate(states):
    #         mapping[tuple(state)] = int(action%n_actions)
    #     return mapping

    # def get_action_from_state(self, subset, n_actions):
    #     """
    #     Returns the index of a sorted subset in the lexicographically ordered powerset
    #     of a sorted original list.

    #     Args:
    #         original_list: The sorted list representing the original set.
    #         subset: The sorted list representing the subset.

    #     Returns:
    #         The integer index of the subset in the powerset.
    #     """
    #     # Ensure both lists are sorted for the binary counting method to work correctly

    #     # Create a mapping from element value to its index in the original list
    #     elem_to_index = {elem: i for i, elem in enumerate(list(range(len(self.synapses))))}

    #     index = 0
    #     # Iterate through the subset elements and set the corresponding bit in the index
    #     for elem in subset:
    #         if elem in elem_to_index:
    #             # The bit position corresponds to the element's index in the original list.
    #             # We use bitwise OR to set the bit.
    #             # The order in the powerset generally corresponds to standard binary counting.
    #             # The snippet builds the index in a way that the 0-th element corresponds to the 0-th bit (1<<0)
    #             # This bit corresponds to the least significant position. The following logic ensures that.
    #             bit_position = elem_to_index[elem]
    #             index |= (1 << bit_position)
    #         else:
    #             # Handle cases where the element is not in the original list (error or unexpected input)
    #             raise ValueError(f"Element {elem} not found in original list")

    #     action = index % n_actions
    #     return action