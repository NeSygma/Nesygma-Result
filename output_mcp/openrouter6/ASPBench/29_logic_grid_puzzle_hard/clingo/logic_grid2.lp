% Logic Grid Puzzle: Assignment of attributes for 5 people

% Domain facts
person("Evelyn"). person("Frank"). person("Grace"). person("Henry"). person("Iris").
location("Library"). location("Park"). location("Cafe"). location("Museum"). location("Studio").
hobby("Painting"). hobby("Coding"). hobby("Gardening"). hobby("Baking"). hobby("Sculpting").
snack("Apple"). snack("Muffin"). snack("Nuts"). snack("Yogurt"). snack("Tea").
project("A"). project("B"). project("C"). project("D"). project("E").

% Alphabetical ranking for locations (Cafe, Library, Museum, Park, Studio)
location_rank("Cafe", 1). location_rank("Library", 2). location_rank("Museum", 3).
location_rank("Park", 4). location_rank("Studio", 5).

% Alphabetical ranking for projects (A, B, C, D, E)
project_rank("A", 1). project_rank("B", 2). project_rank("C", 3).
project_rank("D", 4). project_rank("E", 5).

% Alphabetical before/after for locations
alphabetical_before(L1, L2) :- location_rank(L1, R1), location_rank(L2, R2), R1 < R2.
alphabetical_after(L1, L2) :- location_rank(L1, R1), location_rank(L2, R2), R1 > R2.

% Alphabetical distance for projects (absolute difference)
project_distance(Proj1, Proj2, D) :-
    project_rank(Proj1, R1), project_rank(Proj2, R2),
    D = R1 - R2, R1 >= R2.
project_distance(Proj1, Proj2, D) :-
    project_rank(Proj1, R1), project_rank(Proj2, R2),
    D = R2 - R1, R2 > R1.

% Compatibility scores for hobby-snack pairs
comp_score("Painting", "Apple", 3).
comp_score("Coding", "Muffin", 5).
comp_score("Gardening", "Nuts", 2).
comp_score("Baking", "Yogurt", 4).
comp_score("Sculpting", "Tea", 1).

% Assignment predicates (derived via choice rules)
{ has_location(P, L) } :- person(P), location(L).
{ has_hobby(P, H) } :- person(P), hobby(H).
{ has_snack(P, S) } :- person(P), snack(S).
{ has_project(P, Proj) } :- person(P), project(Proj).

% Each person has exactly one of each attribute
1 { has_location(P, L) : location(L) } 1 :- person(P).
1 { has_hobby(P, H) : hobby(H) } 1 :- person(P).
1 { has_snack(P, S) : snack(S) } 1 :- person(P).
1 { has_project(P, Proj) : project(Proj) } 1 :- person(P).

% Each location, hobby, snack, project assigned to exactly one person
1 { has_location(P, L) : person(P) } 1 :- location(L).
1 { has_hobby(P, H) : person(P) } 1 :- hobby(H).
1 { has_snack(P, S) : person(P) } 1 :- snack(S).
1 { has_project(P, Proj) : person(P) } 1 :- project(Proj).

% Constraint 1: Coding person location before Gardening person location
:- has_hobby(P1, "Coding"), has_hobby(P2, "Gardening"),
   has_location(P1, L1), has_location(P2, L2),
   not alphabetical_before(L1, L2).

% Constraint 2: If hobby not Painting, snack not Apple
:- has_hobby(P, H), H != "Painting", has_snack(P, "Apple").

% Constraint 3: Exactly 2 people have hobby starting with 'S' or 'C' (Coding or Sculpting)
% Helper predicate for hobbies starting with S or C
sc_hobby("Coding"). sc_hobby("Sculpting").
count_sc(N) :- N = #count{ P : has_hobby(P, H), sc_hobby(H) }.
:- count_sc(N), N != 2.

% Constraint 4: Henry works on Project D
:- has_project("Henry", Proj), Proj != "D".

% Constraint 5: Person in Museum does not eat Nuts
:- has_location(P, "Museum"), has_snack(P, "Nuts").

% Constraint 6: Person with project E is in location alphabetically after person with project A
:- has_project(P1, "E"), has_project(P2, "A"),
   has_location(P1, L1), has_location(P2, L2),
   not alphabetical_after(L1, L2).

% Constraint 7: Person who enjoys Baking has project alphabetically after project of person in Park
:- has_hobby(P1, "Baking"), has_location(P2, "Park"),
   has_project(P1, Proj1), has_project(P2, Proj2),
   not alphabetical_after(Proj1, Proj2).

% Constraint 8: Frank is at Cafe
:- has_location("Frank", L), L != "Cafe".

% Constraint 9: Evelyn does not enjoy Gardening
:- has_hobby("Evelyn", "Gardening").

% Constraint 10: Alphabetical distance between project of person eating Muffins and project of person enjoying Sculpting is exactly 2
:- has_snack(P1, "Muffin"), has_hobby(P2, "Sculpting"),
   has_project(P1, Proj1), has_project(P2, Proj2),
   project_distance(Proj1, Proj2, D), D != 2.

% Constraint 11: Sum of compatibility scores for all five hobby-snack assignments must be exactly 15
% Compute total score
total_score(T) :- T = #sum{ Score, P : has_hobby(P, H), has_snack(P, S), comp_score(H, S, Score) }.
:- total_score(T), T != 15.

% Show assignments
#show has_location/2.
#show has_hobby/2.
#show has_snack/2.
#show has_project/2.