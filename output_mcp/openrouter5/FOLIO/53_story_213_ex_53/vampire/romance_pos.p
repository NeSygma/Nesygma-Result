% Positive version: original claim as conjecture
% Premises:
% 1. All Romance languages are Indo-European languages.
fof(premise1, axiom, ! [L] : (romance_language(L) => indo_european_language(L))).

% 2. Romance languages are a language family.
fof(premise2, axiom, language_family(romance)).

% 3. All languages within a language family are related to each other.
fof(premise3, axiom, ! [F, L1, L2] : ((language_family(F) & in_family(L1, F) & in_family(L2, F)) => related(L1, L2))).

% 4. French and Spanish are both Romance languages.
fof(premise4a, axiom, romance_language(french)).
fof(premise4b, axiom, romance_language(spanish)).

% 5. German is related to Spanish.
fof(premise5, axiom, related(german, spanish)).

% 6. Basque is not related to any other language.
fof(premise6, axiom, ! [L] : (L != basque => ~related(basque, L))).
fof(premise6b, axiom, ! [L] : (L != basque => ~related(L, basque))).

% Distinctness
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).

% Conclusion: German is a Romance language.
fof(conclusion, conjecture, romance_language(german)).