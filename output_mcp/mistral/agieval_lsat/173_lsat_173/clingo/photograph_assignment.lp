% Define sections and photographers
section(lifestyle; metro; sports).
photographer(fuentes; gagnon; hue).

% Exactly 2 photos per section
1 { photo(S, P) : photographer(P) } 2 :- section(S).

% Each photographer has at least 1 and at most 3 photos total
:- photographer(P), #count { S : photo(S, P) } < 1.
:- photographer(P), #count { S : photo(S, P) } > 3.

% Helper: photographer has at least one photo in a section
has_photo_in(P, S) :- photo(S, P).

% Constraint: At least one photo in Lifestyle must be by a photographer who has at least one photo in Metro
:- photo(lifestyle, P), not has_photo_in(P, metro).

% Constraint: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
hue_lifestyle_count(N) :- N = #count { P : photo(lifestyle, P), P = hue }.
fuentes_sports_count(N) :- N = #count { P : photo(sports, P), P = fuentes }.
:- hue_lifestyle_count(N), fuentes_sports_count(M), N != M.

% Constraint: None of Gagnon's photos in Sports
:- photo(sports, gagnon).

% Scenario: Both photographs in one of the three sections are by Gagnon
% (This is the condition given in the question)
section_both_gagnon(lifestyle) :- photo(lifestyle, gagnon), photo(lifestyle, gagnon).
section_both_gagnon(metro) :- photo(metro, gagnon), photo(metro, gagnon).
section_both_gagnon(sports) :- photo(sports, gagnon), photo(sports, gagnon).

% Ensure at least one section has both photos by Gagnon
:- not section_both_gagnon(lifestyle), not section_both_gagnon(metro), not section_both_gagnon(sports).

% --- Answer Choice Conditions ---
% (A) Both photographs in the Lifestyle section are by Hue.
option(a) :- photo(lifestyle, hue), photo(lifestyle, hue).

% (B) One photograph in the Lifestyle section is by Fuentes and one is by Hue.
option(b) :- photo(lifestyle, fuentes), photo(lifestyle, hue).

% (C) Both photographs in the Metro section are by Fuentes.
option(c) :- photo(metro, fuentes), photo(metro, fuentes).

% (D) One photograph in the Metro section is by Gagnon and one is by Hue.
option(d) :- photo(metro, gagnon), photo(metro, hue).

% (E) Both photographs in the Sports section are by Hue.
option(e) :- photo(sports, hue), photo(sports, hue).

% Ensure only one option is selected as possible
:- option(X), option(Y), X != Y.

#show option/1.