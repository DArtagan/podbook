var getAbsoluteUrl = (() => {
	var a;

	return (url) => {
		if (!a) a = document.createElement("a");
		a.href = url;

		return a.href;
	};
})();

// Clipboard
var clipboard = new Clipboard(".clipboard", {
	text: (trigger) => {
		//var txt = trigger.textContent, // txt of clicked link
		//    url = trigger.previousElementSibling.getAttribute('href'); // Get url out of previous <a>
		var url = getAbsoluteUrl(trigger.getAttribute("href"));
		return url;
	},
});

clipboard.on("success", (e) => {
	$("#copied").modal("show");
});

clipboard.on("error", (e) => {
	window.location = e.trigger.getAttribute("href");
});

$(".clipboard").click((e) => {
	e.preventDefault();
});
