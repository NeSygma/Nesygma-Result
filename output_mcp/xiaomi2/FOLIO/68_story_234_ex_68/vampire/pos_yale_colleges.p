fof(yale_private, axiom, private_ivy_league_research_university(yale)).
fof(yale_moved, axiom, moved_to_new_haven_in_1716(yale)).
fof(yale_endowment, axiom, endowment_valued_at_42_3_billion(yale)).

% Residential colleges at Yale (from premise 4)
fof(res_benjamin_franklin, axiom, residential_college_at(benjamin_franklin_college, yale)).
fof(res_berkeley, axiom, residential_college_at(berkeley_college, yale)).
fof(res_branford, axiom, residential_college_at(branford_college, yale)).
fof(res_davenport, axiom, residential_college_at(davenport_college, yale)).
fof(res_ezra_stiles, axiom, residential_college_at(ezra_stiles_college, yale)).
fof(res_grace_hopper, axiom, residential_college_at(grace_hopper_college, yale)).
fof(res_jonathan_edwards, axiom, residential_college_at(jonathan_edwards_college, yale)).
fof(res_morse, axiom, residential_college_at(morse_college, yale)).
fof(res_pauli_murray, axiom, residential_college_at(pauli_murray_college, yale)).
fof(res_pierson, axiom, residential_college_at(pierson_college, yale)).
fof(res_saybrook, axiom, residential_college_at(saybrook_college, yale)).
fof(res_silliman, axiom, residential_college_at(silliman_college, yale)).
fof(res_timothy_dwight, axiom, residential_college_at(timothy_dwight_college, yale)).
fof(res_trumbull, axiom, residential_college_at(trumbull_college, yale)).

% Conclusion: Pierson College is a residential college at Yale
fof(goal, conjecture, residential_college_at(pierson_college, yale)).