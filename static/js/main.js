const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const generateBtn = document.getElementById("generate-btn");
const quantityInput = document.getElementById("quantity-input");
const numBitsInput = document.getElementById("numBits-input");
const resultTable = document.getElementById("result-table");
const toggleBtn = document.getElementById("toggleBtn");
const alertDiv = document.getElementById("alertDiv");
let isRunning = false;

toggleBtn.addEventListener("click", () => {
  if (!isRunning) {
    fetch("http://192.168.136.27:8080/trng/randomNum/init")
      .then((response) => {
        console.log("Started");
        const button = document.getElementById('generate-btn');
        button.disabled = false;
        const canvas = document.getElementById('canvas');
        canvas.hidden = false;
        toggleBtn.textContent = "Stop";
        toggleBtn.classList.add("stop");
        toggleBtn.style.backgroundColor = "red";
        isRunning = true;
      })
      .catch((error) => {
        console.error("Error starting:", error);
      });
  } else {
    fetch("http://192.168.136.27:8080/trng/randomNum/shutdown")
      .then((response) => {
        console.log("Stopped");
        hideSpinner();
        resetTable();
        const button = document.getElementById('generate-btn');
        button.disabled = true;
        const button2 = document.getElementById('export-btn');
        button2.disabled = true;
        const quantity_input = document.getElementById('quantity-input');
        quantity_input.value = 1;
        const numBits_input = document.getElementById('numBits-input');
        numBits_input.value = 1;
        const canvas = document.getElementById('canvas');
        canvas.hidden = true;
        let alert = alertDiv;
        alert.hidden = true;
        toggleBtn.textContent = "Start";
        toggleBtn.classList.remove("stop");
        toggleBtn.style.backgroundColor = "green";
        isRunning = false;
      })
      .catch((error) => {
        console.error("Error stopping:", error);
      });
  }
});


generateBtn.addEventListener("click", () => {
  const quantity = quantityInput.value;
  const numBits = numBitsInput.value;
  const url = `http://192.168.136.27:8080/trng/randomNum/getRandom?quantity=${quantity}&numBits=${numBits}`;
  const button = document.getElementById('generate-btn');
  button.disabled = true;
  const button2 = document.getElementById('export-btn');
  button2.disabled = true;
  resetTable();
  const requiredBits = quantity * numBits;
  showTimeAlert(requiredBits);
  showSpinner();
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      //console.log(data.randomBits);
      exportToFile(data.randomBits);
      const tableRows = data.randomBits.map((num, index) => {
        const tableData1 = document.createElement("td");
        const tableData2 = document.createElement("td");
        const tableData3 = document.createElement("td");
        tableData1.textContent = index + 1;
        //console.log(num);
        numLineBreak = insertLineBreaks(num,64);
        //console.log(numLineBreak);
        tableData2.innerHTML = numLineBreak;
        //tableData2.textContent = numLineBreak;
        tableData2.style.fontFamily = "monospace";
        tableData2.style.whiteSpace = "pre-wrap";
        //tableData2.textContent = num;
        const button = document.createElement("button");
        button.textContent = "Copy";
        button.addEventListener("click", function () {
          copyRow(this.parentNode.parentNode);
        });
        tableData3.appendChild(button);
        const tableRow = document.createElement("tr");
        tableRow.appendChild(tableData1);
        tableRow.appendChild(tableData2);
        tableRow.appendChild(tableData3);
        return tableRow;
      });
      resultTable.innerHTML =
        "<tr><th>Nr.</th><th>Random Hex Values</th><th>Actions</th></tr>";
      tableRows.forEach((row) => resultTable.appendChild(row));
      button.disabled = false;
      hideSpinner();
    })
    .catch((error) => {
      button.disabled = false;
      hideSpinner();
      console.error(error);
    });

});

function copyRow(row) {
  const numberValue = row.querySelector("td:nth-child(2)").textContent;
  const stringWithoutLineBreaks = numberValue.replace(/\r?\n|\r/g, '');
  navigator.clipboard.writeText(stringWithoutLineBreaks);
}

function exportToFile(hexArray) {
  const arrayWithoutLineBreaks = hexArray.map(str => str.replace(/\r?\n|\r/g, ''));
  const fileContents = arrayWithoutLineBreaks.join('\n');

  const blob = new Blob([fileContents], { type: 'text/plain' });

  const button = document.getElementById('export-btn');
  button.disabled = false;
  button.textContent = 'Export Random Hex Values';
  button.onclick = () => {
    const link = document.createElement('a');
    link.download = "random_hex_values_" + getCurrentDate() + ".txt";
    link.href = window.URL.createObjectURL(blob);
    link.onclick = () => {
      setTimeout(() => {
        window.URL.revokeObjectURL(blob);
        link.remove();
      }, 0);
    };
    document.body.appendChild(link);
    link.click();
  };
}

function getCurrentDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();

  const formattedDateTime = `${year}_${month < 10 ? "0" : ""}${month}_${day < 10 ? "0" : ""
    }${day}_${hours < 10 ? "0" : ""}${hours}_${minutes < 10 ? "0" : ""
    }${minutes}_${seconds < 10 ? "0" : ""}${seconds}`;

  return formattedDateTime;
}

function showSpinner() {
  console.log("showSpinner");
  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "block";
}

function hideSpinner() {
  console.log("hideSpinner");
  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "none";
}

function resetTable() {
  var table = document.getElementById("result-table");
  var rowCount = table.rows.length;
  for (var i = rowCount - 1; i > 0; i--) {
    table.deleteRow(i);
  }
}

function insertLineBreaks(str, breakInterval) {
  var regex = new RegExp(`(.{${breakInterval}})`, 'g');
  return str.replace(regex, '$1\n');
}

function showTimeAlert(requiredBits) {
  
  var currentBits = 0;
  var remainderBits = 0;

  fetch("http://192.168.136.27:8080/trng/getCount")
      .then((response) => response.json())
      .then((data) => {
        currentBits = data;
        if (currentBits > requiredBits) {
          remainderBits = 0;
        } else {
          remainderBits = requiredBits - currentBits;
        }

        var seconds = remainderBits/2;
        var time = convertSecondsToTime(seconds);
        
        var description = "Bits currently stored: " + currentBits + "<br>Bits to be generated: " + remainderBits + "<br>Estimated time to wait: " + time + " (hh:mm:ss)";

        let alert = alertDiv;
        alert.innerHTML = description;
        alert.hidden = false;

        setTimeout(function() {
          alert.hidden = true;
        }, 10000);

       })
      .catch((error) => {
        console.error(error);
      });
}

function convertSecondsToTime(seconds) {
  var hours = Math.floor(seconds / 3600);
  var minutes = Math.floor((seconds % 3600) / 60);
  var remainingSeconds = seconds % 60;

  var timeString = padNumber(hours) + ":" + padNumber(minutes) + ":" + padNumber(remainingSeconds);
  return timeString;
}

function padNumber(number) {
  return number.toString().padStart(2, "0");
}

function toggleTheme() {
  const body = document.querySelector('body');
  const toggleBtn = document.querySelector('.toggle-btn');
  
  body.classList.toggle('dark');
  toggleBtn.classList.toggle('animate');
}