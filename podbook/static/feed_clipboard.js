var getAbsoluteUrl = (function() {
  var a;

  return function(url) {
    if(!a) a = document.createElement('a');
    a.href = url;

    return a.href;
  };
})();

// Clipboard
var clipboard = new Clipboard('.clipboard', {
  text: function(trigger) {
  //var txt = trigger.textContent, // txt of clicked link
  //    url = trigger.previousElementSibling.getAttribute('href'); // Get url out of previous <a>
    var url = getAbsoluteUrl(trigger.getAttribute('href'));
  return url;
  }
});

clipboard.on('success', function(e) {
  $('#copied').modal('show')
});

clipboard.on('error', function(e) {
  window.location = e.trigger.getAttribute('href');
});

$('.clipboard').click(function(e) {
  e.preventDefault();
});
