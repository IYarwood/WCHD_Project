document.addEventListener("DOMContentLoaded", function () {
  //Calling getActivities view whihc returns json data of the activities pulled from model
  let activities = [];
  fetch("/getActivities/")
    .then((response) => response.json())
    .then((data) => {
      //console.log("Fetched JSON:", data);
      //console.log(data["activities"]);
      activities = data["activities"];
    })
    .catch((error) => console.error("Error fetching data:", error));

  //Selecting rows from activity Table
  const rows = document.querySelectorAll("#activityTable tr");

  //When fund dropdown changes pull data from dataset for each row matching fund to make calculations
  const fundDropdown = document.querySelector("#fundDropdown");
  fundDropdown.addEventListener("change", function () {
    let sum = 0;
    let hours = 0;
    const fund = this.value;
    const fundName = this.options[this.selectedIndex].text;
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].dataset.fundid == fund) {
        sum += parseFloat(rows[i].dataset.billamount);
        hours += parseFloat(rows[i].dataset.hours);
      }
    }
    const sumOutput = document.querySelector("#fundInfo");
    const tableHTML = `
        <table>
            <tr>
                <th>Fund Name</th>
                <th>Total Sum</th>
                <th>Total Hours</th>
            </tr>
            <tr>
                <td>${fundName}</td>
                <td>$${sum.toFixed(2)}</td>
                <td>${hours}</td>
            </tr>
        </table>
        `;
    //Define table structure in string then pass it as the innerhtml
    //sumOutput.innerHTML = fundName + ": $" + sum.toFixed(2) + " total hours = " + hours;
    sumOutput.innerHTML = tableHTML;
  });

  //Same logic as fund
  const activityDropdown = document.querySelector("#activityDropdown");
  activityDropdown.addEventListener("change", function () {
    let sum = 0;
    let hours = 0;
    const activity = this.value;
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].dataset.activityid == activity) {
        sum += parseFloat(rows[i].dataset.billamount);
        hours += parseFloat(rows[i].dataset.hours);
      }
    }
    const sumOutput = document.querySelector("#fundActivity");
    const tableHTML = `
    <table>
        <tr>
            <th>Activity</th>
            <th>Total Sum</th>
            <th>Total Hours</th>
        </tr>
        <tr>
            <td>${activity}</td>
            <td>${sum.toFixed(2)}</td>
            <td>${hours}</td>
        </tr>
    </table>`
    //sumOutput.innerHTML ="Fund by Activity: $" + sum.toFixed(2) + " total hours = " + hours;
    sumOutput.innerHTML = tableHTML;
  });

  //Same logic as fund
  const employeeDropdown = document.querySelector("#employeeDropdown");
  employeeDropdown.addEventListener("change", function () {
    const sumOutput = document.querySelector("#fundEmployee");
    sumOutput.innerHTML = "";

    const totalHourOutput = document.querySelector("#totalHourOutput");
    totalHourOutput.innerHTML = "";
    const employee = this.value;
    const employeeName = this.options[this.selectedIndex].text;
    let totalHours = 0;

    let tableRows = '';
    for (let i = 0; i < activities.length; i++) {
      let sum = 0;
      let hours = 0;
      for (let j = 0; j < rows.length; j++) {
        if (
          rows[j].dataset.employeeid == employee &&
          rows[j].dataset.activityid == activities[i][0]
        ) {
          sum += parseFloat(rows[j].dataset.billamount);
          hours += parseFloat(rows[j].dataset.hours);
          totalHours += parseFloat(rows[j].dataset.hours);
        }
      }
      tableRows += `
        <tr>
          <td>${activities[i][1]}</td>
          <td>$${sum.toFixed(2)}</td>
          <td>${hours}</td>
        </tr>
      `;

      const sumOutput = document.querySelector("#fundEmployee");

      //sumOutput.innerHTML += employeeName + " in " + activities[i][1] + ": $" + sum.toFixed(2) + " in " + hours + " hours<br>";
    }

    const tableHTML = `
    <table>
        <tr>
            <th>Activity Name</th>
            <th>Total Sum</th>
            <th>Total Hours</th>
        </tr>

        ${tableRows}
        <tr>
            <td></td>
            <td></td>
            <td>${totalHours}</td>
        </tr>
    </table>`;
    //totalHourOutput.innerHTML = employeeName + " total hours: " + totalHours;
    totalHourOutput.innerHTML = tableHTML;
  });
});
