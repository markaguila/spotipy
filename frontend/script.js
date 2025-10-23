// --- State ---
const state = {
  view: null // "albums" or "artists"
};

// --- Element references ---
const albumBtn = document.getElementById("albumBtn");
const artistBtn = document.getElementById("artistBtn");
const panel = document.getElementById("panel");
const rangeButtons = document.getElementById("range-buttons");
const resultsDiv = document.getElementById("results");

// --- View selection ---
albumBtn.addEventListener("click", () => {
  state.view = "albums";
  renderAnalysisView();
});

artistBtn.addEventListener("click", () => {
  state.view = "artists";
  renderAnalysisView();
});

// --- Render analysis view ---
function renderAnalysisView() {
  // Show the panel area
  panel.removeAttribute("hidden");

  // Update heading
  panel.querySelector(".results").innerHTML = "";
  rangeButtons.hidden = false;
  resultsDiv.hidden = false;

  // Set ARIA labels for accessibility
  albumBtn.setAttribute("aria-selected", state.view === "albums");
  artistBtn.setAttribute("aria-selected", state.view === "artists");

  // Update the panel title text visually
  document.getElementById("panel-title").textContent =
    state.view === "albums" ? "Album Analysis" : "Artist Analysis";
}

// --- Handle range button clicks ---
rangeButtons.addEventListener("click", (e) => {
  if (!e.target.classList.contains("range-btn")) return;
  let limit = e.target.dataset.range;
  if (limit === "all") limit = 1000;
  fetchAndRenderData(state.view, limit);
});


// --- Fetch data from backend ---
function fetchAndRenderData(view, limit) {
  resultsDiv.innerHTML = "<p>Loading data...</p>";

  // Use full backend URL if serving frontend on a different port
  fetch(`http://localhost:5000/api/stats?view=${view}&limit=${limit}`)
    .then((response) => {
      if (!response.ok) throw new Error("Failed to fetch data");
      return response.json();
    })
    .then((data) => {
      console.log("Fetched data:", data);

      renderResults(view, data);
    })
    .catch((err) => {
      console.error("Error fetching data:", err);
      resultsDiv.innerHTML = "<p>Error loading data. Check console for details.</p>";
    });
}

function renderResults(view, data) {
  const resultsDiv = document.getElementById("results");

  // Make sure it's visible
  resultsDiv.removeAttribute("hidden");
  resultsDiv.style.display = "block";

  // Safety check
  if (!data || data.length === 0) {
    resultsDiv.innerHTML = "<p>No data available.</p>";
    return;
  }

  console.log("Rendering", data.length, "rows for", view);

  // Define table headers
  const headers =
    view === "albums"
      ? "<th>#</th><th>Album</th><th>Artist</th><th>Total Tracks</th>"
      : "<th>#</th><th>Artist</th><th>Total Tracks</th>";

  // Build rows dynamically
  const rows = data
    .map((item) => {
      if (view === "albums") {
        return `
          <tr>
            <td>${item.rank}</td>
            <td>${item.album}</td>
            <td>${item.artist}</td>
            <td>${item.total}</td>
          </tr>
        `;
      } else {
        return `
          <tr>
            <td>${item.rank}</td>
            <td>${item.artist}</td>
            <td>${item.total}</td>
          </tr>
        `;
      }
    })
    .join("");

  // Build full table markup
  const tableHTML = `
    <table border="1" cellspacing="0" cellpadding="6" style="width: 100%; border-collapse: collapse;">
      <thead style="background: #f0f0f0;">
        <tr>${headers}</tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;

  // Inject into DOM
  resultsDiv.innerHTML = tableHTML;
}
