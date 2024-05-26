<script>
  import 'bootstrap/dist/css/bootstrap.css';
  // TODO: can we remove the bootstrap js?
  import bootstrapScriptSource from 'bootstrap/dist/js/bootstrap.bundle.js?url';
  import '../app.scss';
</script>

<svelte:head>
  <script src={bootstrapScriptSource}></script>
</svelte:head>

<div class="container mt-3 mb-4">
  <h1 class="display-4">Podbook Rebound</h1>
</div>

<slot></slot>

<style></style>
