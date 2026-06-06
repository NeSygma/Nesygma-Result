fof(premise1, axiom, ! [X] : ((at_mary_school(X) & works_in_student_jobs_on_campus(X)) => needs_to_earn_money(X))).
fof(premise2, axiom, ! [X] : ((at_mary_school(X) & orders_takeout_frequently_in_college(X)) => works_in_student_jobs_on_campus(X))).
fof(premise3, axiom, ! [X] : (at_mary_school(X) => (orders_takeout_frequently_in_college(X) | enjoys_dining_hall_meals_and_recipes(X)))).
fof(premise4, axiom, ! [X] : ((at_mary_school(X) & enjoys_dining_hall_meals_and_recipes(X)) => ~is_picky_eater(X))).
fof(premise5, axiom, ! [X] : ((at_mary_school(X) & enjoys_dining_hall_meals_and_recipes(X)) => spends_a_lot_of_time_eating_and_catching_up_with_friends_in_campus_dining_halls(X))).
fof(premise6, axiom, at_mary_school(hannah)).
fof(premise7a, axiom, works_in_student_jobs_on_campus(hannah)).
fof(premise7b, axiom, needs_to_earn_money(hannah) => (~is_picky_eater(hannah) & ~needs_to_earn_money(hannah))).
fof(conjecture, conjecture, (at_mary_school(hannah) & (~is_picky_eater(hannah) | (is_picky_eater(hannah) => spends_a_lot_of_time_eating_and_catching_up_with_friends_in_campus_dining_halls(hannah))))).