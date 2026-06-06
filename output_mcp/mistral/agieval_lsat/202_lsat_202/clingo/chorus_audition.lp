% Singers
singer(kammer; lugo; trillo; waite; yoshida; zinn).

% Positions
position(1..6).

% Recorded singers (only Kammer and Lugo are recorded)
recorded(kammer).
recorded(lugo).

% Each singer appears exactly once
1 { assigned(S, P) : position(P) } 1 :- singer(S).

% Each position has exactly one singer
1 { assigned(S, P) : singer(S) } 1 :- position(P).

% Position P is recorded if the singer assigned to it is recorded
is_recorded(P) :- assigned(S, P), recorded(S).

% Constraint: Position 4 cannot be recorded
:- is_recorded(4).

% Constraint: Position 5 must be recorded
is_recorded(5).

% Constraint: Position is recorded only if the singer is recorded
:- assigned(S, P), not recorded(S), is_recorded(P).

% Helper: Get position of each singer
pos_of_singer(S, P) :- assigned(S, P).

% Constraint: Waite's audition must be earlier than BOTH recorded auditions
% (The two recorded auditions are at positions of Kammer and Lugo)
:- pos_of_singer(waite, PW),
   pos_of_singer(kammer, PK),
   PW >= PK.
:- pos_of_singer(waite, PW),
   pos_of_singer(lugo, PL),
   PW >= PL.

% Constraint: Kammer's audition must be earlier than Trillo's
:- pos_of_singer(kammer, PK), pos_of_singer(trillo, PT), PK >= PT.

% Constraint: Zinn's audition must be earlier than Yoshida's
:- pos_of_singer(zinn, PZ), pos_of_singer(yoshida, PY), PZ >= PY.

% Map the options to conditions
% Option A: Kammer, Trillo, Zinn, Waite, Lugo, Yoshida
option(a) :- assigned(kammer, 1), assigned(trillo, 2), assigned(zinn, 3),
             assigned(waite, 4), assigned(lugo, 5), assigned(yoshida, 6).

% Option B: Waite, Kammer, Yoshida, Zinn, Lugo, Trillo
option(b) :- assigned(waite, 1), assigned(kammer, 2), assigned(yoshida, 3),
             assigned(zinn, 4), assigned(lugo, 5), assigned(trillo, 6).

% Option C: Waite, Lugo, Kammer, Trillo, Zinn, Yoshida
option(c) :- assigned(waite, 1), assigned(lugo, 2), assigned(kammer, 3),
             assigned(trillo, 4), assigned(zinn, 5), assigned(yoshida, 6).

% Option D: Waite, Zinn, Kammer, Trillo, Lugo, Yoshida
option(d) :- assigned(waite, 1), assigned(zinn, 2), assigned(kammer, 3),
             assigned(trillo, 4), assigned(lugo, 5), assigned(yoshida, 6).

% Option E: Zinn, Yoshida, Waite, Lugo, Kammer, Trillo
option(e) :- assigned(zinn, 1), assigned(yoshida, 2), assigned(waite, 3),
             assigned(lugo, 4), assigned(kammer, 5), assigned(trillo, 6).

#show option/1.