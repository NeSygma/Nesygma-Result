fof(rule1, axiom, ! [X] : (transport_multiple(X) => ~one_seater(X))).
fof(rule2, axiom, ! [X] : (tesla_model3(X) => transport_multiple(X))).
fof(rule3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).
fof(rule4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(rule5, axiom, (~tesla_model3(john) => ~single_seat_electric(john))).
fof(goal, conjecture, tesla_model3(john)).