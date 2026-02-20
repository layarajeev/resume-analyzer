document.getElementById("resumeForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const file = document.getElementById("resumeFile").files[0];

    if (!file) {
        alert("Please upload a resume file.");
        return;
    }

    // Show results section
    document.getElementById("results").classList.remove("hidden");

    // Demo AI Results (Fake for frontend)
    document.getElementById("score").innerText = "82";

    document.getElementById("skillsList").innerHTML =
        "<li>Python</li><li>HTML</li><li>JavaScript</li>";

    document.getElementById("grammarList").innerHTML =
        "<li>Capitalize 'I'</li><li>Add more project details</li>";
});