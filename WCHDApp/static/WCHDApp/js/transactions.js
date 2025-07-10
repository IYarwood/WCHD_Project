addEventListener("DOMContentLoaded", function(){
    const fundSelect = this.document.getElementById("fundsSelect")
    const linesDiv = document.getElementById('lines');
    const lines = linesDiv.querySelectorAll('p')
    const outputP = this.document.getElementById('outputs')

    fundSelect.addEventListener('change', function (e) {
        lines.forEach(function(line){
            console.log(line.dataset.line_name);
        });
    });
});