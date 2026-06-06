% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Exactly three members
3 { member(W) : worker(W) } 3.

% Exactly one leader among members
1 { leader(W) : member(W) } 1.

% Constraints
% Quinn or Ruiz can be a project member only if leading the project.
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be.
:- member(smith), not member(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be.
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Given: Taylor is the project leader and Wells is a project member.
leader(taylor).
member(wells).

% Ensure Taylor is a member (since leader)
member(taylor) :- leader(taylor).

% Derive the third member (the one besides Taylor and Wells)
third_member(X) :- member(X), X != taylor, X != wells.

% Map the correct answer to option/1
% Option D: Smith or Xue
option(d) :- third_member(smith) ; third_member(xue).

% Show the option
#show option/1.
#show member/1.
#show leader/1.
#show third_member/1.