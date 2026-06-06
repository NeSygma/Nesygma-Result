% --- Domains ---
person(evelyn; frank; grace; henry; iris).
location(cafe; library; museum; park; studio).
hobby(baking; coding; gardening; painting; sculpting).
snack(apple; muffin; nuts; tea; yogurt).
project(a; b; c; d; e).

% --- Orderings ---
loc_order(cafe, 1).
loc_order(library, 2).
loc_order(museum, 3).
loc_order(park, 4).
loc_order(studio, 5).

proj_order(a, 1).
proj_order(b, 2).
proj_order(c, 3).
proj_order(d, 4).
proj_order(e, 5).

% --- Assignment ---
{ has_loc(P, L) } = 1 :- person(P), location(L).
{ has_hobby(P, H) } = 1 :- person(P), hobby(H).
{ has_snack(P, S) } = 1 :- person(P), snack(S).
{ has_project(P, Pr) } = 1 :- person(P), project(Pr).

% --- Uniqueness ---
:- has_loc(P1, L), has_loc(P2, L), P1 != P2.
:- has_hobby(P1, H), has_hobby(P2, H), P1 != P2.
:- has_snack(P1, S), has_snack(P2, S), P1 != P2.
:- has_project(P1, Pr), has_project(P2, Pr), P1 != P2.

% --- Compatibility Scores ---
score(painting, apple, 3).
score(coding, muffin, 5).
score(gardening, nuts, 2).
score(baking, yogurt, 4).
score(sculpting, tea, 1).

% --- Constraints ---
% 1. Coding location < Gardening location (alphabetical)
:- has_hobby(P1, coding), has_loc(P1, L1), has_hobby(P2, gardening), has_loc(P2, L2), 
   loc_order(L1, V1), loc_order(L2, V2), V1 >= V2.

% 2. Not Painting -> Not Apple
:- has_hobby(P, H), has_snack(P, apple), H != painting.

% 3. Hobby starts with 'S' or 'C' is exactly 2
starts_sc(coding). starts_sc(sculpting).
:- #count{ P : has_hobby(P, H), starts_sc(H) } != 2.

% 4. Henry works on Project D
has_project(henry, d).

% 5. Museum person does not eat Nuts
:- has_loc(P, museum), has_snack(P, nuts).

% 6. Project E location > Project A location (alphabetical)
:- has_project(P1, e), has_loc(P1, L1), has_project(P2, a), has_loc(P2, L2), 
   loc_order(L1, V1), loc_order(L2, V2), V1 <= V2.

% 7. Baking project > Park project (alphabetical)
:- has_hobby(P1, baking), has_project(P1, Pr1), has_loc(P2, park), has_project(P2, Pr2), 
   proj_order(Pr1, V1), proj_order(Pr2, V2), V1 <= V2.

% 8. Frank is at the Cafe
has_loc(frank, cafe).

% 9. Evelyn does not enjoy Gardening
:- has_hobby(evelyn, gardening).

% 10. Alphabetical distance between Muffin-eater's project and Sculpting-hobbyist's project is 2
:- has_snack(P1, muffin), has_project(P1, Pr1), has_hobby(P2, sculpting), has_project(P2, Pr2), 
   proj_order(Pr1, V1), proj_order(Pr2, V2), V1 - V2 != 2, V2 - V1 != 2.

% 11. Sum of compatibility scores = 15
% Need to define score for all pairs. If not in list, score is 0.
get_score(P, S) :- has_hobby(P, H), has_snack(P, S), score(H, S, S).
get_score(P, 0) :- has_hobby(P, H), has_snack(P, S), not score(H, S, _).
:- 15 != #sum { S,P : get_score(P, S) }.

% --- Output ---
#show has_loc/2.
#show has_hobby/2.
#show has_snack/2.
#show has_project/2.