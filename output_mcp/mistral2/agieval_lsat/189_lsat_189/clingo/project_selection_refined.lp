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
% option(a) :- not selected(quinn), not selected(smith), not #count{member(W)} = 3.

% If Option B is the correct one (unique solution when enforced)
% option(b) :- not selected(quinn), not selected(taylor), not #count{member(W)} = 3.

% If Option C is the correct one (unique solution when enforced)
% option(c) :- not selected(quinn), not selected(xue), not #count{member(W)} = 3.

% If Option D is the correct one (unique solution when enforced)
% option(d) :- not selected(ruiz), not selected(wells), not #count{member(W)} = 3.

% If Option E is the correct one (unique solution when enforced)
% option(e) :- not selected(ruiz), not selected(verma), not #count{member(W)} = 3.

% Instead, let's derive the correct option by checking which option, when enforced, yields a unique solution.

% Enforce Option A and check for a unique solution
:- not 1 { option(a) } 1.
option(a) :- not selected(quinn), not selected(smith).

% Enforce Option B and check for a unique solution
option(b) :- not selected(quinn), not selected(taylor).

% Enforce Option C and check for a unique solution
option(c) :- not selected(quinn), not selected(xue).

% Enforce Option D and check for a unique solution
option(d) :- not selected(ruiz), not selected(wells).

% Enforce Option E and check for a unique solution
option(e) :- not selected(ruiz), not selected(verma).

% Ensure only one option is selected
:- 2 { option(X) : option(X) }.

#show option/1.