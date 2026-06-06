fof(employee_schedules_meetings_implies_goes_to_company, axiom,
    ! [X] : (schedules_meetings_with_customers(X) => goes_to_company_today(X))).

fof(has_lunch_in_company_implies_schedules_meetings, axiom,
    ! [X] : (has_lunch_in_company_building(X) => schedules_meetings_with_customers(X))).

fof(lunch_location_disjoint, axiom,
    ! [X] : (~(has_lunch_in_company_building(X) & has_lunch_at_home(X)))).

fof(lunch_location_total, axiom,
    ! [X] : (has_lunch_in_company_building(X) | has_lunch_at_home(X))).

fof(has_lunch_at_home_implies_works_remotely, axiom,
    ! [X] : (has_lunch_at_home(X) => works_remotely_from_home(X))).

fof(in_other_countries_implies_works_remotely, axiom,
    ! [X] : (in_other_countries(X) => works_remotely_from_home(X))).

fof(manager_implies_not_works_remotely, axiom,
    ! [X] : (manager(X) => ~works_remotely_from_home(X))).

fof(james_goes_to_company_iff_manager, axiom,
    goes_to_company_today(james) <=> manager(james)).

fof(distinct_constants, axiom,
    (james != manager & james != in_other_countries & james != has_lunch_at_home & james != works_remotely_from_home)).

fof(conclusion, conjecture,
    ((manager(james) | in_other_countries(james)) <=>
     ~(has_lunch_at_home(james) | works_remotely_from_home(james)))).