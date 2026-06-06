% Negative version
fof(ax1, axiom, ! [L] : (romance(L) => indo_european(L))).
fof(ax2, axiom, language_family(romance_family)).
fof(ax3, axiom, ! [L] : (romance(L) => member_of(L, romance_family))).
fof(ax4, axiom, ! [F, L1, L2] : ((language_family(F) & member_of(L1,F) & member_of(L2,F)) => related(L1, L2))).
fof(ax5, axiom, romance(french)).
fof(ax6, axiom, romance(spanish)).
fof(ax7, axiom, related(german, spanish)).
fof(ax8, axiom, ! [L] : (related(basque, L) => L = basque)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, ~romance(basque)).