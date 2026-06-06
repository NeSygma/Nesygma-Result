% Explicitly test if Wayne can have 0 traditional pieces
position(1..5).
person(wayne; zara).
type(modern; traditional).

% Full assignment
1 { pianist(P, Person) : person(Person) } 1 :- position(P).
1 { piece(P, Type) : type(Type) } 1 :- position(P).

% Constraint 1
:- piece(3, modern).

% Constraint 2: exactly one pair of consecutive traditional pieces
consec_pair(P) :- piece(P, traditional), piece(P+1, traditional), position(P+1).
:- not #count { P : consec_pair(P) } = 1.

% Constraint 3
:- pianist(4, wayne), piece(4, modern).
:- pianist(4, zara), piece(4, traditional).

% Constraint 4
:- pianist(2, P), pianist(5, P).

% Constraint 5
wayne_modern_before(P) :- position(P), position(Q), Q < P, pianist(Q, wayne), piece(Q, modern).
:- piece(P, traditional), not wayne_modern_before(P).

% Force Wayne to have 0 traditional pieces
:- pianist(P, wayne), piece(P, traditional).

% Show everything
#show pianist/2.
#show piece/2.