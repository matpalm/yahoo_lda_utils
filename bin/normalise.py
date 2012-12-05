#!/usr/bin/env python
import math

# from ruby statistics2
def p_normal_dist(qn):
  b = [1.570796288, 0.03706987906, -0.8364353589e-3,
       -0.2250947176e-3, 0.6841218299e-5, 0.5824238515e-5,
       -0.104527497e-5, 0.8360937017e-7, -0.3231081277e-8,
       0.3657763036e-10, 0.6936233982e-12]
  if qn == 0.5 or qn <= 0.0 or qn >= 1.0:
    return 0
  w1 = 1.0 - qn if qn > 0.5 else qn
  w3 = -math.log(4.0 * w1 * (1.0 - w1))
  w1 = 0
  for i, bb in enumerate(b):
    w1 += b[i] * w3 ** i
  return math.sqrt(w1 * w3) if qn > 0.5 else -math.sqrt(w1 * w3) 

# from http://en.wikipedia.org/wiki/Wilson_score_interval#Wilson_score_interval
def wilson_score_interval(p, n, confidence):
  if n == 0:
    return 0
  p_hat = float(p) / n
  z = p_normal_dist(1 - (1 - confidence) / 2)
  z_s = z * z
  numerator_lhs = p_hat + z_s / (2 * n) 
  numerator_rhs = z * math.sqrt(((p_hat * (1 - p_hat) / n) + (z_s / (4 * n * n))))
  denominator = 1 + z_s / n  
  return [(numerator_lhs - numerator_rhs) / denominator, (numerator_lhs + numerator_rhs) / denominator]

def l1_norm(data):
  return [float(d) / sum(data) for d in data]

def wilson_lower_bound(data, confidence=0.999):
  return [wilson_score_interval(d, sum(data), confidence)[0] for d in data]

# high egs
egs = [[23700, 20, 1060, 11, 4],
       [1581, 889, 20140, 1967, 200],
       [1, 0, 1, 76, 0 ],
       [22, 0, 0, 0, 0 ]]

for eg in egs:
  print "eg\t", eg
  print "l1_norm\t", l1_norm(eg)
  wlb = wilson_lower_bound(eg)
  print "wlb\t", wlb, "left over", 1.0 - sum(wlb)
  print

