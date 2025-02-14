let isSingleMode = false;
let isAgent = true;
const avgServer = document.getElementById('average_server');
const firstServer = document.getElementById('first_server');
const secondServer = document.getElementById('second_server');
let tempElement1 = document.querySelector('#temp_s1');
let humElement1 = document.querySelector('#hum_s1');
let heatElement1 = document.querySelector('#heat_s1');
let curElement1 = document.querySelector('#cur_s1');
let fanElement1 = document.querySelector('#fan_s1');
let optElement1 = document.querySelector('#opt_s1');
let tempElement2 = document.querySelector('#temp_s2');
let humElement2 = document.querySelector('#hum_s2');
let heatElement2 = document.querySelector('#heat_s2');
let curElement2 = document.querySelector('#cur_s2');
let fanElement2 = document.querySelector('#fan_s2');
let optElement2 = document.querySelector('#opt_s2');
let tempElement3 = document.querySelector('#temp_s3');
let humElement3 = document.querySelector('#hum_s3');
let heatElement3 = document.querySelector('#heat_s3');
let curElement3 = document.querySelector('#cur_s3');
let fanElement3 = document.querySelector('#fan_s3');
let optElement3 = document.querySelector('#opt_s3');
let dropIconElement1 = document.querySelector('#drop_icon_s1');
let dropIconElement2 = document.querySelector('#drop_icon_s2');
let dropIconElement3 = document.querySelector('#drop_icon_s3');
let fanIconElement1 = document.querySelector('#fan_icon_s1');
let fanIconElement2 = document.querySelector('#fan_icon_s2');
let fanIconElement3 = document.querySelector('#fan_icon_s3');
let warnIconElement1 = document.querySelector('#warn_icon_s1');
let warnIconElement2 = document.querySelector('#warn_icon_s2');
let warnIconElement3 = document.querySelector('#warn_icon_s3');

const sendButton = document.querySelector('.button_send');

const textElements = [
  document.getElementById('temp_p'),
  document.getElementById('hum_p'),
  document.getElementById('cur_p'),
  document.getElementById('heat_p'),
  document.getElementById('power_p'),
  document.getElementById('opt_hum_p'),
  document.getElementById('server_container_s1'),
  document.getElementById('temp_s1'),
  document.getElementById('hum_s1'),
  document.getElementById('heat_s1'),
  document.getElementById('cur_s1'),
  document.getElementById('fan_s1'),
  document.getElementById('opt_s1'),
  document.getElementById('server_container_s2'),
  document.getElementById('temp_s2'),
  document.getElementById('hum_s2'),
  document.getElementById('heat_s2'),
  document.getElementById('cur_s2'),
  document.getElementById('fan_s2'),
  document.getElementById('opt_s2'),
];

const inputElements = [
  document.getElementById('cur_s1'),
  document.getElementById('fan_s1'),
  document.getElementById('opt_s1'),
  document.getElementById('cur_s2'),
  document.getElementById('fan_s2'),
  document.getElementById('opt_s2'),
];

const textElementswS3 = [
  document.getElementById('server_container_s3'),
  document.getElementById('temp_s3'),
  document.getElementById('hum_s3'),
  document.getElementById('heat_s3'),
  document.getElementById('cur_s3'),
  document.getElementById('fan_s3'),
  document.getElementById('opt_s3'),
];

// const toggleButton = document.querySelector('.toggle-btn');

