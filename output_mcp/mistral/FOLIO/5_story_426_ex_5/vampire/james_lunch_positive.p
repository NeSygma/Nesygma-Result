tff(employee_type, type, employee: $tType).
tff(james_type, type, james: employee).

tff(schedules_meeting_with_customers_type, type, schedules_meeting_with_customers: (employee > $o)).
tff(has_lunch_in_company_type, type, has_lunch_in_company: (employee > $o)).
tff(has_lunch_at_home_type, type, has_lunch_at_home: (employee > $o)).
tff(works_remotely_from_home_type, type, works_remotely_from_home: (employee > $o)).
tff(in_other_countries_type, type, in_other_countries: (employee > $o)).
tff(is_manager_type, type, is_manager: (employee > $o)).
tff(at_company_today_type, type, at_company_today: (employee > $o)).

fof(premise1, axiom, 
    ! [E: employee] :
      (schedules_meeting_with_customers(E) => at_company_today(E))).

fof(premise2, axiom, 
    ! [E: employee] :
      (has_lunch_in_company(E) => schedules_meeting_with_customers(E))).

fof(premise3a, axiom, 
    ! [E: employee] :
      (has_lunch_in_company(E) | has_lunch_at_home(E))).

fof(premise3b, axiom, 
    ! [E: employee] :
      (~has_lunch_in_company(E) | ~has_lunch_at_home(E))).

fof(premise4, axiom, 
    ! [E: employee] :
      (has_lunch_at_home(E) => works_remotely_from_home(E))).

fof(premise5, axiom, 
    ! [E: employee] :
      (in_other_countries(E) => works_remotely_from_home(E))).

fof(premise6, axiom, 
    ! [E: employee] :
      (is_manager(E) => ~works_remotely_from_home(E))).

fof(premise7, axiom, 
    (at_company_today(james) <=> is_manager(james))).

fof(conclusion, conjecture, 
    ~has_lunch_in_company(james)).