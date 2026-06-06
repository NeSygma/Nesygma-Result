% Football loan problem - Negative version (negated claim)
tff(person_sort, type, person: $tType).
tff(club_sort, type, club: $tType).

tff(ailton_silva_decl, type, ailton_silva: person).
tff(ailton_decl, type, ailton: person).
tff(braga_decl, type, braga: club).
tff(nautico_decl, type, nautico: club).
tff(fluminense_decl, type, fluminense: club).

tff(commonly_known_as_decl, type, commonly_known_as: (person * person) > $o).
tff(loaned_to_decl, type, loaned_to: (person * club) > $o).
tff(plays_for_decl, type, plays_for: (person * club) > $o).

tff(distinct_persons, axiom, (ailton_silva != ailton)).
tff(distinct_clubs, axiom, (braga != nautico & braga != fluminense & nautico != fluminense)).

tff(premise_1, axiom, commonly_known_as(ailton_silva, ailton)).

tff(premise_2, axiom, loaned_to(ailton, braga)).

tff(premise_3, axiom, plays_for(ailton_silva, nautico)).

tff(premise_4, axiom, football_club(nautico) & football_club(braga)).

tff(premise_5, axiom, football_club(fluminense)).

% Negated conclusion: Ailton was loaned out to a football club
tff(goal, conjecture, loaned_to(ailton, braga)).