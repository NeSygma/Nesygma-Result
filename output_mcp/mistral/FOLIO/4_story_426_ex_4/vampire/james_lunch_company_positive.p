fof(premise_1, axiom, ! [E] : (schedules_meeting_with_customer(E) => goes_to_company_building(E))).
fof(premise_2, axiom, ! [E] : (has_lunch_in_company(E) => schedules_meeting_with_customer(E))).
fof(premise_3a, axiom, ! [E] : (has_lunch_in_company(E) | has_lunch_at_home(E))).
fof(premise_3b, axiom, ! [E] : ~(has_lunch_in_company(E) & has_lunch_at_home(E))).
fof(premise_4, axiom, ! [E] : (has_lunch_at_home(E) => works_remotely_from_home(E))).
fof(premise_5, axiom, ! [E] : (is_in_other_country(E) => works_remotely_from_home(E))).
fof(premise_6, axiom, ! [E] : (is_manager(E) => ~works_remotely_from_home(E))).
fof(premise_7, axiom, (appears_in_company(james) <=> is_manager(james))).
fof(conclusion, conjecture, has_lunch_in_company(james)).