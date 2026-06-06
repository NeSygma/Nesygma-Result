fof(can_register_implies_can_participate, axiom, 
    ! [X] : (can_register_vote_us(X) => can_participate_election_2024(X))).

fof(us_citizen_implies_can_register, axiom, 
    ! [X] : (us_citizen(X) => can_register_vote_us(X))).

fof(us_or_taiwanese_citizen, axiom, 
    ! [X] : (us_citizen(X) | taiwanese_citizen(X))).

fof(russian_official_implies_not_taiwanese, axiom, 
    ! [X] : (russian_official(X) => ~taiwanese_citizen(X))).

fof(vladimir_citizenship_and_role, axiom, 
    (~taiwanese_citizen(vladimir) & ~manager_gazprom(vladimir))).

fof(ekaterina_can_register_or_official, axiom, 
    (can_register_vote_us(ekaterina) | russian_official(ekaterina))).

fof(conclusion, conjecture, 
    (can_participate_election_2024(ekaterina) | manager_gazprom(ekaterina))).