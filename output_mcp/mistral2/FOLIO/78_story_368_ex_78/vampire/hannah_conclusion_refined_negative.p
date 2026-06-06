fof(at_school_hannah, axiom, at_school(hannah, marys_school)).
fof(works_in_student_jobs_hannah, axiom, works_in_student_jobs(hannah)).
fof(premise1, axiom, ! [Person] : (works_in_student_jobs(Person) => needs_to_earn_money(Person))).
fof(premise2, axiom, ! [Person] : (orders_takeout_frequently(Person) => works_in_student_jobs(Person))).
fof(premise3, axiom, ! [Person] : (orders_takeout_frequently(Person) | enjoys_dining_hall_meals(Person))).
fof(premise4, axiom, ! [Person] : (enjoys_dining_hall_meals(Person) => ~is_picky_eater(Person))).
fof(premise5, axiom, ! [Person] : (enjoys_dining_hall_meals(Person) => spends_time_in_dining_halls(Person))).

fof(conclusion_negation, conjecture,
    ~(at_school(hannah, marys_school) &
      (~is_picky_eater(hannah) |
       (is_picky_eater(hannah) => spends_time_in_dining_halls(hannah))) )).