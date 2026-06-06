tff(johns_car_type, type, johns_car: $i).

fof(can_transport_multiple_def, axiom, ! [X] : (can_transport_multiple(X) => ~one_seater(X))).
fof(tesla_model_3_implies_transport, axiom, ! [X] : (tesla_model_3(X) => can_transport_multiple(X))).
fof(single_seat_electric_car_implies_one_seater, axiom, ! [X] : (single_seat_electric_car(X) => one_seater(X))).
fof(solo_ev_implies_single_seat_electric_car, axiom, ! [X] : (solo_ev(X) => single_seat_electric_car(X))).
fof(not_tesla_model_3_implies_not_single_seat, axiom, ! [X] : (~tesla_model_3(X) => ~single_seat_electric_car(X))).

fof(conclusion, conjecture, ~solo_ev(johns_car)).