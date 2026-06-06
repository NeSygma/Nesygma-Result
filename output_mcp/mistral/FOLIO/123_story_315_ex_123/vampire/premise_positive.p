fof(can_transport_multiple_implies_not_one_seater, axiom, 
    ! [X] : (can_transport_multiple(X) => ~one_seater(X))).

fof(all_tesla_model_3_can_transport_multiple, axiom, 
    ! [X] : (tesla_model_3(X) => can_transport_multiple(X))).

fof(all_single_seat_electric_are_one_seaters, axiom, 
    ! [X] : (single_seat_electric_car(X) => one_seater(X))).

fof(all_solo_ev_are_single_seat_electric, axiom, 
    ! [X] : (solo_ev(X) => single_seat_electric_car(X))).

fof(johns_car_constraint, axiom, 
    tesla_model_3(johns_car) | ~single_seat_electric_car(johns_car)).

fof(goal, conjecture, solo_ev(johns_car)).