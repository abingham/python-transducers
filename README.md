python-transducers
==================

Transducers for Python.

Transducers are a concept from clojure, or at least that's where I
heard of them first. A *transducer* is a function that takes a
*reducer* (i.e. the kind of function you would pass to
`functools.reduce`) and returns another reducer. Transducers are a
distillation of concepts like mapping and filtering (among other
things) that are easily composable.

Note that this module is largely an exercise is "seeing how it works."
It's not clear if there are any real practical benefits to using
transducers in Python. While they do provide a certain conceptual
clarity and have some pleasing properties, they may be slow, limited
in applicability, and perhaps even non-Pythonic by some measure.

For more information, see
[Transducers are coming](http://blog.cognitect.com/blog/2014/8/6/transducers-are-coming)
and the earlier
[Anatomy of a reducer](http://clojure.com/blog/2012/05/15/anatomy-of-reducer.html),
both by Rich Hickey.

Quickstart
==========

Here's how you can implement Rich Hickey's example ``((def xform (comp
(map inc) (filter even?)))`` using `transducers`.

```python
from transducers import compose, filtering, mapping

# A reducer for appending to a list.
def append(l, item):
    l.append(item)
    return l

# a transducer that maps "x + 1" over input values
inc = mapping(lambda x: x + 1)

# a transducer that filters out odd values
evens = filtering(lambda x: x % 2 == 0)

# a composite transducer of inc and evens -> inc(evens(seq))
odds = compose(inc, events)

# Apply the composite transducer to the first 10 non-negative integers,
# building a list out of the results.
x = reduce(odds(append), range(10), list())

# See that you've indeed got [1, 3, 5, 7, 9]
assert x == list(range(1, 10, 2))
```
