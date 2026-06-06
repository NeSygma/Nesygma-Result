fof(premise1, axiom,
    ! [X] : (schedules_meeting_with_customers(X) => in_company_building(X))).

fof(premise2, axiom,
    ! [X] : (has_lunch_in_company(X) => schedules_meeting_with_customers(X))).

fof(premise3, axiom,
    ! [X] : (has_lunch_in_company(X) | has_lunch_at_home(X))).

fof(premise4, axiom,
    ! [X] : (has_lunch_at_home(X) => works_remotely_from_home(X))).

fof(premise5, axiom,
    ! [X] : (in_other_countries(X) => works_remotely_from_home(X))).

fof(premise6, axiom,
    ! [X] : (manager(X) => ~works_remotely_from_home(X))).

fof(premise7, axiom,
    appears_in_company_today(james) <=> manager(james)).

fof(goal, conjecture,
    has_lunch_in_company(james)).