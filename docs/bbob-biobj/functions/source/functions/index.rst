.. _sec-test-functions:

======================================================
The ``bbob-biobj`` Test Functions and Their Properties
======================================================

In the following, we detail all 55 ``bbob-biobj`` functions
and their properties.

.. todo::
   Eventually, the following shall be provided for each function:

   - its definition and relation to the ``bbob`` test suite (function ids for example)
   - plots of the best known approximations of the Pareto set and the Pareto front
   - potentially the outcomes of example algorithms
   - plots (in objective space) of randomly sampled search points
   - potentially function value distributions along cuts through the search space

Quick access to the functions: :ref:`f1 <f1>`, :ref:`f2 <f2>`, :ref:`f3 <f3>`,
:ref:`f4 <f4>`, :ref:`f5 <f5>`, :ref:`f6 <f6>`, :ref:`f7 <f7>`,
:ref:`f8 <f8>`, :ref:`f9 <f9>`, :ref:`f10 <f10>`, :ref:`f11 <f11>`,
:ref:`f12 <f12>`, :ref:`f13 <f13>`, :ref:`f14 <f14>`, :ref:`f15 <f15>`,
:ref:`f16 <f16>`, :ref:`f17 <f17>`, :ref:`f18 <f18>`, :ref:`f19 <f19>`,
:ref:`f20 <f20>`, :ref:`f21 <f21>`, :ref:`f22 <f22>`, :ref:`f23 <f23>`,
:ref:`f24 <f24>`, :ref:`f25 <f25>`, :ref:`f26 <f26>`, :ref:`f27 <f27>`,
:ref:`f28 <f28>`, :ref:`f29 <f29>`, :ref:`f30 <f30>`, :ref:`f31 <f31>`,
:ref:`f32 <f32>`, :ref:`f33 <f33>`, :ref:`f34 <f34>`, :ref:`f35 <f35>`,
:ref:`f36 <f36>`, :ref:`f37 <f37>`, :ref:`f38 <f38>`, :ref:`f39 <f39>`,
:ref:`f40 <f40>`, :ref:`f41 <f41>`, :ref:`f42 <f42>`, :ref:`f43 <f43>`,
:ref:`f44 <f44>`, :ref:`f45 <f45>`, :ref:`f46 <f46>`, :ref:`f47 <f47>`,
:ref:`f48 <f48>`, :ref:`f49 <f49>`, :ref:`f50 <f50>`, :ref:`f51 <f51>`,
:ref:`f52 <f52>`, :ref:`f53 <f53>`, :ref:`f54 <f54>`, :ref:`f55 <f55>`.


Some Function Properties
------------------------
In the description of the 55 ``bbob-biobj`` functions below, several
general properties of objective functions will be mentioned that
shall be quickly defined here.

A *separable* function does not show any dependencies between the
variables and can therefore solves by applying :math:`D` consecutive
one-dimensional optimizations along the coordinate axes while
keeping the other variables fixed. Consequently, *non-separable*
problems must be considered much more difficult and most of the
proposed benchmark functions are designed being non-separable. The
typical well-established technique to generate non-separable
functions from separable ones is the application of a rotation matrix
:math:`\mathbf R`.

A *unimodal* function has only one local minimum which is at the same
time also its global one. The opposite is a *multimodal* function
which appears to have at least one local minimum and which is
highly common in practical optimization problems.

*Ill-conditioning* is a another typical challenge in real-parameter
optimization and, besides multimodality, probably the most common one.
Conditioning of a function can be rigorously formalized in the
case of convex quadratic functions,
:math:`f(x) = \frac{1}{2} x^THx` where :math:`H` is a symmetric
positive definite matrix, as the condition number of the Hessian matrix
:math:`H`. Since contour lines associated to a convex quadratic function
are ellipsoids, the condition number corresponds to the square root of
the ratio between the largest axis of the ellipsoid and the shortest axis.
For more general functions, conditioning loosely refers to the square of
the ratio between the largest and smallest direction of a contour line. 
The proposed ``bbob-biobj`` testbed contains ill-conditioned functions
with a typical conditioning of :math:`10^6`. We believe this a realistic
requirement, while we have seen practical problems with conditioning
as large as :math:`10^{10}`.




   

The 55 ``bbob-biobj`` Functions
-------------------------------

.. _f1:

:math:`f_1`: Sphere/Sphere
^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of two sphere functions (:math:`f_1` in the ``bbob`` suite).

Both objectives are unimodal, highly symmetric, rotational and scale
invariant. The Pareto set is known to be a straight line and the Pareto 
front is convex. Considered as the simplest bi-objective problem in
continuous domain.

Contained in the *separable - separable* function class.


Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* What is the optimal convergence rate of a bi-objective algorithm?


.. _f2:

