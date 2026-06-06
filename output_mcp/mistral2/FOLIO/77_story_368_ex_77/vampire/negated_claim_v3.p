fof(at_school_def, axiom, at_school(hannah, marys_school)).

fof(works_in_student_jobs_def, axiom, works_in_student_jobs(hannah)).

fof(premise1, axiom,
    ! [X] :
      ( (works_in_student_jobs(X) & at_school(X, marys_school))
      => needs_to_earn_money(X) )).

fof(premise2, axiom,
    ! [X] :
      ( (orders_takeout_frequently(X) & at_school(X, marys_school))
      => works_in_student_jobs(X) )).

fof(premise3, axiom,
    ! [X] :
      ( at_school(X, marys_school)
      => (orders_takeout_frequently(X) | enjoys_dining_hall_meals(X)) )).

fof(premise4, axiom,
    ! [X] :
      ( (enjoys_dining_hall_meals(X) & at_school(X, marys_school))
      => ~is_picky_eater(X) )).

fof(premise5, axiom,
    ! [X] :
      ( (enjoys_dining_hall_meals(X) & at_school(X, marys_school))
      => spends_time_eating_with_friends(X) )).

fof(premise7a, axiom, works_in_student_jobs(hannah)).

fof(premise7b, axiom,
    (needs_to_earn_money(hannah) & at_school(hannah, marys_school) & works_in_student_jobs(hannah))
    => (~is_picky_eater(hannah) & ~needs_to_earn_money(hannah))).

fof(goal_negation, conjecture,
    ~(at_school(hannah, marys_school)
      & ~is_picky_eater(hannah)
      & spends_time_eating_with_friends(hannah))).