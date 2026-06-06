% Premises
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(class_member_michael, axiom, class_member(michael)).

% Michael is taller than everyone else in his class
fof(michael_taller_than_class, axiom, 
    ! [X] : (class_member(X) & X != michael => taller_than(michael, X))).

% Peter is taller than Michael
fof(peter_taller_than_michael, axiom, taller_than(peter, michael)).

% Transitivity of taller_than
fof(transitivity_taller, axiom,
    ! [X,Y,Z] : ((taller_than(X,Y) & taller_than(Y,Z)) => taller_than(X,Z))).

% Michael can block shooting from someone who doesn't jump
fof(michael_blocks_non_jumpers, axiom,
    ! [X] : (~can_jump(X) => can_block(michael, X))).

% Michael cannot block Windy's shooting
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).

% Every shooter who can jump is a great shooter
fof(jumpers_are_great, axiom,
    ! [X] : ((shooter(X) & can_jump(X)) => great_shooter(X))).

% Conclusion: Peter is shorter than a man in Michael's class
fof(goal, conjecture, 
    ? [X] : (class_member(X) & man(X) & ~taller_than(peter, X))). % Peter is shorter than X means X is taller than Peter