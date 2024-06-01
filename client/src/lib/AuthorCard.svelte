<script>
  import Title from './Title.svelte';
  export let author;
  export let books;
</script>

<div class="card mb-2">
  <p class="card-header">{author}</p>
  <ul class="list-group list-group-flush">
    {#each books as { title, uuid }}
      <Title {title} {uuid} />
    {/each}
  </ul>
</div>

<style>
</style>
