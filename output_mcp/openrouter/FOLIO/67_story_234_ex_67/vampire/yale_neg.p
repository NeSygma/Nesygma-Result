% Negative run: negation of the claim (there exists an institution with larger endowment)
fof(priv_yale, axiom, private(yale)).
fof(ivy_yale, axiom, ivy_league(yale)).
fof(research_yale, axiom, research_university(yale)).
fof(endowment_yale, axiom, endowment(yale, e423)).
fof(col1, axiom, residential_college(benjamin_franklin_college)).
fof(col2, axiom, residential_college(berkeley_college)).
fof(col3, axiom, residential_college(branford_college)).
fof(col4, axiom, residential_college(davenport_college)).
fof(col5, axiom, residential_college(ezra_stiles_college)).
fof(col6, axiom, residential_college(grace_hopper_college)).
fof(col7, axiom, residential_college(jonathan_edwards_college)).
fof(col8, axiom, residential_college(morse_college)).
fof(col9, axiom, residential_college(pauli_murray_college)).
fof(col10, axiom, residential_college(pierson_college)).
fof(col11, axiom, residential_college(saybrook_college)).
fof(col12, axiom, residential_college(silliman_college)).
fof(col13, axiom, residential_college(timothy_dwight_college)).
fof(col14, axiom, residential_college(trumbull_college)).
fof(edu_yale, axiom, educational_institution(yale)).
% Negated claim: there exists an educational institution with larger endowment than Yale
fof(goal, conjecture, ? [X] : (educational_institution(X) & larger_than(X, yale))).