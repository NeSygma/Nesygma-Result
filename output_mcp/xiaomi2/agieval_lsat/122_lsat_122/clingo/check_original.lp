band(u). band(v). band(w). band(x). band(y). band(z).
slot(1..6).

{ assign(B, S) : slot(S) } 1 :- band(B).
:- assign(B1, S), assign(B2, S), B1 != B2.

% Base constraints
:- assign(v, S1), assign(z, S2), S1 >= S2.
:- assign(u, S), S < 4.
:- assign(y, S), S > 3.

% Original constraint: W < X and Z < X
:- assign(w, Sw), assign(x, Sx), Sw >= Sx.
:- assign(z, Sz), assign(x, Sx), Sz >= Sx.

#show assign/2.