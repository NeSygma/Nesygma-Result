% Positive version
fof(ax1, axiom, ? [X] : (professional(X) & ~american(X))).
fof(ax2, axiom, ! [X] : (professional(X) => can_jump(X))).
fof(ax3, axiom, ! [X] : (can_jump(X) => leap(X))).
fof(ax4, axiom, ! [X] : (leap(X) => activate(X))).
fof(ax5, axiom, ~activate(yuri)).
fof(goal, conjecture, ~ (american(yuri) & professional(yuri))).