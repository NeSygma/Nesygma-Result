% Problem: Tom's license plate from Istanbul (negated)
% Premises and negated conclusion

% Distinct plates
fof(distinct_plates, axiom, (joe_plate != tom_plate)).

% Distinct numbers
fof(distinct_numbers, axiom, (num_34 != num_35)).

% Premise 1: All plates from Istanbul begin with 34
fof(premise_1, axiom, ! [X] : (from_istanbul(X) => begins_with(X, num_34))).

% Premise 2: Plates not beginning with 34 are not from Istanbul
fof(premise_2, axiom, ! [X] : (~begins_with(X, num_34) => ~from_istanbul(X))).

% Premise 3: Joe's plate is from Istanbul
fof(premise_3, axiom, from_istanbul(joe_plate)).

% Premise 4: Tom's plate begins with 35
fof(premise_4, axiom, begins_with(tom_plate, num_35)).

% Premise 5: If a plate begins with 35, it doesn't begin with 34
fof(premise_5, axiom, ! [X] : (begins_with(X, num_35) => ~begins_with(X, num_34))).

% Negated conclusion: Tom's plate is NOT from Istanbul
fof(negated_conclusion, conjecture, ~from_istanbul(tom_plate)).