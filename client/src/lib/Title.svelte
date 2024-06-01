<script>
  import CopyToClipboardLink from './CopyToClipboardLink.svelte';
  export let title;
  export let uuid;
</script>

<li class="list-group-item"><CopyToClipboardLink text={title} url="feed/{uuid}.xml" /></li>

<style>
</style>