const toggleMode = function () {
  console.log(this, 'wefr');
  toggleButton.classList.toggle('active');

  if (isSingleMode) {
    // Switch to Dual Mode
    avgServer.classList.remove('visible');
    avgServer.classList.add('invisible');
    textElementswS3.forEach(text => text.classList.remove('visible'));
    textElementswS3.forEach(text => text.classList.add('invisible'));
    setTimeout(() => {
      avgServer.style.display = 'none';
      textElementswS3.forEach(text => (text.style.display = 'none'));
      firstServer.style.display = 'flex';
      secondServer.style.display = 'flex';
      textElements.forEach(text => (text.style.display = 'block'));
      firstServer.classList.remove('invisible');
      secondServer.classList.remove('invisible');
      textElements.forEach(text => text.classList.remove('invisible'));
      textElements.forEach(text => text.classList.add('visible'));
      firstServer.classList.add('visible');
      secondServer.classList.add('visible');
    }, 1000);
  } else {
    // Switch to Single Mode
    firstServer.classList.remove('visible');
    secondServer.classList.remove('visible');
    textElements.forEach(text => text.classList.remove('visible'));
    textElements.forEach(text => text.classList.add('invisible'));
    firstServer.classList.add('invisible');
    secondServer.classList.add('invisible');

    setTimeout(() => {
      firstServer.style.display = 'none';
      secondServer.style.display = 'none';
      textElements.forEach(text => (text.style.display = 'none'));
      avgServer.style.display = 'flex';
      avgServer.classList.remove('invisible');
      avgServer.classList.add('visible');
      textElementswS3.forEach(text => (text.style.display = 'block'));
      textElementswS3.forEach(text => text.classList.remove('invisible'));
      textElementswS3.forEach(text => text.classList.add('visible'));
    }, 1000);
  }

  isSingleMode = !isSingleMode;
};

const toggleButton = document.querySelector('.toggle-btn');
toggleButton.addEventListener('click', toggleMode);

toggleButton.addEventListener('click', function () {
  console.log(this);
  // this.classList.toggle('active'); // Toggles active state
});

function showOrHide() {
  const sendButton = document.querySelector('.button_send');

  if (!isAgent) {
    console.log(
      'Switching to Manual Mode - Hiding Toggle, Showing Send Button'
    );

    toggleButton.classList.add('hidden'); // Hide Toggle Button
    sendButton.classList.remove('hidden'); // Show Send Button
  } else {
    console.log('Switching to Agent Mode - Showing Toggle, Hiding Send Button');

    toggleButton.classList.remove('hidden'); // Show Toggle Button
    sendButton.classList.add('hidden'); // Hide Send Button
  }
}

const modeSwitch = document.getElementById('modeSwitch');

modeSwitch.addEventListener('click', function () {
  this.classList.toggle('active');
  isAgent = !isAgent;
  console.log(isAgent, isSingleMode);

  if (!isAgent && isSingleMode) {
    toggleMode(); // Ensure Single Mode is turned off in Manual Mode
  }

  console.log('Agent-Manual Toggle');
  showOrHide();

  if (!isAgent) {
    inputElements.forEach(ele => ele.removeAttribute('disabled'));
  } else {
    inputElements.forEach(ele => ele.setAttribute('disabled', 'true'));
  }
});

const text = document.getElementById('ai_text');
text.innerHTML = text.innerHTML = `
- <b>Previous State:</b>
  <ul>
    <li>DataCube1: Temperature = 24.49°C, Humidity = 55.39%RH</li>
    <li>DataCube2: Temperature = 24.49°C, Humidity = 54.39%RH</li>
  </ul>
- <b>Current State:</b>
  <ul>
    <li>DataCube1: Temperature = 24.44°C, Humidity = 55.34%RH</li>
    <li>DataCube2: Temperature = 24.44°C, Humidity = 54.34%RH</li>
  </ul>
<h3>Heat Calculation</h3>
Using the formula:
<b>Q = m ⋅ c ⋅ ΔT</b><br>
Where:
<ul>
  <li><b>m</b> = 30 grams</li>
  <li><b>c</b> = 0.0012 J/g°C</li>
  <li><b>ΔT</b> = current temperature - previous temperature</li>
</ul>

<h3>Calculations</h3>
<b>1. DataCube1:</b><br>
<ul>
  <li>Previous Temperature: 24.49°C</li>
  <li>Current Temperature: 24.44°C</li>
  <li>ΔT = 24.44 - 24.49 = <b>-0.05°C</b></li>
  <li>Heat (Q1) = 30 × 0.0012 × (-0.05) = <b>-0.0018 J</b> (indicating cooling)</li>
</ul>

<b>2. DataCube2:</b><br>
<ul>
  <li>Previous Temperature: 24.49°C</li>
  <li>Current Temperature: 24.44°C</li>
  <li>ΔT = 24.44 - 24.49 = <b>-0.05°C</b></li>
  <li>Heat (Q2) = 30 × 0.0012 × (-0.05) = <b>-0.0018 J</b> (indicating cooling)</li>
</ul>

<h3>Fan Speed and Humidity Settings</h3>
<ul>
  <li><b>Fan Speed:</b> Since the temperatures are well below the threshold of 40°C, we can set the fan speeds to a moderate level.</li>
  <li><b>Humidity:</b> The humidity levels are within acceptable ranges, but we can slightly adjust them for optimal performance.</li>
</ul>

<h3>Suggested Settings:</h3>
<b>DataCube1:</b>
<ul>
  <li>Fan Speed: 100</li>
  <li>Humidity: 55%RH</li>
  <li>Suggestion: <b>Optimal cooling for DataCube1</b></li>
</ul>

<b>DataCube2:</b>
<ul>
  <li>Fan Speed: 100</li>
  <li>Humidity: 54%RH</li>
  <li>Suggestion: <b>Optimal cooling for DataCube2</b></li>
</ul>

<h3>Final Output (JSON)</h3>
<pre>
[
  [100, 55, -0.0018, [24.44, 55.34], "AI Suggestion: Optimal cooling for DataCube1"],
  [100, 54, -0.0018, [24.44, 54.34], "AI Suggestion: Optimal cooling for DataCube2"]
]
</pre>
`;

