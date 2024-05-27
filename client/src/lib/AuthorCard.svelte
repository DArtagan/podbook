<script>
  export let author;
  export let books;
</script>

<div class="card mb-2">
  <p class="card-header">{author}</p>
  <ul class="list-group list-group-flush">
    {#each books as { title, uuid }}
      <li class="list-group-item"><a class="clipboard" href="feed/{uuid}.xml">{title}</a></li>
    {/each}
  </ul>
</div>

<style>
</style>
