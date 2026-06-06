% Positive version: original claim as conjecture
% Premises:
% 1. All Romance languages are Indo-European languages.
fof(romance_indo_european, axiom, ! [L] : (romance_language(L) => indo_european_language(L))).

% 2. Romance languages are a language family.
fof(romance_family, axiom, language_family(romance)).

% 3. All languages within a language family are related to each other.
fof(family_related, axiom, ! [F, L1, L2] : ((language_family(F) & member_of_family(L1, F) & member_of_family(L2, F)) => related(L1, L2))).

% 4. French and Spanish are both Romance languages.
fof(french_romance, axiom, romance_language(french)).
fof(spanish_romance, axiom, romance_language(spanish)).

% 5. German is related to Spanish.
fof(german_related_spanish, axiom, related(german, spanish)).

% 6. Basque is not related to any other language.
fof(basque_not_related, axiom, ! [L] : ~related(basque, L)).

% Distinctness
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).

% Additional: Romance languages are members of the Romance family
fof(romance_members, axiom, ! [L] : (romance_language(L) => member_of_family(L, romance))).

% Conclusion: Basque is a Romance language.
fof(goal, conjecture, romance_language(basque)).