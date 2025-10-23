const albumBtn = document.getElementById("albumBtn");
const artistBtn = document.getElementById("artistBtn");
const rangeButtons = document.getElementById("range-buttons");
const sortOptions = document.getElementById("sort-options");
const resultsDiv = document.getElementById("results");

let currentView = null;
let currentUser = "badbunny"; // test user
let currentSort = "total";

albumBtn.addEventListener("click", () => {
  currentView = "albums";
  rangeButtons.hidden = false;
  sortOptions.hidden = false;
  resultsDiv.hidden = true;
});

artistBtn.addEventListener("click", () => {
  currentView = "artists";
  rangeButtons.hidden = false;
  sortOptions.hidden = false;
  resultsDiv.hidden = true;
});

document.querySelectorAll('input[name="sort"]').forEach((radio) => {
  radio.addEventListener("change", (e) => {
    currentSort = e.target.value;
    console.log("Sort changed to:", currentSort);
  });
});

document.querySelectorAll(".range-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const limit = btn.dataset.range === "all" ? 9999 : btn.dataset.range;
    const url = `http://localhost:5000/api/stats?view=${currentView}&limit=${limit}&user=${currentUser}&sort=${currentSort}`;
    console.log("Fetching:", url);

    try {
      const res = await fetch(url);
      const data = await res.json();
      renderResults(data, currentView);
    } catch (err) {
      console.error("Error fetching data:", err);
      resultsDiv.innerHTML = `<p>Error loading data. Check console for details.</p>`;
      resultsDiv.hidden = false;
    }
  });
});

function renderResults(data, view) {
  resultsDiv.hidden = false;

  if (!data || data.length === 0) {
    resultsDiv.innerHTML = `<p>No data found for this user/view.</p>`;
    return;
  }

  let html = `<table border="1" cellspacing="0" cellpadding="6" style="width:100%;border-collapse:collapse;">
      <thead style="background:#f0f0f0;">
        <tr>`;

  if (view === "albums") {
    html += `<th>#</th><th>Album</th><th>Artist</th><th>Liked</th><th>Total</th><th>%</th>`;
  } else {
    html += `<th>#</th><th>Artist</th><th>Liked</th><th>Total</th><th>%</th>`;
  }

  html += `</tr></thead><tbody>`;

  for (const row of data) {
    if (view === "albums") {
      html += `
        <tr>
          <td>${row.rank}</td>
          <td>${row.album}</td>
          <td>${row.artist}</td>
          <td>${row.liked}</td>
          <td>${row.total}</td>
          <td>${row.percent}%</td>
        </tr>`;
    } else {
      html += `
        <tr>
          <td>${row.rank}</td>
          <td>${row.artist}</td>
          <td>${row.liked}</td>
          <td>${row.total}</td>
          <td>${row.percent}%</td>
        </tr>`;
    }
  }

  html += `</tbody></table>`;
  resultsDiv.innerHTML = html;
}
