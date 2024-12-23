---
title:  "Introduction to Causal Inference"
excerpt_separator: <!--more-->
category: 
    - technical
tags:
    - artificial intelligence
    - machine learning
    - causal inference
---

"Causality is essential to solve Simpson's paradox." ~Brady Neal, Introduction to Causal Inference. 

Spurious correlations are common across the world, where two events are caused by one common event and while the two events might seem correlated, the correlation is indeed spurious. In causal inference, we identify such confounders and resolve Simposon's paradox to quantify causal association between any two entities. Checkout this [website](https://www.tylervigen.com/spurious-correlations) to some examples of spurious correlations. 

Technically, correlation is a measure of linear statistical dependence. Classifications introduced in this book include: (1) Statistical vs. Causal, (2) Identification vs. Estimation, and (3) Interventional vs. Observational. Further, last but not the least, it is very important to state the *assumptions*.

The fundamental problem of causal inference is the fact that we cannot observe both Y(1): outcome of getting a treatment and Y(0): outcome of not getting a treatment. It is the case because the second observation will be influenced by the actions we took between the two observations and anything else that changed since the first observation. The potential outcomes that we do not observe are known as *counterfactuals*. Note that there are no counterfactuals or factuals until the outcome is observed. Before that, they are only *potential* outcomes. For this fundamental problem, instead of computing the *Individual Treatment Effect*, we can compute *Average Treatment Effect* by taking an average over the ITEs: $$\mathbb{E}[Y_i(1)-Y_i(0)]$$. 

However,

$$
\mathbb{E}[Y(1)] - \mathbb{E}[Y(0)] \ne \mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]
$$

While the left term is a causal quantity, the right term is an association quantity. How can we estimate the causal inference if we cannot reduce a causal expression to a purely statistical expression? Can we make some assumption that will allow us to estimate causal impact from association quantity? 

Yes, and the assumption is *ignorability* i.e. $$(Y(1), Y(0))  \perp\!\!\!\perp T$$. Assuming ignorability is like ignoring how people ended up selecting the treatment they selected and just assuming that they were randomly assigned their treatment. In other words, the assumption states that once covariates are observed, the outcome is independent of the treatment assignment - the treatment assignment is as good as random. Another perspective on this assumption is *exchangeability*, which means that if the groups were swapped, the new treatment group would observe the same outcomes as the old treatment group, and the new control group would observe the same outcome as the old control group. 

Ignorability/exchangeability allows us to estimate causal quantity by using purely statistical expression and that makes the causal quantity *identifiable* because we can compute it from a purely statistical quantity. But, how realistic is ignorability? To be honest, not much! In reality, the observed data is confounded and we must carry out multiple randomized experiments to ensure ignorability/exchangeability. To enable causal inference on observation data, we consider the assumption of conditional exchangeability, which allows conditioning of relevant variables and make subgroups exchangeable, i.e., $$(Y(1), Y(0))\perp\!\!\!\perp T \mid X$$. The idea is that although the treatment and potential outcomes may be unconditionally associated (due to unconfounding), within levels of X, they are not associated. 

However, we often cannot know for certain if conditional exchangeability holds. There might exist some unobserved confounders that are not part of X, usually a problem with observational data. The best thing to do usually is to observe and fit in as many covariates into X as possible to try to ensure unconfoundedness. But, positivity restricts the number of covariates that can be observed and fit for achieving the unconfoundedness. Having too many covariates can reduce the size of subgroup to a level where everyone is either always receive the treatment or everyone is always receiving the control, which is a positivity violation. The tradeoff is called **Positivity-Unconfoundedness Tradeoff**. 

Other key assumptions include:
- *No Interference*: The outcome is only a function of its own treatment and is unaffected by anyone else's treatment. Violation of no interference assumption is rampant in network data. 
- *Consistency*: Also, referred to as "no multiple versions of treatment", consistency ensures that different values of treatment will lead to same outcome.
- *SUTVA*: Stable unit-treatment value assumption is satisfied if unit *i's* outcome is simply a function of unit *i's* treatment. Therefore, SUTVA is a combination of no-interference and consistency. 

$$
\begin{align}
\mathbb{E}[Y(1)-Y(0)] &= \mathbb{E}[Y(1)] - \mathbb{E}[Y(0)] \\ &\text{ (linearity of expectation)} \\
&= \mathbb{E}_X[\mathbb{E}[Y(1) \mid X] - \mathbb{E}[Y(0) \mid X]] \\ & \text{ (law of iterated expectations)} \\
&= \mathbb{E}_X[\mathbb{E}[Y(1) \mid T=1, X] - \mathbb{E}[Y(0) \mid T=0, X]] \\ & \text{ (unconfoundedness and positivity)} \\
&= \mathbb{E}_X[\mathbb{E}[Y \mid T=1, X] - \mathbb{E}[Y \mid T=0, X]] \\ & \text{ (consistency)}
\end{align}
$$

