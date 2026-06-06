fof(schedule_to_company, axiom, ! [E] : (schedule_meeting(E) => go_to_company_today(E))).
fof(lunch_to_schedule, axiom, ! [E] : (lunch_in_company(E) => schedule_meeting(E))).
fof(lunch_disjunction, axiom, ! [E] : (lunch_in_company(E) | lunch_at_home(E))).
fof(lunch_at_home_remote, axiom, ! [E] : (lunch_at_home(E) => remote_home(E))).
fof(in_other_country_remote, axiom, ! [E] : (in_other_country(E) => remote_home(E))).
fof(manager_not_remote, axiom, ! [E] : (manager(E) => ~remote_home(E))).
fof(james_bicond, axiom, (appears_in_company_today(james) <=> manager(james))).
fof(conjecture, conjecture, lunch_in_company(james)).