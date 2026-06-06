% Lifestyle, Metro, Sports sections
section(lifestyle). section(metro). section(sports).

% Photographers
photographer(fuentes). photographer(gagnon). photographer(hue).

% Six distinct photos
photo_id(1..6).

% Assign each photo to exactly one section and one photographer
1 { photo(PhotoID, Section, Photographer) : section(Section), photographer(Photographer) } 1 :- photo_id(PhotoID).

% Exactly two photos per section
section_photo_count(Section, N) :- section(Section), N = #count { PhotoID : photo(PhotoID, Section, _) }.
:- section_photo_count(Section, N), N != 2.

% Total photos per photographer
photographer_total(Photographer, N) :- photographer(Photographer), N = #count { PhotoID : photo(PhotoID, _, Photographer) }.

% Constraint 1: each photographer appears 1-3 times
:- photographer_total(Photographer, N), N < 1.
:- photographer_total(Photographer, N), N > 3.

% Constraint 2: at least one L photo by a photographer who also has at least one M photo
constraint2 :- photo(_, lifestyle, P), photo(_, metro, P).
:- not constraint2.

% Constraint 3: number of Hue's photos in L equals number of Fuentes's photos in S
hue_lifestyle(N) :- N = #count { PhotoID : photo(PhotoID, lifestyle, hue) }.
fuentes_sports(N) :- N = #count { PhotoID : photo(PhotoID, sports, fuentes) }.
:- hue_lifestyle(N1), fuentes_sports(N2), N1 != N2.

% Constraint 4: no Gagnon in Sports
:- photo(_, sports, gagnon).

% Assumption: both photos in Lifestyle are by Hue
% This means any photo assigned to Lifestyle must have photographer hue
:- photo(PhotoID, lifestyle, P), P != hue.
% Also ensure exactly two photos in Lifestyle (already enforced by section count)

% Compute totals for each photographer
total_fuentes(N) :- photographer_total(fuentes, N).
total_gagnon(N) :- photographer_total(gagnon, N).
total_hue(N) :- photographer_total(hue, N).

% Answer choices
option(a) :- total_fuentes(1).
option(b) :- total_fuentes(3).
option(c) :- total_gagnon(1).
option(d) :- total_gagnon(2).
option(e) :- total_hue(2).

#show option/1.