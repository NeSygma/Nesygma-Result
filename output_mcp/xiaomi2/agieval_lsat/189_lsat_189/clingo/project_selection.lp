% Workers
worker(quinn; ruiz; smith; taylor; verma; wells; xue).

% Generate all possible teams of 3 with a designated leader
% leader is one of the 3 members
{ team(ID, W) : worker(W) } 3 :- id(ID).
leader(ID, W) :- id(ID), team(ID, W), W = L, { team(ID, L) } > 0.

% Actually, let me use a simpler encoding
% Each selection has a leader and 2 other members
% leader + 2 members = 3 total

id(1..50).

% Choose a leader
{ l(ID, W) : worker(W) } 1 :- id(ID).

% Choose 2 other members (not the leader)
{ m(ID, W) : worker(W), not l(ID, W) } 2 :- id(ID).

% A worker is selected if they are leader or member
sel(ID, W) :- l(ID, W).
sel(ID, W) :- m(ID, W).

% Constraint 1: Quinn or Ruiz can be a member only if leading
:- id(ID), sel(ID, quinn), not l(ID, quinn).
:- id(ID), sel(ID, ruiz), not l(ID, ruiz).

% Constraint 2: If Smith is selected, Taylor must also be
:- id(ID), sel(ID, smith), not sel(ID, taylor).

% Constraint 3: If Wells is selected, neither Ruiz nor Verma can be
:- id(ID), sel(ID, wells), sel(ID, ruiz).
:- id(ID), sel(ID, wells), sel(ID, verma).

% Symmetry breaking: order members to avoid duplicates
m_order(ID, W, 1) :- id(ID), m(ID, W), W = #min { V : m(ID, V) }.
m_order(ID, W, 2) :- id(ID), m(ID, W), not m_order(ID, W, 1).
:- id(ID1), id(ID2), ID1 < ID2,
   l(ID1, L), l(ID2, L),
   m_order(ID1, W1, 1), m_order(ID2, W2, 1), W1 = W2,
   m_order(ID1, V1, 2), m_order(ID2, V2, 2), V1 = V2.

% Define conditions for each answer choice
cond_a(ID) :- id(ID), not sel(ID, quinn), not sel(ID, smith).
cond_b(ID) :- id(ID), not sel(ID, quinn), not sel(ID, taylor).
cond_c(ID) :- id(ID), not sel(ID, quinn), not sel(ID, xue).
cond_d(ID) :- id(ID), not sel(ID, ruiz), not sel(ID, wells).
cond_e(ID) :- id(ID), not sel(ID, ruiz), not sel(ID, verma).

% Count selections satisfying each condition
cnt_a(N) :- N = #count { ID : id(ID), cond_a(ID) }.
cnt_b(N) :- N = #count { ID : id(ID), cond_b(ID) }.
cnt_c(N) :- N = #count { ID : id(ID), cond_c(ID) }.
cnt_d(N) :- N = #count { ID : id(ID), cond_d(ID) }.
cnt_e(N) :- N = #count { ID : id(ID), cond_e(ID) }.

% Selection is completely determined if exactly 1 selection satisfies the condition
option(a) :- cnt_a(1).
option(b) :- cnt_b(1).
option(c) :- cnt_c(1).
option(d) :- cnt_d(1).
option(e) :- cnt_e(1).

#show option/1.