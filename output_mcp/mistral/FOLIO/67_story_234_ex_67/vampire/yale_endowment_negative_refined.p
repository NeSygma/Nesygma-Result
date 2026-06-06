tff(entity_type, type, entity: $tType).
tff(university_type, type, university: entity > $o).
tff(private_ivy_league_research_university_type, type, private_ivy_league_research_university: entity > $o).
tff(moved_to_type, type, moved_to: (entity * entity * entity) > $o).
tff(endowment_type, type, endowment: entity > $real).
tff(residential_college_type, type, residential_college: (entity * entity) > $o).
tff(yale, entity).
tff(new_haven, entity).
tff(year_1716, entity).
tff(benjamin_franklin, entity).
tff(berkeley, entity).
tff(branford, entity).
tff(davenport, entity).
tff(ezra_stiles, entity).
tff(grace_hopper, entity).
tff(jonathan_edwards, entity).
tff(morse, entity).
tff(pauli_murray, entity).
tff(pierson, entity).
tff(saybrook, entity).
tff(silliman, entity).
tff(timothy_dwight, entity).
tff(trumbull, entity).

tff(yale_is_university, axiom, university(yale)).
tff(yale_is_private_ivy_league, axiom, private_ivy_league_research_university(yale)).
tff(yale_moved_to_new_haven, axiom, moved_to(yale, new_haven, year_1716)).
tff(yale_endowment_value, axiom, endowment(yale) = 42.3).
tff(residential_colleges_list, axiom, 
    (residential_college(yale, benjamin_franklin) & 
     residential_college(yale, berkeley) & 
     residential_college(yale, branford) & 
     residential_college(yale, davenport) & 
     residential_college(yale, ezra_stiles) & 
     residential_college(yale, grace_hopper) & 
     residential_college(yale, jonathan_edwards) & 
     residential_college(yale, morse) & 
     residential_college(yale, pauli_murray) & 
     residential_college(yale, pierson) & 
     residential_college(yale, saybrook) & 
     residential_college(yale, silliman) & 
     residential_college(yale, timothy_dwight) & 
     residential_college(yale, trumbull))).

tff(distinct_entities_1, axiom, yale != new_haven).
tff(distinct_entities_2, axiom, yale != year_1716).
tff(distinct_entities_3, axiom, new_haven != year_1716).
tff(distinct_entities_4, axiom, benjamin_franklin != berkeley).
tff(distinct_entities_5, axiom, benjamin_franklin != branford).
tff(distinct_entities_6, axiom, benjamin_franklin != davenport).
tff(distinct_entities_7, axiom, benjamin_franklin != ezra_stiles).
tff(distinct_entities_8, axiom, benjamin_franklin != grace_hopper).
tff(distinct_entities_9, axiom, benjamin_franklin != jonathan_edwards).
tff(distinct_entities_10, axiom, benjamin_franklin != morse).
tff(distinct_entities_11, axiom, benjamin_franklin != pauli_murray).
tff(distinct_entities_12, axiom, benjamin_franklin != pierson).
tff(distinct_entities_13, axiom, benjamin_franklin != saybrook).
tff(distinct_entities_14, axiom, benjamin_franklin != silliman).
tff(distinct_entities_15, axiom, benjamin_franklin != timothy_dwight).
tff(distinct_entities_16, axiom, benjamin_franklin != trumbull).

tff(largest_endowment_def, axiom, 
    ! [X: entity] : (largest_endowment(X) <=> 
        ! [Y: entity] : (endowment(Y) = endowment(X)))).

tff(conclusion_negation, conjecture, ~largest_endowment(yale)).