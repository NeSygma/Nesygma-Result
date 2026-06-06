% Positive version: original conclusion as conjecture
% Premise 1: If something can transport multiple passengers, then they are not one-seaters.
fof(premise1, axiom, ! [X] : (can_transport_multiple(X) => ~one_seater(X))).

% Premise 2: All Tesla Model 3 can transport multiple passengers.
fof(premise2, axiom, ! [X] : (tesla_model3(X) => can_transport_multiple(X))).

% Premise 3: All single-seat electric cars are one-seaters.
fof(premise3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).

% Premise 4: All Solo EV cars are single-seat electric cars.
fof(premise4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).

% Premise 5: If John's car is not a Tesla Model 3, then John's car is not a Tesla Model 3 or a single-seat electric car.
% Let jc = johns_car
fof(premise5, axiom, (~tesla_model3(johns_car) => (~tesla_model3(johns_car) | ~single_seat_electric(johns_car)))).

% Conclusion: John's car is a Solo EV.
fof(conclusion, conjecture, solo_ev(johns_car)).