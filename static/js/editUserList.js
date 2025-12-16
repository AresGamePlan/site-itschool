document.querySelectorAll(".watch-form").forEach(form => {
    const saveBtn = form.querySelector(".save-btn");

    // сохраняем исходные значения для конкретной формы
    form.querySelectorAll("input, select, textarea").forEach(input => {
        input.dataset.initial = input.value;
    });

    // проверяем изменения только внутри этой формы
    function checkChanges() {
        let changed = false;

        form.querySelectorAll("input, select, textarea").forEach(input => {
            if (input.value !== input.dataset.initial) {
                changed = true;
            }
        });

        saveBtn.style.display = changed ? "inline-block" : "none";
    }

    form.addEventListener("input", () => {
        checkChanges();
    });
});