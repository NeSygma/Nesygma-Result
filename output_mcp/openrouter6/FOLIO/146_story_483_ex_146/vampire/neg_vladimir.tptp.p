fof(can_register_implies_participate, axiom, 
    ! [X] : (can_register_to_vote(X) => can_participate_election(X))).

fof(us_citizenship_implies_register, axiom,
    ! [X] : (has_us_citizenship(X) => can_register_to_vote(X))).

fof(citizenship_disjunction, axiom,
    ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).

fof(russian_officials_no_taiwanese, axiom,
    ! [X] : (is_russian_federation_official(X) => ~has_taiwanese_citizenship(X))).

fof(vladimir_facts, axiom,
    (~has_taiwanese_citizenship(vladimir) & ~is_manager_at_gazprom(vladimir))).

fof(ekaterina_fact, axiom,
    (can_register_to_vote(ekaterina) | is_russian_federation_official(ekaterina))).

fof(distinct_individuals, axiom,
    (vladimir != ekaterina)).

fof(goal, conjecture, is_russian_federation_official(vladimir)).