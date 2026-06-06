% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Base constraints

% Exactly 3 workers are selected as project members
3 { selected(W) : worker(W) } 3.

% Exactly 1 worker is the project leader
1 { leader(W) : worker(W) } 1.

% The leader must be among the selected members
:- leader(W), not selected(W).

% Quinn or Ruiz can be a project member only if they are the leader
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Given: Taylor is NOT a project member
:- selected(taylor).

% Map the correct answer to option/1 (MANDATORY)
% Xue must be a project member in all valid solutions
option(e) :- selected(xue).

#show option/1.