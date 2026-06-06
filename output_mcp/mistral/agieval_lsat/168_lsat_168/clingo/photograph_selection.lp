% Domains
photographer(fuentes; gagnon; hue).
section(lifestyle; metro; sports).
photo(1..6).

% Each photo is assigned to exactly one section
1 { section_photo(P, S) : section(S) } 1 :- photo(P).

% Each photo is by exactly one photographer
1 { photographer_photo(P, F) : photographer(F) } 1 :- photo(P).

% Exactly 2 photos per section
:- section(S), { section_photo(P, S) : photo(P) } != 2.

% Photographer count constraints: each photographer has at least 1 and at most 3 photos
photographer_count(F, N) :- N = #count{ P : photographer_photo(P, F) }, photographer(F).
:- photographer_count(fuentes, N), N < 1.
:- photographer_count(fuentes, N), N > 3.
:- photographer_count(gagnon, N), N < 1.
:- photographer_count(gagnon, N), N > 3.
:- photographer_count(hue, N), N < 1.
:- photographer_count(hue, N), N > 3.

% Constraint 4: At least one photo in Lifestyle must be by a photographer who has at least one photo in Metro
photographer_in_section(F, metro) :- photographer_photo(P, F), section_photo(P, metro).
:- section_photo(P, lifestyle), photographer_photo(P, F), not photographer_in_section(F, metro).

% Constraint 5: Number of Hue's photos in Lifestyle = number of Fuentes' photographs in Sports
hue_lifestyle_count(N) :- N = #count{ P : photographer_photo(P, hue), section_photo(P, lifestyle) }.
fuentes_sports_count(N) :- N = #count{ P : photographer_photo(P, fuentes), section_photo(P, sports) }.
:- hue_lifestyle_count(N1), fuentes_sports_count(N2), N1 != N2.

% Constraint 6: None of Gagnon's photographs can be in the Sports section
:- photographer_photo(P, gagnon), section_photo(P, sports).

% Define the assignments for each option as separate facts for clarity

% Option A: Lifestyle: both by Fuentes, Metro: 1 Fuentes 1 Hue, Sports: 1 Gagnon 1 Hue
option_a :-
    % Lifestyle: both by Fuentes
    photographer_photo(1, fuentes), photographer_photo(2, fuentes), section_photo(1, lifestyle), section_photo(2, lifestyle),
    % Metro: 1 Fuentes, 1 Hue
    photographer_photo(3, fuentes), photographer_photo(4, hue), section_photo(3, metro), section_photo(4, metro),
    % Sports: 1 Gagnon, 1 Hue
    photographer_photo(5, gagnon), photographer_photo(6, hue), section_photo(5, sports), section_photo(6, sports).

% Option B: Lifestyle: 1 Fuentes 1 Gagnon, Metro: 1 Fuentes 1 Gagnon, Sports: 2 Hue
option_b :-
    % Lifestyle: 1 Fuentes, 1 Gagnon
    photographer_photo(1, fuentes), photographer_photo(2, gagnon), section_photo(1, lifestyle), section_photo(2, lifestyle),
    % Metro: 1 Fuentes, 1 Gagnon
    photographer_photo(3, fuentes), photographer_photo(4, gagnon), section_photo(3, metro), section_photo(4, metro),
    % Sports: 2 Hue
    photographer_photo(5, hue), photographer_photo(6, hue), section_photo(5, sports), section_photo(6, sports).

% Option C: Lifestyle: both by Fuentes, Metro: both by Gagnon, Sports: both by Hue
option_c :-
    % Lifestyle: both by Fuentes
    photographer_photo(1, fuentes), photographer_photo(2, fuentes), section_photo(1, lifestyle), section_photo(2, lifestyle),
    % Metro: both by Gagnon
    photographer_photo(3, gagnon), photographer_photo(4, gagnon), section_photo(3, metro), section_photo(4, metro),
    % Sports: both by Hue
    photographer_photo(5, hue), photographer_photo(6, hue), section_photo(5, sports), section_photo(6, sports).

% Option D: Lifestyle: both by Gagnon, Metro: 1 Fuentes 1 Gagnon, Sports: 1 Fuentes 1 Hue
option_d :-
    % Lifestyle: both by Gagnon
    photographer_photo(1, gagnon), photographer_photo(2, gagnon), section_photo(1, lifestyle), section_photo(2, lifestyle),
    % Metro: 1 Fuentes, 1 Gagnon
    photographer_photo(3, fuentes), photographer_photo(4, gagnon), section_photo(3, metro), section_photo(4, metro),
    % Sports: 1 Fuentes, 1 Hue
    photographer_photo(5, fuentes), photographer_photo(6, hue), section_photo(5, sports), section_photo(6, sports).

% Option E: Lifestyle: 1 Gagnon 1 Hue, Metro: both by Hue, Sports: 1 Fuentes 1 Hue
option_e :-
    % Lifestyle: 1 Gagnon, 1 Hue
    photographer_photo(1, gagnon), photographer_photo(2, hue), section_photo(1, lifestyle), section_photo(2, lifestyle),
    % Metro: both by Hue
    photographer_photo(3, hue), photographer_photo(4, hue), section_photo(3, metro), section_photo(4, metro),
    % Sports: 1 Fuentes, 1 Hue
    photographer_photo(5, fuentes), photographer_photo(6, hue), section_photo(5, sports), section_photo(6, sports).

% Map the correct answer to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.