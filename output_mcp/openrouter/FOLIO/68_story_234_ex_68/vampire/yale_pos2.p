% Positive version without numeric endowment
fof(yale_private, axiom, private_university(yale_university)).
fof(yale_ivy, axiom, ivy_league_university(yale_university)).
fof(yale_research, axiom, research_university(yale_university)).
fof(yale_moved, axiom, moved_to(yale_university, new_haven)).
% Residential colleges list
fof(res_bc, axiom, residential_college_at(benjamin_franklin_college, yale_university)).
fof(res_bc2, axiom, residential_college_at(berkeley_college, yale_university)).
fof(res_bc3, axiom, residential_college_at(branford_college, yale_university)).
fof(res_dc, axiom, residential_college_at(davenport_college, yale_university)).
fof(res_ec, axiom, residential_college_at(ezra_stiles_college, yale_university)).
fof(res_gc, axiom, residential_college_at(grace_hopper_college, yale_university)).
fof(res_jc, axiom, residential_college_at(jonathan_edwards_college, yale_university)).
fof(res_mc, axiom, residential_college_at(morse_college, yale_university)).
fof(res_pm, axiom, residential_college_at(pauli_murray_college, yale_university)).
fof(res_pc, axiom, residential_college_at(pierson_college, yale_university)).
fof(res_sc, axiom, residential_college_at(saybrook_college, yale_university)).
fof(res_sic, axiom, residential_college_at(silliman_college, yale_university)).
fof(res_tdc, axiom, residential_college_at(timothy_dwight_college, yale_university)).
fof(res_tc, axiom, residential_college_at(trumbull_college, yale_university)).
% Conjecture
fof(goal, conjecture, residential_college_at(pierson_college, yale_university)).