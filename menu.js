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
});
