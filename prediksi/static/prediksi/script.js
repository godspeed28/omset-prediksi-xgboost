      // Dark mode toggle
      const darkModeToggle = document.getElementById("darkModeToggle");
      const body = document.body;

      // Check for saved user preference
      if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
      }

      darkModeToggle.addEventListener("click", () => {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
          localStorage.setItem("darkMode", "enabled");
          darkModeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
        } else {
          localStorage.setItem("darkMode", "disabled");
          darkModeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
        }
      });

      // File upload handling
      const fileUploadArea = document.getElementById("fileUploadArea");
      const dataFileInput = document.getElementById("data_file");
      const selectFileBtn = document.getElementById("selectFileBtn");
      const fileNameDisplay = document.getElementById("fileNameDisplay");
      const fileName = document.getElementById("fileName");
      const removeFileBtn = document.getElementById("removeFileBtn");

      // Click on upload area triggers file input
      fileUploadArea.addEventListener("click", () => {
        dataFileInput.click();
      });

      // Select file button also triggers file input
      selectFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        dataFileInput.click();
      });

      // Handle file selection
      dataFileInput.addEventListener("change", () => {
        if (dataFileInput.files.length > 0) {
          fileName.textContent = dataFileInput.files[0].name;
          fileNameDisplay.classList.remove("d-none");
          fileUploadArea.style.display = "none";
        }
      });

      // Remove file
      removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        dataFileInput.value = "";
        fileNameDisplay.classList.add("d-none");
        fileUploadArea.style.display = "block";
      });

      // Drag and drop functionality
      fileUploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        fileUploadArea.classList.add("dragover");
      });

      fileUploadArea.addEventListener("dragleave", () => {
        fileUploadArea.classList.remove("dragover");
      });

      fileUploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        fileUploadArea.classList.remove("dragover");

        if (e.dataTransfer.files.length) {
          dataFileInput.files = e.dataTransfer.files;
          fileName.textContent = dataFileInput.files[0].name;
          fileNameDisplay.classList.remove("d-none");
          fileUploadArea.style.display = "none";
        }
      });

      // Form submission loading state
      const predictionForm = document.getElementById("predictionForm");
      const submitBtn = document.getElementById("submitBtn");

      if (predictionForm) {
        predictionForm.addEventListener("submit", () => {
          submitBtn.innerHTML =
            '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Memproses...';
          submitBtn.disabled = true;
        });
      }

      // Initialize modals
      document.addEventListener("DOMContentLoaded", function () {
        // Documentation modal
        const docModalBtn = document.getElementById("docModal");
        if (docModalBtn) {
          docModalBtn.addEventListener("click", function () {
            const docsModal = new bootstrap.Modal(
              document.getElementById("documentationModal")
            );
            docsModal.show();
          });
        }

        // Support modal
        const supportBtns = document.querySelectorAll(".btn-outline-info");
        supportBtns.forEach((btn) => {
          btn.addEventListener("click", function () {
            const supportModal = new bootstrap.Modal(
              document.getElementById("supportModal")
            );
            supportModal.show();
          });
        });
      });