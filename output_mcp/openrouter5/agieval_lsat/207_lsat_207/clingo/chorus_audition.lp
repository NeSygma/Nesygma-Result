% Domain: positions 1..6
pos(1..6).

% Singers
singer(kammer; lugo; trillo; waite; yoshida; zinn).

% Recorded auditions: Kammer and Lugo
recorded(kammer).
recorded(lugo).
not_recorded(X) :- singer(X), not recorded(X).

% Each position gets exactly one singer
1 { at(X, P) : pos(P) } 1 :- singer(X).
1 { at(X, P) : singer(X) } 1 :- pos(P).

% --- Original constraints ---

% The fourth audition cannot be recorded
:- at(X, 4), recorded(X).

% The fifth audition must be recorded
:- at(X, 5), not_recorded(X).

% Waite's audition must take place earlier than the two recorded auditions
:- at(waite, PW), at(kammer, PK), PW >= PK.
:- at(waite, PW), at(lugo, PL), PW >= PL.

% Kammer's audition must take place earlier than Trillo's
:- at(kammer, PK), at(trillo, PT), PK >= PT.

% Zinn's audition must take place earlier than Yoshida's
:- at(zinn, PZ), at(yoshida, PY), PZ >= PY.

% --- Now let's find all valid orders ---
% We'll enumerate all solutions and see what patterns emerge.

#show at/2.