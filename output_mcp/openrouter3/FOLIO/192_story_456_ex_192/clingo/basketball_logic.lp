% Basketball Logic Problem
% Premises and conclusion evaluation

% Domain: People
person(yuri).

% Premise 2: All professional basketball players can do jump shots
can_jump_shot(X) :- professional_basketball_player(X).

% Premise 3: If someone can jump shots, they leap straight into the air
leaps_straight_into_air(X) :- can_jump_shot(X).

% Premise 4: If someone leaps straight into the air, they activate their leg muscles
activates_leg_muscles(X) :- leaps_straight_into_air(X).

% Premise 5: Yuri does not activate his leg muscles
% This is a fact about Yuri
fact_yuri_no_leg_muscles.

% From premises 2-5, we can derive that Yuri cannot be a professional basketball player
% Because if he were, he would activate his leg muscles, but he doesn't

% Let's encode this derivation more carefully
% Rule: If Yuri is a professional basketball player, then he activates leg muscles
% But we know he doesn't activate leg muscles, so he can't be a professional basketball player
:- professional_basketball_player(yuri), not activates_leg_muscles(yuri).

% Since we have the constraint above and premise 5, we can derive:
not_professional_basketball_player(yuri) :- not activates_leg_muscles(yuri).

% Now evaluate the conclusion:
% "If Yuri is not an American professional basketball player, then Yuri is a professional basketball player"
% This is: ¬(american_national(yuri) ∧ professional_basketball_player(yuri)) → professional_basketball_player(yuri)

% Define the antecedent: Yuri is NOT an American professional basketball player
% This is true if either Yuri is not American OR Yuri is not a professional basketball player
antecedent(yuri) :- not (american_national(yuri) ∧ professional_basketball_player(yuri)).

% Since we know Yuri is NOT a professional basketball player, the antecedent is definitely true
antecedent_true(yuri) :- not_professional_basketball_player(yuri).

% Define the consequent: Yuri IS a professional basketball player
consequent(yuri) :- professional_basketball_player(yuri).

% Since we know Yuri is NOT a professional basketball player, the consequent is definitely false
consequent_false(yuri) :- not_professional_basketball_player(yuri).

% Now evaluate the implication: antecedent → consequent
% Since antecedent is true and consequent is false, the implication is false

% Positive logic for False: The conclusion is definitely false
conclusion_false :- antecedent_true(yuri), consequent_false(yuri).

% Positive logic for True: The conclusion is definitely true
% This would require that whenever antecedent is true, consequent is also true
% But we have a counterexample: antecedent true, consequent false
conclusion_true :- false.  % Cannot be true given premises

% Positive logic for Uncertain: The conclusion might be true or false depending on interpretation
% But given our derivation, it's definitely false

% Final answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show the answer
#show answer/1.