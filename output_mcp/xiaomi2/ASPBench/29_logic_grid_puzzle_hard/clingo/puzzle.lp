% Domains
person(evelyn). person(frank). person(grace). person(henry). person(iris).
location(library). location(park). location(cafe). location(museum). location(studio).
hobby(painting). hobby(coding). hobby(gardening). hobby(baking). hobby(sculpting).
snack(apple). snack(muffin). snack(nuts). snack(yogurt). snack(tea).
project(a). project(b). project(c). project(d). project(e).

% Alphabetical ordering for locations: Cafe < Library < Museum < Park < Studio
loc_order(cafe, 1). loc_order(library, 2). loc_order(museum, 3). loc_order(park, 4). loc_order(studio, 5).

% Alphabetical ordering for projects: A < B < C < D < E
proj_order(a, 1). proj_order(b, 2). proj_order(c, 3). proj_order(d, 4). proj_order(e, 5).

% Compatibility scores
compat(painting, apple, 3).
compat(coding, muffin, 5).
compat(gardening, nuts, 2).
compat(baking, yogurt, 4).
compat(sculpting, tea, 1).

% Each person has exactly one of each attribute
1 { has_location(P, L) : location(L) } 1 :- person(P).
1 { has_hobby(P, H) : hobby(H) } 1 :- person(P).
1 { has_snack(P, S) : snack(S) } 1 :- person(P).
1 { has_project(P, Pr) : project(Pr) } 1 :- person(P).

% Each attribute value is assigned to exactly one person
1 { has_location(P, L) : person(P) } 1 :- location(L).
1 { has_hobby(P, H) : person(P) } 1 :- hobby(H).
1 { has_snack(P, S) : person(P) } 1 :- snack(S).
1 { has_project(P, Pr) : person(P) } 1 :- project(Pr).

% Constraint 1: Coding person's location alphabetically before Gardening person's location
:- has_hobby(P1, coding), has_hobby(P2, gardening),
   has_location(P1, L1), has_location(P2, L2),
   loc_order(L1, N1), loc_order(L2, N2),
   N1 >= N2.

% Constraint 2: If hobby != Painting, snack != Apple
:- has_hobby(P, H), H != painting, has_snack(P, apple).

% Constraint 3: Exactly 2 people with hobby starting with 'S' or 'C' (Sculpting, Coding)
hobby_sc(P) :- has_hobby(P, sculpting).
hobby_sc(P) :- has_hobby(P, coding).
:- #count { P : hobby_sc(P) } != 2.

% Constraint 4: Henry has Project D
has_project(henry, d).

% Constraint 5: Museum person doesn't eat Nuts
:- has_location(P, museum), has_snack(P, nuts).

% Constraint 6: Project E person's location alphabetically after Project A person's location
:- has_project(P1, e), has_project(P2, a),
   has_location(P1, L1), has_location(P2, L2),
   loc_order(L1, N1), loc_order(L2, N2),
   N1 <= N2.

% Constraint 7: Baking person's project alphabetically after Park person's project
:- has_hobby(P1, baking), has_location(P2, park),
   has_project(P1, Pr1), has_project(P2, Pr2),
   proj_order(Pr1, N1), proj_order(Pr2, N2),
   N1 <= N2.

% Constraint 8: Frank is at Cafe
has_location(frank, cafe).

% Constraint 9: Evelyn doesn't enjoy Gardening
:- has_hobby(evelyn, gardening).

% Constraint 10: Alphabetical distance between Muffin-eater's project and Sculpting-enjoyer's project is exactly 2
:- has_snack(P1, muffin), has_hobby(P2, sculpting),
   has_project(P1, Pr1), has_project(P2, Pr2),
   proj_order(Pr1, N1), proj_order(Pr2, N2),
   N1 - N2 != 2, N1 - N2 != -2.

% Constraint 11: Sum of compatibility scores = 15
total_score(S) :- S = #sum { Score,P : has_hobby(P,H), has_snack(P,Sn), compat(H,Sn,Score) }.
:- total_score(S), S != 15.

#show has_location/2.
#show has_hobby/2.
#show has_snack/2.
#show has_project/2.