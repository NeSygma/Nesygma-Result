% Define the entities
photographer(fuentes; gagnon; hue).
section(lifestyle; metro; sports).
photo(1..6).

% Each photo has exactly one photographer
1 { photographer_of(P, Ph) : photographer(Ph) } 1 :- photo(P).

% Each photo is assigned to exactly one section
1 { assigned_to(P, S) : section(S) } 1 :- photo(P).

% Exactly 2 photos per section
2 { assigned_to(P, S) : photo(P) } 2 :- section(S).

% Each photographer has at least 1, at most 3 photos
1 { photographer_of(P, Ph) : photo(P) } 3 :- photographer(Ph).

% No Gagnon photos in Sports
:- photographer_of(P, gagnon), assigned_to(P, sports).

% Given condition: One Metro photo is by Fuentes, one Metro photo is by Hue
fuentes_metro_count(N) :- N = #count { P : photographer_of(P, fuentes), assigned_to(P, metro) }.
hue_metro_count(N) :- N = #count { P : photographer_of(P, hue), assigned_to(P, metro) }.
:- fuentes_metro_count(N), N != 1.
:- hue_metro_count(N), N != 1.

% Define which photographers have at least one Metro photo
has_metro_photo(Ph) :- photographer_of(P, Ph), assigned_to(P, metro).

% At least one Lifestyle photo is by a photographer who has at least one Metro photo
lifestyle_photo_by_metro_photographer :-
    assigned_to(P, lifestyle),
    photographer_of(P, Ph),
    has_metro_photo(Ph).
:- not lifestyle_photo_by_metro_photographer.

% Number of Hue's photos in Lifestyle = number of Fuentes' photos in Sports
hue_lifestyle_count(N) :- N = #count { P : photographer_of(P, hue), assigned_to(P, lifestyle) }.
fuentes_sports_count(N) :- N = #count { P : photographer_of(P, fuentes), assigned_to(P, sports) }.
:- hue_lifestyle_count(N1), fuentes_sports_count(N2), N1 != N2.

% Answer choice conditions
% Option A: Both Lifestyle photos are by Fuentes
both_lifestyle_fuentes :-
    assigned_to(P1, lifestyle), assigned_to(P2, lifestyle), P1 < P2,
    photographer_of(P1, fuentes), photographer_of(P2, fuentes).

% Option B: Both Lifestyle photos are by Gagnon
both_lifestyle_gagnon :-
    assigned_to(P1, lifestyle), assigned_to(P2, lifestyle), P1 < P2,
    photographer_of(P1, gagnon), photographer_of(P2, gagnon).

% Option C: One Lifestyle is by Gagnon and one is by Hue
one_lifestyle_gagnon_one_hue :-
    assigned_to(P1, lifestyle), assigned_to(P2, lifestyle), P1 < P2,
    photographer_of(P1, gagnon), photographer_of(P2, hue).
one_lifestyle_gagnon_one_hue :-
    assigned_to(P1, lifestyle), assigned_to(P2, lifestyle), P1 < P2,
    photographer_of(P1, hue), photographer_of(P2, gagnon).

% Option D: Both Lifestyle photos are by Hue
both_lifestyle_hue :-
    assigned_to(P1, lifestyle), assigned_to(P2, lifestyle), P1 < P2,
    photographer_of(P1, hue), photographer_of(P2, hue).

% Option E: Both Sports photos are by Fuentes
both_sports_fuentes :-
    assigned_to(P1, sports), assigned_to(P2, sports), P1 < P2,
    photographer_of(P1, fuentes), photographer_of(P2, fuentes).

% Map the correct answer to option/1
option(a) :- both_lifestyle_fuentes.
option(b) :- both_lifestyle_gagnon.
option(c) :- one_lifestyle_gagnon_one_hue.
option(d) :- both_lifestyle_hue.
option(e) :- both_sports_fuentes.

#show option/1.