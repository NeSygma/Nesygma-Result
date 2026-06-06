% Domains and basic facts
section(lifestyle; metro; sports).
photographer(fuentes; gagnon; hue).

% Six photographs in total, exactly two per section
photo(1..6).

% Assign each photo to a section and a photographer
1 { section_photo(P, S) : section(S) } 1 :- photo(P).
1 { assigned_to(P, F) : photographer(F) } 1 :- photo(P).

% Exactly two photos per section
:- section(S), #count { P : section_photo(P, S) } != 2.

% Constraints on photographers:
% For each photographer, at least one but no more than three photographs
:- photographer(F), #count { P : assigned_to(P, F) } < 1.
:- photographer(F), #count { P : assigned_to(P, F) } > 3.

% At least one photograph in the Lifestyle section must be by a photographer
% who has at least one photograph in the Metro section.
metro_photographer(F) :- assigned_to(P, F), section_photo(P, metro).
lifestyle_photographer(F) :- assigned_to(P, F), section_photo(P, lifestyle).
:- not 1 { F : lifestyle_photographer(F), metro_photographer(F) } 1.

% The number of Hue's photographs in the Lifestyle section must be the same as
% the number of Fuentes' photographs in the Sports section.
hue_lifestyle_count(N) :- N = #count { P : assigned_to(P, hue), section_photo(P, lifestyle) }.
fuentes_sports_count(N) :- N = #count { P : assigned_to(P, fuentes), section_photo(P, sports) }.
:- hue_lifestyle_count(N1), fuentes_sports_count(N2), N1 != N2.

% None of Gagnon's photographs can be in the Sports section.
:- assigned_to(P, gagnon), section_photo(P, sports).

% Hypothesis: Both photographs in the Lifestyle section are by Hue.
% This is a specific scenario to evaluate.
:- section_photo(P1, lifestyle), section_photo(P2, lifestyle), P1 != P2,
   not assigned_to(P1, hue).
:- section_photo(P1, lifestyle), section_photo(P2, lifestyle), P1 != P2,
   not assigned_to(P2, hue).

% Count the number of photographs by each photographer
fuentes_count(N) :- N = #count { P : assigned_to(P, fuentes) }.
gagnon_count(N) :- N = #count { P : assigned_to(P, fuentes) }.
hue_count(N) :- N = #count { P : assigned_to(P, hue) }.

% Map the correct answer to option/1 (MANDATORY)
% (A) Exactly one is by Fuentes.
option(a) :- fuentes_count(1).

% (B) Exactly three are by Fuentes.
option(b) :- fuentes_count(3).

% (C) Exactly one is by Gagnon.
option(c) :- gagnon_count(1).

% (D) Exactly two are by Gagnon.
option(d) :- gagnon_count(2).

% (E) Exactly two are by Hue.
option(e) :- hue_count(2).

#show option/1.