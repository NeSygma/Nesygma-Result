% Positive version: original claim as conjecture
fof(premise_1, axiom, german_politician(heinrich_schmidt)).
fof(premise_2, axiom, member_of(heinrich_schmidt, prussian_state_parliament)).
fof(premise_3, axiom, member_of(heinrich_schmidt, nazi_reichstag)).

fof(goal, conjecture, ? [X] :
    (german_politician(X)
    & member_of(X, prussian_state_parliament)
    & member_of(X, nazi_reichstag))).