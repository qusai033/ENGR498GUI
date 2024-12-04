 
/home/tuser/Desktop/ENGR498/ENGR498GUI/fd.py:16: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.


  data['Delta T'].fillna(0.0, inplace=True)
Traceback (most recent call last):
  File "/home/tuser/Desktop/ENGR498/ENGR498GUI/fd.py", line 22, in <module>
    increasing = all(data['Delta T'][1:] >= data['Delta T'][:-1])
  File "/home/tuser/.local/lib/python3.10/site-packages/pandas/core/ops/common.py", line 76, in new_method
    return method(self, other)
  File "/home/tuser/.local/lib/python3.10/site-packages/pandas/core/arraylike.py", line 60, in __ge__
    return self._cmp_method(other, operator.ge)
  File "/home/tuser/.local/lib/python3.10/site-packages/pandas/core/series.py", line 6114, in _cmp_method
    raise ValueError("Can only compare identically-labeled Series objects")
ValueError: Can only compare identically-labeled Series objects
