% Workers and roles
worker(quinn). worker(ruiz). worker(smith). worker(taylor).
worker(verma). worker(wells). worker(xue).

% Project roles
1 { leader(X) : worker(X) } 1.
3 { selected(X) : worker(X) } 3.

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
option(a) :- leader(ruiz), selected(ruiz), selected(taylor), selected(wells),
             not selected(quinn), not selected(smith),
             not selected(verma), not selected(xue).

% (B) Verma (leader), Quinn, Taylor
option(b) :- leader(verma), selected(verma), selected(quinn), selected(taylor),
             not selected(ruiz), not selected(smith),
             not selected(wells), not selected(xue).

% (C) Verma (leader), Smith, Taylor
option(c) :- leader(verma), selected(verma), selected(smith), selected(taylor),
             not selected(quinn), not selected(ruiz),
             not selected(wells), not selected(xue).

% (D) Verma (leader), Smith, Xue
option(d) :- leader(verma), selected(verma), selected(smith), selected(xue),
             not selected(quinn), not selected(ruiz),
             not selected(taylor), not selected(wells).

% (E) Xue (leader), Verma, Wells
option(e) :- leader(xue), selected(xue), selected(verma), selected(wells),
             not selected(quinn), not selected(ruiz),
             not selected(smith), not selected(taylor).

% Ensure only one option is selected
1 { chosen(A) : option(A) } 1.

chosen(A) :- option(A), not other_option(A).
other_option(A) :- option(A), option(B), A != B, chosen(B).

#show chosen/1.
#show option/1.