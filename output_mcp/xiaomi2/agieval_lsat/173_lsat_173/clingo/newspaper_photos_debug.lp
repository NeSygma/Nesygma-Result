% Domains
photo(1..6).
section(lifestyle). section(metro). section(sports).
photographer(fuentes). photographer(gagnon). photographer(hue).

% Each photo is assigned to exactly one section
1 { in_section(P, S) : section(S) } 1 :- photo(P).

% Each photo is by exactly one photographer
1 { by_photographer(P, Ph) : photographer(Ph) } 1 :- photo(P).

% Exactly 2 photos per section
2 { in_section(P, S) : photo(P) } 2 :- section(S).

% Each photographer has at least 1 but no more than 3 photos total
:- photographer(Ph), #count{P : photo(P), by_photographer(P, Ph)} < 1.
:- photographer(Ph), #count{P : photo(P), by_photographer(P, Ph)} > 3.

% At least one photo in Lifestyle is by a photographer who also has at least one photo in Metro
exists_shared :- photographer(Ph), in_section(P1, lifestyle), by_photographer(P1, Ph), in_section(P2, metro), by_photographer(P2, Ph).
:- not exists_shared.

% Number of Hue photos in Lifestyle = Number of Fuentes photos in Sports
hue_lifestyle(N) :- N = #count{P : photo(P), in_section(P, lifestyle), by_photographer(P, hue)}.
fuentes_sports(M) :- M = #count{P : photo(P), in_section(P, sports), by_photographer(P, fuentes)}.
:- hue_lifestyle(N), fuentes_sports(M), N != M.

% No Gagnon photos in Sports
:- in_section(P, sports), by_photographer(P, gagnon).

% Condition: Both photos in one section are by Gagnon (must be Lifestyle or Metro since no Gagnon in Sports)
gagnon_both(S) :- section(S), S != sports, #count{P : photo(P), in_section(P, S), by_photographer(P, gagnon)} = 2.
:- not gagnon_both(lifestyle), not gagnon_both(metro).

% Answer choice conditions
% (A) Both photographs in the Lifestyle section are by Hue
cond_a :- #count{P : photo(P), in_section(P, lifestyle), by_photographer(P, hue)} = 2.

% (B) One photograph in the Lifestyle section is by Fuentes and one is by Hue
cond_b :- #count{P : photo(P), in_section(P, lifestyle), by_photographer(P, fuentes)} = 1,
          #count{P : photo(P), in_section(P, lifestyle), by_photographer(P, hue)} = 1.

% (C) Both photographs in the Metro section are by Fuentes
cond_c :- #count{P : photo(P), in_section(P, metro), by_photographer(P, fuentes)} = 2.

% (D) One photograph in the Metro section is by Gagnon and one is by Hue
cond_d :- #count{P : photo(P), in_section(P, metro), by_photographer(P, gagnon)} = 1,
          #count{P : photo(P), in_section(P, metro), by_photographer(P, hue)} = 1.

% (E) Both photographs in the Sports section are by Hue
cond_e :- #count{P : photo(P), in_section(P, sports), by_photographer(P, hue)} = 2.

option(a) :- cond_a.
option(b) :- cond_b.
option(c) :- cond_c.
option(d) :- cond_d.
option(e) :- cond_e.

#show option/1.
#show in_section/2.
#show by_photographer/2.
#show cond_a.
#show cond_b.
#show cond_c.
#show cond_d.
#show cond_e.
#show gagnon_both/1.