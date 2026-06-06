fof(breeding_back_is_artificial_selection, axiom, 
    ! [X, Y] : (breeding_back(X, Y) => form_of_artificial_selection(X))).

fof(heck_cattle_breeding_back, axiom, 
    breeding_back(heck_cattle, aurochs)).

fof(heck_cattle_is_animal, axiom, 
    animal(heck_cattle)).

fof(aurochs_is_animal, axiom, 
    animal(aurochs)).

fof(form_of_artificial_selection_implies_artificially_selected, axiom, 
    ! [X] : (form_of_artificial_selection(X) => artificially_selected(X))).

fof(goal_negation, conjecture, 
    ~? [X] : (X = heck_cattle & artificially_selected(X))).