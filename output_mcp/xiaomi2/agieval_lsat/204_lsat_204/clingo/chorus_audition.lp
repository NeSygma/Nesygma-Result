% Domain: singers and positions
singer(kammer). singer(lugo). singer(trillo). singer(waite). singer(yoshida). singer(zinn).
position(1..6).

% Recorded singers
recorded(kammer). recorded(lugo).
not_recorded(trillo). not_recorded(waite). not_recorded(yoshida). not_recorded(zinn).

% Each singer gets exactly one position
1 { at(S, P) : position(P) } 1 :- singer(S).

% Each position has exactly one singer
1 { at(S, P) : singer(S) } 1 :- position(P).

% Condition 1: Fourth audition cannot be recorded
:- at(S, 4), recorded(S).

% Condition 2: Fifth audition must be recorded
:- at(S, 5), not_recorded(S).

% Condition 3: Waite's audition must take place earlier than the two recorded auditions
:- at(waite, PW), at(kammer, PK), PW >= PK.
:- at(waite, PW), at(lugo, PL), PW >= PL.

% Condition 4: Kammer's audition must take place earlier than Trillo's audition
:- at(kammer, PK), at(trillo, PT), PK >= PT.

% Condition 5: Zinn's audition must take place earlier than Yoshida's audition
:- at(zinn, PZ), at(yoshida, PY), PZ >= PY.

% Determine which singers could be at position 6
could_be_sixth(S) :- at(S, 6).

% Map to answer options
option(a) :- could_be_sixth(kammer).
option(b) :- could_be_sixth(lugo).
option(c) :- could_be_sixth(trillo).
option(d) :- could_be_sixth(waite).
option(e) :- could_be_sixth(zinn).

#show option/1.
#show at/2.