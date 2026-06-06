% Premises about the mixer
fof(at_mixer_djokovic, axiom, at_mixer(djokovic)).

% Premise 1: Everyone at the mixer is a Grand Slam champion or an Oscar-nominated actor
fof(premise_1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).

% Premise 2: Every Grand Slam champion at the mixer is a professional tennis player
fof(premise_2, axiom, ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).

% Premise 3: All Oscar-nominated actors at the mixer are celebrities
fof(premise_3, axiom, ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).

% Premise 4: All professional tennis players at the mixer are athletes
fof(premise_4, axiom, ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).

% Premise 5: If a person at the mixer is a celebrity, then they are well paid
fof(premise_5, axiom, ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).

% Premise 6: If a person at the mixer is an athlete, then they are famous
fof(premise_6, axiom, ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).

% Premise 7: All well-paid people at the mixer live in tax havens
fof(premise_7, axiom, ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).

% Premise 8: Djokovic is at the mixer: if Djokovic is a famous athlete, then Djokovic is well-paid
fof(premise_8, axiom, (at_mixer(djokovic) & famous(djokovic) & athlete(djokovic)) => well_paid(djokovic)).

% Negated conclusion
fof(goal_negated, conjecture, ~grand_slam_champion(djokovic)).