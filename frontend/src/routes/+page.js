/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
  const res = await fetch(`/api/books-by-author`);
  const library = await res.json();

  return { library };
}
