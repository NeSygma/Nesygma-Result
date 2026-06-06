% Domain: singers and positions
singer(kammer). singer(lugo). singer(trillo). singer(waite). singer(yoshida). singer(zinn).
position(1). position(2). position(3). position(4). position(5). position(6).

% Recorded singers
recorded(kammer).
recorded(lugo).

% Each singer gets exactly one position
1 { assign(S, P) : position(P) } 1 :- singer(S).

% Each position has exactly one singer
1 { assign(S, P) : singer(S) } 1 :- position(P).

% Constraint 1: The fourth audition cannot be recorded
:- assign(S, 4), recorded(S).

% Constraint 2: The fifth audition must be recorded
:- assign(S, 5), not recorded(S).

% Constraint 3: Waite's audition must take place earlier than the two recorded auditions
:- assign(waite, PW), assign(kammer, PK), PW >= PK.
:- assign(waite, PW), assign(lugo, PL), PW >= PL.

% Constraint 4: Kammer's audition must take place earlier than Trillo's audition
:- assign(kammer, PK), assign(trillo, PT), PK >= PT.

% Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
:- assign(zinn, PZ), assign(yoshida, PY), PZ >= PY.

% Determine which positions Yoshida could be in
yoshida_at(P) :- assign(yoshida, P).

% Map to answer options
option(a) :- yoshida_at(5).
option(b) :- yoshida_at(4).
option(c) :- yoshida_at(3).
option(d) :- yoshida_at(2).
option(e) :- yoshida_at(1).

#show option/1.
#show assign/2.