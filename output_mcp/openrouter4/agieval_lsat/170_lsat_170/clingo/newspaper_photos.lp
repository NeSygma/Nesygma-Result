%% Domain
photo(1..6).
section(l; m; s).
photographer(f; g; h).

%% Each photo in exactly one section
1 { in_section(P, S) : section(S) } 1 :- photo(P).

%% Each photo by exactly one photographer
1 { by_photographer(P, Ph) : photographer(Ph) } 1 :- photo(P).

%% Exactly 2 photos per section
:- section(S), #count { P : photo(P), in_section(P, S) } != 2.

%% Constraint 1: each photographer has 1-3 photos total
:- photographer(Ph), #count { P : photo(P), by_photographer(P, Ph) } < 1.
:- photographer(Ph), #count { P : photo(P), by_photographer(P, Ph) } > 3.

%% Constraint 2: At least one photographer has a photo in Lifestyle and a photo in Metro
has_both_lm :- photographer(Ph), in_section(P1, l), by_photographer(P1, Ph),
               in_section(P2, m), by_photographer(P2, Ph).
:- not has_both_lm.

%% Constraint 3: # Hue in Lifestyle = # Fuentes in Sports
cnt_h_l(N) :- N = #count { P : photo(P), in_section(P, l), by_photographer(P, h) }.
cnt_f_s(N) :- N = #count { P : photo(P), in_section(P, s), by_photographer(P, f) }.
:- cnt_h_l(N1), cnt_f_s(N2), N1 != N2.

%% Constraint 4: No Gagnon in Sports
:- in_section(P, s), by_photographer(P, g).

%% Given: Lifestyle has 1 by Gagnon and 1 by Hue
:- #count { P : photo(P), in_section(P, l), by_photographer(P, g) } != 1.
:- #count { P : photo(P), in_section(P, l), by_photographer(P, h) } != 1.

%% Count for options
cnt_m_f(N) :- N = #count { P : photo(P), in_section(P, m), by_photographer(P, f) }.
cnt_m_g(N) :- N = #count { P : photo(P), in_section(P, m), by_photographer(P, g) }.
cnt_s_h(N) :- N = #count { P : photo(P), in_section(P, s), by_photographer(P, h) }.

option(a) :- cnt_m_f(1).
option(b) :- cnt_m_g(1).
option(c) :- cnt_m_g(2).
option(d) :- cnt_s_h(1).
option(e) :- cnt_s_h(2).

#show option/1.