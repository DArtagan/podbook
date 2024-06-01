<script>
  import { toast } from '@zerodevx/svelte-toast';

  export let text;
  export let url;
  let link;

  function handleClick(event) {
    navigator.clipboard.writeText(link.href);
    toast.push('Copied podcast feed address to clipboard');
    event.preventDefault();
  }
</script>

<a href={url} on:click={handleClick} bind:this={link}>{text}</a>
