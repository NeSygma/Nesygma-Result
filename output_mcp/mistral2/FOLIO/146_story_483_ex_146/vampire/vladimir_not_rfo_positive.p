fof(election_2024_usa_decl, axiom, election_2024_usa = election_2024_usa).
fof(united_states_decl, axiom, united_states = united_states).
fof(taiwan_decl, axiom, taiwan = taiwan).
fof(russian_federation_decl, axiom, russian_federation = russian_federation).
fof(gazprom_decl, axiom, gazprom = gazprom).

fof(premise1, axiom,
    ! [P] : (can_register_to_vote(P, united_states) =>
             can_participate_in_election(P, election_2024_usa))).

fof(premise2, axiom,
    ! [P] : (has_citizenship(P, united_states) =>
             can_register_to_vote(P, united_states))).

fof(premise3, axiom,
    ! [P] : (has_citizenship(P, united_states) |
             has_citizenship(P, taiwan))).

fof(premise4, axiom,
    ! [P] : (russian_federation_official(P) =>
             ~has_citizenship(P, taiwan))).

fof(premise5, axiom,
    ~has_citizenship(vladimir, taiwan) &
    ~manager_at(vladimir, gazprom)).

fof(premise6, axiom,
    can_register_to_vote(ekaterina, united_states) |
    russian_federation_official(ekaterina)).

fof(conclusion, conjecture,
    ~russian_federation_official(vladimir)).