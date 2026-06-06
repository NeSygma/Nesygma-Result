fof(all_books_contain_knowledge, axiom, ! [B] : (book(B) => contains_knowledge(B))).
fof(harry_reads_walden, axiom, reads(harry, walden)).
fof(walden_is_book, axiom, book(walden)).
fof(walden_does_not_contain_knowledge, conjecture, ~contains_knowledge(walden)).