% Workers
worker(quinn; ruiz; smith; taylor; verma; wells; xue).

% Base constraints
1 { selected(W) : worker(W) } 3.
1 { leader(W) : selected(W) } 1.

% Quinn/Ruiz constraint: if selected, must be leader
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% Smith implies Taylor
:- selected(smith), not selected(taylor).

% Wells implies not Ruiz and not Verma
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Define the conditions for each option
% A: Neither Quinn nor Smith is selected
option_a :- not selected(quinn), not selected(smith).
% B: Neither Ruiz nor Taylor is selected
option_b :- not selected(ruiz), not selected(taylor).
% C: Neither Smith nor Taylor is selected
option_c :- not selected(smith), not selected(taylor).
% D: Neither Smith nor Xue is selected
option_d :- not selected(smith), not selected(xue).
% E: Neither Taylor nor Wells is selected
option_e :- not selected(taylor), not selected(wells).

% Verma is selected and is the leader
verma_leader :- selected(verma), leader(verma).

% Ensure that Verma is selected and is the leader
:- not verma_leader.

% Map the correct answer: the condition under which verma_leader is possible
% We want to find which condition allows verma_leader to be true
% So we derive option(X) if the condition for X is true AND verma_leader is true

% For option A: If neither Quinn nor Smith is selected, can Verma be leader?
% We need to check if verma_leader is possible under option_a
% To do this, we allow the solver to explore the possibility of verma_leader under each condition

% We will derive option(X) if the condition for X is true AND verma_leader is true
option(a) :- option_a, verma_leader.
option(b) :- option_b, verma_leader.
option(c) :- option_c, verma_leader.
option(d) :- option_d, verma_leader.
option(e) :- option_e, verma_leader.

% Ensure that only one option is correct
:- option(X), option(Y), X != Y.

#show option/1.