fof(spill_implies_not_tidy, axiom, 
    ! [X] : (spill_lots(X) => ~notably_tidy(X))).

fof(clumsy_foodies_implies_spill, axiom, 
    ! [X] : ((clumsy_foodies(X) & go_out_frequently(X)) => spill_lots(X))).

fof(cleanly_implies_tidy, axiom, 
    ! [X] : (cleanly(X) => notably_tidy(X))).

fof(values_order_implies_cleanly, axiom, 
    ! [X] : (values_order_spotlessness(X) => cleanly(X))).

fof(family_prioritizes_implies_values, axiom, 
    ! [X] : (family_prioritizes_order_spotlessness(X) => values_order_spotlessness(X))).

fof(peter_condition, axiom, 
    (spill_lots(peter) & cleanly(peter)) | (~spill_lots(peter) & ~cleanly(peter))).

fof(goal, conjecture, 
    notably_tidy(peter)).