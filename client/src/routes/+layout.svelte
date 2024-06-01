<script>
  import 'bootstrap/dist/css/bootstrap.css';
  import { SvelteToast } from '@zerodevx/svelte-toast';
  //import bootstrapScriptSource from 'bootstrap/dist/js/bootstrap.bundle.js?url';
  import '../app.scss';
</script>

<svelte:head></svelte:head>

<SvelteToast />

<div class="container mt-3 mb-4">
  <h1 class="display-4">Podbook Rebound</h1>
</div>

<slot></slot>

<style></style>
