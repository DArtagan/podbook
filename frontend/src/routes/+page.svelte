<script>
  import AuthorCard from '$lib/AuthorCard.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<div class="container">
  <div class="card-columns">
    {#each data.library as { author, books }}
      <AuthorCard {author} {books} />
    {:else}
      <p>No books found.</p>
    {/each}
  </div>
</div>
