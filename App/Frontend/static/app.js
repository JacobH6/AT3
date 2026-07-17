document.addEventListener("DOMContentLoaded", () => {

    const cancelEdit = document.getElementById("cancel-edit");

    if (cancelEdit) {

        cancelEdit.addEventListener("click", () => {

            document.getElementById("edit-popup")
                .classList.add("hidden");

        });

    }

    const popup = document.getElementById("edit-popup");

        if (popup) {

            popup.addEventListener("click", (e) => {

                if (e.target === popup) {

                    popup.classList.add("hidden");

                }

            });

        }

    // Dark mode toggle
    const darkModeButton = document.getElementById("darkModeButton");

    if (darkModeButton) {

        darkModeButton.addEventListener("click", async () => {

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


    // Load leaderboard
    const leaderboard = document.getElementById("leaderboard");

    if (leaderboard) {
        loadLeaderboard();
    }


    // Workout form
    const workoutForm = document.getElementById("workout-form");

    if (workoutForm) {

    workoutForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const message = document.getElementById("workout-message");

        const data = {
            exercise: document.getElementById("exercise").value,
            weight: document.getElementById("weight").value,
            reps: document.getElementById("reps").value
        };


        const response = await fetch(
            "/api/workouts",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );


        const result = await response.json();


        if (!response.ok) {

            if (message) {
                message.textContent = result.error;
                message.className = "error-message";
            }

            return;
        }


        if (message) {
            message.textContent = "Workout added!";
            message.className = "success-message";
        }


        // Update player stats
        if (result.success) {

            const level = document.getElementById("level");
            const xp = document.getElementById("xp");
            const title = document.getElementById("title");

            if (level) {
                level.textContent = `Level ${result.level}`;
            }

            if (xp) {
                xp.textContent = `${result.experience}/100 XP`;
            }

            if (title) {
                title.textContent = result.title;
            }
            if (document.getElementById("workout-list")) {
            loadWorkouts();
            }
        }

    });
    }


    if (document.getElementById("xpGraph")) {
    loadXPGraph();
    }

    if (document.getElementById("workout-list")) {
    loadWorkouts();
    }
});

// Leaderboard function
async function loadLeaderboard() {

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

async function loadXPGraph(){

    const response = await fetch("/api/xp-history");

    const data = await response.json();

    const history = data.history;


    const exercises = {};


    Object.entries(history).forEach(([date, workouts]) => {

        Object.entries(workouts).forEach(([exercise, xp]) => {

            if (!exercises[exercise]) {
                exercises[exercise] = [];
            }

            exercises[exercise].push({
                x: date,
                y: xp
            });

        });

    });


    const datasets = Object.entries(exercises).map(
        ([exercise, points]) => ({
            label: exercise,
            data: points
        })
    );


    new Chart(
        document.getElementById("xpGraph"),
        {
            type: "line",

            data: {
                datasets: datasets
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
    );
}

async function loadWorkouts(){

    const response = await fetch("/api/workouts");

    const data = await response.json();

    const list = document.getElementById("workout-list");

    list.innerHTML = "";


    data.workouts
        .sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        )
        .forEach(workout => {

        list.innerHTML += `

        <div class="workout-entry">

            <div class="workout-info">

                <h3>${workout.exercise}</h3>

                <p>
                    ${workout.weight} x ${workout.reps}
                </p>

                <p>
                    ${workout.xp_gained} XP
                </p>

                <p>
                    ${new Date(workout.timestamp).toLocaleString()}
                </p>

            </div>


            <div class="workout-buttons">

                <button onclick="editWorkout('${workout.id}')">
                    Edit
                </button>

                <button onclick="deleteWorkout('${workout.id}')">
                    Delete
                </button>

            </div>

        </div>

        `;

    });

}

async function deleteWorkout(id){

    if (!confirm("Delete this workout?")) {
        return;
    }


    const response = await fetch(
        `/api/workouts/${id}`,
        {
            method: "DELETE"
        }
    );


    const result = await response.json();


    if(result.success){
        loadWorkouts();
    }

}

async function editWorkout(id){

    const response = await fetch("/api/workouts");

    const data = await response.json();


    const workout = data.workouts.find(
        w => w.id === id
    );


    document.getElementById("edit-id").value = workout.id;

    document.getElementById("edit-exercise").value =
        workout.exercise;

    document.getElementById("edit-weight").value =
        workout.weight;

    document.getElementById("edit-reps").value =
        workout.reps;


    document.getElementById("edit-popup")
        .classList.remove("hidden");

}

document.getElementById("save-edit")
.addEventListener("click", async ()=>{

    const id =
        document.getElementById("edit-id").value;


    await fetch(
        `/api/workouts/${id}`,
        {
            method:"PUT",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                exercise:
                document.getElementById("edit-exercise").value,

                weight:
                document.getElementById("edit-weight").value,

                reps:
                document.getElementById("edit-reps").value

            })
        }
    );


    document.getElementById("edit-popup")
        .classList.add("hidden");


    loadWorkouts();

});