% Domains
solo(1..5).
pianist(wayne; zara).
type(modern; traditional).

% Each solo has exactly one pianist and one type
1 { pianist(S, P) : pianist(P) } 1 :- solo(S).
1 { type(S, T) : type(T) } 1 :- solo(S).

% Condition 1: Third solo is traditional
type(3, traditional).

% Condition 2: Exactly two traditional pieces are consecutive
% Count pairs (I, I+1) where both are traditional
consecutive_trad(I) :- solo(I), I < 5, type(I, traditional), type(I+1, traditional).
:- not 1 = #count { I : consecutive_trad(I) }.

% Condition 3: Fourth solo: either Wayne performs traditional or Zara performs modern
cond3 :- pianist(4, wayne), type(4, traditional).
cond3 :- pianist(4, zara), type(4, modern).
:- not cond3.

% Condition 4: Pianist of second solo does not perform fifth solo
:- pianist(2, P), pianist(5, P).

% Condition 5: No traditional piece until Wayne performs at least one modern piece
wayne_modern_before(S) :- solo(S), solo(J), J < S, pianist(J, wayne), type(J, modern).
:- type(S, traditional), not wayne_modern_before(S).

% Additional condition: Pianist of first solo also performs second solo
:- pianist(1, P1), pianist(2, P2), P1 != P2.

% Show assignments
#show pianist/2.
#show type/2.