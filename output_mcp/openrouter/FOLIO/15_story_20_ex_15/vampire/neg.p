% Negative test: conjecture that Legend of Zelda IS on Top10
fof(ax_exist_jp_creator, axiom, ? [C] : (japanese_company(C) & created_by(legend_of_zelda, C))).
fof(ax_top10_made_by_jp, axiom, ! [G] : (top10(G) => ? [C] : (created_by(G, C) & japanese_company(C)))).
fof(ax_sales_imp_top10, axiom, ! [G] : (sells_million(G) => top10(G))).
fof(ax_zelda_sales, axiom, sells_million(legend_of_zelda)).
fof(conj_top10, conjecture, top10(legend_of_zelda)).