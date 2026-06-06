fof(financial_aid_def, axiom,
    ! [A] : (provides_financial_aid(ets, A) <=>
             (applying_for_gre(A) & proves_economic_hardship(A)))).
fof(economic_hardship_def, axiom,
    ! [A] : (proves_economic_hardship(A) <=>
             (lives_single_parent_family(A) | few_resources(A)))).
fof(tom_single_parent, axiom, lives_single_parent_family(tom)).
fof(tom_few_resources, axiom, few_resources(tom)).
fof(tom_applying, axiom, applying_for_gre(tom)).
fof(conclusion, conjecture, provides_financial_aid(ets, tom)).