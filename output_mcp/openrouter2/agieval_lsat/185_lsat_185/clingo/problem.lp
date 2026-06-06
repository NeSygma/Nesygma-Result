% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Scenarios
scenario(a). scenario(b). scenario(c). scenario(d). scenario(e).

% Facts for each scenario
selected_fact(a, ruiz). selected_fact(a, taylor). selected_fact(a, wells). leader_fact(a, ruiz).
selected_fact(b, verma). selected_fact(b, quinn). selected_fact(b, taylor). leader_fact(b, verma).
selected_fact(c, verma). selected_fact(c, smith). selected_fact(c, taylor). leader_fact(c, verma).
selected_fact(d, verma). selected_fact(d, smith). selected_fact(d, xue). leader_fact(d, verma).
selected_fact(e, xue). selected_fact(e, verma). selected_fact(e, wells). leader_fact(e, xue).

% Choose exactly one active scenario
1 { active(S) : scenario(S) } 1.

% Define selected and leader for active scenario
selected(S, X) :- active(S), selected_fact(S, X).
leader(S, X) :- active(S), leader_fact(S, X).

% Constraints
3 { selected(S, X) : worker(X) } 3 :- active(S).
1 { leader(S, X) : worker(X) } 1 :- active(S).

% Quinn or Ruiz can be a member only if leading
:- selected(S, quinn), not leader(S, quinn).
:- selected(S, ruiz), not leader(S, ruiz).

% Leader must be a member
:- leader(S, X), not selected(S, X).

% If Smith is a member, Taylor must also be
:- selected(S, smith), not selected(S, taylor).

% If Wells is a member, neither Ruiz nor Verma can be
:- selected(S, wells), selected(S, ruiz).
:- selected(S, wells), selected(S, verma).

% Map options
option(a) :- active(a).
option(b) :- active(b).
option(c) :- active(c).
option(d) :- active(d).
option(e) :- active(e).

#show option/1.