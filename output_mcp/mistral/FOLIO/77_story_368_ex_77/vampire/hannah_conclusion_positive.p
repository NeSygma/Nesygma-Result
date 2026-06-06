tff(person_type, type, person: $tType).
tff(school_type, type, school: $tType).

tff(is_at_school_type, type, is_at_school: (person * school) > $o).
tff(works_in_student_jobs_type, type, works_in_student_jobs: person > $o).
tff(needs_to_earn_money_type, type, needs_to_earn_money: person > $o).
tff(orders_takeout_frequently_type, type, orders_takeout_frequently: person > $o).
tff(enjoys_dining_hall_type, type, enjoys_dining_hall: person > $o).
tff(is_picky_eater_type, type, is_picky_eater: person > $o).
tff(spends_time_eating_with_friends_type, type, spends_time_eating_with_friends: person > $o).

tff(marys_school, type, marys_school: school).
tff(hannah, type, hannah: person).

tff(premise1, axiom, 
    ! [X: person] : 
      ((works_in_student_jobs(X) & is_at_school(X, marys_school)) 
       => needs_to_earn_money(X))).

tff(premise2, axiom, 
    ! [X: person] : 
      ((orders_takeout_frequently(X) & is_at_school(X, marys_school)) 
       => works_in_student_jobs(X))).

tff(premise3, axiom, 
    ! [X: person] : 
      (is_at_school(X, marys_school) 
       => (orders_takeout_frequently(X) | enjoys_dining_hall(X)))).

tff(premise4, axiom, 
    ! [X: person] : 
      ((enjoys_dining_hall(X) & is_at_school(X, marys_school)) 
       => ~is_picky_eater(X))).

tff(premise5, axiom, 
    ! [X: person] : 
      ((enjoys_dining_hall(X) & is_at_school(X, marys_school)) 
       => spends_time_eating_with_friends(X))).

tff(premise6, axiom, 
    is_at_school(hannah, marys_school)).

tff(premise7a, axiom, 
    works_in_student_jobs(hannah)).

tff(premise7b, axiom, 
    (needs_to_earn_money(hannah) 
     => (~is_picky_eater(hannah) & ~needs_to_earn_money(hannah)))).

tff(conclusion, conjecture, 
    (is_at_school(hannah, marys_school) & 
     ~is_picky_eater(hannah) & 
     spends_time_eating_with_friends(hannah))).