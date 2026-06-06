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

% Determine the third project member (since Wells and Taylor are already selected)
third_member(W) :- selected(W), worker(W), W != wells, W != taylor.

% Map the correct answer to option/1
% The third member must be either Smith or Xue (since Quinn and Ruiz cannot be members unless they are leaders, and Taylor is already the leader)
% Quinn cannot be a member unless he is the leader, but Taylor is the leader, so Quinn cannot be a member.
% Ruiz cannot be a member unless he is the leader, but Taylor is the leader, so Ruiz cannot be a member.
% Verma cannot be a member if Wells is a member (constraint), so Verma is excluded.
% Thus, the third member must be either Smith or Xue.

option(a) :- third_member(quinn).
option(b) :- third_member(quinn).
option(a) :- third_member(smith).
option(d) :- third_member(smith).
option(c) :- third_member(ruiz).
option(c) :- third_member(verma).
option(b) :- third_member(xue).
option(d) :- third_member(xue).
option(e) :- third_member(verma).
option(e) :- third_member(xue).

#show option/1.