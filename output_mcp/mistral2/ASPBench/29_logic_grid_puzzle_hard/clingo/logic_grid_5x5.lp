% Domains
person(evelyn). person(frank). person(grace). person(henry). person(iris).
location(library). location(park). location(cafe). location(museum). location(studio).
hobby(painting). hobby(coding). hobby(gardening). hobby(baking). hobby(sculpting).
snack(apple). snack(muffin). snack(nuts). snack(yogurt). snack(tea).
project(a). project(b). project(c). project(d). project(e).

% Compatibility scores
compatibility(painting, apple, 3).
compatibility(coding, muffin, 5).
compatibility(gardening, nuts, 2).
compatibility(baking, yogurt, 4).
compatibility(sculpting, tea, 1).

% Helper: hobby starts with 'S' or 'C'
hobby_starts_with_s_or_c(coding).
hobby_starts_with_s_or_c(sculpting).

% Helper: project distance
project_distance(a, c, 2).
project_distance(b, d, 2).
project_distance(c, e, 2).
project_distance(c, a, 2).
project_distance(d, b, 2).
project_distance(e, c, 2).

% Choice rule: assign attributes to each person
{
    assigns(P, L, H, S, Pr)
} :- person(P), location(L), hobby(H), snack(S), project(Pr).

% Uniqueness constraints
:- person(P1), person(P2), P1 != P2,
   assigns(P1, L, _, _, _), assigns(P2, L, _, _, _).
:- person(P1), person(P2), P1 != P2,
   assigns(P1, _, H, _, _), assigns(P2, _, H, _, _).
:- person(P1), person(P2), P1 != P2,
   assigns(P1, _, _, S, _), assigns(P2, _, _, S, _).
:- person(P1), person(P2), P1 != P2,
   assigns(P1, _, _, _, Pr), assigns(P2, _, _, _, Pr).

% Constraint 1: Coding before Gardening
:- assigns(P1, L1, coding, _, _), assigns(P2, L2, gardening, _, _),
   not (L1 @< L2).

% Constraint 2: Non-Painting hobby not Apple snack
:- assigns(P, _, H, apple, _), H != painting.

% Constraint 3: Exactly 2 hobbies start with 'S' or 'C'
:- 2 != #count { H : assigns(_, _, H, _, _), hobby_starts_with_s_or_c(H) }.

% Constraint 4: Henry works on Project D
:- not assigns(henry, _, _, _, d).

% Constraint 5: Museum not Nuts
:- assigns(P, museum, _, nuts, _).

% Constraint 6: Project E after A
:- assigns(P1, L1, _, _, a), assigns(P2, L2, _, _, e),
   not (L1 @< L2).

% Constraint 7: Baking after Park
:- assigns(P1, park, _, _, Pr1), assigns(P2, _, baking, _, Pr2),
   not (Pr1 @< Pr2).

% Constraint 8: Frank at Cafe
:- not assigns(frank, cafe, _, _, _).

% Constraint 9: Evelyn not Gardening
:- assigns(evelyn, _, gardening, _, _).

% Constraint 10: Alphabetical distance between Muffin and Sculpting projects is 2
:- assigns(P1, _, _, muffin, Pr1), assigns(P2, _, sculpting, _, Pr2),
   not project_distance(Pr1, Pr2, 2).

% Constraint 11: Sum of compatibility scores is exactly 15
score_sum(Sum) :- Sum = #sum { H, S, Score : assigns(_, _, H, S, _), compatibility(H, S, Score) }.
:- score_sum(Sum), Sum != 15.

% Show the assignments
#show assigns/5.