const calculate = function (a, b) {
  let min, max;
  if (a < b) {
    min = a;
    max = b;
  } else {
    min = b;
    max = a;
  }
  if (max > 1.1 * min) {
    return max;
  } else {
    return (max + min) / 2;
  }
};

const abs = function (a) {
  if (a > 0) return a;
  else return -1 * a;
};

const displayIcon = function (temp1, temp2, temp3) {
  if (temp1 > 24) {
    warnIconElement1.style.display = 'flex';
    fanIconElement1.style.display = 'none';
    dropIconElement1.style.display = 'none';
  } else if (temp1 > 22) {
    warnIconElement1.style.display = 'none';
    dropIconElement1.style.display = 'flex';
    fanIconElement1.style.display = 'none';
  } else {
    warnIconElement1.style.display = 'none';
    dropIconElement1.style.display = 'none';
    fanIconElement1.style.display = 'flex';
  }
  if (temp2 > 28) {
    warnIconElement2.style.display = 'flex';
    fanIconElement2.style.display = 'none';
    dropIconElement2.style.display = 'none';
  } else if (temp2 > 25) {
    warnIconElement2.style.display = 'none';
    dropIconElemen2.style.display = 'flex';
    fanIconElement2.style.display = 'none';
  } else {
    warnIconElement2.style.display = 'none';
    dropIconElement2.style.display = 'none';
    fanIconElement2.style.display = 'flex';
  }
  if (temp3 > 28) {
    warnIconElement3.style.display = 'flex';
    fanIconElement3.style.display = 'none';
    dropIconElement3.style.display = 'none';
  } else if (temp3 > 25) {
    warnIconElement3.style.display = 'none';
    dropIconElemen3.style.display = 'flex';
    fanIconElement3.style.display = 'none';
  } else {
    warnIconElement3.style.display = 'none';
    dropIconElement3.style.display = 'none';
    fanIconElement3.style.display = 'flex';
  }
};

const displayIcon2 = function (temp1, temp2) {
  if (temp1 > 28) {
    warnIconElement1.style.display = 'flex';
    fanIconElement1.style.display = 'none';
    dropIconElement1.style.display = 'none';
  } else if (temp1 > 25) {
    warnIconElement1.style.display = 'none';
    dropIconElement1.style.display = 'flex';
    fanIconElement1.style.display = 'none';
  } else {
    warnIconElement1.style.display = 'none';
    dropIconElement1.style.display = 'none';
    fanIconElement1.style.display = 'flex';
  }
  if (temp2 > 28) {
    warnIconElement2.style.display = 'flex';
    fanIconElement2.style.display = 'none';
    dropIconElement2.style.display = 'none';
  } else if (temp2 > 25) {
    warnIconElement2.style.display = 'none';
    dropIconElemen2.style.display = 'flex';
    fanIconElement2.style.display = 'none';
  } else {
    warnIconElement2.style.display = 'none';
    dropIconElement2.style.display = 'none';
    fanIconElement2.style.display = 'flex';
  }
};

