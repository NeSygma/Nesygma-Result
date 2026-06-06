% Define the domain of solos and pianists
solo(1..5).
pianist(wayne; zara).
type(modern; traditional).

% Assign a pianist to each solo
1 { assigned_pianist(S, P) : pianist(P) } 1 :- solo(S).

% Assign a type to each solo
1 { piece_type(S, T) : type(T) } 1 :- solo(S).

% The third solo is a traditional piece
:- piece_type(3, modern).

% Exactly two of the traditional pieces are performed consecutively
consecutive_traditional(S) :- piece_type(S, traditional), piece_type(S+1, traditional), solo(S), solo(S+1).
:- 2 { consecutive_traditional(S) : solo(S) }.

% In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece
:- piece_type(4, traditional), assigned_pianist(4, zara).
:- piece_type(4, modern), assigned_pianist(4, wayne).

% The pianist who performs the second solo does not perform the fifth solo
:- assigned_pianist(2, P), assigned_pianist(5, P).

% No traditional piece is performed until Wayne performs at least one modern piece
:- piece_type(S, traditional), S < 5, not has_modern_wayne.
has_modern_wayne :- assigned_pianist(S, wayne), piece_type(S, modern).

% Count the number of solos where Wayne performs a traditional piece
wayne_traditional_count(N) :-
    N = #count { S : assigned_pianist(S, wayne), piece_type(S, traditional) }.

% Minimize the number of solos where Wayne performs a traditional piece
#minimize { N : wayne_traditional_count(N) }.

% Define the answer options based on the count
option(a) :- wayne_traditional_count(0).
option(b) :- wayne_traditional_count(1).
option(c) :- wayne_traditional_count(2).
option(d) :- wayne_traditional_count(3).
option(e) :- wayne_traditional_count(4).

#show option/1.