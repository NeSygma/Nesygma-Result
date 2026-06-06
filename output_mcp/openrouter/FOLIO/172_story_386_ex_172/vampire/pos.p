% Positive version
fof(ax1, axiom, ! [X] : (deadly_disease(X) => low_survival_rate(X))).
fof(ax2, axiom, ! [X] : (severe_cancer(X) => deadly_disease(X))).
fof(ax3, axiom, severe_cancer(bile_duct_cancer)).
fof(ax4, axiom, ! [X] : (cholangiocarcinoma(X) => bile_duct_cancer(X))).
fof(ax5, axiom, ! [X] : (mild_flu(X) => low_survival_rate(X))).
fof(ax6, axiom, ~ (bile_duct_cancer(colorectal_cancer) & low_survival_rate(colorectal_cancer))).
fof(distinct_consts, axiom, colorectal_cancer != bile_duct_cancer).
fof(goal, conjecture, cholangiocarcinoma(colorectal_cancer) & (mild_flu(colorectal_cancer) | bile_duct_cancer(colorectal_cancer))).