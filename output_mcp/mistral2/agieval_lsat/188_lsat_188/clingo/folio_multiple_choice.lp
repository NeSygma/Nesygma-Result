% Workers and roles
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Exactly three workers are selected as project members
1 { selected(W) : worker(W) } 3.

% Exactly one project member is the project leader
1 { leader(W) : worker(W) } 1.

% The project leader must be one of the selected project members
:- leader(W), not selected(W).

% Constraint: Quinn or Ruiz can be a project member only if they are the project leader
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% Constraint: If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% Constraint: If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Given condition: Taylor is not a project member
:- selected(taylor).

% --- Multiple Choice Logic ---
% We need to determine which worker MUST be a project member under these constraints.
% The answer choices are A: Quinn, B: Ruiz, C: Verma, D: Wells, E: Xue

% Define which workers are project members
project_member(W) :- selected(W).

% Check which of the answer choices must be true
% A: Quinn must be a project member
option(a) :- project_member(quinn).

% B: Ruiz must be a project member
option(b) :- project_member(ruiz).

% C: Verma must be a project member
option(c) :- project_member(verma).

% D: Wells must be a project member
option(d) :- project_member(wells).

% E: Xue must be a project member
option(e) :- project_member(xue).

#show option/1.