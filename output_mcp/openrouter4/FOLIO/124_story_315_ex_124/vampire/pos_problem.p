fof(premise_1, axiom, ! [X] : (multiple_passenger(X) => ~one_seater(X))).
fof(premise_2, axiom, ! [X] : (tesla_model_3(X) => multiple_passenger(X))).
fof(premise_3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).
fof(premise_4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(premise_5, axiom, (~tesla_model_3(johns_car) => (~tesla_model_3(johns_car) & ~single_seat_electric(johns_car)))).
fof(distinct, axiom, true).
fof(goal, conjecture, ~solo_ev(johns_car)).