% Base facts
house(j; k; l; m; n; o; p).
position(1..7).

% Time periods
morning(1..2).
afternoon(3..5).
evening(6..7).

% Choice: assign each house to a position
{ assigned(H, P) : position(P) } = 1 :- house(H).

% Each position has exactly one house
:- position(P), not 1 { assigned(H, P) : house(H) } 1.

% J must be shown in the evening
:- assigned(j, P), not evening(P).

% K cannot be shown in the morning
:- assigned(k, P), morning(P).

% L must be shown after K and before M (K < L < M in position order)
:- assigned(k, PK), assigned(l, PL), assigned(m, PM), PK >= PL.
:- assigned(k, PK), assigned(l, PL), assigned(m, PM), PL >= PM.

% Now determine which option MUST be true

% Option A: K is shown in the evening
% This would require K in position 6 or 7
% But then L must be after K, which is impossible since max position is 7
% So this option cannot be true in any valid schedule
option(a) :- assigned(k, 6).
option(a) :- assigned(k, 7).

% Option B: L is shown in the afternoon
% We need to prove this must be true
% If L were NOT in afternoon, L would be in morning or evening
% - L cannot be in morning because K must be before L and K cannot be in morning
%   (if L in 1 or 2, K would need to be before L, but K cannot be in morning)
% - L cannot be in evening because then M would need to be after L (position >7), impossible
% Therefore L must be in afternoon
option(b) :- assigned(l, 3).
option(b) :- assigned(l, 4).
option(b) :- assigned(l, 5).

% Option C: L is shown in the evening
% As reasoned above, this is impossible
option(c) :- assigned(l, 6).
option(c) :- assigned(l, 7).

% Option D: M is shown in the morning
% Morning is positions 1-2
% For M to be in morning, both K and L must be before M
% But K cannot be in morning, so K would need to be before position 1 (impossible)
% Therefore this option cannot be true
option(d) :- assigned(m, 1).
option(d) :- assigned(m, 2).

% Option E: M is shown in the afternoon
% This could be true, but is it necessary?
% Counterexample: K in 3, L in 4, M in 6 (evening), J in 7
% This satisfies all constraints, and M is not in afternoon
% So this option is not necessarily true
option(e) :- assigned(m, 3).
option(e) :- assigned(m, 4).
option(e) :- assigned(m, 5).

#show option/1.