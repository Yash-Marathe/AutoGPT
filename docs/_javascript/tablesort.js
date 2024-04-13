document$.subscribe(() => {
  const tables = Array.from(document.querySelectorAll("article table:not([class])"));
  tables.forEach(table => new Tablesort(table));
});


document$.subscribe(() => {
  const tables = Array.from(document.querySelectorAll("article table:not([class])"));
  tables.forEach(Tablesort);
});
