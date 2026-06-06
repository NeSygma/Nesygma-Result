fof(can_transport_multiple_passengers_implies_not_one_seater, axiom,
    ! [X] : (can_transport_multiple_passengers(X) => ~one_seater(X))).

fof(tesla_model_3_implies_can_transport_multiple_passengers, axiom,
    ! [X] : (is_tesla_model_3(X) => can_transport_multiple_passengers(X))).

fof(single_seat_electric_car_implies_one_seater, axiom,
    ! [X] : (is_single_seat_electric_car(X) => one_seater(X))).

fof(solo_ev_implies_single_seat_electric_car, axiom,
    ! [X] : (is_solo_ev(X) => is_single_seat_electric_car(X))).

fof(not_tesla_model_3_implies_not_single_seat_electric_car, axiom,
    ~is_tesla_model_3(johns_car) => ~is_single_seat_electric_car(johns_car)).

fof(goal, conjecture,
    is_solo_ev(johns_car)).