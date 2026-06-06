% Sections and photographers
section(lifestyle; metro; sports).
photographer(fuentes; gagnon; hue).

% Photos: 6 photos, 2 per section
photo(1..6).
section_of(1, lifestyle). section_of(2, lifestyle).
section_of(3, metro). section_of(4, metro).
section_of(5, sports). section_of(6, sports).

% Assign photographers to photos
{ assigned_to(P, Ph) : photographer(Ph) } = 1 :- photo(P).

% Constraint: Each photographer has at least 1 and at most 3 photos
:- photographer(Ph), #count{P : assigned_to(P, Ph)} < 1.
:- photographer(Ph), #count{P : assigned_to(P, Ph)} > 3.

% Constraint: At least one Lifestyle photo is by a photographer who has at least one Metro photo
% Define which photographers have at least one Metro photo
has_metro_photo(Ph) :- assigned_to(P, Ph), section_of(P, metro).

% Define which photographers have at least one Lifestyle photo
has_lifestyle_photo(Ph) :- assigned_to(P, Ph), section_of(P, lifestyle).

% Ensure at least one photographer has both a Lifestyle and Metro photo
:- has_lifestyle_photo(Ph), has_metro_photo(Ph), not has_both(Ph).
has_both(Ph) :- has_lifestyle_photo(Ph), has_metro_photo(Ph).
:- photographer(Ph), has_lifestyle_photo(Ph), not has_metro_photo(Ph).

% Constraint: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
hue_in_lifestyle_count(N) :- N = #count{P : assigned_to(P, hue), section_of(P, lifestyle)}.
fuentes_in_sports_count(N) :- N = #count{P : assigned_to(P, fuentes), section_of(P, sports)}.
:- hue_in_lifestyle_count(N), fuentes_in_sports_count(M), N != M.

% Constraint: None of Gagnon's photographs can be in Sports
:- assigned_to(P, gagnon), section_of(P, sports).

% Given condition: In Lifestyle, exactly one Fuentes and exactly one Hue
:- #count{P : assigned_to(P, fuentes), section_of(P, lifestyle)} != 1.
:- #count{P : assigned_to(P, hue), section_of(P, lifestyle)} != 1.

% Ensure at least one solution exists (sentinel)
solution_exists.

% Answer choice conditions
% (A) Both photographs in the Metro section are by Fuentes.
option(a) :- assigned_to(3, fuentes), assigned_to(4, fuentes).

% (B) Both photographs in the Metro section are by Gagnon.
option(b) :- assigned_to(3, gagnon), assigned_to(4, gagnon).

% (C) Exactly one photograph in the Metro section is by Hue.
option(c) :- #count{P : assigned_to(P, hue), section_of(P, metro)} = 1.

% (D) Both photographs in the Sports section are by Hue.
option(d) :- assigned_to(5, hue), assigned_to(6, hue).

% (E) Neither photograph in the Sports section is by Hue.
option(e) :- not assigned_to(5, hue), not assigned_to(6, hue).

#show option/1.
#show solution_exists.