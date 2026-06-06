fof(romance_family_def, axiom, language_family(romance_family)).
fof(romance_is_family, axiom, ! [L] : (romance_language(L) <=> is_family_of(L, romance_family))).
fof(romance_are_indoeuropean, axiom, ! [L] : (romance_language(L) => indo_european_language(L))).
fof(family_members_related, axiom, ! [L1, L2, F] : ((is_family_of(L1, F) & is_family_of(L2, F) & L1 != L2) => related_to(L1, L2))).
fof(french_romance, axiom, romance_language(french)).
fof(spanish_romance, axiom, romance_language(spanish)).
fof(german_related_to_spanish, axiom, related_to(german, spanish)).
fof(basque_unrelated, axiom, ! [L] : (L != basque => (~related_to(basque, L) & ~related_to(L, basque)))).
fof(distinct_languages, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(conclusion_negation, conjecture, ~romance_language(basque)).