% Sections and photographers
section(lifestyle; metro; sports).
photographer(fuentes; gagnon; hue).

% Each section has exactly 2 photos
% Represent as photo(Section, PhotoID)
photo(Section, 1..2) :- section(Section).

% Assign a photographer to each photo
1 { assigned_to(Section, PhotoID, Photographer) : photographer(Photographer) } 1 :-
    photo(Section, PhotoID).

% Count photos per photographer per section
fuentes_lifestyle_count(N) :- N = #count{ PhotoID : assigned_to(lifestyle, PhotoID, fuentes) }.
fuentes_metro_count(N) :- N = #count{ PhotoID : assigned_to(metro, PhotoID, fuentes) }.
fuentes_sports_count(N) :- N = #count{ PhotoID : assigned_to(sports, PhotoID, fuentes) }.

gagnon_lifestyle_count(N) :- N = #count{ PhotoID : assigned_to(lifestyle, PhotoID, gagnon) }.
gagnon_metro_count(N) :- N = #count{ PhotoID : assigned_to(metro, PhotoID, gagnon) }.
gagnon_sports_count(N) :- N = #count{ PhotoID : assigned_to(sports, PhotoID, gagnon) }.

hue_lifestyle_count(N) :- N = #count{ PhotoID : assigned_to(lifestyle, PhotoID, hue) }.
hue_metro_count(N) :- N = #count{ PhotoID : assigned_to(metro, PhotoID, hue) }.
hue_sports_count(N) :- N = #count{ PhotoID : assigned_to(sports, PhotoID, hue) }.

% Total photos per photographer
fuentes_total(N) :- N = #sum{ 1,PhotoID,Section : assigned_to(Section, PhotoID, fuentes) }.
gagnon_total(N) :- N = #sum{ 1,PhotoID,Section : assigned_to(Section, PhotoID, gagnon) }.
hue_total(N) :- N = #sum{ 1,PhotoID,Section : assigned_to(Section, PhotoID, hue) }.

% Constraint 1: Each photographer must have at least 1 but no more than 3 photos
:- fuentes_total(N), N < 1.
:- fuentes_total(N), N > 3.
:- gagnon_total(N), N < 1.
:- gagnon_total(N), N > 3.
:- hue_total(N), N < 1.
:- hue_total(N), N > 3.

% Constraint 2: At least one Lifestyle photo must be by a photographer who has at least one Metro photo
:- photo(lifestyle, PhotoID), assigned_to(lifestyle, PhotoID, Photog),
   not (metro_photo_by(Photog)).
metro_photo_by(Photog) :- photo(metro, PhotoID), assigned_to(metro, PhotoID, Photog).

% Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
:- hue_lifestyle_count(HL), fuentes_sports_count(FS), HL != FS.

% Constraint 4: None of Gagnon's photographs can be in the Sports section
:- photo(sports, PhotoID), assigned_to(sports, PhotoID, gagnon).

% Define the distribution of Fuentes' photos for each option
% Option A: One in Lifestyle, one in Metro, one in Sports
fuentes_dist_a :- fuentes_lifestyle_count(1), fuentes_metro_count(1), fuentes_sports_count(1).

% Option B: One in Lifestyle, and two in Sports
fuentes_dist_b :- fuentes_lifestyle_count(1), fuentes_sports_count(2).

% Option C: Two in Lifestyle, and one in Sports
fuentes_dist_c :- fuentes_lifestyle_count(2), fuentes_sports_count(1).

% Option D: One in Metro, and two in Sports
fuentes_dist_d :- fuentes_metro_count(1), fuentes_sports_count(2).

% Option E: Two in Metro, and one in Sports
fuentes_dist_e :- fuentes_metro_count(2), fuentes_sports_count(1).

% Map the correct answer to option/1
option(a) :- fuentes_dist_a.
option(b) :- fuentes_dist_b.
option(c) :- fuentes_dist_c.
option(d) :- fuentes_dist_d.
option(e) :- fuentes_dist_e.

#show option/1.