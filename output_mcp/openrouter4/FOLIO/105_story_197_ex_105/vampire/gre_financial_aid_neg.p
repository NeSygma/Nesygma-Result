% Negative version: Claim that ETS does NOT provide financial aid to Tom
fof(axiom_2, axiom,
    ! [X] : ((gre_applicant(X) & proves_economic_hardship(X)) => ets_provides_financial_aid(X))).
fof(axiom_3, axiom,
    ! [X] : ((lives_in_single_parent_family(X) | has_few_resources(X)) => can_prove_economic_hardship(X))).
fof(fact_4, axiom, lives_in_single_parent_family(tom)).
fof(fact_5, axiom, has_few_resources(tom)).
fof(fact_6, axiom, gre_applicant(tom)).
fof(goal, conjecture, ~ets_provides_financial_aid(tom)).