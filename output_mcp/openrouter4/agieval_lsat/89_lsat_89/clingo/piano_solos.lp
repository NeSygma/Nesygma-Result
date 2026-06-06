% Domains
position(1..5).
person(wayne; zara).
piece_type(modern; traditional).

% Assign pianist and piece type to each position
{ pianist(P, Person) : person(Person) } 1 :- position(P).
{ piece_type(P, Type) : piece_type(Type) } 1 :- position(P).

% Constraint 1: The third solo is a traditional piece.
:- piece_type(3, modern).

% Constraint 2: Exactly two of the traditional pieces are performed consecutively.
% Count consecutive traditional pairs
consecutive_trad_pair(P) :- position(P), piece_type(P, traditional), piece_type(P+1, traditional), position(P+1).
:- not #count { P : consecutive_trad_pair(P) } = 1.

% Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
:- pianist(4, wayne), piece_type(4, modern).
:- pianist(4, zara), piece_type(4, traditional).

% Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
:- pianist(2, P), pianist(5, P).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
% wayne_modern_before(P): there exists Q < P such that Wayne performs modern at Q.
wayne_modern_before(P) :- position(P), position(Q), Q < P, pianist(Q, wayne), piece_type(Q, modern).
% If a traditional piece occurs at P, then wayne_modern_before(P) must hold.
:- piece_type(P, traditional), not wayne_modern_before(P).

% Count traditional pieces performed by Wayne
wayne_traditional(P) :- pianist(P, wayne), piece_type(P, traditional).
wayne_trad_count(N) :- N = #count { P : wayne_traditional(P) }.

% Minimize Wayne's traditional piece count
#minimize { N : wayne_trad_count(N) }.

% Map answer
option(a) :- wayne_trad_count(0).
option(b) :- wayne_trad_count(1).
option(c) :- wayne_trad_count(2).
option(d) :- wayne_trad_count(3).
option(e) :- wayne_trad_count(4).

#show option/1.
#show wayne_trad_count/1.
#show pianist/2.
#show piece_type/2.