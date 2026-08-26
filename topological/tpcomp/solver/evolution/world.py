import numpy as np
class World():
  def __init__(self, organism_cls, env):
    
    """
      Manages action predictions for networks interfacing with an environment.
      Implicitly determines if a Time distributed observation is necessary, 
      and evaluates model predictions into interpretable actions.
    """

    self.env = env
    self.organism_cls = organism_cls
  
  def run(self, individual, max_steps, render=False):
    """
      Runs an environment through to completion taking models best determined 
      actions.
    """

    stimulus = self.env.reset()

    done = False
    rewards = []
    remaining_steps = max_steps
    organism = self.organism_cls(genome=individual.genome)
    while not done and remaining_steps:
      action = organism.response(stimulus, deadline=None)

      #take action
      stimulus, reward, done, success = self.env.step(action)
      rewards.append(reward)

      if render:
        self.env.render()
    
    return rewards

