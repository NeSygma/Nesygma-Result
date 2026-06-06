fof(premise1, axiom, ! [X] : (spill_lots(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : ((clumsy_foodies(X) & goes_out_frequently(X)) => spill_lots(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (values_order_spotlessness(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes_order_spotlessness(X) => values_order_spotlessness(X))).
fof(peter_condition, axiom, (spill_lots(peter) & cleanly(peter)) | (~spill_lots(peter) & ~cleanly(peter))).
fof(conclusion_negation, conjecture, ~((clumsy_foodies(peter) & goes_out_frequently(peter)) | family_prioritizes_order_spotlessness(peter))).