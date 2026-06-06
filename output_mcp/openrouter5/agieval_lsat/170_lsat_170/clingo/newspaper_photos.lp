%% Problem: Newspaper photographs
%% Sections: Lifestyle, Metro, Sports
%% Photographers: Fuentes, Gagnon, Hue
%% Total 6 photos, exactly 2 per section.

%% --- Domains ---
section(lifestyle). section(metro). section(sports).
photographer(fuentes). photographer(gagnon). photographer(hue).

%% Each photo is assigned to a section and a photographer.
%% We have exactly 6 photos, but we can model it as:
%% For each section, exactly 2 photos. Each photo has a photographer.
%% We'll use an abstraction: for each section S and photographer P,
%% count(S,P) = number of photos by P in section S.
%% Total photos per section = 2, total per photographer between 1 and 3.

%% count(S,P) is a number from 0 to 2 (since each section has exactly 2 photos)
%% We'll use choice rules to assign counts.

%% Domain for counts: each section-photographer pair gets a count 0..2
{ count(S, P, N) : N = 0..2 } = 1 :- section(S), photographer(P).

%% Exactly 2 photos per section
:- section(S), #sum{ N, P : count(S, P, N) } != 2.

%% For each photographer, at least 1 but no more than 3 photos total
:- photographer(P), #sum{ N, S : count(S, P, N) } < 1.
:- photographer(P), #sum{ N, S : count(S, P, N) } > 3.

%% At least one photograph in Lifestyle by a photographer who has at least one photograph in Metro.
%% i.e., exists P such that count(lifestyle, P, N1), N1 >= 1, and count(metro, P, N2), N2 >= 1.
:- not exists_shared_photographer.
exists_shared_photographer :- photographer(P), count(lifestyle, P, N1), N1 >= 1, count(metro, P, N2), N2 >= 1.

%% Number of Hue's photos in Lifestyle = number of Fuentes' photos in Sports.
:- count(lifestyle, hue, N1), count(sports, fuentes, N2), N1 != N2.

%% None of Gagnon's photos can be in Sports.
:- count(sports, gagnon, N), N > 0.

%% --- Given condition for the specific question ---
%% One photo in Lifestyle is by Gagnon and one is by Hue.
%% So count(lifestyle, gagnon, 1) and count(lifestyle, hue, 1).
%% Since total in Lifestyle is 2, that means count(lifestyle, fuentes, 0).
:- not count(lifestyle, gagnon, 1).
:- not count(lifestyle, hue, 1).

%% --- Now evaluate each option ---

%% (A) Exactly one photograph in Metro is by Fuentes.
option(a) :- count(metro, fuentes, 1).

%% (B) Exactly one photograph in Metro is by Gagnon.
option(b) :- count(metro, gagnon, 1).

%% (C) Both photographs in Metro are by Gagnon.
option(c) :- count(metro, gagnon, 2).

%% (D) Exactly one photograph in Sports is by Hue.
option(d) :- count(sports, hue, 1).

%% (E) Both photographs in Sports are by Hue.
option(e) :- count(sports, hue, 2).

%% We need to find which option MUST be true (i.e., holds in ALL valid models).
%% So we need to check which option holds in every answer set.
%% We can do this by checking if there exists a model where the option is false.
%% If an option is false in some model, it's not "must be true".
%% We'll use a trick: for each option, check if it's forced.
%% Actually, we can just enumerate all models and see which option is in all of them.
%% But simpler: we can add constraints to test each option.

%% Let's just run and see all models, then deduce.

#show count/3.
#show option/1.