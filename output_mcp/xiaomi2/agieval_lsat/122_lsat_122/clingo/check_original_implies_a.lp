band(u). band(v). band(w). band(x). band(y). band(z).
slot(1..6).

{ assign(B, S) : slot(S) } 1 :- band(B).
:- assign(B1, S), assign(B2, S), B1 != B2.

% Base constraints
:- assign(v, S1), assign(z, S2), S1 >= S2.
:- assign(u, S), S < 4.
:- assign(y, S), S > 3.

% Original constraints
:- assign(w, S1), assign(x, S2), S1 >= S2.
:- assign(z, S1), assign(x, S2), S1 >= S2.

% Violation of (A): exists B != u with B after X
violation_a :- assign(B, S1), assign(x, S2), B != u, S1 > S2.

% We want a model that satisfies original but violates (A)
:- not violation_a.

#show assign/2.