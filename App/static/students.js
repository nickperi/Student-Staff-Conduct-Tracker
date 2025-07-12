const dropdown = document.getElementById('sort-by');
const table = document.getElementById('students-table');

function getStudents(sortAttribute) {
    fetch(sortAttribute)
        .then(response => response.json())
        .then(data => {
        console.log(data);
        loadTable(data);
    });
}

function loadTable(students) {
    table.innerHTML = "";
    students.forEach(student => {
        table.innerHTML += `<tr>
            <td>${student.id}</td>
            <td>${student.username}</td>
            <td>${student.email}</td>
            <td>${student.score}</td>
        </tr>`;
    });
}

dropdown.addEventListener("change", (e) => {
    switch(e.target.value) {

        case "id-asc":
        getStudents('/api/students/sort-by-id-asc');
        break;

        case "id-desc":
        getStudents('/api/students/sort-by-id-desc');
        break;

        case "username-asc":
        getStudents('/api/students/sort-by-username-asc');
        break;

        case "username-desc":
        getStudents('/api/students/sort-by-username-desc');
        break;

        case "score-asc":
        getStudents('/api/students/sort-by-score-asc');
        break;

        case "score-desc":
        getStudents('/api/students/sort-by-score-desc');
        break;

        default:
        getStudents('/api/students');
        break;
    }
});