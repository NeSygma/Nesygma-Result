% Workers and roles
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Project roles
project_member(X) :- selected(X), leader(X).
project_member(X) :- selected(X), not leader(X).

% Exactly three project members
3 { project_member(X) : worker(X) } 3.

% Exactly one project leader
1 { leader(X) : worker(X) } 1.

% Constraints

% Quinn or Ruiz can be a project member only if leading the project
:- project_member(quinn), not leader(quinn).
:- project_member(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- project_member(smith), not project_member(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- project_member(wells), project_member(ruiz).
:- project_member(wells), project_member(verma).

% Define selected/1 as a helper to represent project members (including leader)
selected(X) :- project_member(X).

% --- Multiple Choice Options ---
% (A) Ruiz (leader), Taylor, Wells
option(a) :- leader(ruiz), project_member(taylor), project_member(wells),
             not project_member(quinn), not project_member(smith),
             not project_member(verma), not project_member(xue).

% (B) Verma (leader), Quinn, Taylor
option(b) :- leader(verma), project_member(quinn), project_member(taylor),
             not project_member(ruiz), not project_member(smith),
             not project_member(wells), not project_member(xue).

% (C) Verma (leader), Smith, Taylor
option(c) :- leader(verma), project_member(smith), project_member(taylor),
             not project_member(quinn), not project_member(ruiz),
             not project_member(wells), not project_member(xue).

% (D) Verma (leader), Smith, Xue
option(d) :- leader(verma), project_member(smith), project_member(xue),
             not project_member(quinn), not project_member(ruiz),
             not project_member(taylor), not project_member(wells).

% (E) Xue (leader), Verma, Wells
option(e) :- leader(xue), project_member(verma), project_member(wells),
             not project_member(quinn), not project_member(ruiz),
             not project_member(smith), not project_member(taylor).

#show option/1.