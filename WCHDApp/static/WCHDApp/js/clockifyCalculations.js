document.addEventListener("DOMContentLoaded", function(){
    let activities = [];
    fetch('/getActivities/')
      .then(response => response.json())
      .then(data => {
        //console.log("Fetched JSON:", data);
        //console.log(data["activities"]);
        activities = data["activities"];
      })
      .catch(error => console.error("Error fetching data:", error));
    const rows = document.querySelectorAll("#activityTable tr");

    const activityDropdown = document.querySelector("#activityDropdown");
    activityDropdown.addEventListener("change", function(){
        let sum = 0;
        let hours = 0;
        const activity = this.value;
        for (let i = 0; i<rows.length; i++){
            if (rows[i].dataset.activityid == activity){
                sum += parseFloat(rows[i].dataset.billamount);
                hours += parseFloat(rows[i].dataset.hours);
            }
        }
        const sumOutput = document.querySelector("#fundActivity");
        sumOutput.innerHTML = "Fund by Activity: $" + sum + " total hours = " + hours;
    });

   
    const employeeDropdown = document.querySelector("#employeeDropdown");
    employeeDropdown.addEventListener("change", function(){
        const sumOutput = document.querySelector("#fundEmployee");
        sumOutput.innerHTML = "";
        const employee = this.value;
        const employeeName = this.options[this.selectedIndex].text;
        console.log(employeeName);

        for (let i=0; i<activities.length; i++){
            let sum = 0;
            let hours = 0;
            console.log(activities[i][0]);
            for (let j=0; j <rows.length; j ++){
                if ((rows[j].dataset.employeeid == employee) && (rows[j].dataset.activityid == activities[i][0])){
                    console.log("Matched");
                    sum += parseFloat(rows[j].dataset.billamount);
                    hours += parseFloat(rows[j].dataset.hours);
                }
            }

            const sumOutput = document.querySelector("#fundEmployee");
            sumOutput.innerHTML += employeeName + " in " + activities[i][1]+ ": $" + sum + " in "+hours+" hours<br>";
        }
    });

});