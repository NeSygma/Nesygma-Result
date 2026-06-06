% Negative version: negated claim as conjecture
% Using fof
fof(yale_university, axiom, private_ivy_league_research_university(yale)).
fof(moved_to_new_haven, axiom, moved_to(yale, new_haven, year_1716)).
fof(endowment_value, axiom, endowment_valued_at(yale, billion_42_3)).

% Residential colleges at Yale
fof(college_benjamin_franklin, axiom, residential_college_at_yale(benjamin_franklin_college)).
fof(college_berkeley, axiom, residential_college_at_yale(berkeley_college)).
fof(college_branford, axiom, residential_college_at_yale(branford_college)).
fof(college_davenport, axiom, residential_college_at_yale(davenport_college)).
fof(college_ezra_stiles, axiom, residential_college_at_yale(ezra_stiles_college)).
fof(college_grace_hopper, axiom, residential_college_at_yale(grace_hopper_college)).
fof(college_jonathan_edwards, axiom, residential_college_at_yale(jonathan_edwards_college)).
fof(college_morse, axiom, residential_college_at_yale(morse_college)).
fof(college_pauli_murray, axiom, residential_college_at_yale(pauli_murray_college)).
fof(college_pierson, axiom, residential_college_at_yale(pierson_college)).
fof(college_saybrook, axiom, residential_college_at_yale(saybrook_college)).
fof(college_silliman, axiom, residential_college_at_yale(silliman_college)).
fof(college_timothy_dwight, axiom, residential_college_at_yale(timothy_dwight_college)).
fof(college_trumbull, axiom, residential_college_at_yale(trumbull_college)).

% Negated conclusion: Pierson College is NOT a residential college at Yale
fof(goal_negated, conjecture, ~residential_college_at_yale(pierson_college)).