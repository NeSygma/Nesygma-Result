% Domain
solo(1..5).
person(wayne; zara).
% Exactly one pianist per solo
{ pianist(S, wayne); pianist(S, zara) } = 1 :- solo(S).
% Exactly one type per solo
{ type(S, modern); type(S, traditional) } = 1 :- solo(S).

% Constraint 1: third solo is traditional
:- not type(3, traditional).

% Constraint 2: exactly two traditional pieces, consecutive
% Count traditional
num_trad(N) :- N = #count { S : type(S, traditional) }.
:- num_trad(N), N != 2.
% adjacency existence
adjacent_trad :- solo(S), S < 5, type(S, traditional), type(S+1, traditional).
:- not adjacent_trad.

% Constraint 3: fourth solo condition (either Wayne traditional OR Zara modern)
cond4a :- pianist(4, wayne), type(4, traditional).
cond4b :- pianist(4, zara), type(4, modern).
:- not cond4a, not cond4b.

% Constraint 4: pianist of second solo != pianist of fifth solo
:- pianist(2, P), pianist(5, P).

% Constraint 5: No traditional until Wayne performs a modern earlier
earlier_modern(S) :- solo(S), pianist(J, wayne), type(J, modern), solo(J), J < S.
:- type(S, traditional), not earlier_modern(S).

% Premise: pianist of first solo = pianist of second solo
pianist(2, P) :- pianist(1, P).

% Options mapping
option(a) :- pianist(1, zara).
option(b) :- pianist(3, wayne).
option(c) :- pianist(5, zara).
option(d) :- type(2, traditional).
option(e) :- type(4, modern).

% Exactly one option must hold
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.