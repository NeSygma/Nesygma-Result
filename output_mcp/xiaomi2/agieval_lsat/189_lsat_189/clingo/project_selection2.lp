% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Choose exactly 3 members and 1 leader among them
{ sel(W) : worker(W) } 3.
{ lead(W) : sel(W) } 1.

% Constraint 1: Quinn or Ruiz can be a member only if leading
:- sel(quinn), not lead(quinn).
:- sel(ruiz), not lead(ruiz).

% Constraint 2: If Smith is selected, Taylor must also be
:- sel(smith), not sel(taylor).

% Constraint 3: If Wells is selected, neither Ruiz nor Verma can be
:- sel(wells), sel(ruiz).
:- sel(wells), sel(verma).

% For each answer choice, define the condition
% A: Neither Quinn nor Smith is selected
cond_a :- not sel(quinn), not sel(smith).
% B: Neither Quinn nor Taylor is selected
cond_b :- not sel(quinn), not sel(taylor).
% C: Neither Quinn nor Xue is selected
cond_c :- not sel(quinn), not sel(xue).
% D: Neither Ruiz nor Wells is selected
cond_d :- not sel(ruiz), not sel(wells).
% E: Neither Ruiz nor Verma is selected
cond_e :- not sel(ruiz), not sel(verma).

% Count models satisfying each condition
% We need to check: given the condition, is there exactly 1 valid selection?
% We'll use #count to count answer sets

% Show the selection for debugging
#show sel/1.
#show lead/1.
#show cond_a/0.
#show cond_b/0.
#show cond_c/0.
#show cond_d/0.
#show cond_e/0.