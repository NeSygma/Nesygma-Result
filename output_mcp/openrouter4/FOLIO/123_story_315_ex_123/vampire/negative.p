fof(premise_1, axiom, ! [X] : (can_transport_multiple_passengers(X) => ~one_seater(X))).
fof(premise_2, axiom, ! [X] : (tesla_model_3(X) => can_transport_multiple_passengers(X))).
fof(premise_3, axiom, ! [X] : (single_seat_electric_car(X) => one_seater(X))).
fof(premise_4, axiom, ! [X] : (solo_ev(X) => single_seat_electric_car(X))).
fof(premise_5, axiom, (~tesla_model_3(johns_car) => ~(tesla_model_3(johns_car) | single_seat_electric_car(johns_car)))).
fof(negated_conclusion, conjecture, ~solo_ev(johns_car)).