:math:`f_2`: Sphere/Ellipsoid separable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and separable ellipsoid function (:math:`f_2` in the ``bbob`` suite).

Both objectives are unimodal and separable. While the first objective is
truly convex-quadratic with a condition number of 1, the second
objective is only globally quadratic with smooth local
irregularities and highly ill-conditioned with a condition number of
about :math:`10^6`.

Contained in the *separable - separable* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to :math:`f_1`: Is symmetry exploited?


.. _f3:

:math:`f_3`: Sphere/Attractive sector
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and attractive sector function (:math:`f_6` in the ``bbob`` suite).

Both objective functions are unimodal, but only the first objective is
separable and truly convex quadratic. The attractive sector
function is highly asymmetric, where only one *hypercone* (with
angular base area) with a volume of roughly :math:`(1/2)^D`
yields low function values. The optimum of it is located at the tip
of this cone. This function can be deceptive for cumulative step
size adaptation.

Contained in the *separable - moderate* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to :math:`f_1` and :math:`f_{20}`:  What is the
  effect of a highly asymmetric landscape in both or one
  objective?


  
.. _f4:

:math:`f_4`: Sphere/Rosenbrock original
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and original, i.e., unrotated Rosenbrock function (:math:`f_8` in the
``bbob`` suite).

The first objective is separable and truly convex, the second
objective is partially separable (tri-band structure). The first
objective is unimodal while the second objective has a local
optimum with an attraction volume of about 25\%.

Contained in the *separable - moderate* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* Can the search follow a long path with :math:`D-1` changes in
  the direction when it approaches one of the extremes of the
  Pareto front/Pareto set?





.. _f5:

:math:`f_5`: Sphere/Sharp ridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and sharp ridge function (:math:`f_{13}` in the ``bbob`` suite).

Both objective functions are unimodal.
In addition to the simple, separable, and differentiable first
objective, a sharp, i.e., non-differentiable ridge has to be
followed for optimizing the (non-separable) second objective. The
gradient towards the ridge remains constant, when the ridge is
approached from a given point.
Approaching the ridge is initially effective, but becomes ineffective
close to the ridge when the rigde needs to be followed in direction
to its optimum.  The necessary change in *search behavior* close to
the ridge is diffiult to diagnose, because the gradient
towards the ridge does not flatten out.

Contained in the *separable - ill-conditioned* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* Can the search continuously change its search direction when
  approaching one of the extremes of the Pareto front/Pareto set?
* What is the effect of having a non-smooth, non-differentiabale
  function to optimize?


.. _f6:

:math:`f_6`: Sphere/Sum of different powers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and sum of different powers function (:math:`f_{14}` in the ``bbob``
suite).

Both objective functions are unimodal. The first objective is
separable, the second non-separable.
When approaching the second objective's optimum, the sensitivies
of the variables in the rotated search space become more and
more different. In addition, the second objective function
possesses a small solution volume.

.. todo::

   the above text should be checked for clarity and correctness


Contained in the *separable - ill-conditioned* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
.. todo::

   to be written
   

.. _f7:

:math:`f_7`: Sphere/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and Rastrigin function (:math:`f_{15}` in the ``bbob`` suite).

In addition to the simple sphere function, the prototypical highly
multimodal Rastrigin function needs to be solved which has originally
a very regular and symmetric structure for the placement of the optima.
Here, however, transformations are performed to alleviate
the original symmetry and regularity in the second objective.

The properties of the second objective contain non-separabilty,
multimodality (roughly :math:`10^D` local optima), a conditioning of
about 10, and a large global amplitude compared to the local amplitudes.

Contained in the *separable - multi-modal* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* With respect to fully unimodal functions: what is the effect of
  multimodality?

  
.. _f8:

:math:`f_8`: Sphere/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and Schaffer F7 function with condition number 10 (:math:`f_{17}` in
the ``bbob`` suite).

In addition to the simple sphere function, an asymmetric, non-separable,
and highly multimodal function needs to be solved to approach the Pareto
front/Pareto set where the frequency and amplitude of the modulation
in the second objective vary. The conditioning of the second objective
and thus the entire bi-objective function is low.

Contained in the *separable - multi-modal* function class.


Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to :math:`f_7` and :math:`f_{50}`:  What is the
  effect of multimodality on a less regular function?


.. _f9:

:math:`f_9`: Sphere/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and Schwefel function (:math:`f_{20}` in the ``bbob`` suite).

While the first objective function is separable and unimodal,
the second objective function is partially separable and highly
multimodal---having the most prominent :math:`2^D` minima located
comparatively close to the corners of the unpenalized search area. 

Contained in the *separable - weakly-structured* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to e.g. :math:`f_8`: What is the effect of a weak
  global structure?

  
.. _f10:

