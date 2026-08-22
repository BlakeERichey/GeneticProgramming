import numpy as np
import gymnasium as gym
from tpcomp.inference import Topology
from tpcomp.solver import Genome
from datetime import datetime
import logging
# logging.getLogger().setLevel(logging.DEBUG)

import cProfile, pstats, io
def profile(fnc):
  """A decorator that uses cProfile to profile a function"""
  
  def inner(*args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()
    retval = fnc(*args, **kwargs)
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(0.5)
    print(s.getvalue())
    return retval

  return inner

@profile
def main():
    genome = Genome(n_obs=255, n_act=10)
    top = Topology(genome)

    stream = np.random.randint(0, 256, 784)
    top.stage(stream)
    response = top.response()
    print(response)
    print(response.most_common())
    print(top._energy_history)
    top.reset()

    # print(top)
main()


# Ordered by: cumulative time
#    List reduced from 112 to 56 due to restriction <0.5>

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    8.048    8.048 mnist.py:27(main)
#         1    0.397    0.397    6.944    6.944 tpcomp\inference\topology.py:157(response)
#   1305824    1.343    0.000    5.389    0.000 tpcomp\constructs\node.py:36(stage)
#   1305759    2.890    0.000    4.024    0.000 tpcomp\constructs\node.py:59(ignore)
#       605    0.144    0.000    1.757    0.003 tpcomp\inference\topology.py:89(prune_signals)
#    121048    1.489    0.000    1.521    0.000 tpcomp\inference\topology.py:71(check_points_outside)
#   2541878    0.785    0.000    1.199    0.000 tpcomp\constructs\signal.py:10(radius_at)
#         1    0.155    0.155    1.092    1.092 tpcomp\inference\topology.py:125(stage)
#   2749058    0.456    0.000    0.456    0.000 {built-in method builtins.max}
#    205970    0.090    0.000    0.133    0.000 tpcomp\constructs\node.py:32(reflect)
#       605    0.009    0.000    0.128    0.000 tpcomp\solver\chromosome.py:90(lookup)
#      1210    0.003    0.000    0.112    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:1685(_array_str_implementation)
#      1210    0.006    0.000    0.108    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:605(array2string)
#      1210    0.004    0.000    0.090    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:550(wrapper)
#      1210    0.008    0.000    0.084    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:567(_array2string)
#      1210    0.002    0.000    0.064    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:828(_formatArray)
# 10890/1210    0.029    0.000    0.062    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:837(recurser)
#    226160    0.051    0.000    0.051    0.000 {method 'append' of 'list' objects}
#      6305    0.027    0.000    0.039    0.000 tpcomp\constructs\node.py:46(commit)
#    121064    0.032    0.000    0.032    0.000 {method 'tolist' of 'numpy.ndarray' objects}
#      9680    0.009    0.000    0.028    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:801(_extendLine_pretty)
#     95618    0.018    0.000    0.019    0.000 tpcomp\constructs\signal.py:3(__init__)
#      9680    0.010    0.000    0.015    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:787(_extendLine)
#     96567    0.011    0.000    0.011    0.000 {built-in method builtins.min}
#      1210    0.006    0.000    0.011    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:496(_get_format_function)
#      1210    0.006    0.000    0.011    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:50(_make_options_dict)
#     70982    0.010    0.000    0.010    0.000 {built-in method builtins.len}
#         1    0.000    0.000    0.008    0.008 tpcomp\solver\genome.py:4(__init__)
#       255    0.001    0.000    0.007    0.000 tpcomp\solver\chromosome.py:22(__init__)
#       605    0.002    0.000    0.007    0.000 tpcomp\inference\topology.py:201(get_state)
#      1111    0.006    0.000    0.006    0.000 tpcomp\solver\gene.py:9(random)
#      1741    0.006    0.000    0.006    0.000 {built-in method numpy.array}
#      6305    0.003    0.000    0.004    0.000 tpcomp\constructs\node.py:87(record_history)
#      1210    0.004    0.000    0.004    0.000 {built-in method builtins.locals}
#      6305    0.002    0.000    0.004    0.000 tpcomp\constructs\node.py:53(response)
#      1210    0.002    0.000    0.004    0.000 \AppData\Local\Programs\Python\Python313\Lib\logging\__init__.py:2197(debug)
#      1210    0.003    0.000    0.003    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:446(_get_formatdict)
#       784    0.003    0.000    0.003    0.000 tpcomp\inference\jitter.py:2(int_to_jitter)
#     12355    0.003    0.000    0.003    0.000 tpcomp\constructs\node.py:28(triggered)
#      9680    0.003    0.000    0.003    0.000 {method 'splitlines' of 'str' objects}
#      1210    0.002    0.000    0.002    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:453(<lambda>)
#         2    0.001    0.000    0.002    0.001 tpcomp\inference\topology.py:12(__init__)
#      9680    0.002    0.000    0.002    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:1306(__call__)
#       605    0.002    0.000    0.002    0.000 {built-in method builtins.any}
#      1210    0.001    0.000    0.001    0.000 \AppData\Local\Programs\Python\Python313\Lib\logging\__init__.py:1497(debug)
#       530    0.000    0.000    0.001    0.000 tpcomp\constructs\node.py:10(__init__)
#         1    0.000    0.000    0.001    0.001 tpcomp\inference\topology.py:64(reset)
#       606    0.001    0.000    0.001    0.000 tpcomp\inference\topology.py:119(update_energy)
#         3    0.001    0.000    0.001    0.000 {built-in method builtins.print}
#      1476    0.001    0.000    0.001    0.000 {method 'update' of 'dict' objects}
#      1210    0.001    0.000    0.001    0.000 {method 'rstrip' of 'str' objects}
#        10    0.000    0.000    0.001    0.000 tpcomp\solver\chromosome.py:40(__init__)
#      2420    0.001    0.000    0.001    0.000 {method 'get' of '_contextvars.ContextVar' objects}
#      1210    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
#      1210    0.001    0.000    0.001    0.000 \AppData\Local\Programs\Python\Python313\Lib\site-packages\numpy\_core\arrayprint.py:1301(__init__)
#      1210    0.001    0.000    0.001    0.000 {method 'copy' of 'dict' objects}