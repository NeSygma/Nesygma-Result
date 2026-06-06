% Negative file: Negated conclusion as conjecture
% Premise 1: Animals are either invertebrates or vertebrates (exclusive)
fof(premise_1a, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(premise_1b, axiom, ! [X] : (animal(X) => (~invertebrate(X) | ~vertebrate(X)))).

% Premise 2: All animals with backbones reproduce by male-and-female mating
fof(premise_2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduce_male_female(X))).

% Premise 3: All vertebrate animals have a backbone
fof(premise_3, axiom, ! [X] : ((animal(X) & vertebrate(X)) => has_backbone(X))).

% Premise 4: All bees do not reproduce by male-and-female mating
fof(premise_4, axiom, ! [X] : (bee(X) => ~reproduce_male_female(X))).

% Premise 5: All queen bees are bees
fof(premise_5, axiom, ! [X] : (queen_bee(X) => bee(X))).

% Premise 6: Harry is a bee
fof(premise_6, axiom, bee(harry)).

% Negated conclusion:
% ~{ [(vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry))]
%     => (~invertebrate(harry) & ~queen_bee(harry)) }
% = [(vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry))]
%   & ~(~invertebrate(harry) & ~queen_bee(harry))
% = [(vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry))]
%   & (invertebrate(harry) | queen_bee(harry))
fof(negated_conclusion, conjecture,
    ((vertebrate(harry) & has_backbone(harry)) | (~vertebrate(harry) & ~has_backbone(harry)))
    & (invertebrate(harry) | queen_bee(harry))).