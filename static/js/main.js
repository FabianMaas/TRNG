// Get references to HTML elements
const startStopBtn = document.getElementById("startStopBtn");
const generateBtn = document.getElementById("generate-btn");
const quantityInput = document.getElementById("quantity-input");
const numBitsInput = document.getElementById("numBits-input");
const resultTable = document.getElementById("result-table");
const estimatedWaitTimeAlert = document.getElementById("estimatedWaitTimeAlert");
const inputErrorAlert = document.getElementById("inputErrorAlert");
const github_icon = document.getElementById("github-icon");
const ipAddress = "172.16.78.61" // IP address for communication with rest api
const protocol = "https" // Defines if HTTP or HTTPS is used
let isRunning = false;


// Event listener for the start/stopp button
startStopBtn.addEventListener("click", () => {
  if (!isRunning) {
    // Initialize the TRNG
    fetch(`${protocol}://${ipAddress}:8080/trng/randomNum/init`)
      .then((response) => {
        console.log("Started");
        // Enable generate button and show canvas
        const button = document.getElementById('generate-btn');
        button.disabled = false;
        const canvas = document.getElementById('canvas');
        canvas.hidden = false;
        // Update toggle button appearance and state
        startStopBtn.textContent = "Stop";
        startStopBtn.classList.add("stop");
        startStopBtn.style.backgroundColor = "red";
        isRunning = true;
      })
      .catch((error) => {
        console.error("Error starting:", error);
      });
  } else {
    // Shutdown the TRNG
    fetch(`${protocol}://${ipAddress}:8080/trng/randomNum/shutdown`)
      .then((response) => {
        console.log("Stopped");
        hideSpinner();
        resetTable();
        // Disable generate and export buttons, reset input values, hide canvas
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
        // Hide alerts and update toggle button appearance and state
        let alert = estimatedWaitTimeAlert;
        alert.hidden = true;
        startStopBtn.textContent = "Start";
        startStopBtn.classList.remove("stop");
        startStopBtn.style.backgroundColor = "green";
        isRunning = false;
      })
      .catch((error) => {
        console.error("Error stopping:", error);
      });
  }
});


// Event listener for the generate button
generateBtn.addEventListener("click", () => {
  const quantity = quantityInput.value;
  const numBits = numBitsInput.value;
  const url = `${protocol}://${ipAddress}:8080/trng/randomNum/getRandom?quantity=${quantity}&numBits=${numBits}`;
  
  if(quantity < 1 || numBits < 1){
    showInfoAlert();
    return;
  }

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
      exportToFile(data.randomBits);
      // Generate table rows for random hex values
      const tableRows = data.randomBits.map((num, index) => {
        const tableData1 = document.createElement("td");
        const tableData2 = document.createElement("td");
        const tableData3 = document.createElement("td");
        tableData1.textContent = index + 1;
        numLineBreak = insertLineBreaks(num,64);
        tableData2.innerHTML = numLineBreak;
        tableData2.style.fontFamily = "monospace";
        tableData2.style.whiteSpace = "pre-wrap";
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
      // Add table rows to the result table
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


// Copy a row to the clipboard
function copyRow(row) {
  const numberValue = row.querySelector("td:nth-child(2)").textContent;
  const stringWithoutLineBreaks = numberValue.replace(/\r?\n|\r/g, '');
  navigator.clipboard.writeText(stringWithoutLineBreaks);
}


// Export hex values to a text file
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


// Get the current date and time as a formatted string
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


// Show the loading spinner
function showSpinner() {
  console.log("showSpinner");
  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "block";
}


// Hide the loading spinner
function hideSpinner() {
  console.log("hideSpinner");
  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "none";
}


// Reset the result table
function resetTable() {
  var table = document.getElementById("result-table");
  var rowCount = table.rows.length;
  for (var i = rowCount - 1; i > 0; i--) {
    table.deleteRow(i);
  }
}


// Insert line breaks in a string at a specified interval
function insertLineBreaks(str, breakInterval) {
  var regex = new RegExp(`(.{${breakInterval}})`, 'g');
  return str.replace(regex, '$1\n');
}


// Show an alert with the estimated time to wait based on the number of required bits
function showTimeAlert(requiredBits) {
  
  var currentBits = 0;
  var remainderBits = 0;

  // Fetch the current count of generated bits
  fetch(`${protocol}://${ipAddress}:8080/trng/getCount`)
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

        let alert = estimatedWaitTimeAlert;
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


// Convert seconds to a time string (hh:mm:ss)
function convertSecondsToTime(seconds) {
  var hours = Math.floor(seconds / 3600);
  var minutes = Math.floor((seconds % 3600) / 60);
  var remainingSeconds = seconds % 60;

  var timeString = padNumber(hours) + ":" + padNumber(minutes) + ":" + padNumber(remainingSeconds);
  return timeString;
}


// Pad a number with leading zeros if necessary
function padNumber(number) {
  return number.toString().padStart(2, "0");
}


// Show an information alert for invalid input
function showInfoAlert(){
  const quantity = quantityInput.value;
  const numBits = numBitsInput.value;
  let description = "";
  if (quantity < 1 && numBits >= 1){
    description = "quantity must be at least 1";
    quantityInput.value = 1;
  }
  if (quantity >= 1 && numBits < 1){
    description = "numBits must be at least 1";
    numBitsInput.value = 1;
  }
  if(quantity < 1 && numBits < 1){
    description = "quantity and numBits must be at least 1";
    quantityInput.value = 1;
    numBitsInput.value = 1;
  }

  let alert = inputErrorAlert;
  alert.innerHTML = description;
  alert.hidden = false;
  setTimeout(function() {
    alert.hidden = true;
  }, 3000);
}


// Toggle between light and dark theme
function toggleTheme() {
  const body = document.querySelector('body');
  const startStopBtn = document.querySelector('.toggle-btn');
  
  body.classList.toggle('dark');
  startStopBtn.classList.toggle('animate');

  if (document.body.classList.contains('dark')) {
    console.log('Die Klasse "dark" ist gesetzt.');
    github_icon.src = 'static/img/github-mark-white.png';
    setThemePreference('dark')
  } else {
    console.log('Die Klasse "dark" ist nicht gesetzt.');
    github_icon.src = 'static/img/github-mark.png';
    setThemePreference('light')
  }
}


// Set the theme preference in a cookie
function setThemePreference(theme) {
  document.cookie = `themePreference=${theme}; expires=${new Date(Date.now() + 31536000000).toUTCString()}; path=/; SameSite=Strict`;
}


// Check if the theme preference cookie exists and apply the theme
function getThemePreference() {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith('themePreference=')) {
      const theme = cookie.substring('themePreference='.length);
      return theme;
    }
  }
  return 'light';
}


// Event listener that listens for the 'DOMContentLoaded' event, 
// which is triggered when the initial HTML document has been completely loaded and parsed.
document.addEventListener('DOMContentLoaded', function() {
  const body = document.querySelector('body');
  const startStopBtn = document.querySelector('.toggle-btn');
  const savedTheme = getThemePreference();
  if (savedTheme === 'dark') {
    body.classList.toggle('dark');
    startStopBtn.classList.toggle('animate');
    github_icon.src = 'static/img/github-mark-white.png';
  } else {

  }
});