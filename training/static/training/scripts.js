document.addEventListener('DOMContentLoaded', () => {
    const sportSelect = document.getElementById('sport');
    const detailsDiv = document.getElementById('details');
    const fields = {
        running: ['time', 'distance'],
        swimming: ['time', 'pool_lengths'],
        pullups: ['sets', 'reps_per_set'],
        cycling: ['time', 'distance'],
        pushups: ['sets', 'reps_per_set'],
        weights: ['exercise_type', 'sets', 'reps_per_set']
    };

    function updateFields() {
        const selectedSport = sportSelect.value;

        // Hide all fields
        Array.from(detailsDiv.querySelectorAll('input')).forEach(input => {
            input.closest('label').style.display = 'none';
            input.value = '';
        });

        // Show relevant fields
        fields[selectedSport].forEach(field => {
            const input = document.getElementById(field);
            if (input) {
                input.closest('label').style.display = 'block';
            }
        });
    }

    sportSelect.addEventListener('change', updateFields);
    updateFields(); // Initialize fields
});
