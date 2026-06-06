% Positive version
fof(ax1, axiom, ! [X] : (multiple_birth(X) => spend_time_with_siblings(X))).
fof(ax2, axiom, ! [X] : (siblings_together(X) => multiple_birth(X))).
fof(ax3, axiom, ! [X] : (complain_about_siblings(X) => siblings_together(X))).
fof(ax4, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(ax5, axiom, ! [X] : (spend_time_with_siblings(X) => live_at_home(X))).
fof(ax6, axiom, ( (multiple_birth(luke) & live_with_strangers(luke)) | (~multiple_birth(luke) & ~live_with_strangers(luke)) ) ).
fof(conj, conjecture, spend_time_with_siblings(luke)).