% Positive version: original conclusion as conjecture
% Premises

% Animals are either invertebrates or vertebrates.
fof(ax1, axiom, ! [X] : (animal(X) => (invertebrate(X) <=> ~vertebrate(X)))).

% All animals with backbones reproduce by male-and-female mating.
fof(ax2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_male_female(X))).

% All vertebrate animals have a backbone.
fof(ax3, axiom, ! [X] : ((animal(X) & vertebrate(X)) => has_backbone(X))).

% All bees do not reproduce by male-and-female mating.
fof(ax4, axiom, ! [X] : (bee(X) => ~reproduces_male_female(X))).

% All queen bees are bees.
fof(ax5, axiom, ! [X] : (queen_bee(X) => bee(X))).

% Harry is a bee.
fof(ax6, axiom, bee(harry)).

% Harry is an animal (implicit from context - bees are animals)
fof(ax7, axiom, ! [X] : (bee(X) => animal(X))).

% Conclusion: If Harry is either both a vertebrate and an animal with a backbone, or neither a vertebrate nor an animal with a backbone, then Harry is neither an invertebrate nor a queen bee.
% Let P = (vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry))
% Let Q = ~invertebrate(harry) & ~queen_bee(harry)
% Conjecture: P => Q

fof(conclusion, conjecture,
    ( ( (vertebrate(harry) & has_backbone(harry))
      | (~vertebrate(harry) & ~has_backbone(harry)) )
    => ( ~invertebrate(harry) & ~queen_bee(harry) ) )).