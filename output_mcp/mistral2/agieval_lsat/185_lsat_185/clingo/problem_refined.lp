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
3 { selected(X) : worker(X) } 3.

% Exactly one project leader
1 { leader(X) : worker(X) } 1.

% Constraints

% Quinn or Ruiz can be a project member only if leading the project
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% --- Multiple Choice Options ---
% (A) Ruiz (leader), Taylor, Wells
option(a) :- leader(ruiz), selected(taylor), selected(wells),
             selected(ruiz),
             not selected(quinn), not selected(smith),
             not selected(verma), not selected(xue).

% (B) Verma (leader), Quinn, Taylor
option(b) :- leader(verma), selected(quinn), selected(taylor),
             selected(verma),
             not selected(ruiz), not selected(smith),
             not selected(wells), not selected(xue).

% (C) Verma (leader), Smith, Taylor
option(c) :- leader(verma), selected(smith), selected(taylor),
             selected(verma),
             not selected(quinn), not selected(ruiz),
             not selected(wells), not selected(xue).

% (D) Verma (leader), Smith, Xue
option(d) :- leader(verma), selected(smith), selected(xue),
             selected(verma),
             not selected(quinn), not selected(ruiz),
             not selected(taylor), not selected(wells).

% (E) Xue (leader), Verma, Wells
option(e) :- leader(xue), selected(verma), selected(wells),
             selected(xue),
             not selected(quinn), not selected(ruiz),
             not selected(smith), not selected(taylor).

#show option/1.
#show leader/1.
#show selected/1.