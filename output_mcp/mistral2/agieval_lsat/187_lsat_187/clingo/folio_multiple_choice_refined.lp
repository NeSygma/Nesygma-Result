% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Roles
role(member).
role(leader).

% Selection: Exactly 3 workers are selected as members
1 { selected(W) : worker(W) } 3.

% Exactly one leader, who must be a selected member
1 { leader(W) : worker(W) } 1.
:- leader(W), not selected(W).

% Constraint 1: Quinn or Ruiz can be a project member only if leading the project
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% Constraint 2: If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Verma is the project leader and must be a member
leader(verma).
selected(verma).

% --- Multiple Choice Conditions ---
% Define conditions for each option

% Option A: Neither Quinn nor Smith is selected
% This is valid if Quinn and Smith are not selected
option(a) :- not selected(quinn), not selected(smith).

% Option B: Neither Ruiz nor Taylor is selected
% This is valid if Ruiz and Taylor are not selected
option(b) :- not selected(ruiz), not selected(taylor).

% Option C: Neither Smith nor Taylor is selected
% This is valid if Smith and Taylor are not selected
option(c) :- not selected(smith), not selected(taylor).

% Option D: Neither Smith nor Xue is selected
% This is valid if Smith and Xue are not selected
option(d) :- not selected(smith), not selected(xue).

% Option E: Neither Taylor nor Wells is selected
% This is valid if Taylor and Wells are not selected
option(e) :- not selected(taylor), not selected(wells).

% Ensure only one option is satisfied
:- option(A), option(B), A != B.
:- option(A), option(C), A != C.
:- option(A), option(D), A != D.
:- option(A), option(E), A != E.
:- option(B), option(C), B != C.
:- option(B), option(D), B != D.
:- option(B), option(E), B != E.
:- option(C), option(D), C != D.
:- option(C), option(E), C != E.
:- option(D), option(E), D != E.

#show option/1.