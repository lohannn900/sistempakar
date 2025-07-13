const kategoriSelect = document.getElementById("kategori");
const pelakuBox = document.getElementById("pelakuBox");
const hasilDiv = document.getElementById("hasil");
const formMasalah = document.getElementById("formMasalah");

kategoriSelect.addEventListener("change", function () {
  const kategori = kategoriSelect.value;
  pelakuBox.innerHTML = "";
  hasilDiv.innerHTML = "";

  if (kategori && data[kategori]) {
    const keys = Object.keys(data[kategori]);
    const options = keys
      .map(p => `<option value="${p}">${p.replace(/([A-Z])/g, " $1").trim()}</option>`)
      .join("");
    pelakuBox.innerHTML = `
      <label for="pelaku">Pelaku:</label>
      <select id="pelaku" required>
        <option value="">-- pilih pelaku --</option>
        ${options}
      </select>
    `;

    // Reset hasil jika pelaku berubah
    document.getElementById("pelaku").addEventListener("change", () => {
      hasilDiv.innerHTML = "";
    });
  }
});

formMasalah.addEventListener("submit", function (e) {
  e.preventDefault();
  const kategori = kategoriSelect.value;
  const pelakuSelect = document.getElementById("pelaku");
  const pelaku = pelakuSelect ? pelakuSelect.value : "";

  if (!kategori || !pelaku) {
    hasilDiv.innerHTML = "<p class='error'>Lengkapi pilihan kategori dan pelaku!</p>";
    return;
  }

  hasilDiv.innerHTML = "<p>Sedang memproses...</p>";

  fetch("/cek_aturan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kategori, pelaku }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        hasilDiv.innerHTML = "<p class='error'>Aturan tidak ditemukan.</p>";
      } else {
        hasilDiv.innerHTML = `
          <h3>Hasil Aturan Adat</h3>
          <p><strong>Fakta / Kondisi:</strong> ${data.fakta}</p>
          <p><strong>Sanksi:</strong> ${data.sanksi}</p>
        `;
      }
    })
    .catch((err) => {
      hasilDiv.innerHTML = "<p class='error'>Terjadi kesalahan pada server.</p>";
      console.error(err);
    });
});
