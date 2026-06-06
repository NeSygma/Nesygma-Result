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

% Derive that Smith cannot be selected (since Taylor is not selected)
:- selected(smith).

% Xue must be selected in all valid cases
:- not selected(xue).

% Map the correct answer to option/1
option(e) :- selected(xue).

#show option/1.