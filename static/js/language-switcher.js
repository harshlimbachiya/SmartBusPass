document.addEventListener("DOMContentLoaded", function () {
	const languageLinks = document.querySelectorAll(".language-link");

	languageLinks.forEach(link => {
		link.addEventListener("click", function (event) {
			event.preventDefault();
			const newLanguage = this.getAttribute("data-language");
			const currentPath = window.location.pathname;
			const newPath = currentPath.replace(/\/[a-z\-_]+\/?/, `/${newLanguage}/`);
			window.location.href = newPath;
		});
	});
});