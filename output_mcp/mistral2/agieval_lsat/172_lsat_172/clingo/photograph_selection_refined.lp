% Base facts: sections and photographers
section(lifestyle).
section(metro).
section(sports).

photographer(fuentes).
photographer(gagnon).
photographer(hue).

% Each section has exactly two photographs
2 { assigned_photo(Section, Photographer) : photographer(Photographer) } 2 :- section(Section).

% Count the number of photographs per photographer
fuentes_count(N) :- N = #count { S : assigned_photo(S, fuentes) }.
gagnon_count(N) :- N = #count { S : assigned_photo(S, gagnon) }.
hue_count(N) :- N = #count { S : assigned_photo(S, hue) }.

% Each photographer must have at least one but no more than three photographs
:- photographer(P), P = fuentes, fuentes_count(N), N < 1.
:- photographer(P), P = fuentes, fuentes_count(N), N > 3.
:- photographer(P), P = gagnon, gagnon_count(N), N < 1.
:- photographer(P), P = gagnon, gagnon_count(N), N > 3.
:- photographer(P), P = hue, hue_count(N), N < 1.
:- photographer(P), P = hue, hue_count(N), N > 3.

% At least one photograph in the Lifestyle section must be by a photographer who has at least one photograph in the Metro section.
lifestyle_photographer(P) :- assigned_photo(lifestyle, P).
metro_photographer(P) :- assigned_photo(metro, P).
:- lifestyle_photographer(P), not metro_photographer(P).

% The number of Hue's photographs in the Lifestyle section must be the same as the number of Fuentes' photographs in the Sports section.
hue_lifestyle_count(N) :- N = #count { P : assigned_photo(lifestyle, P), P = hue }.
fuentes_sports_count(N) :- N = #count { P : assigned_photo(sports, P), P = fuentes }.
:- hue_lifestyle_count(N), fuentes_sports_count(M), N != M.

% None of Gagnon's photographs can be in the Sports section.
:- assigned_photo(sports, gagnon).

% Given condition: One photograph in the Lifestyle section is by Fuentes and one is by Hue.
:- not 1 { assigned_photo(lifestyle, fuentes) } 1.
:- not 1 { assigned_photo(lifestyle, hue) } 1.

% Helper predicates for counting assignments per section and photographer
fuentes_metro_count(N) :- N = #count { S : assigned_photo(S, fuentes), S = metro }.
gagnon_metro_count(N) :- N = #count { S : assigned_photo(S, gagnon), S = metro }.
hue_metro_count(N) :- N = #count { S : assigned_photo(S, hue), S = metro }.

fuentes_sports_count(N) :- N = #count { S : assigned_photo(S, fuentes), S = sports }.
gagnon_sports_count(N) :- N = #count { S : assigned_photo(S, gagnon), S = sports }.
hue_sports_count(N) :- N = #count { S : assigned_photo(S, hue), S = sports }.

% Map the correct answer to option/1 (MANDATORY)
% (A) Both photographs in the Metro section are by Fuentes.
option(a) :- fuentes_metro_count(2).

% (B) Both photographs in the Metro section are by Gagnon.
option(b) :- gagnon_metro_count(2).

% (C) Exactly one photograph in the Metro section is by Hue.
option(c) :- hue_metro_count(1).

% (D) Both photographs in the Sports section are by Hue.
option(d) :- hue_sports_count(2).

% (E) Neither photograph in the Sports section is by Hue.
option(e) :- hue_sports_count(0).

#show option/1.