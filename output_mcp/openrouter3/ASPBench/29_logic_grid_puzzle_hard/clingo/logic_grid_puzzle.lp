% Logic Grid Puzzle - Complete Assignment

% ===== DOMAINS =====
person(evelyn). person(frank). person(grace). person(henry). person(iris).
location(library). location(park). location(cafe). location(museum). location(studio).
hobby(painting). hobby(coding). hobby(gardening). hobby(baking). hobby(sculpting).
snack(apple). snack(muffin). snack(nuts). snack(yogurt). snack(tea).
project(a). project(b). project(c). project(d). project(e).

% ===== ASSIGNMENT PREDICATES =====
% Each person has exactly one of each attribute
1 { has_location(P, L) : location(L) } 1 :- person(P).
1 { has_hobby(P, H) : hobby(H) } 1 :- person(P).
1 { has_snack(P, S) : snack(S) } 1 :- person(P).
1 { has_project(P, Pr) : project(Pr) } 1 :- person(P).

% ===== COMPATIBILITY SCORES =====
score(painting, apple, 3).
score(coding, muffin, 5).
score(gardening, nuts, 2).
score(baking, yogurt, 4).
score(sculpting, tea, 1).

% Helper: get compatibility score for a person
person_score(P, Score) :- 
    has_hobby(P, H), 
    has_snack(P, S), 
    score(H, S, Score).

% ===== CONSTRAINTS =====

% Constraint 1: Coding person is in location alphabetically before Gardening person
% We need to compare locations alphabetically
location_order(library, 1). location_order(park, 2). location_order(cafe, 3). 
location_order(museum, 4). location_order(studio, 5).

:- has_hobby(P1, coding), has_hobby(P2, gardening),
   has_location(P1, L1), has_location(P2, L2),
   location_order(L1, O1), location_order(L2, O2),
   O1 >= O2.

% Constraint 2: If hobby is not Painting, snack must not be Apple
:- has_hobby(P, H), H != painting, has_snack(P, apple).

% Constraint 3: Exactly 2 people with hobby starting with 'S' or 'C'
% Hobbies starting with S: Sculpting
% Hobbies starting with C: Coding, Cooking (but we have Coding, Baking, etc.)
% Actually: Sculpting (S), Coding (C), and Baking (B), Gardening (G), Painting (P)
% So only Sculpting and Coding start with S or C
count_sc_or_c(N) :- N = #count{P : has_hobby(P, sculpting); P : has_hobby(P, coding)}.
:- count_sc_or_c(N), N != 2.

% Constraint 4: Henry works on Project D
has_project(henry, d).

% Constraint 5: Person in Museum does not eat Nuts
:- has_location(P, museum), has_snack(P, nuts).

% Constraint 6: Project E is alphabetically after Project A
% Projects: A=1, B=2, C=3, D=4, E=5
project_order(a, 1). project_order(b, 2). project_order(c, 3). 
project_order(d, 4). project_order(e, 5).

:- has_project(P1, a), has_project(P2, e),
   has_location(P1, L1), has_location(P2, L2),
   location_order(L1, O1), location_order(L2, O2),
   O1 >= O2.

% Constraint 7: Baking person has project after Park person's project
:- has_hobby(P1, baking), has_location(P2, park),
   has_project(P1, Pr1), has_project(P2, Pr2),
   project_order(Pr1, O1), project_order(Pr2, O2),
   O1 <= O2.

% Constraint 8: Frank is at Cafe
has_location(frank, cafe).

% Constraint 9: Evelyn does not enjoy Gardening
:- has_hobby(evelyn, gardening).

% Constraint 10: Alphabetical distance between Muffin eater's project and Sculpting person's project is exactly 2
:- has_snack(P1, muffin), has_hobby(P2, sculpting),
   has_project(P1, Pr1), has_project(P2, Pr2),
   project_order(Pr1, O1), project_order(Pr2, O2),
   |O1 - O2| != 2.

% Constraint 11: Sum of compatibility scores is exactly 15
total_score(S) :- S = #sum{Score, P : person_score(P, Score)}.
:- total_score(S), S != 15.

% ===== SHOW DIRECTIVES =====
#show has_location/2.
#show has_hobby/2.
#show has_snack/2.
#show has_project/2.
#show person_score/2.
#show total_score/1.