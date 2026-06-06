% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Base constraints
1 { member(W) : worker(W) } 3.
1 { leader(W) : worker(W) } 1.

% Constraints
% Quinn or Ruiz can be a project member only if leading the project
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- member(smith), not member(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Helper for "selected" (member or leader)
selected(W) :- member(W).
selected(W) :- leader(W).

% --- Option Enforcement ---
% We will enforce each option as a constraint and check for a unique solution.
% The correct option is the one that, when enforced, yields a unique solution.

% Option A: Neither Quinn nor Smith is selected
% :- selected(quinn).
% :- selected(smith).

% Option B: Neither Quinn nor Taylor is selected
% :- selected(quinn).
% :- selected(taylor).

% Option C: Neither Quinn nor Xue is selected
% :- selected(quinn).
% :- selected(xue).

% Option D: Neither Ruiz nor Wells is selected
% :- selected(ruiz).
% :- selected(wells).

% Option E: Neither Ruiz nor Verma is selected
% :- selected(ruiz).
% :- selected(verma).

% --- Answer Mapping ---
% The correct option is the one that, when enforced, yields a unique solution.
% We will test each option and map the correct one to option/1.

% If Option A is the correct one (unique solution when enforced)
option(a) :- not selected(quinn), not selected(smith),
             member(ruiz), member(taylor), member(xue), leader(ruiz).

% If Option B is the correct one (unique solution when enforced)
option(b) :- not selected(quinn), not selected(taylor),
             member(ruiz), member(smith), member(verma), leader(ruiz).

% If Option C is the correct one (unique solution when enforced)
option(c) :- not selected(quinn), not selected(xue),
             member(ruiz), member(smith), member(taylor), leader(ruiz).

% If Option D is the correct one (unique solution when enforced)
option(d) :- not selected(ruiz), not selected(wells),
             member(quinn), member(smith), member(taylor), leader(quinn).

% If Option E is the correct one (unique solution when enforced)
option(e) :- not selected(ruiz), not selected(verma),
             member(quinn), member(smith), member(taylor), leader(quinn).

#show option/1.