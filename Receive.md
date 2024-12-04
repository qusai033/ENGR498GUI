Traceback (most recent call last):
  File "/home/tuser/Desktop/ENGR498/ENGR498GUI/fd.py", line 24, in <module>
    increasing = all(data['Delta T'][1:] >= data['Delta T'][:-1])
  File "/home/tuser/.local/lib/python3.10/site-packages/pandas/core/ops/common.py", line 76, in new_method
    return method(self, other)
  File "/home/tuser/.local/lib/python3.10/site-packages/pandas/core/arraylike.py", line 60, in __ge__
    return self._cmp_method(other, operator.ge)
  File "/home/tuser/.local/lib/python3.10/site-packages/pandas/core/series.py", line 6114, in _cmp_method
    raise ValueError("Can only compare identically-labeled Series objects")
ValueError: Can only compare identically-labeled Series objects
