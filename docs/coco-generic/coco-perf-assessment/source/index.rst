.. title:: COCO: Performance Assessment

##############################
COCO: Performance Assessment
##############################

.. .. toctree::
   :maxdepth: 2

..
   sectnum::

.. |ftarget| replace:: :math:`I^{{\rm target},\theta}`
.. |nruns| replace:: :math:`\texttt{Ntrial}`
.. |DIM| replace:: :math:`n`
.. _2009: http://www.sigevo.org/gecco-2009/workshops.html#bbob
.. _2010: http://www.sigevo.org/gecco-2010/workshops.html#bbob
.. _2012: http://www.sigevo.org/gecco-2012/workshops.html#bbob
.. _BBOB-2009: http://coco.gforge.inria.fr/doku.php?id=bbob-2009-results
.. _BBOB-2010: http://coco.gforge.inria.fr/doku.php?id=bbob-2010-results
.. _BBOB-2012: http://coco.gforge.inria.fr/doku.php?id=bbob-2012
.. _GECCO: http://www.sigevo.org/gecco-2012/
.. _COCO: https://github.com/numbbo/coco
.. .. _COCO: http://coco.gforge.inria.fr
.. |ERT| replace:: :math:`\mathrm{ERT}`
.. |aRT| replace:: :math:`\mathrm{aRT}`
.. |dim| replace:: :math:`\mathrm{dim}`
.. |function| replace:: :math:`\mathrm{function}`
.. |instance| replace:: :math:`\mathrm{instance}`
.. |R| replace:: :math:`\mathbb{R}`
.. |I| replace:: :math:`\mathcal{I}`
.. |i| replace:: :math:`i`
.. |t| replace:: :math:`t`
.. |p| replace:: :math:`p`
.. |x| replace:: :math:`x`
.. |N| replace:: :math:`N`
.. |n| replace:: :math:`n`
.. |J| replace:: :math:`J`
.. |RTus| replace:: :math:`\mathrm{RT}^{\mathrm{us}}`
.. |RTs| replace:: :math:`\mathrm{RT}^{\mathrm{s}}`
.. |calP| replace:: :math:`\mathcal{P}`
.. |calP.| replace:: :math:`\mathcal{P}.`
.. |thetai| replace:: :math:`\theta_i`
.. |ftheta| replace::  :math:`f_{\theta}`


.. the next two lines are necessary in LaTeX. They will be automatically 
  replaced to put away the \chapter level as ^^^ and let the "current" level
  become \section. 

CHAPTERTITLE
?????????????????????????????????????????????????????????????????????????

.. raw:: html

   See: <I>ArXiv e-prints</I>,
   <A HREF="http://arxiv.org/abs/1605.xxxxx">arXiv:1605.xxxxx</A>, 2016.

.. raw:: latex

  % \tableofcontents is automatic with sphinx and moved behind the abstract 
  % by swap...py
  
  \begin{abstract}

We present an  any-time performance assessment for benchmarking numerical
optimization algorithms in a black-box scenario, applied within the COCO_ benchmarking platform. 
The performance assessment is based on *runtimes* measured in number of objective function evaluations to reach one or several quality indicator target values.
We argue that runtime is the only available measure with a generic, meaningful, and quantitative interpretation.
We discuss the choice of the target values, runlength-based targets, and the aggregation of results by using simulated restarts, averages, and empirical distribution functions. 

.. raw:: latex

  \end{abstract}
  \newpage


Introduction
=============

.. budget-free

This document presents the main ideas and concepts of the performance assessment
when benchmarking numerical optimization algorithms in a black-box scenario within the COCO_ platform. Going beyond a simple ranking of algorithms, we aim
to provide a *quantitative* and *meaningful* performance assessment, which
allows for conclusions like *algorithm A is seven times faster than algorithm
B* in solving a given problem or in solving problems with certain
characteristics. 
For this end, we record algorithm *runtimes*, measured in
number of function evaluations to reach predefined target values during the
algorithm run.

