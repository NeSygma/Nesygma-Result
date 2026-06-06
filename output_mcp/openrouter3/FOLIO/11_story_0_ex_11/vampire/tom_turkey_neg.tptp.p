% Negative file: Negated conclusion as conjecture
fof(distinct_types, axiom, (eastern != osceola & eastern != goulds & eastern != merriams & eastern != rio_grande & eastern != ocellated &
osceola != goulds & osceola != merriams & osceola != rio_grande & osceola != ocellated &
goulds != merriams & goulds != rio_grande & goulds != ocellated &
merriams != rio_grande & merriams != ocellated &
rio_grande != ocellated)).

fof(premise_1, axiom, wild_turkey(tom)).
fof(premise_2, axiom, ~type(tom, eastern)).
fof(premise_3, axiom, ~type(tom, osceola)).
fof(premise_4, axiom, ~type(tom, goulds)).
fof(premise_5, axiom, ~type(tom, merriams)).
fof(premise_6, axiom, ~type(tom, rio_grande)).

fof(conclusion_negated, conjecture, ~type(tom, eastern)).