document.addEventListener("DOMContentLoaded", () => {
    fetch("/menu.html")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("menu-container").innerHTML = data;
        })
        .catch(error => {
            console.error("Fehler beim Laden des Menüs:", error);
        });

    const footerHTML = `
      <footer class="text-center py-4 mt-auto">
         <small>
            <a href="/impressum.html" class="kategory-text-link text-decoration-none mx-2">Impressum</a>
            <a href="/datenschutz.html" class="kategory-text-link text-decoration-none mx-2">Datenschutz</a>
            <a href="/kontakt.html" class="kategory-text-link text-decoration-none mx-2">Kontakt</a>
         </small>
      </footer>
    `;
    document.body.insertAdjacentHTML('beforeend', footerHTML);
});
