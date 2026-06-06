band(u). band(v). band(w). band(x). band(y). band(z).
slot(1..6).

{ assign(B, S) : slot(S) } 1 :- band(B).
:- assign(B1, S), assign(B2, S), B1 != B2.

% Base constraints (always present)
:- assign(v, S1), assign(z, S2), S1 >= S2.
:- assign(u, S), S < 4.
:- assign(y, S), S > 3.

% Original constraint: W < X and Z < X
orig_ok :- assign(w, S1), assign(x, S2), S1 < S2, assign(z, S3), assign(x, S4), S3 < S4.
:- not orig_ok.

% Check each option:
% (A) Only U can be after X: for all B != u, B's slot < X's slot
opt_a_ok :- assign(x, Sx), assign(v, Sv), Sv < Sx, assign(w, Sw), Sw < Sx, assign(y, Sy), Sy < Sx, assign(z, Sz), Sz < Sx.

% (B) V < W < Z
opt_b_ok :- assign(v, Sv), assign(w, Sw), assign(z, Sz), Sv < Sw, Sw < Sz.

% (C) V < X and W < X
opt_c_ok :- assign(v, Sv), assign(x, Sx), Sv < Sx, assign(w, Sw), Sw < Sx.

% (D) X immediately before or after U
opt_d_ok :- assign(x, Sx), assign(u, Su), Sx = Su + 1.
opt_d_ok :- assign(x, Sx), assign(u, Su), Sx = Su - 1.

% (E) X in slot 5 or 6
opt_e_ok :- assign(x, 5).
opt_e_ok :- assign(x, 6).

% Show which options are satisfied
show_a :- opt_a_ok.
show_b :- opt_b_ok.
show_c :- opt_c_ok.
show_d :- opt_d_ok.
show_e :- opt_e_ok.

#show show_a/0.
#show show_b/0.
#show show_c/0.
#show show_d/0.
#show show_e/0.
#show assign/2.