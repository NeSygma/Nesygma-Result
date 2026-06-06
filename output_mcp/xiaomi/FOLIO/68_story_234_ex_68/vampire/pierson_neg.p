fof(yale_university, axiom, university(yale)).
fof(yale_private, axiom, private(yale)).
fof(yale_ivy_league, axiom, ivy_league(yale)).
fof(yale_research, axiom, research_university(yale)).
fof(yale_moved_new_haven_1716, axiom, moved_to(yale, new_haven, year_1716)).

% List of residential colleges at Yale
fof(benjamin_franklin_college, axiom, residential_college_at(benjamin_franklin_college, yale)).
fof(berkeley_college, axiom, residential_college_at(berkeley_college, yale)).
fof(branford_college, axiom, residential_college_at(branford_college, yale)).
fof(davenport_college, axiom, residential_college_at(davenport_college, yale)).
fof(ezra_stiles_college, axiom, residential_college_at(ezra_stiles_college, yale)).
fof(grace_hopper_college, axiom, residential_college_at(grace_hopper_college, yale)).
fof(jonathan_edwards_college, axiom, residential_college_at(jonathan_edwards_college, yale)).
fof(morse_college, axiom, residential_college_at(morse_college, yale)).
fof(pauli_murray_college, axiom, residential_college_at(pauli_murray_college, yale)).
fof(pierson_college, axiom, residential_college_at(pierson_college, yale)).
fof(saybrook_college, axiom, residential_college_at(saybrook_college, yale)).
fof(silliman_college, axiom, residential_college_at(silliman_college, yale)).
fof(timothy_dwight_college, axiom, residential_college_at(timothy_dwight_college, yale)).
fof(trumbull_college, axiom, residential_college_at(trumbull_college, yale)).

% Negated conclusion: Pierson College is NOT a residential college at Yale
fof(goal, conjecture, ~residential_college_at(pierson_college, yale)).