:math:`f_{10}`: Sphere/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of sphere function (:math:`f_1` in the ``bbob`` suite)
and Gallagher function with 101 peaks (:math:`f_{21}` in the ``bbob``
suite).

While the first objective function is separable and unimodal,
the second objective function is non-separable and consists
of 101 optima with position and height being unrelated and
randomly chosen (different for each instantiation of the function).
The conditioning around the global optimum of the second
objective function is about 30.

Contained in the *separable - weakly-structured* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* Is the search effective without any global structure?


.. _f11:

:math:`f_{11}`: Ellipsoid separable/Ellipsoid separable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of two separable ellipsoid functions (:math:`f_2` in the
``bbob`` suite).

Both objectives are unimodal, separable, only globally
quadratic with smooth local irregularities, and highly
ill-conditioned with a condition number of
about :math:`10^6`.

Contained in the *separable - separable* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to :math:`f_1`: Is symmetry exploited?


.. _f12:

:math:`f_{12}`: Ellipsoid separable/Attractive sector
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and attractive sector function (:math:`f_{6}`
in the ``bbob`` suite).

Both objective functions are unimodal but only the first
one is separable. The first objective function, in addition,
is globally quadratic with smooth local irregularities, and
highly ill-conditioned with a condition number of about
:math:`10^6`. The second objective function is highly
asymmetric, where only one *hypercone* (with
angular base area) with a volume of roughly :math:`(1/2)^D`
yields low function values. The optimum of it is located at
the tip of this cone. This function can be deceptive for
cumulative step size adaptation.

Contained in the *separable - moderate* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to, for example, :math:`f_1`: Is symmetry exploited?


.. _f13:

:math:`f_{13}`: Ellipsoid separable/Rosenbrock original
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and original, i.e., unrotated Rosenbrock function
(:math:`f_{8}`
in the ``bbob`` suite).


Only the first objective is separable and unimodal. The second
objective is partially separable (tri-band structure) and has a local
optimum with an attraction volume of about 25\%.
In addition, the first objective function shows smooth local
irregularities from a globally convex quadratic function and is
highly ill-conditioned with a condition number of about
:math:`10^6`. 

Contained in the *separable - moderate* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* Can the search handle highly conditioned functions and follow a long
  path with :math:`D-1` changes in the direction when it approaches the
  Pareto front/Pareto set?


.. _f14:

:math:`f_{14}`: Ellipsoid separable/Sharp ridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and sharp ridge function (:math:`f_{13}`
in the ``bbob`` suite).

Both objective functions are unimodal but only the first one is
separable.

The first objective is globally quadratic but with smooth local
irregularities and highly ill-conditioned with a condition number of
about :math:`10^6`. For optimizing the second objective, a sharp,
i.e., non-differentiable ridge has to be followed.

Contained in the *separable - ill-conditioned* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* Can the search continuously change its search direction when
  approaching one of the extremes of the Pareto front/Pareto set?
* What is the effect of having to solve both a highly-conditioned
  and a non-smooth, non-differentiabale function to approximate
  the Pareto front/Pareto set?


.. _f15:

:math:`f_{15}`: Ellipsoid separable/Sum of different powers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and sum of different powers function
(:math:`f_{14}` in the ``bbob`` suite).

Both objective functions are unimodal but only the first one is
separable.

The first objective is globally quadratic but with smooth local
irregularities and highly ill-conditioned with a condition number of
about :math:`10^6`. When approaching the second objective's optimum,
the sensitivies of the variables in the rotated search space become
more and more different.

Contained in the *separable - ill-conditioned* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* Can the Pareto front/Pareto set be approached when both a
  highly conditioned function and a function, the conditioning
  of which increases when approaching the optimum, must be solved?

.. _f16:

:math:`f_{16}`: Ellipsoid separable/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and Rastrigin function (:math:`f_{15}`
in the ``bbob`` suite).

The objective functions show rather opposite properties.
The first one is separable, the second not. The first one
is unimodal, the second highly multimodal (roughly :math:`10^D` local
optima). The first one s highly ill-conditioning (condition number of
:math:`10^6`), the second one has a conditioning of about 10. Local
non-linear transformations are performed in both objective functions
to alleviate the original symmetry and regularity of the two
baseline functions.

Contained in the *separable - multi-modal* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* With respect to fully unimodal functions: what is the effect of
  multimodality?
* With respect to low-conditioned problems: what is the effect of
  high conditioning?



.. _f17:

:math:`f_{17}`: Ellipsoid separable/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and Schaffer F7 function with condition number 10
(:math:`f_{17}` in the ``bbob`` suite).

Also here, both single objectives possess opposing properties.
The first objective is unimodal, besides small local non-linearities symmetric,
separable and highly ill-conditioned while the second objective is highly
multi-modal, asymmetric, and non-separable, with only a low conditioning.

