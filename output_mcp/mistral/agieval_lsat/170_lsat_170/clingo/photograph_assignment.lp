% Define sections and photographers
section(lifestyle; metro; sports).
photographer(fuentes; gagnon; hue).

% Define 6 distinct photographs
photo(1..6).

% Assign photos to sections: exactly 2 photos per section
1 { assigned(P, S) : photo(P) } 2 :- section(S).

% Each photo is assigned to exactly one section
:- assigned(P, S1), assigned(P, S2), S1 != S2.

% Each photo is taken by exactly one photographer
1 { taken_by(P, F) : photographer(F) } 1 :- photo(P).

% Each photographer has at least 1 and at most 3 photos
:- photographer(F), #count { P : taken_by(P, F) } < 1.
:- photographer(F), #count { P : taken_by(P, F) } > 3.

% Constraint: At least one Lifestyle photo must be by a photographer who has at least one Metro photo
lifestyle_photo_by(F) :- taken_by(P, F), assigned(P, lifestyle).
metro_photo_by(F) :- taken_by(P, F), assigned(P, metro).
:- lifestyle_photo_by(F), photographer(F), not metro_photo_by(F).

% Constraint: Number of Hue's photographs in Lifestyle = Number of Fuentes' photographs in Sports
hue_lifestyle_count(N) :- N = #count { P : taken_by(P, hue), assigned(P, lifestyle) }.
fuentes_sports_count(N) :- N = #count { P : taken_by(P, fuentes), assigned(P, sports) }.
:- hue_lifestyle_count(N1), fuentes_sports_count(N2), N1 != N2.

% Constraint: None of Gagnon's photographs can be in the Sports section
:- taken_by(P, gagnon), assigned(P, sports).

% Given condition: One Lifestyle photo is by Gagnon and one is by Hue
:- not 1 { taken_by(P, F) : F=gagnon, assigned(P, lifestyle) }.
:- not 1 { taken_by(P, F) : F=hue, assigned(P, lifestyle) }.

% Map the correct answer to option/1
% (A) Exactly one photograph in the Metro section is by Fuentes
option(a) :- 1 { taken_by(P, fuentes) : assigned(P, metro) } 1.

% (B) Exactly one photograph in the Metro section is by Gagnon
option(b) :- 1 { taken_by(P, gagnon) : assigned(P, metro) } 1.

% (C) Both photographs in the Metro section are by Gagnon
option(c) :- 2 { taken_by(P, gagnon) : assigned(P, metro) } 2.

% (D) Exactly one photograph in the Sports section is by Hue
option(d) :- 1 { taken_by(P, hue) : assigned(P, sports) } 1.

% (E) Both photographs in the Sports section are by Hue
option(e) :- 2 { taken_by(P, hue) : assigned(P, sports) } 2.

#show option/1.