async function fetchDataAgent() {
    fetch("http://127.0.0.1:5002/receive_ai_response")
  .then(response => response.text())  // Get raw text
  .then(function(text) {

    // console.log(typeof(text));

    let x = text.split("### Final Output")[1]?.trim()?.replace("json\n", "")?.trim();
    let y=x.split(',');
    console.log(y);
    

// Extract values for DataCube1
let fan_speed1 =  (parseFloat(y[0].split('[')[2])*3400)/255;
let op_hum1 = parseFloat(y[1].trim());
let delta_h1 = parseFloat(y[2].trim());
let temp1 = parseFloat(y[3].split('[')[1]);
let hum1 = parseFloat(y[4].split(']')[0].trim());

// Extract values for DataCube2
let fan_speed2 = (parseFloat(y[6].split('[')[1])*3400)/255;
let op_hum2 =  parseFloat(y[7].trim());
let delta_h2 =  parseFloat(y[8].trim());
let temp2 = parseFloat(y[9].split('[')[1]);
let hum2 =  parseFloat(y[10].split(']')[0].trim());

// Print the extracted values
console.log(`temp1=${temp1}, hum1=${hum1}, fan_speed1=${fan_speed1}, op_hum1=${op_hum1}, delta_h1=${delta_h1}`);
console.log(`temp2=${temp2}, hum2=${hum2}, fan_speed2=${fan_speed2}, op_hum2=${op_hum2}, delta_h2=${delta_h2}`);


      tempElement1.textContent = temp1+" °C";
      humElement1.textContent = hum1+" %RH";
      heatElement1.innerHTML = `&Delta;H1: ${delta_h1}`+" J/g°C";
      fanElement1.value = fan_speed1.toFixed(2)+" rpm";
      optElement1.value = op_hum1+" %RH";

      // Extract values for DataCube2
      // let fan_speed2 = jsonData[1][0];
      // let op_hum2 = jsonData[1][1];
      // let delta_h2 = jsonData[1][2];
      // let temp2 = jsonData[1][3][0];
      // let hum2 = jsonData[1][3][1];

      tempElement2.textContent = temp2+" °C";
      humElement2.textContent = hum2+" %RH";
      heatElement2.innerHTML = `&Delta;H1: ${delta_h2}`+" J/g°C";
      fanElement2.value = fan_speed2.toFixed(2)+" rpm";
      optElement2.value = op_hum2+" %RH";

      let temp3 = calculate(temp1, temp2);

      tempElement3.textContent = calculate(temp1, temp2)+" °C";
      humElement3.textContent = calculate(hum1, hum2)+" %RH";
      heatElement3.innerHTML = `&Delta;H: ${delta_h1 + delta_h2}`+" J/g°C";
      fanElement3.innerHTML = calculate(fan_speed1, fan_speed2).toFixed(2)+" rpm";
      optElement3.innerHTML = calculate(op_hum1, op_hum2)+" %RH";

      displayIcon(temp1,temp2,temp3);

    //   console.log(
    //     `temp1=${temp1}, hum1=${hum1}, delta_h1=${delta_h1}, op_hum1=${op_hum1}, fan_speed1=${fan_speed1}`
    //   );
    //   console.log(
    //     `temp2=${temp2}, hum2=${hum2}, delta_h2=${delta_h2}, op_hum2=${op_hum2}, fan_speed2=${fan_speed2}`
    //   );

    // // console.log('Agent A Data:', data);
  } 


  );

    
}

