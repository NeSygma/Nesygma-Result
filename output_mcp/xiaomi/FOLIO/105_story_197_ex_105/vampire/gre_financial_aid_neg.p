% Premise: ETS provides financial aid to GRE applicants who prove economic hardship
fof(ets_policy, axiom, ! [Person] : 
    ((applicant(Person, gre_test) & proves_economic_hardship(Person)) 
     => provides_financial_aid(ets, Person))).

% Premise: Those living in single-parent families can prove economic hardship
fof(single_parent_rule, axiom, ! [Person] : 
    (single_parent_family(Person) => proves_economic_hardship(Person))).

% Premise: Those having few resources can prove economic hardship
fof(few_resources_rule, axiom, ! [Person] : 
    (few_resources(Person) => proves_economic_hardship(Person))).

% Premise: Tom lives in a single-parent family
fof(tom_single_parent, axiom, single_parent_family(tom)).

% Premise: Tom has few resources available
fof(tom_few_resources, axiom, few_resources(tom)).

% Premise: Tom is applying to take the GRE test
fof(tom_applicant, axiom, applicant(tom, gre_test)).

% Negated conclusion: ETS does NOT provide financial aid to Tom
fof(goal, conjecture, ~provides_financial_aid(ets, tom)).