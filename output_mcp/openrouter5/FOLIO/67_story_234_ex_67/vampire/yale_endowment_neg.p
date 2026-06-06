% Negative version: negated claim as conjecture
% Premises
fof(yale_is_private, axiom, private_university(yale)).
fof(yale_is_ivy_league, axiom, ivy_league(yale)).
fof(yale_is_research, axiom, research_university(yale)).
fof(yale_moved_1716, axiom, moved_to_new_haven(yale)).
fof(yale_endowment_val, axiom, endowment_valued_at(yale, forty_two_point_three_billion)).
fof(residential_colleges, axiom,
    (has_college(yale, benjamin_franklin) &
     has_college(yale, berkeley) &
     has_college(yale, branford) &
     has_college(yale, davenport) &
     has_college(yale, ezra_stiles) &
     has_college(yale, grace_hopper) &
     has_college(yale, jonathan_edwards) &
     has_college(yale, morse) &
     has_college(yale, pauli_murray) &
     has_college(yale, pierson) &
     has_college(yale, saybrook) &
     has_college(yale, silliman) &
     has_college(yale, timothy_dwight) &
     has_college(yale, trumbull))).

% Negated conclusion: There exists some educational institution X with a greater endowment than Yale
fof(goal_neg, conjecture, ? [X] :
    (educational_institution(X) & greater_endowment_than(X, yale))).