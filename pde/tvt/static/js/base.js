if ('scrollRestoration' in history) {
	history.scrollRestoration = 'manual';
}

window.addEventListener('beforeunload', function () {
	localStorage.setItem('scrollPosition', window.scrollY);
});

function restoreScrollWhenReady() {
	const scrollPos = localStorage.getItem('scrollPosition');
	if (!scrollPos) return;

	let attempts = 0;
	const maxAttempts = 20;

	const interval = setInterval(() => {
		const pageHeight = document.body.scrollHeight;
		const viewportHeight = window.innerHeight;

		if (pageHeight > parseInt(scrollPos) || attempts > maxAttempts) {
			window.scrollTo(0, parseInt(scrollPos));
			clearInterval(interval);
		}

		attempts++;
	}, 200);
}

window.addEventListener('load', restoreScrollWhenReady);