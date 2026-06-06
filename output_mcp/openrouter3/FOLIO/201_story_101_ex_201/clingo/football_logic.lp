% Logical premises about Ailton Silva

% 1. Ailton Silva, born in 1995, is commonly known as Ailton.
person("Ailton Silva", 1995).
known_as("Ailton Silva", "Ailton").

% 2. Ailton is a football player who was loaned out to Braga.
football_player("Ailton Silva").
loaned_to("Ailton Silva", "Braga").

% 3. Ailton Silva is a Brazilian footballer who plays for Náutico.
nationality("Ailton Silva", "Brazil").
plays_for("Ailton Silva", "Náutico").

% 4. Náutico is a football club along with Braga.
football_club("Náutico").
football_club("Braga").

% 5. Fluminense is a football club.
football_club("Fluminense").

% --- Conclusion Evaluation ---
% The conclusion: "Ailton was not loaned out to a football club."
% This means: NOT (there exists a football club C such that loaned_to(Ailton, C))

% Positive logic for True (conclusion holds)
% This would require that Ailton was NOT loaned to any football club
conclusion_true :- not loaned_to_any_football_club.

% Helper predicate: Ailton was loaned to at least one football club
loaned_to_any_football_club :- loaned_to("Ailton Silva", C), football_club(C).

% Positive logic for False (conclusion does NOT hold)
% This means Ailton WAS loaned to a football club
conclusion_false :- loaned_to_any_football_club.

% Final Answer Mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show the answer
#show answer/1.
#show loaned_to_any_football_club.
#show loaned_to/2.
#show football_club/1.