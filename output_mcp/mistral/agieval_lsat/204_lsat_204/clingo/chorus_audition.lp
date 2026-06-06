% Define singers
singer(kammer; lugo; trillo; waite; yoshida; zinn).

% Recorded singers (only Kammer and Lugo are recorded)
recorded(kammer).
recorded(lugo).

% Positions (1 through 6)
position(1..6).

% Each singer is assigned to exactly one position
1 { assigned(S, P) : position(P) } 1 :- singer(S).

% Each position has exactly one singer
1 { assigned(S, P) : singer(S) } 1 :- position(P).

% Constraint: Position 4 cannot be recorded
:- assigned(S, 4), recorded(S).

% Constraint: Position 5 must be recorded
:- assigned(S, 5), not recorded(S).

% Find all recorded positions
recorded_pos(P) :- assigned(S, P), recorded(S).

% Find the earliest (minimum) recorded position
min_recorded(P) :- recorded_pos(P), not recorded_pos(P-1).

% Waite's audition must be earlier than the earliest recorded audition
:- assigned(waite, PW), min_recorded(PR), PW >= PR.

% Constraint: Kammer's audition must be earlier than Trillo's
:- assigned(kammer, PK), assigned(trillo, PT), PK >= PT.

% Constraint: Zinn's audition must be earlier than Yoshida's
:- assigned(zinn, PZ), assigned(yoshida, PY), PZ >= PY.

% Map the correct answer to option/1
option(a) :- assigned(kammer, 6).
option(b) :- assigned(lugo, 6).
option(c) :- assigned(trillo, 6).
option(d) :- assigned(waite, 6).
option(e) :- assigned(zinn, 6).

#show option/1.