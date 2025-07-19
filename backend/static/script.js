console.log("script loaded");

const startTime = Date.now();
let mouseMoves = [];
let clicks = [];
let scrolls = [];

document.addEventListener("mousemove", e => {
  mouseMoves.push({ x: e.clientX, y: e.clientY, t: Date.now() });
});
document.addEventListener("click", e => {
  clicks.push({ x: e.clientX, y: e.clientY, t: Date.now() });
});
document.addEventListener("scroll", () => {
  scrolls.push({ scrollY: window.scrollY, t: Date.now() });
});

window.addEventListener("beforeunload", () => {
  const endTime = Date.now();
  const timeOnPage = (endTime - startTime) / 1000;

  const data = {
    userAgent: navigator.userAgent,
    language: navigator.language,
    screenWidth: screen.width,
    screenHeight: screen.height,
    timeOnPage,
    mouseMoves,
    clicks,
    scrolls
  };

  navigator.sendBeacon("/submit-data", JSON.stringify(data));
});

async function submitForm() {
  const name = document.getElementById("name").value.trim();
  const aadhaar = document.getElementById("aadhaar").value.trim();
  const resultEl = document.getElementById("result");

  if (!/^\d{12}$/.test(aadhaar)) {
    resultEl.textContent = "❌ Please enter a valid 12-digit Aadhaar number.";
    return;
  }

  const endTime = Date.now();
  const timeOnPage = (endTime - startTime) / 1000;

  const payload = {
    userAgent: navigator.userAgent,
    language: navigator.language,
    screenWidth: screen.width,
    screenHeight: screen.height,
    timeOnPage,
    mouseMoves,
    clicks,
    scrolls
  };

  try {
    const res = await fetch("/submit-data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const json = await res.json();

    if (json.prediction === "human") {
      resultEl.textContent = `✅ Verified as Human. Welcome, ${name || "User"}!`;
    } else {
      resultEl.textContent = "⚠️ Bot-like behavior detected. Submission blocked.";
    }
  } catch (err) {
    resultEl.textContent = "❌ Error occurred during verification.";
    console.error(err);
  }
}


// Fetch stats and render bar chart
fetch("/stats")
    .then(res => res.json())
    .then(data => {
        const ctx = document.getElementById("barChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Human", "Bot"],
                datasets: [{
                    label: "Prediction Count",
                    data: [data.human, data.bot],
                    backgroundColor: ["#007bff", "#dc3545"]
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    })
    .catch(err => console.error("Failed to load stats", err));