Key Terminologies:
- Estimand: The quantity that we want to estimate. Causal estimand is any estimand that contains a potential outcome. For example, $$E[Y(1)-Y(0)]$$ is the causal estimand and $$\mathbb{E}_X[\mathbb{E}[Y \mid T=1, X] - \mathbb{E}[Y \mid T=0, X]]$$ is the statistical estimand. 
- Identification: Process of moving from a causal estimand to an equivalent statistical estimand. 
- Estimate: The approximation an estimand using the data. 
- Estimator: The function that maps a dataset to an estimate of the estimand. 
- Estimation: The process of going from estimand + data to an estimate (a concrete number) is called estimation. It is also referred to as the process of moving from a statistical estimand to an estimate. 

Once we get an statistical estimand, we often use a model in place of the conditional expectations and refer to them as model-assisted estimators.  
  
Causal relations are represented using Graphical models. Probabilistic graphical models are statistical models while causal graphical models are causal models. Bayesian networks are the main probabilistic graphical model that causal graphical model inherit most of their properties from. 

Causal graphs involve causal assumptions. Following is a list of assumptions to turn statistical models into causal models. 
1. *Local markov assumption*: Given its parents in the DAG, a node X is independent of all its non-descendents, and 
2. *Minimality*: Local markov assumption + Adjacent nodes in the DAG are dependent. Because removing edges in a Bayesian network is equivalent to adding independencies, the minimality assumption is equivalent to saying that we can't remove any more edges in the graph.   
3. *((Strict) Causal Edges Assumption)*: In a directed graph, every parent is a direct cause of all its children. The non-strict causal edges assumption would allow for some parents to not be causes of their children. Until otherwise specified, causal graph would usually refer to a DAG (Directed Acyclic Graph) that satisfies the strict causal edges assumption.   

## Flow of Association
*Berkson's paradox (selection bias)*: Conditioning on a collider can induce association in two independent parents. Conditioning on descendents of a collider also induces association in between the parents of the collider. 

Association can flow through chain or forks, which causation only follows the directed path. 

*d-separation:* Two (sets of) nodes X and Y are d-separated by a set of nodes Z if all of the paths between (any node in) X and (any node in) Y are blocked by Z.

## Causal Models
*do-operator:* Conditioning on T=t just means that we are restricting our focus to the subset of the population to those who received treatment *t*, however, intervention denoted by do(T=t) would be to take the whole population and give everyone treatment t. For causal model, the average treatment effect when the treatment is binary is:

$$\mathbb{E}[Y \mid do(T=1)]-\mathbb{E}[Y \mid do(T=0)]$$

If we can reduce an expression Q with do in it, to one without do in it, then Q is said to be identifiable. A causal estimand contains a do-operator and a statistical estimand doesn't. Whenever, do(t) appears after the conditioning bar, it means that everything in that expression is in the post-intervention world where the  intervention do(t) occurs.

*Causal mechanism:* Process that generates $$X_i$$ as the conditional distribution of $$X_i$$, given all of its causes: $$P(x_i \mid pa_i)$$.

*Modularity Assumption:* Intervening on a variable $$X_i$$ only changes the causal mechanism for $$X_i$$, it does not change the causal mechanisms that generate any other variables. 

*Manipulated Graph:* The graph with edges to the intervened node(s) removed. 

The causal mechanisms are not modular. 

*Truncated Factorization:* We assume that P and G satisfy the Markov assumption and modularity. Given a set of intervention nodes S, if x is consistent with the intervension then all of the factors should remain same except for the factors $$X_i \in S$$; those factors would change to 1. 

*Backdoor Criterion:* The unblocked association paths between T to Y are known as backdoor paths and a set of variables W that can block backdoor paths by conditioning on W are known as backdoor criterion. Once blocked, all of the association that flows from T to Y in the manipulated graph is purely causal. Satisfying the backdoor criterion makes W a *sufficient adjustment set*.

*Backdoor Adjustment:* Given the modularity assumption, that W satisfies the backdoor criterion and positivity, we can identify the causal effect of T on Y: 
$$
    P(y \mid do(t)) = \sum_w{P(y \mid t, w) P(w)}
$$

We can use the backdoor adjustment if W d-separates T from Y in the manipulated graph. 

A structural equation denotes the function that maps A to B, i.e., $$B := f(A)$$. Here, ":=" denotes asymmetry where A causes B but not vice-a-versa. However, currently this mapping is deterministic and to make it probabilistic, we add some randomness to it, i.e. $$B:=f(A, \mathbb{U})$$, where \mathbb{U} is the unobserved random variable. A single model may contain a large collection of structural equations, and is known as *Structural Causal Model (SCM)*. The variables for which we write structure equations are called *endogenous* variables, and *exogenous* variables are variables who do not have any parents in the causal graph - we choose not to model their causes.

If the causal graph is DAG and unobserved random variables are independent, then the causal graph is *Markovian* and the distribution P is Markov with respect to the causal graph. If the causal graph is a DAG but the noise terms are dependent, the model is *semi-Markovian*. For example, if there is unobserved confounding, the model is *semi-Markovian*.

*Modularity Assumption for SCMs:* Consider an SCM M and an interventional SCM $$M_t$$ that we get by performing the intervention do(T = t). The modularity assumption states that M and $$M_t$$ share all of their structural equations except the structural equation for T, which is T := t in $$M_t$$.

In other words, the intervension *do(T=t)* is localized to T.

*The Law of Counterfactuals (and Interventions):* $$Y_t(u) = Y_{M_t}(u)$$
