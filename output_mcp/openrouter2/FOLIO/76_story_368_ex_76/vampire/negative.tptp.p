fof(prem1, axiom, ! [X] : ((at_mary_school(X) & works_in_student_jobs_on_campus(X)) => needs_to_earn_money(X))).
fof(prem2, axiom, ! [X] : ((at_mary_school(X) & orders_takeout_frequently_in_college(X)) => works_in_student_jobs_on_campus(X))).
fof(prem3, axiom, ! [X] : (at_mary_school(X) => (orders_takeout_frequently_in_college(X) | enjoys_dining_hall_meals_and_recipes(X)))).
fof(prem4, axiom, ! [X] : ((at_mary_school(X) & enjoys_dining_hall_meals_and_recipes(X)) => ~is_picky_eater(X))).
fof(prem5, axiom, ! [X] : ((at_mary_school(X) & enjoys_dining_hall_meals_and_recipes(X)) => spends_a_lot_of_time_eating_and_catching_up_with_friends_in_campus_dining_halls(X))).
fof(prem6, axiom, at_mary_school(h)).
fof(prem7, axiom, works_in_student_jobs_on_campus(h)).
fof(prem8, axiom, (needs_to_earn_money(h) => (~is_picky_eater(h) & ~needs_to_earn_money(h)))).
fof(goal, conjecture, ~needs_to_earn_money(h)).