% Domains
person(evelyn; frank; grace; henry; iris).
location(library; park; cafe; museum; studio).
hobby(painting; coding; gardening; baking; sculpting).
project(a; b; c; d; e).

% Assignments - each person has exactly one location, hobby, and project
1 { has_location(P, L) : location(L) } 1 :- person(P).
1 { has_hobby(P, H) : hobby(H) } 1 :- person(P).
1 { has_project(P, Pr) : project(Pr) } 1 :- person(P).

% Hobby determines snack (fixed pairs based on compatibility scores)
has_snack(P, apple)   :- has_hobby(P, painting).
has_snack(P, muffin)  :- has_hobby(P, coding).
has_snack(P, nuts)    :- has_hobby(P, gardening).
has_snack(P, yogurt)  :- has_hobby(P, baking).
has_snack(P, tea)     :- has_hobby(P, sculpting).

% Constraint 4: Henry works on Project D
:- has_project(henry, Pr), Pr != d.

% Constraint 8: Frank is at Cafe
:- has_location(frank, L), L != cafe.

% Constraint 9: Evelyn does not enjoy Gardening
:- has_hobby(evelyn, gardening).

% Helper predicate for hobbies starting with 'S' or 'C'
hobby_starts_with_sc(P) :- has_hobby(P, coding).
hobby_starts_with_sc(P) :- has_hobby(P, sculpting).

% Constraint 3: Exactly 2 people have hobbies starting with 'S' or 'C'
:- { hobby_starts_with_sc(P) : person(P) } != 2.

% Define alphabetical order for locations
location_order(library, 1).
location_order(park, 2).
location_order(cafe, 3).
location_order(museum, 4).
location_order(studio, 5).

% Constraint 1: Coding hobby location < Gardening hobby location
% Find the person with coding and the person with gardening
:- has_hobby(P, coding), has_hobby(Q, gardening),
   has_location(P, L1), has_location(Q, L2),
   location_order(L1, X), location_order(L2, Y),
   X >= Y.

% Constraint 5: Museum location person does not eat Nuts
% Nuts is paired with gardening, so museum person cannot have gardening hobby
:- has_location(P, museum), has_hobby(P, gardening).

% Define alphabetical order for projects
project_order(a, 1).
project_order(b, 2).
project_order(c, 3).
project_order(d, 4).
project_order(e, 5).

% Constraint 6: Project E location > Project A location
:- has_project(P, e), has_project(Q, a),
   has_location(P, L1), has_location(Q, L2),
   location_order(L1, X), location_order(L2, Y),
   X =< Y.

% Constraint 7: Baking hobby project > Park location project
:- has_hobby(P, baking), has_location(Q, park),
   has_project(P, Pr1), has_project(Q, Pr2),
   project_order(Pr1, X), project_order(Pr2, Y),
   X =< Y.

% Constraint 10: Distance between Muffin project and Sculpting project is exactly 2
% Muffin is paired with coding, so distance between coding person's project and sculpting person's project
:- has_hobby(P, coding), has_hobby(Q, sculpting),
   has_project(P, Pr1), has_project(Q, Pr2),
   project_order(Pr1, X), project_order(Pr2, Y),
   abs(X - Y) != 2.

% Constraint 2: For any person whose hobby is not Painting, their snack must not be Apple
:- person(P), not has_hobby(P, painting), has_snack(P, apple).

% Constraint 11: Sum of compatibility scores must be exactly 15
% Compatibility scores: (Painting, Apple): 3, (Coding, Muffin): 5, (Gardening, Nuts): 2, (Baking, Yogurt): 4, (Sculpting, Tea): 1
% Since each snack is uniquely determined by hobby, we can compute the sum directly
:- #sum { S,P : has_hobby(P, painting), has_snack(P, apple), S=3;
                   has_hobby(P, coding), has_snack(P, muffin), S=5;
                   has_hobby(P, gardening), has_snack(P, nuts), S=2;
                   has_hobby(P, baking), has_snack(P, yogurt), S=4;
                   has_hobby(P, sculpting), has_snack(P, tea), S=1 } != 15.

% Show the assignments
#show has_location/2.
#show has_hobby/2.
#show has_project/2.
#show has_snack/2.