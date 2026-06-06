% Base facts: sections and photographers
section(lifestyle).
section(metro).
section(sports).

photographer(fuentes).
photographer(gagnon).
photographer(hue).

% Each section has exactly two photographs
1 { assigned_photo(Section, Photographer) : photographer(Photographer) } 2 :- section(Section).

% Each photographer must have at least one but no more than three photographs
:- photographer(P), #count { S, P : assigned_photo(S, P) } < 1.
:- photographer(P), #count { S, P : assigned_photo(S, P) } > 3.

% At least one photograph in the Lifestyle section must be by a photographer who has at least one photograph in the Metro section.
metro_photographer(P) :- assigned_photo(metro, P).
lifestyle_photographer(P) :- assigned_photo(lifestyle, P).
:- assigned_photo(lifestyle, P), not metro_photographer(P).

% The number of Hue's photographs in the Lifestyle section must be the same as the number of Fuentes' photographs in the Sports section.
hue_lifestyle_count(Count) :- Count = #count { S : assigned_photo(S, hue), section(S) }.
fuentes_sports_count(Count) :- Count = #count { S : assigned_photo(S, fuentes), section(S) }.
:- hue_lifestyle_count(Count), fuentes_sports_count(Count), Count != Count.

% None of Gagnon's photographs can be in the Sports section.
:- assigned_photo(sports, gagnon).

% Additional constraint: Both photographs in one of the three sections are by Gagnon
both_gagnon_in_section(S) :- section(S), assigned_photo(S, gagnon), assigned_photo(S, gagnon).
:- not 1 { both_gagnon_in_section(S) : section(S) } 1.

% Define the answer choices as conditions
% (A) Both photographs in the Lifestyle section are by Hue.
option(a) :- assigned_photo(lifestyle, hue), assigned_photo(lifestyle, hue).

% (B) One photograph in the Lifestyle section is by Fuentes and one is by Hue.
option(b) :- assigned_photo(lifestyle, fuentes), assigned_photo(lifestyle, hue).

% (C) Both photographs in the Metro section are by Fuentes.
option(c) :- assigned_photo(metro, fuentes), assigned_photo(metro, fuentes).

% (D) One photograph in the Metro section is by Gagnon and one is by Hue.
option(d) :- assigned_photo(metro, gagnon), assigned_photo(metro, hue).

% (E) Both photographs in the Sports section are by Hue.
option(e) :- assigned_photo(sports, hue), assigned_photo(sports, hue).

#show option/1.