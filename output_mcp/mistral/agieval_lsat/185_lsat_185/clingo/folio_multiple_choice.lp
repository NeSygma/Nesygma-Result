% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Base constraints
3 { selected(W) : worker(W) } 3.
1 { leader(W) : worker(W) } 1.

% Constraints
% Quinn or Ruiz can be a project member only if leading the project
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Ensure the leader is among the selected workers
:- leader(W), not selected(W).

% Define the options as potential solutions
% Option A: Ruiz (leader), Taylor, Wells
option(a) :- selected(ruiz), selected(taylor), selected(wells), leader(ruiz).

% Option B: Verma (leader), Quinn, Taylor
option(b) :- selected(verma), selected(quinn), selected(taylor), leader(verma).

% Option C: Verma (leader), Smith, Taylor
option(c) :- selected(verma), selected(smith), selected(taylor), leader(verma).

% Option D: Verma (leader), Smith, Xue
option(d) :- selected(verma), selected(smith), selected(xue), leader(verma).

% Option E: Xue (leader), Verma, Wells
option(e) :- selected(xue), selected(verma), selected(wells), leader(xue).

% Ensure only one option is selected
1 { option(X) : X=a..e } 1.

#show option/1.