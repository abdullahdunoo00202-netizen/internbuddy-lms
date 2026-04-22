document.querySelectorAll(".upload-form").forEach(form => {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const res = await fetch("/lms/submit-task", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (data.message) {
                // ✅ SUCCESS → reload page
                window.location.reload();
            } else {
                alert(data.error || "Upload failed");
            }

        } catch (err) {
            alert("Server error");
        }
    });
});