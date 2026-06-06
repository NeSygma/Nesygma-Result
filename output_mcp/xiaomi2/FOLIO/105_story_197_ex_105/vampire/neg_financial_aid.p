fof(premise_1, axiom,
    ! [X] : (
        (gre_applicant(X) & proves_economic_hardship(X))
        => provides_financial_aid(ets, X)
    )).

fof(premise_2, axiom,
    ! [X] : (
        (single_parent_family(X) | few_resources(X))
        => proves_economic_hardship(X)
    )).

fof(premise_3, axiom, single_parent_family(tom)).

fof(premise_4, axiom, few_resources(tom)).

fof(premise_5, axiom, gre_applicant(tom)).

fof(goal, conjecture, ~provides_financial_aid(ets, tom)).