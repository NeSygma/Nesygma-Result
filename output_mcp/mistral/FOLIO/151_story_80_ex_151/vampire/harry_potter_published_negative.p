tff(book_type, type, book: $tType).
tff(publisher_type, type, publisher: $tType).

tff(new_vessel_press, type, new_vessel_press: publisher).
tff(neapolitan_chronicles, type, neapolitan_chronicles: book).
tff(palace_of_flies, type, palace_of_flies: book).
tff(harry_potter, type, harry_potter: book).

tff(published_by_type, type, published_by: (book * publisher) > $o).

fof(neapolitan_published, axiom,
    published_by(neapolitan_chronicles, new_vessel_press)).

fof(palace_published, axiom,
    published_by(palace_of_flies, new_vessel_press)).

fof(distinct_books, axiom,
    (neapolitan_chronicles != palace_of_flies &
     neapolitan_chronicles != harry_potter &
     palace_of_flies != harry_potter)).

fof(conclusion_negation, conjecture,
    ~published_by(harry_potter, new_vessel_press)).