async function fetchDataManual() {
  try {
    let response = await fetch('http://127.0.0.1:5000/process_data');
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    // Given response object
    // let response = {
    //   sensor_data: [
    //     [
    //       { 'temperature1.1': 23.0, 'humidity1.1': 60.0 },
    //       { 'temperature2.1': 26.2, 'humidity2.1': 47.0 },
    //     ],
    //     [
    //       { 'temperature1.2': 23.0, 'humidity1.2': 60.0 },
    //       { 'temperature2.2': 26.2, 'humidity2.2': 47.0 },
    //     ],
    //     [{ current1: -4.94 }, { current2: -4.73 }],
    //   ],
    // };

    // Extract and rename values
    let temp11 = response.sensor_data[0][0]['temperature1.1'];
    let temp12 = response.sensor_data[1][0]['temperature1.2'];
    let hum1 = response.sensor_data[1][0]['humidity1.2'];
    let curr1 = response.sensor_data[2][0]['current1'];

    let temp21 = response.sensor_data[0][1]['temperature2.1'];
    let temp22 = response.sensor_data[1][1]['temperature2.2'];
    let hum2 = response.sensor_data[1][1]['humidity2.2'];
    let curr2 = response.sensor_data[2][1]['current2'];

    let delta_h1 = 30 * 0.0012 * (temp12 - temp11);
    let delta_h2 = 30 * 0.0012 * (temp22 - temp21);

    tempElement1.textContent = temp12;
    humElement1.textContent = hum1;
    heatElement1.innerHTML = `&Delta;H1: ${delta_h1}`;
    curElement1.innerHTML = curr1;

    tempElement2.textContent = temp22;
    humElement2.textContent = hum2;
    heatElement2.innerHTML = `&Delta;H1: ${delta_h2}`;
    curElement2.innerHTML = curr2;

    displayIcon2(temp12,temp22);

    // Output the extracted values
    console.log(`temp1 = ${temp12}, hum1 = ${hum1}, curr1 = ${curr1}`);
    console.log(`temp2 = ${temp22}, hum2 = ${hum2}, curr2 = ${curr2}`);

    // console.log('Agent B Data:', response);
  } catch (error) {
    console.error('Error fetching Agent B data:', error);
  }
}

async function fetchDataCurrent() {
  try {
    // let response = await fetch('http://127.0.0.1:5000/process_data');
    // if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    // Given response object
    let response = {
      sensor_data: [
        [
          { 'temperature1.1': 23.0, 'humidity1.1': 60.0 },
          { 'temperature2.1': 26.2, 'humidity2.1': 47.0 },
        ],
        [
          { 'temperature1.2': 23.0, 'humidity1.2': 60.0 },
          { 'temperature2.2': 26.2, 'humidity2.2': 47.0 },
        ],
        [{ current1: -4.94 }, { current2: -4.73 }],
      ],
    };

    // Extracting values
    let curr1 = response.sensor_data[2][0]['current1'];
    let curr2 = response.sensor_data[2][1]['current2'];

    curElement1.innerHTML = abs(curr1) / 2;
    curElement2.innerHTML = abs(curr2) / 2;
    curElement3.innerHTML = calculate(abs(curr1) / 2, abs(curr2) / 2).toFixed(2);

    console.log(`curr1=${curr1}, curr2=${curr2}`);

    console.log('Agent B Data:', response);
  } catch (error) {
    console.error('Error fetching Agent B data:', error);
  }
}

sendButton.addEventListener('click', function () {
  let x = [
    fanElement1.value,
    optElement1.value,
    fanElement2.value,
    optElement2.value,
  ];
  console.log(x);
  fetch("https://example.com/api/data", {  // Replace with actual API URL
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: x }),  // Sending x wrapped inside an object
})
.then(response => response.json())  // Convert response to JSON
.then(data => console.log("Success:", data))  // Log successful response
.catch(error => console.error("Error:", error));
});

// const fetchData=function(){
//   fetch("http://127.0.0.1:5002/receive_ai_response")
//   .then(response => response.text())  // Get raw text
//   .then(text => {
//       console.log("Raw Response Text:", text);
//       return JSON.parse(text);  // Manually parse JSON
//   })
//   .then(data => console.log("Parsed Data:", data))
//   .catch(error => console.error("Error fetching AI response:", error));
// }

// Function that checks `isAgent` every 5 seconds and calls the correct function
function checkAndFetch() {
  if (isAgent) {
    // fetchData()
    fetchDataAgent();
    fetchDataCurrent();
  } else {
    fetchDataManual();
  }

  setTimeout(checkAndFetch, 5000); // Run the check again after 1 seconds
}

// Start the process
checkAndFetch();


const analyticsButton = document.querySelector('.analytics');

function openNewWindow() {
  window.open('http://127.0.0.1:8050/', '_blank');
}

analyticsButton.addEventListener('click', openNewWindow);