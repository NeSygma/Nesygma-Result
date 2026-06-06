% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Choose exactly 3 members
{ sel(W) : worker(W) } 3.

% Exactly 1 leader among selected members
{ lead(W) : sel(W) } 1.

% Constraint 1: Quinn or Ruiz can be a member only if leading
:- sel(quinn), not lead(quinn).
:- sel(ruiz), not lead(ruiz).

% Constraint 2: If Smith is selected, Taylor must also be
:- sel(smith), not sel(taylor).

% Constraint 3: If Wells is selected, neither Ruiz nor Verma can be
:- sel(wells), sel(ruiz).
:- sel(wells), sel(verma).

% Assign a unique ID to each valid selection
% Use binary encoding of workers
id_val(0..127).

sel_id(N) :- N = #sum{ 1,W : sel(quinn), W=0; 2,W : sel(ruiz), W=1; 4,W : sel(smith), W=2; 8,W : sel(taylor), W=3; 16,W : sel(verma), W=4; 32,W : sel(wells), W=5; 64,W : sel(xue), W=6 }.

lead_id(N) :- N = #sum{ 1,W : lead(quinn), W=0; 2,W : lead(ruiz), W=1; 4,W : lead(smith), W=2; 8,W : lead(taylor), W=3; 16,W : lead(verma), W=4; 32,W : lead(wells), W=5; 64,W : lead(xue), W=6 }.

full_id(N) :- sel_id(S), lead_id(L), N = S*128 + L.

% For each condition, check if this selection satisfies it
% A: Neither Quinn nor Smith is selected
satisfies_a :- not sel(quinn), not sel(smith).
% B: Neither Quinn nor Taylor is selected
satisfies_b :- not sel(quinn), not sel(taylor).
% C: Neither Quinn nor Xue is selected
satisfies_c :- not sel(quinn), not sel(xue).
% D: Neither Ruiz nor Wells is selected
satisfies_d :- not sel(ruiz), not sel(wells).
% E: Neither Ruiz nor Verma is selected
satisfies_e :- not sel(ruiz), not sel(verma).

% Count selections satisfying each condition
count_a(N) :- N = #count{ I : full_id(I), satisfies_a }.
count_b(N) :- N = #count{ I : full_id(I), satisfies_b }.
count_c(N) :- N = #count{ I : full_id(I), satisfies_c }.
count_d(N) :- N = #count{ I : full_id(I), satisfies_d }.
count_e(N) :- N = #count{ I : full_id(I), satisfies_e }.

% The answer is the condition where count = 1
option(a) :- count_a(1).
option(b) :- count_b(1).
option(c) :- count_c(1).
option(d) :- count_d(1).
option(e) :- count_e(1).

#show option/1.
#show count_a/1.
#show count_b/1.
#show count_c/1.
#show count_d/1.
#show count_e/1.