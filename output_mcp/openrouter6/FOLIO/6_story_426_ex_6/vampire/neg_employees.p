fof(premise1, axiom, ! [X] : (employee(X) & schedule_meeting(X) => go_to_company_today(X))).
fof(premise2, axiom, ! [X] : (has_lunch_in_company(X) => schedule_meeting(X))).
fof(premise3, axiom, ! [X] : (employee(X) => (has_lunch_in_company(X) | has_lunch_at_home(X)))).
fof(premise4, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => work_remotely(X))).
fof(premise5, axiom, ! [X] : (employee(X) & in_other_countries(X) => work_remotely(X))).
fof(premise6, axiom, ! [X] : (manager(X) => ~work_remotely(X))).
fof(premise7, axiom, appear_in_company_today(james) <=> manager(james)).
fof(neg_conclusion, conjecture, (manager(james) | in_other_countries(james)) & (has_lunch_at_home(james) | work_remotely(james))).