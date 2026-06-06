fof(heinrich_german_politician, axiom,
    ( german(heinrich_schmidt) & politician(heinrich_schmidt) )).

fof(heinrich_prussian_member, axiom,
    member_of(heinrich_schmidt, prussian_state_parliament)).

fof(heinreich_reichstag_member, axiom,
    member_of(heinrich_schmidt, nazi_reichstag)).

fof(goal, conjecture,
    ~( german(heinrich_schmidt) | russian(heinrich_schmidt) )).