% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Exactly 3 workers are selected as project members
3 { member(W) : worker(W) } 3.

% Exactly 1 project member is the leader
1 { leader(W) : member(W) } 1.

% Constraint: Quinn can be a project member only if leading
:- member(quinn), not leader(quinn).

% Constraint: Ruiz can be a project member only if leading
:- member(ruiz), not leader(ruiz).

% Constraint: If Smith is a member, Taylor must also be
:- member(smith), not member(taylor).

% Constraint: If Wells is a member, neither Ruiz nor Verma can be
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Given: Taylor is NOT a project member
:- member(taylor).

% Helper: check if a worker is absent
absent(W) :- worker(W), not member(W).

% For each worker, define a flag: is_present if they are a member
is_present(W) :- member(W).

% We need to find which worker appears in ALL answer sets
% Use a counting approach across models
% A worker is "required" if no valid model exists where they are absent

% Let's use a different approach: 
% For each worker, try to force them to be absent and see if UNSAT results
% We'll do this by adding a "test" worker and checking

% Actually, simplest: just run and check which workers appear in ALL models
% We'll use #count to check

% Define: a worker is "can_be_absent" if there's a valid model without them
% We use a choice to optionally exclude each worker, then check

% Let me just enumerate valid triples directly
triple(W1,W2,W3) :- worker(W1), worker(W2), worker(W3), W1 < W2, W2 < W3.

in_triple(W, W1,W2,W3) :- triple(W1,W2,W3), W = W1.
in_triple(W, W1,W2,W3) :- triple(W1,W2,W3), W = W2.
in_triple(W, W1,W2,W3) :- triple(W1,W2,W3), W = W3.

% A triple is valid if all constraints hold
% No Taylor
valid(W1,W2,W3) :- triple(W1,W2,W3),
    not in_triple(taylor, W1,W2,W3),
    not in_triple(smith, W1,W2,W3),
    not in_triple(quinn, W1,W2,W3),
    not in_triple(ruiz, W1,W2,W3).

valid(W1,W2,W3) :- triple(W1,W2,W3),
    not in_triple(taylor, W1,W2,W3),
    not in_triple(smith, W1,W2,W3),
    in_triple(quinn, W1,W2,W3),
    not in_triple(ruiz, W1,W2,W3),
    not in_triple(wells, W1,W2,W3).

valid(W1,W2,W3) :- triple(W1,W2,W3),
    not in_triple(taylor, W1,W2,W3),
    not in_triple(smith, W1,W2,W3),
    in_triple(ruiz, W1,W2,W3),
    not in_triple(quinn, W1,W2,W3),
    not in_triple(wells, W1,W2,W3).

valid(W1,W2,W3) :- triple(W1,W2,W3),
    not in_triple(taylor, W1,W2,W3),
    not in_triple(smith, W1,W2,W3),
    in_triple(wells, W1,W2,W3),
    not in_triple(ruiz, W1,W2,W3),
    not in_triple(verma, W1,W2,W3),
    not in_triple(quinn, W1,W2,W3).

valid(W1,W2,W3) :- triple(W1,W2,W3),
    not in_triple(taylor, W1,W2,W3),
    not in_triple(smith, W1,W2,W3),
    in_triple(wells, W1,W2,W3),
    not in_triple(ruiz, W1,W2,W3),
    not in_triple(verma, W1,W2,W3),
    in_triple(quinn, W1,W2,W3).

% Count valid triples containing each worker
count_valid(W, N) :- worker(W), N = #count{W1,W2,W3 : valid(W1,W2,W3), in_triple(W, W1,W2,W3)}.

% Count total valid triples
total_valid(N) :- N = #count{W1,W2,W3 : valid(W1,W2,W3)}.

% A worker must be a member if they appear in ALL valid triples
must_be_member(W) :- count_valid(W, N1), total_valid(N2), N1 = N2, N1 > 0.

% Map to answer choices
option(a) :- must_be_member(quinn).
option(b) :- must_be_member(ruiz).
option(c) :- must_be_member(verma).
option(d) :- must_be_member(wells).
option(e) :- must_be_member(xue).

#show option/1.
#show valid/3.
#show must_be_member/1.
#show total_valid/1.