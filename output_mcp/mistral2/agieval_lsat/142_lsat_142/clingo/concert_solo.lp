% Base domain: band members and solo positions
member(guitarist).
member(keyboard_player).
member(percussionist).
member(saxophonist).
member(trumpeter).
member(violinist).

position(1..6).

% Each member performs exactly one solo
1 { performs(M, P) : position(P) } 1 :- member(M).

% Each position is performed by exactly one member
1 { performs(M, P) : member(M) } 1 :- position(P).

% The guitarist does not perform the fourth solo
:- performs(guitarist, 4).

% The percussionist performs a solo at some time before the keyboard player does
:- performs(percussionist, P1), performs(keyboard_player, P2), P1 >= P2.

% The keyboard player performs a solo at some time after the violinist does
:- performs(keyboard_player, P1), performs(violinist, P2), P1 =< P2.

% The keyboard player performs a solo at some time before the guitarist does
:- performs(keyboard_player, P1), performs(guitarist, P2), P1 >= P2.

% The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both
% Helper to check if saxophonist is after percussionist
sax_after_perc :- performs(saxophonist, P1), performs(percussionist, P2), P1 > P2.

% Helper to check if saxophonist is after trumpeter
sax_after_trump :- performs(saxophonist, P1), performs(trumpeter, P2), P1 > P2.

% Ensure saxophonist is after exactly one of percussionist or trumpeter
:- performs(saxophonist, _), not sax_after_perc, not sax_after_trump.
:- performs(saxophonist, _), sax_after_perc, sax_after_trump.

% Query: Which member CANNOT perform the third solo?
% We will check for each member if they can be assigned to position 3.

% Define the condition for each option being the third solo
option(a) :- performs(guitarist, 3).
option(b) :- performs(keyboard_player, 3).
option(c) :- performs(saxophonist, 3).
option(d) :- performs(trumpeter, 3).
option(e) :- performs(violinist, 3).

#show option/1.