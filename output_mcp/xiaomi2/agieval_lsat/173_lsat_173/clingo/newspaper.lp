% Domains
section(l). section(m). section(s).
photographer(f). photographer(g). photographer(h).
n(0). n(1). n(2).

% Each section-photographer pair has exactly one count from 0,1,2.
1 { count(S, P, N) : n(N) } 1 :- section(S), photographer(P).

% Each section has total 2 photos.
:- section(S), Total = #sum{ N, P : count(S, P, N) }, Total != 2.

% Each photographer has total between 1 and 3.
:- photographer(P), Total = #sum{ N, S : count(S, P, N) }, Total < 1.
:- photographer(P), Total = #sum{ N, S : count(S, P, N) }, Total > 3.

% Constraint 2: There exists a photographer with at least one in Lifestyle and at least one in Metro.
exists_p :- count(l, P, N1), count(m, P, N2), N1 > 0, N2 > 0.
:- not exists_p.

% Constraint 3: Number of Hue in Lifestyle equals number of Fuentes in Sports.
:- count(l, h, N1), count(s, f, N2), N1 != N2.

% Constraint 4: No Gagnon in Sports.
:- count(s, g, N), N > 0.

% Condition: There is a section (not Sports) with both photos by Gagnon.
condition :- section(S), S != s, count(S, g, 2).
:- not condition.

% Option definitions:
option_a_holds :- count(l, h, 2).
option_b_holds :- count(l, f, 1), count(l, h, 1).
option_c_holds :- count(m, f, 2).
option_d_holds :- count(m, g, 1), count(m, h, 1).
option_e_holds :- count(s, h, 2).

% Choose one option to enforce.
{ enforce_a; enforce_b; enforce_c; enforce_d; enforce_e } 1.

% If an option is enforced, it must hold.
:- enforce_a, not option_a_holds.
:- enforce_b, not option_b_holds.
:- enforce_c, not option_c_holds.
:- enforce_d, not option_d_holds.
:- enforce_e, not option_e_holds.

% Output the enforced option as the answer.
answer(a) :- enforce_a.
answer(b) :- enforce_b.
answer(c) :- enforce_c.
answer(d) :- enforce_d.
answer(e) :- enforce_e.

#show answer/1.