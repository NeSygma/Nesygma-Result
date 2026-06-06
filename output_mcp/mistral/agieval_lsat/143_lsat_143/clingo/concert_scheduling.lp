% Define members and times
member(guitarist).
member(keyboard).
member(percussionist).
member(saxophonist).
member(trumpeter).
member(violinist).

time(1..6).

% Each member performs exactly one solo
1 { solo(M, T) : time(T) } 1 :- member(M).

% Each time has exactly one member
1 { solo(M, T) : member(M) } 1 :- time(T).

% Constraints
% Guitarist does not perform the fourth solo
:- solo(guitarist, 4).

% Percussionist performs before keyboard player
:- solo(percussionist, T1), solo(keyboard, T2), T1 >= T2.

% Keyboard player performs after violinist and before guitarist
:- solo(keyboard, T1), solo(violinist, T2), T1 =< T2.  % Keyboard after violinist
:- solo(keyboard, T1), solo(guitarist, T2), T1 >= T2.  % Keyboard before guitarist

% Saxophonist performs after exactly one of percussionist or trumpeter
% Helper: saxophonist is after percussionist or trumpeter, but not both
:- solo(saxophonist, T), 
   (solo(percussionist, Tp), T > Tp), 
   (solo(trumpeter, Tt), T > Tt).
:- solo(saxophonist, T), 
   not (solo(percussionist, Tp), T > Tp), 
   not (solo(trumpeter, Tt), T > Tt).

% Given condition: violinist performs the fourth solo
solo(violinist, 4).

% Keyboard must be at position 5, guitarist at position 6
:- not solo(keyboard, 5).
:- not solo(guitarist, 6).

% Define the options based on the constraints
% Option A: percussionist before violinist (position 4)
option(a) :- solo(percussionist, T), T < 4.

% Option B: trumpeter before violinist (position 4)
option(b) :- solo(trumpeter, T), T < 4.

% Option C: trumpeter before guitarist (position 6)
option(c) :- solo(trumpeter, T), T < 6.

% Option D: saxophonist before violinist (position 4)
option(d) :- solo(saxophonist, T), T < 4.

% Option E: trumpeter before saxophonist
option(e) :- solo(trumpeter, Tt), solo(saxophonist, Ts), Tt < Ts.

#show option/1.