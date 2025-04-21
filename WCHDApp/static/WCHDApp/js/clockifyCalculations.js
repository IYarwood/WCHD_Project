document.addEventListener("DOMContentLoaded", function(){
    const rows = document.querySelectorAll("#activityTable tr");

    const activityDropdown = document.querySelector("#activityDropdown");
    activityDropdown.addEventListener("change", function(){
        let sum = 0;
        const activity = this.value;
        for (let i = 0; i<rows.length; i++){
            if (rows[i].dataset.activityid == activity){
                console.log("Matched");
                sum += parseFloat(rows[i].dataset.billamount);
            }
        }
        const sumOutput = document.querySelector("#fundActivity");
        sumOutput.innerHTML = "Fund by Activity: $" + sum;
    });

    const employeeDropdown = document.querySelector("#employeeDropdown");
    employeeDropdown.addEventListener("change", function(){
        let sum = 0;
        const employee = this.value;
        for (let i = 0; i<rows.length; i++){
            if (rows[i].dataset.employeeid == employee){
                console.log("Matched");
                sum += parseFloat(rows[i].dataset.billamount);
            }
        }
        const sumOutput = document.querySelector("#fundEmployee");
        sumOutput.innerHTML = "Fund by Employee: $" + sum;
    });

});