Contained in the *separable - multi-modal* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* What is the effect of the opposing difficulties posed by the
  single objectives when parts of the Pareto front (at the extremes, in the
  middle, ...) are explored?

  
.. _f18:

:math:`f_{18}`: Ellipsoid separable/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and Schwefel function (:math:`f_{20}`
in the ``bbob`` suite).

The first objective is unimodal, separable and highly ill-conditioned.
The second objective is partially separable and highly multimodal---having
the most prominent :math:`2^D` minima located comparatively close to the
corners of the unpenalized search area. 


Contained in the *separable - weakly-structured* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""

.. todo::
   Give some details.



.. _f19:

:math:`f_{19}`: Ellipsoid separable/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of separable ellipsoid function (:math:`f_2` in the
``bbob`` suite) and Gallagher function with 101 peaks (:math:`f_{21}`
in the ``bbob`` suite).

The first objective is unimodal, besides small local non-linearities symmetric,
separable and highly ill-conditioned while the second objective is highly

While the first objective function is separable, unimodal, and
highly ill-conditioned (condition number of about :math:`10^6`),
the second objective function is non-separable and consists
of 101 optima with position and height being unrelated and
randomly chosen (different for each instantiation of the function).
The conditioning around the global optimum of the second
objective function is about 30.

Contained in the *separable - weakly-structured* function class.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""

* Is the search effective without any global structure?
* What is the effect of the different condition numbers
  of the two objectives, in particular when combined
  to reach the middle of the Pareto front?


.. _f20:

:math:`f_{20}`: Attractive sector/Attractive sector
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combination of two attractive sector functions (:math:`f_6`
in the ``bbob`` suite).
Both functions are unimodal and highly asymmetric, where only one
*hypercone* (with angular base area) per objective with a volume of
roughly :math:`(1/2)^D` yields low function values. The objective
functions' optima are located at the tips of those two cones. This
function can be deceptive for cumulative step size adaptation.

Information gained from this function:
""""""""""""""""""""""""""""""""""""""
* In comparison to :math:`f_1` and :math:`f_{20}`:  What is the
  effect of a highly asymmetric landscape in both or one
  objective?


  
.. todo::
   finish with the last 25 functions

   
.. _f21:
   
:math:`f_{21}`: Attractive sector/Rosenbrock original
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f22:
   
:math:`f_{22}`: Attractive sector/Sharp ridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f23:
   
:math:`f_{23}`: Attractive sector/Sum of different powers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f24:
   
:math:`f_{24}`: Attractive sector/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f25:
   
:math:`f_{25}`: Attractive sector/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f26:
   
:math:`f_{26}`: Attractive sector/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f27:
   
:math:`f_{27}`: Attractive sector/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f28:
   
:math:`f_{28}`: Rosenbrock original/Rosenbrock original
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f29:
   
:math:`f_{29}`: Rosenbrock original/Sharp ridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f30:
   
:math:`f_{30}`: Rosenbrock original/Sum of different powers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f31:
   
:math:`f_{31}`: Rosenbrock original/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f32:
   
:math:`f_{32}`: Rosenbrock original/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f33:
   
:math:`f_{33}`: Rosenbrock original/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f34:
   
:math:`f_{34}`: Rosenbrock original/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f35:
   
:math:`f_{35}`: Sharp ridge/Sharp ridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f36:
   
:math:`f_{36}`: Sharp ridge/Sum of different powers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f37:
   
:math:`f_{37}`: Sharp ridge/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f38:
   
:math:`f_{38}`: Sharp ridge/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f39:
   
:math:`f_{39}`: Sharp ridge/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f40:
   
:math:`f_{40}`: Sharp ridge/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f41:
   
:math:`f_{41}`: Sum of different powers/Sum of different powers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f42:
   
:math:`f_{42}`: Sum of different powers/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f43:
   
:math:`f_{43}`: Sum of different powers/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f44:
   
:math:`f_{44}`: Sum of different powers/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f45:
   
:math:`f_{45}`: Sum of different powers/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f46:
   
:math:`f_{46}`: Rastrigin/Rastrigin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f47:
   
:math:`f_{47}`: Rastrigin/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f48:
   
:math:`f_{48}`: Rastrigin/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f49:
   
:math:`f_{49}`: Rastrigin/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f50:
   
:math:`f_{50}`: Schaffer F7, condition 10/Schaffer F7, condition 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f51:
   
:math:`f_{51}`: Schaffer F7, condition 10/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f52:
   
:math:`f_{52}`: Schaffer F7, condition 10/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f53:
   
:math:`f_{53}`: Schwefel x*sin(x)/Schwefel x*sin(x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f54:
   
:math:`f_{54}`: Schwefel x*sin(x)/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _f55:
   
:math:`f_{55}`: Gallagher 101 peaks/Gallagher 101 peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^