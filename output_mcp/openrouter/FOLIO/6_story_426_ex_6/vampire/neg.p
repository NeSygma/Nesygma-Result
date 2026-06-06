% Negative version (negated conjecture)
fof(premise1, axiom, ! [X] : (schedule_meeting(X) => go_to_building_today(X))).
fof(premise2, axiom, ! [X] : (lunch_in_building(X) => schedule_meeting(X))).
fof(premise3, axiom, ! [X] : (lunch_in_building(X) | lunch_at_home(X))).
fof(premise4, axiom, ! [X] : (lunch_at_home(X) => work_remotely_home(X))).
fof(premise5, axiom, ! [X] : (in_other_countries(X) => work_remotely_home(X))).
fof(premise6, axiom, ! [X] : (manager(X) => ~work_remotely_home(X))).
fof(premise7a, axiom, appear_company_today(james) => manager(james)).
fof(premise7b, axiom, manager(james) => appear_company_today(james)).

fof(neg_conclusion, conjecture,
    ~(
        ( (manager(james) | in_other_countries(james)) => ~ (lunch_at_home(james) | work_remotely_home(james)) )
        &
        ( (lunch_at_home(james) | work_remotely_home(james)) => ( ~manager(james) & ~in_other_countries(james) ) )
    )
).