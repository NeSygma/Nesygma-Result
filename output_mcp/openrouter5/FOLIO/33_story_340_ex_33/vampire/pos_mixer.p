% Positive version: original conclusion as conjecture
% Conclusion: Djokovic does not live in a tax haven.

% Premise 1: Everyone at the mixer is a Grand Slam champion or an Oscar-nominated actor.
fof(p1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).

% Premise 2: Every Grand Slam champion at the mixer is a professional tennis player.
fof(p2, axiom, ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).

% Premise 3: All Oscar-nominated actors at the mixer are celebrities.
fof(p3, axiom, ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).

% Premise 4: All professional tennis players at the mixer are athletes.
fof(p4, axiom, ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).

% Premise 5: If a person at the mixer is a celebrity, then they are well paid.
fof(p5, axiom, ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).

% Premise 6: If a person at the mixer is an athlete, then they are famous.
fof(p6, axiom, ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).

% Premise 7: All well-paid people at the mixer live in tax havens.
fof(p7, axiom, ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).

% Premise 8: Djokovic is at the mixer: if Djokovic is a famous athlete, then Djokovic is well-paid.
fof(p8a, axiom, at_mixer(djokovic)).
fof(p8b, axiom, ((at_mixer(djokovic) & famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).

% Conclusion: Djokovic does not live in a tax haven.
fof(goal, conjecture, ~lives_in_tax_haven(djokovic)).