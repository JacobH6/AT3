document.addEventListener("DOMContentLoaded", () => {

    const button = document.getElementById("darkModeButton");

    if (button) {
        button.addEventListener("click", async () => {

            const response = await fetch("/api/settings/darkmode", {
                method: "POST"
            });

            const data = await response.json();

            document.body.classList.toggle(
                "dark-mode",
                data.dark_mode
            );
        });
    }

});

const darkMode =
    document.body.dataset.darkMode === "True";

async function loadLeaderboard(){

    const response = await fetch("/api/leaderboard");
    const data = await response.json();

    const table = document.getElementById("leaderboard");

    data.leaderboard.forEach((player, index) => {

        table.innerHTML += `
            <tr>
                <td>${index + 1}</td>
                <td>${player.username}</td>
                <td>${player.level}</td>
                <td>${player.experience}/100</td>
            </tr>
        `;
    });
}


document.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("leaderboard")) {
        loadLeaderboard();
    }

});