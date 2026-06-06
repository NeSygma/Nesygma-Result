fof(from_istanbul_implies_34, axiom, 
    ! [P] : (from_istanbul(P) => begins_with(P, num_34))).

fof(not_34_implies_not_istanbul, axiom, 
    ! [P] : (~begins_with(P, num_34) => ~from_istanbul(P))).

fof(joe_plate_from_istanbul, axiom, 
    from_istanbul(joe_plate)).

fof(tom_plate_begins_with_35, axiom, 
    begins_with(tom_plate, num_35)).

fof(plate_35_not_34, axiom, 
    ! [P] : (begins_with(P, num_35) => ~begins_with(P, num_34))).

fof(conclusion, conjecture, 
    from_istanbul(tom_plate)).