% Concert solo ordering problem

% Members
member(guitarist).
member(keyboard).
member(percussionist).
member(saxophonist).
member(trumpeter).
member(violinist).

% Positions
position(1..6).

% Solo assignment: each member exactly one solo, each position exactly one member
1 { solo(Member, Pos) : position(Pos) } 1 :- member(Member).
1 { solo(Member, Pos) : member(Member) } 1 :- position(Pos).

% Constraints
% Guitarist does not perform the fourth solo
:- solo(guitarist, 4).

% Percussionist before keyboard
:- solo(percussionist, P), solo(keyboard, K), P >= K.

% Keyboard after violinist and before guitarist
:- solo(violinist, V), solo(keyboard, K), solo(guitarist, G), not (V < K < G).

% Saxophonist after exactly one of percussionist or trumpeter
:- solo(saxophonist, S), solo(percussionist, P), solo(trumpeter, T), (S > P) == (S > T).

% Additional condition: violinist performs the fourth solo
solo(violinist, 4).

% Deduce that keyboard must be 5 and guitarist must be 6 (optional, but helps)
% Keyboard must be after 4 and before guitarist, and guitarist must be after keyboard.
% Since positions are 1..6, keyboard can only be 5, guitarist only 6.
:- solo(keyboard, K), K <= 4.
:- solo(guitarist, G), G <= 5.

% The remaining three members (percussionist, saxophonist, trumpeter) must occupy positions 1,2,3
:- solo(percussionist, P), P > 3.
:- solo(saxophonist, S), S > 3.
:- solo(trumpeter, T), T > 3.

% Define assignment for the three remaining members
assignment(P, S, T) :- solo(percussionist, P), solo(saxophonist, S), solo(trumpeter, T), P != S, P != T, S != T.

% Statements
% A: percussionist before violinist (always true since violinist is 4 and percussionist is 1,2,3)
statement_false(a, P, S, T) :- assignment(P, S, T), not (P < 4).

% B: trumpeter before violinist (always true)
statement_false(b, P, S, T) :- assignment(P, S, T), not (T < 4).

% C: trumpeter before guitarist (always true, guitarist is 6)
statement_false(c, P, S, T) :- assignment(P, S, T), not (T < 6).

% D: saxophonist before violinist (always true)
statement_false(d, P, S, T) :- assignment(P, S, T), not (S < 4).

% E: trumpeter before saxophonist (not always true)
statement_false(e, P, S, T) :- assignment(P, S, T), not (T < S).

% Determine which statements are false in some assignment
false_in_some_assignment(a) :- statement_false(a, P, S, T), assignment(P, S, T).
false_in_some_assignment(b) :- statement_false(b, P, S, T), assignment(P, S, T).
false_in_some_assignment(c) :- statement_false(c, P, S, T), assignment(P, S, T).
false_in_some_assignment(d) :- statement_false(d, P, S, T), assignment(P, S, T).
false_in_some_assignment(e) :- statement_false(e, P, S, T), assignment(P, S, T).

% Map the correct answer to option/1 (the exception is the statement that is not forced)
% The exception is the statement that is false in some assignment
option(a) :- false_in_some_assignment(a).
option(b) :- false_in_some_assignment(b).
option(c) :- false_in_some_assignment(c).
option(d) :- false_in_some_assignment(d).
option(e) :- false_in_some_assignment(e).

% Ensure exactly one option is true (the exception)
:- #count{ X : option(X) } != 1.

#show option/1.