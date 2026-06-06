fof(romance_are_indo_european, axiom,
    ! [L] : (is_romance(L) => is_indo_european(L))).

fof(romance_is_family, axiom,
    is_family(romance)).

fof(family_members_related, axiom,
    ! [L1, L2, F] :
        ((belongs_to_family(L1, F) & belongs_to_family(L2, F)) => is_related_to(L1, L2))).

fof(french_spanish_romance, axiom,
    is_romance(french) & is_romance(spanish)).

fof(german_related_to_spanish, axiom,
    is_related_to(german, spanish)).

fof(basque_unrelated, axiom,
    ! [L] : (L != basque => (~is_related_to(basque, L) & ~is_related_to(L, basque)))).

fof(french_indo_european_conjecture, conjecture,
    is_indo_european(french)).