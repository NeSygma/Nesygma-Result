% Photographers and sections
photographer(fuentes). photographer(gagnon). photographer(hue).
section(lifestyle). section(metro). section(sports).

% Each section has exactly 2 photos
1 { photo(P, S) : photographer(P) } 2 :- section(S).

% Count photos per photographer
photo_count(P, N) :- N = #count{ S : photo(P, S) }, photographer(P).
:- photo_count(P, N), N < 1.
:- photo_count(P, N), N > 3.

% At least one Lifestyle photo by a photographer who also has at least one Metro photo
% This means: exists P such that photo(P, lifestyle) AND photo(P, metro)
:- not (photo(P, lifestyle), photo(P, metro)).

% #Hue in Lifestyle = #Fuentes in Sports
hue_lifestyle(N) :- N = #count{ S : photo(hue, lifestyle) }.
fuentes_sports(N) :- N = #count{ S : photo(fuentes, sports) }.
:- hue_lifestyle(N1), fuentes_sports(N2), N1 != N2.

% Gagnon has 0 photos in Sports
:- photo(gagnon, sports).

% Additional condition: Both photos in one section are by Gagnon
% This means: exists S such that both photos in S are by Gagnon
both_gagnon(S) :- section(S), photo(gagnon, S), #count{ P : photo(P, S) } = 2.
:- not (both_gagnon(lifestyle); both_gagnon(metro); both_gagnon(sports)).

% Map the correct answer to option/1
% Option A: Both photographs in the Lifestyle section are by Hue
option(a) :- photo(hue, lifestyle), #count{ P : photo(P, lifestyle) } = 2.

% Option B: One photograph in the Lifestyle section is by Fuentes and one is by Hue
option(b) :- photo(fuentes, lifestyle), photo(hue, lifestyle), #count{ P : photo(P, lifestyle) } = 2.

% Option C: Both photographs in the Metro section are by Fuentes
option(c) :- photo(fuentes, metro), #count{ P : photo(P, metro) } = 2.

% Option D: One photograph in the Metro section is by Gagnon and one is by Hue
option(d) :- photo(gagnon, metro), photo(hue, metro), #count{ P : photo(P, metro) } = 2.

% Option E: Both photographs in the Sports section are by Hue
option(e) :- photo(hue, sports), #count{ P : photo(P, sports) } = 2.

#show option/1.