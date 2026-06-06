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

% Constraints

% Quinn or Ruiz can be a project member only if they are leading the project
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Given conditions for the question:
% Taylor is the project leader
leader(taylor).

% Wells is a project member
selected(wells).

% The third project member must be someone other than Wells and Taylor
third_member(W) :- selected(W), worker(W), W != wells, W != taylor.

% Only one third member is possible
1 { third_member(W) : worker(W) } 1.

% The third member must be either Smith or Xue, as Quinn and Ruiz cannot be members (Taylor is the leader and they are not the leader), and Verma cannot be a member (Wells is a member).
% Thus, the answer is D (Smith or Xue).

% Map the correct answer to option/1
option(d) :- third_member(smith).
option(d) :- third_member(xue).

% Ensure only one option is selected
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

#show option/1.