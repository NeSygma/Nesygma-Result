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

% Map the correct answer: the condition under which verma_leader is possible
% We want to find which condition allows verma_leader to be true
% So we derive option(X) if the condition for X is true AND verma_leader is possible under that condition

% For option A: If neither Quinn nor Smith is selected, can Verma be leader?
% We need to check if verma_leader is possible under option_a
% To do this, we allow the solver to explore the possibility of verma_leader under each condition

% We will derive option(X) if the condition for X is true AND there exists a model where verma_leader is true
% To enforce this, we use the following pattern:

% For each option, we derive option(X) if the condition for X is true AND verma_leader is possible
% We do this by ensuring that verma_leader is possible under the condition for X

% To ensure that verma_leader is possible only under the correct condition, we add:

% If option_a is true, then verma_leader must be possible under option_a
% Similarly for other options

% We will use the following logic:
% option(X) is derived if the condition for X is true AND verma_leader is possible under that condition

% To make this work, we need to ensure that verma_leader is possible only when the condition for the correct option is met

% We will derive option(X) if the condition for X is true AND verma_leader is possible
% We will use the following rules:

option(a) :- option_a, verma_leader_possible_a.
option(b) :- option_b, verma_leader_possible_b.
option(c) :- option_c, verma_leader_possible_c.
option(d) :- option_d, verma_leader_possible_d.
option(e) :- option_e, verma_leader_possible_e.

% Now, we define verma_leader_possible_X for each option X
% verma_leader_possible_X is true if there exists a model where verma_leader is true under the condition for X

% To do this, we use the following pattern:
% We allow the solver to choose verma_leader if the condition for X is true

% We will use choice rules to allow verma_leader to be true under the condition for X

{ verma_leader_a : option_a }.
{ verma_leader_b : option_b }.
{ verma_leader_c : option_c }.
{ verma_leader_d : option_d }.
{ verma_leader_e : option_e }.

% Now, we define verma_leader_possible_X as true if verma_leader_X is true
verma_leader_possible_a :- verma_leader_a.
verma_leader_possible_b :- verma_leader_b.
verma_leader_possible_c :- verma_leader_c.
verma_leader_possible_d :- verma_leader_d.
verma_leader_possible_e :- verma_leader_e.

% Ensure that verma_leader is true if any verma_leader_X is true
verma_leader :- verma_leader_a.
verma_leader :- verma_leader_b.
verma_leader :- verma_leader_c.
verma_leader :- verma_leader_d.
verma_leader :- verma_leader_e.

% Ensure that only one option is correct
:- option(X), option(Y), X != Y.

#show option/1.