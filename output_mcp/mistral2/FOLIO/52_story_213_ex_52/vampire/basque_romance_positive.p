fof(romance_implies_indo_european, axiom,
    ! [L] : (romance(L) => indo_european(L))).

fof(romance_is_family, axiom,
    language_family(romance_family)).

fof(family_members_related, axiom,
    ! [L1, L2] :
        ( (is_family_of(L1, romance_family) & is_family_of(L2, romance_family))
        => related(L1, L2) )).

fof(french_is_romance, axiom,
    romance(french)).

fof(spanish_is_romance, axiom,
    romance(spanish)).

fof(german_related_to_spanish, axiom,
    related(german, spanish)).

fof(basque_not_related_to_any, axiom,
    ! [L] : (L != basque => (~related(basque, L) & ~related(L, basque)))).

fof(define_is_family_of, axiom,
    ! [L] : (is_family_of(L, romance_family) <=> romance(L))).

fof(conclusion, conjecture,
    romance(basque)).