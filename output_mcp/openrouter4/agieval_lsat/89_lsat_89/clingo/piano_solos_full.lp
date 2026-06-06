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
consecutive_trad_pair(P) :- position(P), piece_type(P, traditional), piece_type(P+1, traditional), position(P+1).
:- not #count { P : consecutive_trad_pair(P) } = 1.

% Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
:- pianist(4, wayne), piece_type(4, modern).
:- pianist(4, zara), piece_type(4, traditional).

% Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
:- pianist(2, P), pianist(5, P).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
wayne_modern_before(P) :- position(P), position(Q), Q < P, pianist(Q, wayne), piece_type(Q, modern).
:- piece_type(P, traditional), not wayne_modern_before(P).

% Count traditional pieces performed by Wayne
wayne_traditional(P) :- pianist(P, wayne), piece_type(P, traditional).
wayne_trad_count(N) :- N = #count { P : wayne_traditional(P) }.

% Minimize Wayne's traditional piece count
#minimize { N : wayne_trad_count(N) }.

% Show ALL atoms for verification
#show pianist/2.
#show piece_type/2.
#show consecutive_trad_pair/1.
#show wayne_modern_before/1.
#show wayne_traditional/1.
#show wayne_trad_count/1.