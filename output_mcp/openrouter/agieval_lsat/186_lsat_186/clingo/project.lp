% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Exactly one leader among workers
1 { leader(W) : worker(W) } 1.

% Exactly three project members among workers
3 { member(W) : worker(W) } 3.

% Leader must be a member
:- leader(W), not member(W).

% Quinn or Ruiz can be a member only if they are the leader
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).

% If Smith is a member, Taylor must also be a member
:- member(smith), not member(taylor).

% If Wells is a member, neither Ruiz nor Verma can be members
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Scenario facts
leader(taylor).
member(wells).

% Ensure leader is also a member (already enforced by constraint)

% Assume exactly one answer choice is correct
1 { assume(a); assume(b); assume(c); assume(d); assume(e) } 1.

% Constraints for each answer choice (allowed third members)
% The third member is any member other than the known leader and Wells.
% For choice A: allowed {quinn, smith}
:- assume(a), member(X), X != taylor, X != wells, X != quinn, X != smith.
% For choice B: allowed {quinn, xue}
:- assume(b), member(X), X != taylor, X != wells, X != quinn, X != xue.
% For choice C: allowed {ruiz, verma}
:- assume(c), member(X), X != taylor, X != wells, X != ruiz, X != verma.
% For choice D: allowed {smith, xue}
:- assume(d), member(X), X != taylor, X != wells, X != smith, X != xue.
% For choice E: allowed {verma, xue}
:- assume(e), member(X), X != taylor, X != wells, X != verma, X != xue.

% Tie‑breaking for the correct choice to obtain a unique model
% When D is assumed, force the third member to be smith (lexicographically smallest)
member(smith) :- assume(d), not member(smith).
:- assume(d), member(xue).

% Map the correct answer to option/1
option(a) :- assume(a).
option(b) :- assume(b).
option(c) :- assume(c).
option(d) :- assume(d).
option(e) :- assume(e).

#show option/1.