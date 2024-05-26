document.getElementById('roomFinderForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    fetch(`/room_finder/search?date=${date}&time=${time}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No available rooms found.</p>';
            } else {
                const ul = document.createElement('ul');
                data.forEach(room => {
                    const li = document.createElement('li');
                    li.textContent = room.name;
                    ul.appendChild(li);
                });
                resultsDiv.appendChild(ul);
            }
        })
        .catch(error => console.error('Error fetching rooms:', error));
});
