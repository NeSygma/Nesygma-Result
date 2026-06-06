% Define the singers
singer(kammer).
singer(lugo).
singer(trillo).
singer(waite).
singer(yoshida).
singer(zinn).

% Define positions (1 through 6)
position(1..6).

% Recorded auditions: only Kammer and Lugo are recorded
recorded(kammer).
recorded(lugo).

% Not recorded: the other four
not_recorded(trillo).
not_recorded(waite).
not_recorded(yoshida).
not_recorded(zinn).

% Each position has exactly one singer
1 { audition(S, P) : singer(S) } 1 :- position(P).

% Each singer auditions exactly once
1 { audition(S, P) : position(P) } 1 :- singer(S).

% Constraint: The fourth audition cannot be recorded
:- audition(S, 4), recorded(S).

% Constraint: The fifth audition must be recorded
:- audition(S, 5), not recorded(S).

% Constraint: Waite's audition must be earlier than the two recorded auditions
% (Waite must be before both Kammer and Lugo)
:- audition(waite, P1), audition(kammer, P2), P1 >= P2.
:- audition(waite, P1), audition(lugo, P2), P1 >= P2.

% Constraint: Kammer's audition must be earlier than Trillo's
:- audition(kammer, P1), audition(trillo, P2), P1 >= P2.

% Constraint: Zinn's audition must be earlier than Yoshida's
:- audition(zinn, P1), audition(yoshida, P2), P1 >= P2.

% Constraint: Trillo cannot be in the second position
:- audition(trillo, 2).

% The answer is the option that cannot be the second audition, which is Trillo (option c)
option(c) :- not option(a), not option(b), not option(d), not option(e).

% The other options can be second, so we derive them if they are possible
option(a) :- audition(kammer, 2).
option(b) :- audition(lugo, 2).
option(d) :- audition(waite, 2).
option(e) :- audition(zinn, 2).

#show option/1.

% Debugging output (optional)
% #show audition/2.
% #show recorded/1.