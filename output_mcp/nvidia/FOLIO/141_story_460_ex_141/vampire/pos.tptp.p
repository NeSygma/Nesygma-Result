fof(ax1, axiom, ! [F] : (appropriate_for_all_ages(F) => can_watch_without_guidance(F))).
fof(ax2, axiom, ! [F] : (excessive_erotic_violent_content(F) => ~can_watch_without_guidance(F))).
fof(ax3, axiom, ! [F] : (rated_ga(F) => appropriate_for_all_ages(F))).
fof(ax4, axiom, ! [F] : (family_friendly_animated(F) => rated_ga(F))).
fof(ax5, axiom, ! [F] : (in_frozen_series(F) => family_friendly_animated(F))).
fof(premise7, axiom, family_friendly_animated(hachi) | appropriate_for_all_ages(hachi)).
fof(conclusion, conjecture, excessive_erotic_violent_content(hachi) | in_frozen_series(hachi)).