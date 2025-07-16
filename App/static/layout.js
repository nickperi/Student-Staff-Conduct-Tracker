const myProfileButton = document.getElementById('my-profile');
const addStaffButton = document.getElementById('add-staff');
const addStudentButton = document.getElementById('add-student');
const viewStudentsButton = document.getElementById('view-students');
const logReviewButton = document.getElementById('log-review');

myProfileButton.addEventListener("click", () => {
    myProfileButton.style.color = 'aqua';
    myProfileButton.style.backgroundColor = 'darkmagenta';
});