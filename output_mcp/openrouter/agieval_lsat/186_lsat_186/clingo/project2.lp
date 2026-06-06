% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Exactly one leader
1 { leader(W) : worker(W) } 1.
% Exactly three members
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

% Identify prohibited workers under the scenario (cannot be members)
prohibited(quinn).  % because member(quinn) would require leader(quinn) which is false
prohibited(ruiz).   % same reason
prohibited(verma).  % because member(wells) is true, so member(verma) forbidden

% Allowed workers are those not prohibited
allowed(W) :- worker(W), not prohibited(W).

% The third member is the member that is neither the leader nor Wells
third_member(W) :- member(W), W != taylor, W != wells.

% Map each answer choice to option if both members of the pair are allowed
option(a) :- allowed(quinn), allowed(smith).
option(b) :- allowed(quinn), allowed(xue).
option(c) :- allowed(ruiz), allowed(verma).
option(d) :- allowed(smith), allowed(xue).
option(e) :- allowed(verma), allowed(xue).

% Ensure exactly one option is derived
1 { opt(a); opt(b); opt(c); opt(d); opt(e) } 1.
opt(a) :- option(a).
opt(b) :- option(b).
opt(c) :- option(c).
opt(d) :- option(d).
opt(e) :- option(e).

% Show the selected option
#show opt/1.