addEventListener("DOMContentLoaded", function(){
    const fundSelect = document.getElementById('fund');
    const outputP = this.document.getElementById('output')
    fundSelect.addEventListener('change', function () {
        const selectedFund = fundSelect.value; 
        outputP.textContent = selectedFund
    });
});