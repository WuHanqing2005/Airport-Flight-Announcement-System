$(document).ready(function() {
    // --- INITIALIZATION ---
    // Safely parse initial data passed from the server-side template
    const initialData = JSON.parse(document.getElementById('initial-data').textContent || '[]');
    // Initialize Socket.IO connection
    const socket = io();
    // Initialize Bootstrap modals for later use
    const flightModal = new bootstrap.Modal(document.getElementById('flightModal'));
    const announcementModal = new bootstrap.Modal(document.getElementById('announcementModal'));
    const playOldModal = new bootstrap.Modal(document.getElementById('playOldModal'));
    // Variable to keep track of the currently selected table row
    let selectedRow = null;

    // --- HELPER FUNCTIONS ---

    /**
     * Shows a dynamic toast notification on the screen.
     * @param {string} message The message to display inside the toast.
     * @param {string} type The type of toast: 'success', 'danger', 'warning', or 'info'. This controls the color and icon.
     */
    function showToast(message, type = 'info') {
        const toastId = 'toast-' + Date.now();
        const iconMap = {
            success: 'check-circle-fill',
            danger: 'exclamation-triangle-fill',
            warning: 'exclamation-triangle-fill',
            info: 'info-circle-fill'
        };
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white border-0 bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="bi bi-${iconMap[type]} me-2"></i>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>`;
        $('#toast-container').append(toastHtml);
        const toastEl = new bootstrap.Toast(document.getElementById(toastId), { delay: 5000 });
        toastEl.show();
        // Self-destruct the toast element from the DOM after it's hidden to prevent clutter
        $(`#${toastId}`).on('hidden.bs.toast', function() {
            $(this).remove();
        });
    }

    /**
     * A generic wrapper for making API calls to the backend using fetch.
     * @param {string} endpoint The API endpoint to target (e.g., '/api/flights').
     * @param {string} method The HTTP method ('POST', 'PUT', 'DELETE', etc.).
     * @param {object|null} body The JSON payload for the request.
     * @returns {Promise<object|null>} The JSON response from the server, or null if an error occurred.
     */
    async function apiCall(endpoint, method = 'POST', body = null) {
        try {
            const options = {
                method: method,
                headers: { 'Content-Type': 'application/json' }
            };
            if (body) {
                options.body = JSON.stringify(body);
            }
            const response = await fetch(endpoint, options);
            const result = await response.json();
            
            // If the response is not OK (e.g., 4xx, 5xx), throw an error with the server's message.
            if (!response.ok) {
                throw new Error(result.message || `HTTP error! Status: ${response.status}`);
            }
            return result;
        } catch (error) {
            console.error('API Call Error:', error.message);
            showToast(error.message, 'danger');
            // Hide progress bar on any API error to unblock UI
            $('.progress-container').fadeOut();
            return null;
        }
    }

    // --- TABLE AND DATA HANDLING ---

    /**
     * Clears and repopulates the main flight data table.
     * @param {Array<Array<string>>} flights An array of flight data rows.
     */
    function populateTable(flights) {
        const tableBody = $('#flightTable tbody');
        tableBody.empty();
        if (!flights || flights.length === 0) {
            tableBody.append('<tr><td colspan="12" class="text-center text-muted">No flight data available.</td></tr>');
            return;
        }
        flights.forEach(flight => {
            // Ensure each row has exactly 12 cells, padding with empty strings if necessary
            const rowData = Array.isArray(flight) ? [...flight] : [];
            while (rowData.length < 12) rowData.push('');
            
            // Create the table row and set a data attribute for easy identification
            const row = $('<tr>').attr('data-flight-number', rowData[0]);
            rowData.forEach(cellData => {
                row.append($('<td>').text(cellData));
            });
            tableBody.append(row);
        });
    }

    /**
     * Highlights the selected row in the table and enables associated buttons.
     * @param {HTMLElement} rowElement The table row element that was clicked.
     */
    function updateSelectedRow(rowElement) {
        if (selectedRow) {
            selectedRow.removeClass('table-primary');
        }
        selectedRow = $(rowElement);
        selectedRow.addClass('table-primary');
        // Enable buttons that operate on a selected row
        $('#deleteSelectedFlightBtn, #playNewBtn').prop('disabled', false);
    }

    /**
     * Clears any active row selection and disables associated buttons.
     */
    function clearSelection() {
        if (selectedRow) {
            selectedRow.removeClass('table-primary');
            selectedRow = null;
        }
        $('#deleteSelectedFlightBtn, #playNewBtn').prop('disabled', true);
    }

    // --- SOCKET.IO EVENT LISTENERS ---

    socket.on('connect', () => console.log('Successfully connected to server via WebSocket.'));

    socket.on('new_log', function(msg) {
        const logViewer = $('#log-viewer');
        // Sanitize log message to prevent potential HTML injection
        const sanitizedLog = msg.log.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        logViewer.append(`<div class="log-entry">${sanitizedLog}</div>`);
        // Auto-scroll to the bottom of the log viewer
        logViewer.scrollTop(logViewer[0].scrollHeight);
    });

    socket.on('progress_start', (data) => {
        $('#progressText').text(data.title || 'Starting process...');
        $('#progressBar').css('width', '0%').attr('aria-valuenow', 0);
        $('.progress-container').fadeIn();
    });

    socket.on('progress_update', (data) => {
        $('#progressBar').css('width', data.percent + '%').attr('aria-valuenow', data.percent);
        $('#progressText').text(data.text);
    });

    socket.on('progress_end', () => {
        $('#progressBar').css('width', '100%');
        $('#progressText').text('Process Complete!');
        setTimeout(() => {
            $('.progress-container').fadeOut(() => {
                // Reset progress bar after fading out
                $('#progressBar').css('width', '0%');
                $('#progressText').text('');
            });
        }, 1500);
    });

    // --- UI EVENT BINDINGS ---

    // Handle single click for row selection
    $('#flightTable tbody').on('click', 'tr', e => {
        // Only select row if not clicking on an interactive element inside it
        if ($(e.target).closest('a, button').length === 0) {
            updateSelectedRow(e.currentTarget);
        }
    });

    // Handle double click to open the edit modal
    $('#flightTable tbody').on('dblclick', 'tr', function() {
        updateSelectedRow(this);
        handleEdit();
    });

    // 'Add Flight' button opens the modal in 'add' mode
    $('#addFlightBtn').on('click', () => {
        $('#flightForm')[0].reset();
        $('#flightModalLabel').text('Add New Flight');
        $('#originalFlightNumber').val('');
        // IMPORTANT: Flight number should be editable when adding a new flight
        $('#flight_number').prop('readonly', false);
        flightModal.show();
    });

    // Form submission for both 'Add' and 'Edit'
    $('#flightForm').on('submit', async function(e) {
        e.preventDefault();
        const formData = Object.fromEntries(new FormData(this).entries());
        const originalFlightNumber = $('#originalFlightNumber').val();
        
        // Determine if this is an 'edit' or 'add' operation
        const endpoint = originalFlightNumber ? `/api/flights/${encodeURIComponent(originalFlightNumber)}` : '/api/flights';
        const method = originalFlightNumber ? 'PUT' : 'POST';

        const result = await apiCall(endpoint, method, formData);
        if (result && result.success) {
            populateTable(result.data);
            showToast(result.message, 'success');
            flightModal.hide();
            clearSelection();
        }
        // On failure, the API call handler will show a toast
    });

    // 'Delete' button in the toolbar
    $('#deleteSelectedFlightBtn').on('click', () => {
        if (!selectedRow) return;
        const flightNumber = selectedRow.data('flight-number');
        if (confirm(`Are you sure you want to delete flight: ${flightNumber}? This action cannot be undone.`)) {
            handleDelete(flightNumber);
        }
    });

    // --- Toolbar Button Actions ---
    $('#saveBtn').on('click', async () => {
        const result = await apiCall('/api/actions/save');
        if (result) showToast(result.message, result.success ? 'success' : 'danger');
    });

    $('#refreshBtn').on('click', async () => {
        const result = await apiCall('/api/actions/refresh');
        if (result && result.success) {
            populateTable(result.data);
            showToast(result.message, 'success');
            clearSelection();
        }
    });

    $('#clearBtn').on('click', async () => {
        if (confirm("DANGER: This will delete ALL flight data permanently. Are you absolutely sure?")) {
            const result = await apiCall('/api/actions/clear');
            if (result && result.success) {
                populateTable([]);
                showToast(result.message, 'warning');
                clearSelection();
            }
        }
    });

    $('#stopAllBtn').on('click', async () => {
        const result = await apiCall('/api/actions/stop');
        if (result) showToast(result.message, 'warning');
        $('.progress-container').fadeOut(); // Immediately hide progress bar on stop
        $('#audioPlayer')[0].pause(); // Stop any currently playing audio
    });

    $('#convertStereoBtn').on('click', async () => {
        if (confirm("This will process all .wav files in the 'material' directory to ensure they are stereo. This may take some time. Continue?")) {
            const result = await apiCall('/api/actions/convert_stereo');
            if (result) showToast(result.message, 'info');
        }
    });

    // --- NEW: Clear Cache Button ---
    $('#clearCacheBtn').on('click', async () => {
        if (confirm("Are you sure you want to delete all generated audio files? This cannot be undone.")) {
            const result = await apiCall('/api/actions/clear_cache', 'POST');
            if (result) {
                showToast(result.message, result.success ? 'success' : 'danger');
            }
        }
    });

    // --- Announcement Modals and Playback Logic ---
    $('#playNewBtn').on('click', () => {
        if (!selectedRow) return;
        $('#announceFlightNumber').text(selectedRow.data('flight-number'));
        announcementModal.show();
    });

    $('#generateAndPlayBtn').on('click', async () => {
        const payload = {
            flight_number: $('#announceFlightNumber').text(),
            announcement_type: $('#announcementTypeSelect').val()
        };
        // This is a potentially long operation, the backend will send progress via socket
        const result = await apiCall('/api/actions/synthesize', 'POST', payload);

        if (result && result.success) {
            announcementModal.hide();
            // Play the newly synthesized audio file
            $('#audioPlayer').attr('src', result.audio_url)[0].play();
            showToast(result.message, 'success');
        }
    });

    $('#playOldBtn').on('click', async () => {
        const result = await apiCall('/api/actions/play_old');
        if (result && result.success) {
            const select = $('#oldAnnouncementSelect');
            select.empty().append('<option selected disabled>Select a previously generated audio file...</option>');
            result.files.forEach(file => select.append($('<option>').val(file).text(file)));
            playOldModal.show();
        }
    });

    $('#playOldSelectedBtn').on('click', () => {
        const fileName = $('#oldAnnouncementSelect').val();
        if (fileName) {
            $('#audioPlayer').attr('src', `/output/${fileName}`)[0].play();
            playOldModal.hide();
        }
    });

    // --- CONTEXT MENU (Right-Click) LOGIC ---
    const contextMenu = $('#contextMenu');
    
    // Show context menu on right-click
    $('#flightTable tbody').on('contextmenu', 'tr', function(e) {
        // Prevent the default browser context menu
        e.preventDefault();
        // Select the row that was right-clicked
        updateSelectedRow(this);
        // Position and show the custom context menu
        contextMenu.css({ top: `${e.pageY}px`, left: `${e.pageX}px` }).show();
    });

    // Hide context menu on any other click
    $(document).on('click', () => contextMenu.hide());

    /**
     * Prepares and shows the flight modal for editing a selected row.
     */
    function handleEdit() {
        if (!selectedRow) return;
        const rowData = Array.from(selectedRow.find('td')).map(td => $(td).text());
        $('#flightForm')[0].reset();
        $('#flightModalLabel').text('Edit Flight');
        
        // Populate the form with the data from the selected table row
        $('#originalFlightNumber').val(rowData[0]); // CRITICAL: Store the original flight number
        $('#flight_number').val(rowData[0]).prop('readonly', true); // CRITICAL: Make flight number read-only on edit
        $('#departure').val(rowData[1]);
        $('#stopover').val(rowData[2]);
        $('#destination').val(rowData[3]);
        $('#divert').val(rowData[4]);
        $('#checkin_counter').val(rowData[5]);
        $('#boarding_gate').val(rowData[6]);
        $('#baggage_claim').val(rowData[7]);
        $('#scheduled_arrival_time').val(rowData[8]);
        $('#estimated_arrival_time').val(rowData[9]);
        $('#delay_reason').val(rowData[10]);
        $('#language_type').val(rowData[11]);
        
        flightModal.show();
    }

    /**
     * Handles the deletion of a flight via an API call.
     * @param {string} flightNumber The flight number to delete.
     */
    async function handleDelete(flightNumber) {
        const result = await apiCall(`/api/flights/${encodeURIComponent(flightNumber)}`, 'DELETE');
        if (result && result.success) {
            populateTable(result.data);
            showToast(result.message, 'success');
            clearSelection();
        }
    }

    // Bind functions to context menu items
    $('#contextEdit').on('click', handleEdit);

    $('#contextPlay').on('click', e => {
        e.preventDefault();
        $('#playNewBtn').trigger('click'); // Simulate a click on the main 'Play' button
    });

    $('#contextDelete').on('click', e => {
        e.preventDefault();
        if (!selectedRow) return;
        const flightNumber = selectedRow.data('flight-number');
        if (confirm(`Are you sure you want to delete flight: ${flightNumber}? This action cannot be undone.`)) {
            handleDelete(flightNumber);
        }
    });

    // --- Final Setup on Page Load ---
    populateTable(initialData);
    // Send an initial log message to confirm the UI is ready
    socket.emit('new_log', { log: 'Web client interface initialized successfully.' });
    console.log("Airport Announcement System frontend initialized.");
});