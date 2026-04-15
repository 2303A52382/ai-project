//Develop JavaScript code to send user input to the Flask backend and dynamically display 
// career roles, match score, and skill gaps//
function predict() {
    let skills = document.getElementById("skills").value;
    let fileInput = document.getElementById("file");
    let formData = new FormData();
    formData.append("skills", skills);
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        let output = "";
        let best = data[0];
        output += `<h2>🏆 Best Match: ${best.role} (${best.score}%)</h2>`;
        data.forEach(r => {
            output += `
            <div class="card">
                <h3>${r.role} (${r.score}%)</h3>

                <p><b style="color:green;">✔ Matched:</b> ${r.matched.join(", ") || "None"}</p>
                <p><b style="color:red;">❌ Missing:</b> ${
                    r.missing.length ? r.missing.join(", ") : "No missing skills 🎉"
                }</p>

                <p><b>Roadmap:</b></p>
                <ul>
                    ${r.roadmap.map(step => `<li>${step}</li>`).join("")}
                </ul>
            </div>
            `;
        });
        document.getElementById("result").innerHTML = output;
    });
}