Runtimes represent the cost of the algorithm. Apart from a short, exploratory
experiment [#]_, we do not measure the algorithm cost in CPU or wall-clock time.
See for example [HOO1995]_ for a discussion on shortcomings and
unfortunate consequences of benchmarking based on CPU time.

We display average runtimes (aRT, see Section `Averaging Runtime`_)
and the empirical distribution function of runtimes (ECDF, see Section `Empirical Distribution Functions`_). 
When displaying runtime distributions, we consider the aggregation over 
target values and over subclasses of problems or all problems. 


.. We do not aggregate over dimension, because the dimension of the problem can be used to decide a priori which algorithm (or algorithm variant, or parameter setting) to use.

.. [#] The COCO_ platform provides a CPU timing experiment to get a rough estimate of the time complexity of the algorithm [HAN2016ex]_.


Terminology and Definitions
----------------------------

.. Tea: We have this section in every documentation and every time there are some differences
   between the definitions. Would it be possible to make this more uniform? I understand that
   some documents require more detailed definitions than others, but this could be solved
   differently. For example, (I'm not sure whether the reStructuredText even supports this,
   but I hope it does), the ideal approach would be to have all definitions in a single file
   and then only "pull" the ones that should be in this document here (the same goes for the
   other documents, of course). We could then even have short and long definition variants
   for the terms that require it.
   EDIT: I see now that this section is quite different from the sections with the same
   title in the other documents (i.e., here we go into more detail and explanation why
   things are done the way they are), so maybe my proposal is less suited here than in the
   other documentations (I think we should still consider to do this at least for the other
   documentations).
   
.. It will be nice to have an online glossary at some point that will help keeping things
   consistent.

   
We introduce a few terms and definitions that are used in the rest of the document.

   
*problem, function, indicator*
 In the COCO_ framework, a problem instance is defined as a triple  ``(dimension,
 function, instance)``. 
 In this terminology a ``function``, to be minimized, is parametrized by its input ``dimension`` and its ``instance`` parameters.
 
 More precisely, we consider a set of parametrized benchmark functions
 :math:`f_\theta: \mathbb{R}^n \to \mathbb{R}^m, `\theta \in \Theta`.
 A COCO_ problem derived from function |ftheta| corresponds to :math:`p = (n,
 f_\theta, \theta_i)` where :math:`n \in \mathbb{N}` is the dimension of the
 search space, and :math:`\theta_i` is the set of parameters associated to the
 ``instance`` |i|. 
 The separation of dimension and instance parameters is of entirely semantic
 nature, however meaningful because we always aggregate over all |thetai|-values while we never aggregate over dimension. 

 .. Given a dimension

   :math:`n` and two different instances :math:`\theta_1` and :math:`\theta_2` of
   the same parametrized family :math:`f_{\theta}`, optimizing the associated
   problems means optimizing :math:`f_{\theta_1}(\mathbf{x})` and
   :math:`f_{\theta_2}(\mathbf{x})` for :math:`\mathbf{x} \in \mathbb{R}^n`.
 
 In the performance assessment setting, we associate to a problem 
 instance :math:`p` a quality indicator and a target value, 
 such that a problem becomes a quintuple ``(dimension, function, instance, quality indicator, target)``. 
 Usually, the quality indicator remains the same for all problems, while we have sets of
 problems which only differ in their target value. 
 The first time the quality indicator drops below the target is considered the runtime to solve the problem. 
 The quality indicator target value depends in general on the problem instance :math:`\theta_i`. 
 
*instance*
 Our test functions are parametrized such that different *instances* of the same function are available. Different instances can vary by having different shifted optima, can use different rotations that are applied to the variables, ...  The notion of instance is introduced to generate repetition while avoiding possible exploitation of an artificial function property (like location of the optimum in zero).

 
 ..  We often **interpret different runs performed on different instances**
 .. of the same parametrized function in a given dimension as **independent
 .. repetitions** of the optimization algorithm on the same function. Put
 .. differently, the runs performed on :math:`K` different instances,
 .. :math:`f_{\theta_1}, \ldots,f_{\theta_K}`, of a parametrized problem
 .. :math:`f_\theta`, are assumed to be independent and identically
 .. distributed.

 .. Anne: maybe we should insist more on this dual view of randomizing the problem class via problem isntance - choosing uniformly over set of parameters.

 .. Tea: I'm not sure that our use of instances belongs under the definition of instances.
    I think this (important!) issue should be explained in more detail later, not here.

*runtime*
  We define *runtime*, or *run-length* [HOO1998]_
  as the *number of evaluations*, also referred to as *function* evaluations,
  conducted on a given problem until a given quality indicator target value is reached.
  Runtime is our central performance measure.


On Performance Measures
=======================

Evaluating performance is necessarily based on performance *measures*, the
definition of which plays a crucial role for the evaluation. 
Here, we introduce our requirements for performances measures in general and in
the context of black-box optimization. 
A performance measure in general should be

* quantitative, as opposed to a simple *ranking* of entrants (e.g., algorithms). 
  Ideally, the measure should be defined on a ratio scale (as opposed to an
  interval or ordinal scale) [STE1946]_, which allows to state that "entrant A
  is :math:`x` times better than entrant B". [#]_ 
* assuming a wide variation of values, for example, typical values should 
  not only be ranging between 0.98 and 1.0 [#]_,
* interpretable, in particular by having a meaning and semantics attached to 
  the measured numbers,
* relevant and meaningful with respect to the "real world",
* as simple and as comprehensible as possible.

.. Following [HAN2009ex]_, we advocate **performance measures** that are

.. Tea: Can we give some more explanation here?

In the context of black-box optimization, the **runtime** to reach a target value, measured in number of function evaluations, satisfies all requirements. 
Runtime is well-interpretable and meaningful with respect to the
real-world as it represents time needed to solve a problem. [#]_ Measuring
number of function evaluations avoids the shortcomings of CPU measurements that depend on parameters like the programming language, coding style, machine used to run the experiment, etc., that are difficult or impractical to control.


.. [#] A variable which lives on a ratio scale has a meaningful zero, 
   allows for division, and can be taken to the logarithm in a meaningful way. 
   See for example `Level of measurement on Wikipedia`__.

.. __: https://en.wikipedia.org/wiki/Level_of_measurement?oldid=478392481

.. [#] The transformation :math:`x\mapsto\log(1-x)` could alleviate the problem
   in this case, given it actually zooms in on relevant values.

.. [#] If algorithm internal computations dominate wall-clock time in a practical 
   application, runtime benchmarking results in number of function evaluations 
   can usually be easily adapted *a posteri* to reflect the practical scenario. 


.. _sec:verthori:

Quality Indicators
-------------------

At each time step |t| of an algorithm which optimizes a problem instance
|thetai| of the function |ftheta| in dimension |n|, we define the performance via a quality indicator mapping. 
A quality indicator |I| maps the set of all solutions evaluated 
so far (or recommended [HAN2016ex]_) to a :math:`p`-dependent real value.
That is, the runtime assessment is done on a (large) set of problem instances defined by quintuples 
:math:`p=(n, f_\theta, \theta_i, I, I^\mathrm{target, \theta_i}_{f})`. 

In the single-objective noiseless case, this quality indicator outputs
the best so far observed (i.e. minimal and feasible) function value. 

In the single-objective noisy case, the indicator returns the 1%-tile function value of the last :math:`\lceil\ln(t + 3)^2 / 2\rceil)` evaluated (or recommended) solutions. [#]_

In the multi-objective case, the quality indicator is based on a negative
hypervolume indicator of the set of evaluated solutions (the archive)
[BRO2016]_, while other well- or lesser-known multi-objective quality indicators
are a possible choice.

.. [#] This feature will only be available in the new implementation of the COCO_ framework.


Fixed-Budget versus Fixed-Target Approach
-----------------------------------------

Starting from the most basic convergence graphs, which plot the evolution of a
quality indicator (to be minimized) against the number of function evaluations,
there are essentially two approaches to measure the performance.

**fixed-budget approach**
    We fix a budget of function evaluations,
    and measure the reached quality indicator values. A fixed search
    budget can be pictured as drawing a *vertical* line on the convergence
    graphs (red line in Figure :ref:`fig:HorizontalvsVertical`).

**fixed-target approach**
    We fix a target quality value and measure the number of function
    evaluations, the *runtime*, to reach this target. A fixed target can be
    pictured as drawing a *horizontal* line in the convergence graphs (blue line in Figure
    :ref:`fig:HorizontalvsVertical`).


.. _fig:HorizontalvsVertical:

.. figure:: HorizontalvsVertical.*
   :align: center
   :width: 60%

   **Horizontal versus Vertical View**
   
   Illustration of fixed-budget view (vertical cuts) and fixed-target view
   (horizontal cuts). Black lines depict the best quality indicator value
   plotted versus number of function evaluations.


.. It is often argued that the fixed-cost approach is close to what is needed for
   real world applications where the total number of function evaluations is
   limited. On the other hand, also a minimum target requirement needs to be
   achieved in real world applications, for example, getting (noticeably) better
   than the currently available best solution or than a competitor.

For the performance assessment of algorithms, the fixed-target approach is superior
to the fixed-budget approach since it gives *quantitative and interpretable*
data.

* The fixed-budget approach (vertical cut) does not give *quantitatively
  interpretable*  data:
  the observation that Algorithm A reaches a function value that is, say, two
  times smaller than the one reached by Algorithm B has in general no
  interpretable meaning, mainly because there is no *a priori* way to determine
  *how much* more difficult it is to reach a function value that is two times
  smaller.
  This, indeed, largely depends on the specific function and the specific
  function value reached.

* The fixed-target approach (horizontal cut)
  *measures the time* to
  reach a target function value. The measurement allows conclusions of the
  type: Algorithm A is two (or ten, or a hundred) times faster than Algorithm B
  in solving this problem (i.e. reaching the given target function value). 
  The choice if the target value determines the difficulty and possibly even
  characteristic of the problem to be solved. 

Furthermore, for algorithms that are invariant under certain transformations
of the function value (for example under order-preserving transformations, as
comparison-based algorithms like DE, ES, PSO [AUG2009]_), fixed-target measures become
invariant under these transformations by transformation of the target values
only, while fixed-budget measures require the transformation of all resulting data.


Missing Values
---------------
Investigating Figure :ref:`fig:HorizontalvsVertical` more carefully, we find that not all graphs intersect with either the vertical or the horizontal line. 
On the one hand, if the fixed budget is too large, the algorithm might solve the problem before the budget is exceeded. [#]_ 
The algorithm performs better than the measurement is able to reflect, which can lead to a serious misinterpretation of performance results. 
The remedy is to define a final target value and measure the runtime if the final target is hit. 

On the other hand, if the fixed target is too difficult, the algorithm might never hit the target under the given experimental conditions. [#]_ 
The algorithm performs worse than the experiment is able to reflect, while we get at least a lower bound on the runtime. 
A possible remedy is to run the algorithm longer. 
Another possible remedy is to set a maximum budget. 
However, measurements at the maximum budget can only be interpreted as ranking results, defeating the original objective. Furthermore, introducing a maximum budget prevents to run an algorithm long enough to get an actual runtime measurement.

In COCO_, we collect the runtimes to reach given target values. 
When a target is never reached, the runtime is undefined, 
but the overall number of function evaluations of the corresponding run provides an empirical observation for a lower bound on the runtime to reach the given target.

.. [#] Even in continuous domain, from a benchmarking, a practical, and a numerical viewpoint, the set of solutions that indisputably solve the problem have a volume larger than zero. 

.. [#] However, under mildly randomized conditions, for example with a randomized initial solution, the restarted algorithm reaches any attainable target with probability one. However, the time needed can well be beyond any reasonable practical limitations. 


Target Values
--------------

.. |DI| replace:: :math:`\Delta I`

We define for each problem a reference quality indicator value, :math:`I^{\rm ref, \theta}`. 
In the single-objective case this can be the optimal function value, i.e.
:math:`f^{\mathrm{opt}, \theta} = \min_\mathbf{x} f_\theta(\mathbf{x})`, 
in the multi-objective case this is the indicator value of an approximation of
the Pareto front. 
This reference indicator value depends on the specific instance
:math:`\theta`, and thus does the target indicator value. 
Based on this reference value and a set of target precision values we define for
each problem instance and each precision |DI| (independent of the instance
:math:`\theta`) a target value

.. math::

    I^{\rm target,\theta} = I^{\rm ref,\theta} + \Delta I \enspace,

such that for different instances :math:`({\theta}_1, \ldots,{\theta}_K)` of a
parametrized problem :math:`f_{\theta}(\mathbf{x})`, the set of targets
:math:`I^{\rm target,{\theta}_1}, \ldots,I^{\rm target,{\theta}_K}` are
associated to the same precision. 

Depending on the context, when we refer to a problem this includes the used quality indicator and a given target value (or precision). 
We say, for example, that "algorithm A is solving problem :math:`p=(n, f_\theta,
\theta, I, I^{\rm target})` after :math:`t` function evaluations" if the quality
indicator function value :math:`I` during the optimization of :math:`(n,
f_\theta, \theta)` reaches a value of :math:`I^{\rm target}` or lower for the
first time after :math:`t` function evaluations.


Runlength-based Target Values
------------------------------
.. In addition to the fixed-budget and fixed-target approaches, there is an
  intermediate approach, combining the ideas of *measuring runtime* (to get
  meaningful measurements) and *fixing budgets* (of our interest). The 
  basic idea
  is the following.

Runlength-based target values are a novel way to define the target values based
on a reference data set. Like for *performance profiles* [DOL2002]_, the
resulting empirical distribution can be interpreted *relative* to a reference
algorithm. 
Unlike for performance profiles, the resulting empirical distribution *is* a
data profile [MOR2009]_ and can be understood as absolute runtime distribution,
reflecting the true (opposed to relative) difficulty of the respective problems
for the given algorithm. 

We assume to have given a reference data set with recorded runtimes to reach given quality indicator target values
:math:`\mathcal{I}^{\rm target} = \{ I^{\rm target}_1, \ldots, I^{\rm target}_{|\mathcal{I}^{\rm target}|} \}`
where :math:`I^{\rm target}_i` > :math:`I^{\rm target}_j` for all :math:`i<j`,
as in the fixed-target approach described above. The reference
data serve as a baseline upon which the runlength-based targets are 
computed. To simplify wordings we assume that a reference algorithm :math:`\mathcal{A}` has generated this data set. 

Now we choose a set of increasing reference budgets :math:`B = \{b_1,\ldots, b_{|B|}\}` where :math:`b_i < b_j` for all :math:`i<j`. For each budget :math:`b_i`, we pick the largest (easiest) target that the reference algorithm :math:`\mathcal{A}` did not reach within the given budget and that has not yet been chosen for smaller budgets:

.. math::
  	:nowrap:

 	\begin{equation*}
		I^{\rm chosen}_i = \max_{1\leq j \leq | \mathcal{I}^{\rm target} |}
				I^{\rm target}_j \text{ such that }
				I^{\rm target}_{j} < I(\mathcal{A}, b_i) \text{ and }
				I^{\rm target}_j < I^{\rm chosen}_{k} \text{ for all } k<i
  	\end{equation*}

where :math:`I(\mathcal{A}, t)` is the indicator value of the algorithm
:math:`\mathcal{A}` after :math:`t` function evaluations.
If such target does not exist, we take the smallest (final) target. 

Like this, an algorithm that reaches :math:`I^{\rm chosen}_i` within at most :math:`b_i` evaluations is better than the reference algorithm on this problem. 

 .. Dimo: please check whether the notation is okay

 .. Dimo: TODO: make notation consistent wrt f_target

Runlength-based targets are used in COCO_ for the single-objective expensive optimization scenario. 
The artificial best algorithm of BBOB-2009 is used as reference algorithm with the five budgets of :math:`0.5n`, :math:`1.2n`, :math:`3n`, :math:`10n`, and
:math:`50n` function evaluations, where :math:`n` is the problem
dimension. :math:`I(\mathcal{A}, t)` is the average runtime |aRT| of :math:`\mathcal{A}` for the respective |DI| target precision. 

Runlength-based targets have the advantage to make the target value setting less
dependent on the expertise of a human designer, because only the reference
*budgets* have to be chosen a priori. Reference budgets, as runtimes, are
intuitively meaningful quantities, on which it is comparatively simple to decide
upon. 
Runlength-based targets have the disadvantage to depend on the choice of a reference data set. 


Runtime Computation    
===========================

.. In order to display quantitative measurements, we have seen in the previous section that we should start from the collection of runtimes for different target values. 

In the performance assessment context of COCO_, a problem instance is the 
quintuple :math:`p=(n,f_\theta,\theta_i,I,I^{{\rm target},\theta_i})` containing dimension, function, instantiation parameters, quality indicator mapping, and quality indicator target value. [#]_
For each benchmarked algorithm, a single runtime is measured on each problem.  
From a single run of the algorithm on a given problem instance
:math:`p=(n,f_\theta,\theta_i)`, we obtain a runtime measurement for every target value which has been reached in this run, or equivalently, for the respective target precisions |DI|, which reflects the anytime aspect of 
the performance evaluation. 

Formally, the runtime :math:`\mathrm{RT}(p)` is a random variable that represents the number of function evaluations needed to reach the quality indicator target value for the first time. 
A run or trial that reached the target value is called *successful*. [#]_
For *unsuccessful trials*, the runtime is not defined, but the overall number of function evaluations in the given trial is a random variable denoted by :math:`\mathrm{RT}^{\rm us}(p)`. For a single run, the value of :math:`\mathrm{RT}^{\rm us}(p)` is the same for all failed targets. 

We consider the conceptual **restart algorithm**. 
Given an algorithm has a strictly positive probability |ps| to solve a 
problem :math:`p`, independent restarts of the algorithm solve the problem with
probability one and with runtime

.. |RTforDI| replace:: :math:`\mathbf{RT}(n,f_\theta,\Delta I)`

.. math::
    :nowrap:
    :label: RTrestart
    
    \begin{equation*}%%remove*%%
    \label{index-RTrestart}  
      % ":eq:`RTrestart`" becomes "\eqref{index-RTrestart}" in the LaTeX
    \mathbf{RT}(n,f_\theta,\Delta I) = \sum_{j=1}^{J-1} \mathrm{RT}^{\rm us}_j(n,f_\theta,\Delta I) + \mathrm{RT}^{\rm s}(n,f_\theta,\Delta I)
    \enspace,
    \end{equation*}%%remove*%%

where :math:`J` is a random variable that models the number of unsuccessful
runs until a success is observed, :math:`\mathrm{RT}^{\rm us}_j` are random
variables corresponding to the evaluations in unsuccessful trials and
:math:`\mathrm{RT}^{\rm s}` represents the runtime of a
successful trial [AUG2005]_. 
If the probability of success is one, :math:`J` equals zero with probability one and the restart algorithm coincides with the original algorithm.

Generally, the above equation for |RTforDI| expresses the runtime from repeated independent runs on the same problem instance (while the instance :math:`\theta_i` is not given explicitly). For the performance evaluation in the COCO_ framework, we apply the equation to runs on different instances :math:`\theta_i`, however instances from the same function, with the same dimension and the same target precision. 

.. [#] From the definition of |p|, we can generate a set of problems |calP| by varying one or several of the parameters. We never vary dimension |n| and always vary over all available instances |thetai| for generating |calP.| 

.. [#] The notion of success is directly linked to a target value. A run can be successful with respect to some target values (some problems) and unsuccessful with respect to others. Success also often refers to the final, most difficult, smallest target value, which implies success for all other targets. 


Runs on Different Instances
-----------------------------------------------------------------------
.. The performance assessment in COCO_ heavily relies on the conceptual restart algorithm. 
.. However, we collect at most one single runtime per problem while more data points are needed to display significant data. 

Different instantiations of the parametrized functions |ftheta| are a natural way to represent randomized repetitions. 
For example, different instances implement random translations of the search space and hence a translation of the optimum [HAN2009fun]_. 
Randomized restarts on the other hand are conducted from different initial points. 
For translation invariant algorithms both mechanisms are equivalent and can be mutually exchanged. 

We interpret runs performed on different instances :math:`\theta_1, \ldots, \theta_K` as repetitions of the same problem. 
Thereby we assume that instances of the same parametrized function |ftheta| are 
similar to each other, and more specifically that they exhibit the same runtime
distribution for each given |DI|. 

.. Runtimes collected for the different instances :math:`\theta_1, \ldots, \theta_K` of the same parametrized function :math:`f_\theta` and with respective targets associated to the same target precision :math:`\Delta I` (see above) are thus assumed independent and identically distributed. 

We hence have for each parametrized problem a set of :math:`K\approx15` independent runs, which are used to compute artificial runtimes of the conceptual restart algorithm. 

.. .. Note:: Considering the runtime of the restart algorithm allows to compare
   quantitatively the two different scenarios where

	* an algorithm converges often but relatively slowly
	* an algorithm converges less often, but whenever it converges, it is with a fast convergence rate.

.. we write in the end the runtime of a restart algorithm of a
   parametrized family of function in order to reach a relative target
   :math:`\Delta I` as

.. |K| replace:: :math:`K`

Simulated Restarts and Run-lengths
-----------------------------------

.. Niko: I'd like to reserve the notion of runtime to successful (simulated) runs. 

.. simulated runtime instances of the virtually restarted algorithm

The runtime of the conceptual restart algorithm as given above is the basis for displaying performance within COCO_. 
We use the |K| different runs on the same function and dimension to simulate virtual restarts. 
We assume to have at least one successful run. 
Otherwise, the runtime remains undefined, because the virtual procedure would never stop. 
Then, we construct artificial runs from the available empirical data:
we repeatedly pick, uniformly at random with replacement, one of the |K| trials until we encounter a, for the given target precision, successful trial. 
This procedure simulates a single sample of the virtually restarted algorithm from the given data. 
As computed in |RTforDI| above, the measured runtime is the sum of the number of function evaluations from the unsuccessful trials added to the runtime of the last and successful trial. [#]_

.. [#] In other words, we apply :eq:`RTrestart` such that |RTs| is uniformly distributed over all measured runtimes from successful instances |thetai|, |RTus| is uniformly distributed over all evaluations seen in unsuccessful instances |thetai|, and |J| has a negative binomial distribution :math:`\mathrm{BN(1, p_\mathrm{s})}`, where |ps| is the number of unsuccessful instance divided by all instances.


Bootstrapping Run-lengths
++++++++++++++++++++++++++

In practice, we repeat the above procedure sampling :math:`N\approx100` simulated runtimes from the same underlying distribution, 
which has striking similarities with the true distribution from a restarted algorithm [EFR1994]_. 
To reduce the variance in this procedure, when desired, the first trial in each sample is picked deterministically instead of randomly as the :math:`1 + (N~\mathrm{mod}~K)`-th trial from the data. [#]_
Picking the first trial data as specific instance |thetai| can also be
interpreted as applying simulated restarts to this specific instance rather than
to the entire set of problems :math:`\{p(n, f_\theta, \theta_i, \Delta I) \;|\;
i=1,\dots,K\}`. 

.. Niko: average runtime is not based on simulated restarts, but computed directly...considering the average runtime (Section :ref:`sec:aRT`) or the distribution by displaying empirical cumulative distribution functions (Section :ref:`sec:ECDF`).

.. [#] The variance reducing effect is best exposed in the case where all runs are successful and :math:`N = K`, in which case each data is picked exactly once. 
   This example also suggests to apply a random permutation of the data before to simulate virtually restarted runs. 


Rationales and Limitations
+++++++++++++++++++++++++++

* Simulated restarts allow to compare algorithms with a wide range of different success probabilities [#]_ by a single performance measure. The approach reflects what we need to do when addressing a difficult optimization problem in "the real world". 

* Simulated restarts rely on the assumption that the runtime distribution on each instance is the same. If this is not the case, they still provide a reasonable performance measure, however less of a meaningful interpretation of the result. 

* The runtime of simulated restarts may depend heavily on termination conditions applied in the benchmarked algorithm, due to the evaluations spent in unsuccessful trials, compare :eq:`RTrestart`. This can be interpreted as disadvantage, when termination is considered as a trivial detail in the implementation, or as an advantage, when termination is considered a relevant component in the practical application of numerical optimization algorithms. 

* The maximal number of evaluations for which sampled runtimes are meaningful 
  and representative depends on the experimental conditions. If all runs are successful, no restarts are simulated and all runtimes are meaningful. If all runs terminated due to standard termination conditions in the used algorithm, simulated restarts also reflect the original algorithm. However, if a maximal budget is imposed for the purpose of benchmarking, simulated restarts do not necessarily reflect the real performance. In this case and if the success probability drops below 1/2, the result is likely to give a too pessimistic viewpoint at or beyond the chosen maximal budget. See [HAN2016ex]_ for a more in depth discussion on how to setup restarts in the experiments. 

.. [#] The range of success probabilities is bounded by the number of instances to roughly :math:`2/|K|.`

.. _sec:aRT:

Averaging Runtime
==================

The average runtime (|aRT|), introduced in [PRI1997]_ as ENES and
analyzed in [AUG2005]_ as success performance and referred to as 
ERT in [HAN2009ex]_, estimates the expected runtime of the restart
algorithm given in :eq:`RTrestart` within the COCO_
framework. 

Computation
-----------
We compute the |aRT| from a set of trials as the sum of all evaluations in unsuccessful trials plus the sum of the runtimes in successful trials, both divided by the number of successful trials. 


Motivation
-----------

The expected runtime of the restart algorithm writes [AUG2005]_

.. math::
    :nowrap:

    \begin{eqnarray*}
    \mathbb{E}(\mathbf{RT}) & =
    & \mathbb{E}(\mathrm{RT}^{\rm s})  + \frac{1-p_s}{p_s}
      \mathbb{E}(\mathrm{RT}^{\rm us})
    \enspace,
    \end{eqnarray*}

where |ps| is the probability of success of the algorithm and notations from above are used.

Given a finite number of realizations of the runtime of
an algorithm that comprise at least one successful run, say
:math:`\{\mathrm{RT}^{\rm us}_i, \mathrm{RT}^{\rm s}_j \}`, we
estimate the expected runtime of the restart algorithm from 
the average runtime

.. math::
    :nowrap:

	\begin{eqnarray*}
	\mathrm{aRT} & = & \mathrm{RT}_\mathrm{S} + \frac{1-p_{\mathrm{s}}}{p_{\mathrm{s}}} \,\mathrm{RT}_\mathrm{US} \\  & = & \frac{\sum_i \mathrm{RT}^{\rm us}_i + \sum_j \mathrm{RT}^{\rm us}_j }{\#\mathrm{succ}} \\
	& = & \frac{\#\mathrm{FEs}}{\#\mathrm{succ}}
    \end{eqnarray*}

.. |nbsucc| replace:: :math:`\#\mathrm{succ}`
.. |Ts| replace:: :math:`\mathrm{RT}_\mathrm{S}`
.. |Tus| replace:: :math:`\mathrm{RT}_\mathrm{US}`
.. |ps| replace:: :math:`p_{\mathrm{s}}`

where |Ts| and |Tus| denote the average runtime for successful trials and
the average number of evaluations in unsuccessful trials,  
|nbsucc| denotes the number of successful trials
and  :math:`\#\mathrm{FEs}` is the number of function evaluations
conducted in all trials (before to reach a given target precision).

Rationale and Limitations
--------------------------
The average runtime, |aRT|, is taken over different instances, of the same function, dimension, and target precision, as these instances are interpreted as repetitions. 
Taking the average is (only) meaningful if each instance obeys a similar distribution without heavy tails. 
If one instance is considerably harder than the others, the average is dominated by this instance. 
For this reason we do not average (raw) runtimes from different functions or different target precisions. This can be done however if the logarithm is taken first. 
Plotting the |aRT| divided by dimension against dimension in a log-log plot is the recommended way to investigate the scaling behavior of an algorithm. 

.. _sec:ECDF:

Empirical Distribution Functions
===========================================

We display a set of simulated runtimes with the empirical cumulative
distribution function (ECDF), AKA empirical distribution function. 
Informally, the ECDF displays the *proportion of problems solved within a
specified budget*, where the budget is given on the x-axis. 
More formally, an ECDF gives for each |x|-value the fraction of runtimes which do not exceed |x|, where missing runtime values are counted in the denominator of the fraction.

Rationale and Limitations
-------------------------
Empirical cumulative distribution functions are a universal way to display unlabeled data in a condensed way without loosing information. 
They allow unconstrained aggregation, because each data point remains separately displayed, and they remain meaningful under transformation of the data (e.g. taking the logarithm). 
Displaying the cumulative distribution function on a set of problems from a single function instance where only the target value varies recovers an upside-down convergence graph with a resolution defined by the targets [HAN2010]_.
When runs from several instances are aggregated, the association to the single runs is lost, as is the association the a single function, the function label, when aggregating over several functions. 
This becomes particularly problematic for data in different dimensions, because dimension can be used as decision parameter for algorithm selection. Therefore, we do not aggregate over dimension. 

Relation to Previous Work
--------------------------
Empirical distribution functions over runtimes of optimization algorithms are also known as *data profiles* [MOR2009]_. 
They are widely used for aggregating results from different functions and different dimensions to reach single fixed target precision [RIO2012]_. 
We aggregate also systematically over a large number of target precision values, while we discourage aggregation over dimension. 

.. 
    Formal Definition
    -------------------
    Formally, let us consider a set of problems :math:`\mathcal{P}` 
    and |N| simulated runtimes on each problem. 
    When the problem is not solved, the undefined runtime is considered as infinite. 
    The ECDF is defined as

    .. math::
        :nowrap:

        \begin{equation*}
        \mathrm{ECDF}(t) = \frac{1}{|\mathcal{P}|} \sum_{p \in \mathcal{P}} \frac{1}{N}\sum_{i=1}^N \mathbf{1} \left\{ \mathbf{RT}(p) / n  \leq t \right\} \enspace,
        \end{equation*}

    counting the number of runtimes which do not exceed the time :math:`t\times n`, divided by the number of all simulated runs. 
    The ECDF is displayed in a semi-log (lin-log, semi-logx) plot. 

Examples
----------

We display in Figure :ref:`fig:ecdf` the ECDF of the runtimes of
the pure random search algorithm on the set of problems formed by 15 instances of the sphere function (first function of the single-objective ``bbob`` test
suite) in dimension :math:`n=5` each with 51 target precisions between :math:`10^2` and :math:`10^{-8}` uniform on a log-scale and :math:`N=10^3`. 

.. Dimo/Anne: it will be nice to have a tutorial-like explanation of how an ECDF is constructed (like what we have on the introductory BBOB slides)


.. _fig:ecdf:

.. figure:: pics/plots-RS-2009-bbob/pprldmany_f001_05D.*
   :width: 70%
   :align: center

   ECDF

   Illustration of empirical (cumulative) distribution function (ECDF) of
   runtimes on the sphere function using 51 relative targets uniform on a log
   scale between :math:`10^2` and :math:`10^{-8}`. The runtimes displayed
   correspond to the pure random search algorithm in dimension 5. The cross on
   the ECDF plots of COCO_ represents the median of the maximal length of the
   unsuccessful runs to solve the problems aggregated within the ECDF. 


We can see in this plot, for example, that almost 20 percent of the problems 
were solved within :math:`10^3 \cdot n = 5 \cdot 10^3` function evaluations. 
Runtimes to the right of the cross at :math:`10^6` have at least one unsuccessful run. 
This can be concluded, because with pure random search each unsuccessful run exploits the maximum budget.
The small dot beyond :math:`x=10^7` depicts the overall fraction of all successfully solved functions-target pairs, i.e., the fraction of :math:`(f_\theta, \Delta I)` pairs for which at least one trial (for one :math:`\theta_i`) was successful. 

In the ECDF of Figure :ref:`fig:ecdf` we have **aggregated**
runtimes from 15 instances of the sphere function (we always aggregate over all available function instances |thetai|) times 51 target precision values.

Next, we aggregate **over several functions**. 
We usually divide the set of all (parametrized) benchmark
functions into subgroups sharing similar properties (for instance
separability, unimodality, ...) and display ECDFs which aggregate the
problems induced by these functions and all targets. 
See Figure :ref:`fig:ecdfgroup`.

.. _fig:ecdfgroup:

.. figure:: pics/plots-RS-2009-bbob/gr_separ_05D_05D_separ-combined.*
   :width: 100%
   :align: center

   ECDF for a subgroup of functions

   **Left:** ECDF of the runtime of the pure random search algorithm for
   functions f1, f2, f3, f4 and f5 that constitute the group of
   separable functions for the ``bbob`` testsuite over 51 target values.
   **Right:** Aggregated ECDF of the same data, that is, all functions 
   in one graph.


We can also naturally aggregate over all functions of the benchmark and hence
obtain one single ECDF per algorithm per dimension. 
In Figure :ref:`fig:ecdfall`, the ECDF of different algorithms are displayed in
a single plot. 

.. _fig:ecdfall:

.. figure:: pics/plots-all2009/pprldmany_noiselessall-5and20D.*
   :width: 100%
   :align: center

   ECDF over all functions and all targets

   ECDF of several algorithms benchmarked during the BBOB 2009 workshop
   in dimension 5 (left) and in dimension 20 (right) when aggregating over all functions of the ``bbob`` suite.


Best 2009 Artificial Algorithm
-------------------------------
In COCO_, ECDF plots often display a graph annotated as best 2009
(thick maroon line with diamond markers in Figure :ref:`fig:ecdfall`
for instance). This graph corresponds to an artificial algorithm: for
each set of problems with the same function, dimension and target precision, we select the algorithm from the `BBOB-2009 workshop`__ that has the best |aRT|. 
We then use the runtime measurements of this algorithm. 
The algorithm is artificial because we may use the runtime results from different algorithms for different target values. [#]_

.. __: http://coco.gforge.inria.fr/doku.php?id=bbob-2009
 
.. [#] The best 2009 curve is not guaranteed to be an upper
       left envelope of the ECDF of all algorithms from which it is
       constructed, that is, the ECDF of an algorithm from BBOB-2009 can
       cross the best 2009 curve. This may typically happen if an algorithm
       has for an easy target many very short and few very
       long runtimes such that its aRT is not the best but the short runtimes
       show up to the left of the best 2009 graph.

..  todo
..	* ECDF and uniform pick of a problem
..	* log aRT can be read on the ECDF graphs [requires some assumptions]
..	* The Different Plots Provided by the COCO Platform
..		* aRT Scaling Graphs
..		  The aRT scaling graphs present the average running time to
..		  reach a certain 			precision (relative target)
..		  divided by the dimension versus the dimension. Hence an
..		  horizontal line means a linear scaling with respect to the
..		  dimension.
..		* aRT Loss graphs
..      * scatter plots


.. raw:: html
    
    <H2>Acknowledgments</H2>

.. raw:: latex

    \section*{Acknowledgments}

This work was supported by the grant ANR-12-MONU-0009 (NumBBO)
of the French National Research Agency.


.. ############################# References ##################################
.. raw:: html
    
    <H2>References</H2>


.. [AUG2005] A. Auger and N. Hansen. Performance evaluation of an advanced
   local search evolutionary algorithm. In *Proceedings of the IEEE Congress on
   Evolutionary Computation (CEC 2005)*, pages 1777–1784, 2005.
.. [AUG2009] A. Auger, N. Hansen, J.M. Perez Zerpa, R. Ros and M. Schoenauer (2009). 
   Empirical comparisons of several derivative free optimization algorithms. In Acte du 9ime colloque national en calcul des structures, Giens.
   
.. [BRO2016] D. Brockhoff, T. Tušar, D. Tušar, T. Wagner, N. Hansen, 
   A. Auger, (2016). `Biobjective Performance Assessment with the COCO Platform`__. *ArXiv e-prints*, `arXiv:1605.01746`__
__ http://numbbo.github.io/coco-doc/bi-objeperf-assessment
__ http://arxiv.org/abs/1605.01746

.. [DOL2002] E.D. Dolan, J. J. Moré (2002). Benchmarking optimization software 
   with performance profiles. *Mathematical Programming* 91.2, 201-213. 

.. [EFR1994] B. Efron and R. Tibshirani (1994). *An introduction to the
   bootstrap*. CRC Press.

.. [HAN2009ex] N. Hansen, A. Auger, S. Finck, and R. Ros (2009). Real-Parameter
   Black-Box Optimization Benchmarking 2009: Experimental Setup, 
   `Research Report RR-6828`__, Inria.
.. __: http://hal.inria.fr/inria-00362649/en

.. [HAN2009fun] N. Hansen, S. Finck, R. Ros, and A. Auger (2009). 
   Real-parameter black-box optimization benchmarking 2009: Noiseless
   functions definitions. `Research Report RR-6829`__, Inria, updated
   February 2010.
__ https://hal.inria.fr/inria-00362633

.. [HAN2010] N. Hansen, A. Auger, R. Ros, S. Finck, and P. Posik (2010). 
   Comparing Results of 31 Algorithms from the Black-Box Optimization 
   Benchmarking BBOB-2009. Workshop Proceedings of the GECCO Genetic and 
   Evolutionary Computation Conference 2010, ACM, pp. 1689-1696

.. [HAN2016ex] N. Hansen, T. Tušar, A. Auger, D. Brockhoff, O. Mersmann (2016). 
  `COCO: The Experimental Procedure`__, *ArXiv e-prints*, `arXiv:1603.08776`__. 
__ http://numbbo.github.io/coco-doc/experimental-setup/
__ http://arxiv.org/abs/1603.08776

.. [HOO1995] J. N. Hooker Testing heuristics: We have it all wrong. In Journal of
    Heuristics, pages 33-42, 1995.
.. [HOO1998] H.H. Hoos and T. Stützle. Evaluating Las Vegas
   algorithms—pitfalls and remedies. In *Proceedings of the Fourteenth
   Conference on Uncertainty in Artificial Intelligence (UAI-98)*,
   pages 238–245, 1998.
.. [MOR2009] Jorge J. Moré and Stefan M. Wild. Benchmarking
   Derivative-Free Optimization Algorithms, *SIAM J. Optim.*, 20(1), 172–191, 2009.
.. [PRI1997] K. Price. Differential evolution vs. the functions of
   the second ICEO. In Proceedings of the IEEE International Congress on
   Evolutionary Computation, pages 153–157, 1997.
.. [RIO2012] Luis Miguel Rios and Nikolaos V Sahinidis. Derivative-free optimization:
	A review of algorithms and comparison of software implementations.
	Journal of Global Optimization, 56(3):1247– 1293, 2013.
.. [STE1946] S.S. Stevens (1946).
    On the theory of scales of measurement. *Science* 103(2684), pp. 677-680.
.. .. [TUS2016] T. Tušar, D. Brockhoff, N. Hansen, A. Auger (2016). 
  `COCO: The Bi-objective Black Box Optimization Benchmarking (bbob-biobj) 
  Test Suite`__, *ArXiv e-prints*, `arXiv:1604.00359`__.
.. .. __: http://numbbo.github.io/coco-doc/bbob-biobj/functions/
.. .. __: http://arxiv.org/abs/1604.00359


.. old-bib [Auger:2005a] A Auger and N Hansen. A restart CMA evolution strategy with
   increasing population size. In *Proceedings of the IEEE Congress on
   Evolutionary Computation (CEC 2005)*, pages 1769–1776. IEEE Press, 2005.
.. old-bib
.. old-bib [Auger:2009] Anne Auger and Raymond Ros. Benchmarking the pure
   random search on the BBOB-2009 testbed. In Franz Rothlauf, editor, *GECCO
   (Companion)*, pages 2479–2484. ACM, 2009.
.. old-bib [Efron:1993] B. Efron and R. Tibshirani. *An introduction to the
   bootstrap.* Chapman & Hall/CRC, 1993.
.. old-bib [Harik:1999] G.R. Harik and F.G. Lobo. A parameter-less genetic
   algorithm. In *Proceedings of the Genetic and Evolutionary Computation
   Conference (GECCO)*, volume 1, pages 258–265. ACM, 1999.
