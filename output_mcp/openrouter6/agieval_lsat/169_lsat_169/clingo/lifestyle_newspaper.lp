% Lifestyle, Metro, Sports sections
section(lifestyle). section(metro). section(sports).

% Photographers
photographer(fuentes). photographer(gagnon). photographer(hue).

% Exactly two photos per section
{ photo(Section, Photographer) : photographer(Photographer) } 2 :- section(Section).

% Total photos per photographer
total(Photographer, N) :- photographer(Photographer), N = #count { Section : photo(Section, Photographer) }.

% Constraint 1: each photographer appears 1-3 times
:- total(Photographer, N), N < 1.
:- total(Photographer, N), N > 3.

% Constraint 2: at least one L photo by a photographer who also has at least one M photo
constraint2 :- photo(lifestyle, P), photo(metro, P).
:- not constraint2.

% Constraint 3: number of Hue's photos in L equals number of Fuentes's photos in S
hue_lifestyle(N) :- N = #count { 1 : photo(lifestyle, hue) }.
fuentes_sports(N) :- N = #count { 1 : photo(sports, fuentes) }.
:- hue_lifestyle(N1), fuentes_sports(N2), N1 != N2.

% Constraint 4: no Gagnon in Sports
:- photo(sports, gagnon).

% Assumption: both photos in Lifestyle are by Hue
2 { photo(lifestyle, hue) } 2.
:- photo(lifestyle, P), P != hue.

% Compute totals for each photographer
total_fuentes(N) :- total(fuentes, N).
total_gagnon(N) :- total(gagnon, N).
total_hue(N) :- total(hue, N).

% Answer choices
option(a) :- total_fuentes(1).
option(b) :- total_fuentes(3).
option(c) :- total_gagnon(1).
option(d) :- total_gagnon(2).
option(e) :- total_hue(2).

#show option/1.