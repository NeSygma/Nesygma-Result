fof(single_parent_or_few_resources_implies_hardship, axiom, 
    ! [X] : ((single_parent_family(X) | few_resources(X)) => economic_hardship(X))).

fof(economic_hardship_and_gre_applicant_implies_aid, axiom, 
    ! [X] : ((economic_hardship(X) & gre_applicant(X)) => financial_aid(X))).

fof(tom_is_single_parent, axiom, single_parent_family(tom)).

fof(tom_has_few_resources, axiom, few_resources(tom)).

fof(tom_is_gre_applicant, axiom, gre_applicant(tom)).

fof(tom_receives_financial_aid, conjecture, financial_aid(tom)).