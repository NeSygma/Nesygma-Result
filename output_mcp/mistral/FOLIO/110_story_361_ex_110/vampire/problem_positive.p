fof(spill_implies_not_tidy, axiom, 
    ! [X] : (spill_food(X) => ~notably_tidy(X))).

fof(clumsy_foodies_spill, axiom, 
    ! [X] : ((clumsy_foodies(X) & goes_out_frequently(X)) => spill_food(X))).

fof(cleanly_implies_tidy, axiom, 
    ! [X] : (cleanly(X) => notably_tidy(X))).

fof(values_order_implies_cleanly, axiom, 
    ! [X] : (values_order(X) => cleanly(X))).

fof(family_prioritizes_order_implies_values_order, axiom, 
    ! [X] : (family_prioritizes_order(X) => values_order(X))).

fof(peter_choice, axiom, 
    (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter))).

fof(conclusion, conjecture, 
    ((clumsy_foodies(peter) & goes_out_frequently(peter) & family_prioritizes_order(peter)) |
     (~clumsy_foodies(peter) & ~goes_out_frequently(peter) & ~family_prioritizes_order(peter)))).