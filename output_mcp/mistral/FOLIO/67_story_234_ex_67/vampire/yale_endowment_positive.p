fof(yale_is_university, axiom, university(yale)).
fof(yale_is_private_ivy_league, axiom, private_ivy_league_research_university(yale)).
fof(yale_moved_to_new_haven, axiom, moved_to(yale, new_haven, 1716)).
fof(yale_endowment_value, axiom, endowment(yale, 42.3)).
fof(residential_colleges_list, axiom, 
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
fof(conclusion, conjecture, largest_endowment(yale)).