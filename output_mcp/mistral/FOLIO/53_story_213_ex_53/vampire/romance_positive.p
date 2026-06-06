fof(romance_are_indo_european, axiom, 
    ! [L] : (romance(L) => indo_european(L))).

fof(romance_is_family, axiom, 
    family(romance_family)).

fof(member_of_iff_romance, axiom, 
    ! [L] : (member_of(L, romance_family) <=> romance(L))).

fof(family_members_related, axiom, 
    ! [L1, L2] : 
        ( (member_of(L1, romance_family) & member_of(L2, romance_family) & L1 != L2)
        => related(L1, L2) )).

fof(french_is_romance, axiom, 
    romance(french)).

fof(spanish_is_romance, axiom, 
    romance(spanish)).

fof(german_related_to_spanish, axiom, 
    related(german, spanish)).

fof(basque_unrelated, axiom, 
    ! [L] : (L != basque => (~related(basque, L) & ~related(L, basque)))).

fof(distinct_languages, axiom, 
    french != spanish & 
    french != german & 
    french != basque & 
    spanish != german & 
    spanish != basque & 
    german != basque).

fof(goal, conjecture, 
    romance(german)).