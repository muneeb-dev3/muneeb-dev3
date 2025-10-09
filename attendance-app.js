// Global state
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let people = [];
let selectedPerson = null;
let attendance = {};

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeYearSelector();
    initializeEventListeners();
    setCurrentMonthYear();
    loadDataFromStorage();
    renderPeople();
    renderCalendar();
    renderSummary();
});

// Initialize year selector with a range of years
function initializeYearSelector() {
    const yearSelect = document.getElementById('year');
    const currentYear = new Date().getFullYear();
    
    for (let year = currentYear - 5; year <= currentYear + 5; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    }
}

// Set current month and year in selectors
function setCurrentMonthYear() {
    document.getElementById('month').value = currentMonth;
    document.getElementById('year').value = currentYear;
}

// Initialize event listeners
function initializeEventListeners() {
    document.getElementById('addPerson').addEventListener('click', addPerson);
    document.getElementById('personName').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addPerson();
        }
    });
    
    document.getElementById('month').addEventListener('change', function() {
        currentMonth = parseInt(this.value);
        renderCalendar();
        renderSummary();
    });
    
    document.getElementById('year').addEventListener('change', function() {
        currentYear = parseInt(this.value);
        renderCalendar();
        renderSummary();
    });
}

// Add a new person
function addPerson() {
    const nameInput = document.getElementById('personName');
    const name = nameInput.value.trim();
    
    if (!name) {
        alert('Please enter a name');
        return;
    }
    
    if (people.find(p => p.name === name)) {
        alert('Person already exists');
        return;
    }
    
    const person = {
        id: Date.now().toString(),
        name: name
    };
    
    people.push(person);
    nameInput.value = '';
    
    // Auto-select the newly added person
    selectedPerson = person.id;
    
    saveDataToStorage();
    renderPeople();
    renderCalendar();
    renderSummary();
}

// Remove a person
function removePerson(personId) {
    if (confirm('Are you sure you want to remove this person?')) {
        people = people.filter(p => p.id !== personId);
        
        // Clear attendance data for this person
        delete attendance[personId];
        
        if (selectedPerson === personId) {
            selectedPerson = null;
        }
        
        saveDataToStorage();
        renderPeople();
        renderCalendar();
        renderSummary();
    }
}

// Select a person
function selectPerson(personId) {
    selectedPerson = personId;
    renderPeople();
    renderCalendar();
    renderSummary();
}

// Render people list
function renderPeople() {
    const container = document.getElementById('peopleContainer');
    
    if (people.length === 0) {
        container.innerHTML = '<div class="no-data">No people added yet</div>';
        return;
    }
    
    container.innerHTML = people.map(person => `
        <div class="person-item ${selectedPerson === person.id ? 'selected' : ''}" 
             onclick="selectPerson('${person.id}')">
            <span>${person.name}</span>
            <button onclick="event.stopPropagation(); removePerson('${person.id}')">Remove</button>
        </div>
    `).join('');
}

// Get days in month
function getDaysInMonth(year, month) {
    return new Date(year, month + 1, 0).getDate();
}

// Get day of week for first day of month (0 = Sunday)
function getFirstDayOfMonth(year, month) {
    return new Date(year, month, 1).getDay();
}

// Render calendar
function renderCalendar() {
    const calendar = document.getElementById('calendar');
    const daysInMonth = getDaysInMonth(currentYear, currentMonth);
    const firstDay = getFirstDayOfMonth(currentYear, currentMonth);
    
    // Day labels
    const dayLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    
    let html = '';
    
    // Add day labels
    dayLabels.forEach(label => {
        html += `<div style="text-align: center; font-weight: 600; color: #495057; padding: 10px;">${label}</div>`;
    });
    
    // Add empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        html += '<div class="calendar-day disabled"></div>';
    }
    
    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dateKey = `${currentYear}-${currentMonth}-${day}`;
        let status = '';
        
        if (selectedPerson && attendance[selectedPerson] && attendance[selectedPerson][dateKey]) {
            status = attendance[selectedPerson][dateKey];
        }
        
        const disabledClass = selectedPerson ? '' : 'disabled';
        const statusClass = status ? status : '';
        
        html += `
            <div class="calendar-day ${disabledClass} ${statusClass}" 
                 onclick="${selectedPerson ? `toggleAttendance(${day})` : ''}">
                <div class="day-number">${day}</div>
                ${status === 'present' ? '<div class="day-label">Present</div>' : ''}
                ${status === 'absent' ? '<div class="day-label">Absent</div>' : ''}
            </div>
        `;
    }
    
    calendar.innerHTML = html;
}

// Toggle attendance status
function toggleAttendance(day) {
    if (!selectedPerson) return;
    
    const dateKey = `${currentYear}-${currentMonth}-${day}`;
    
    if (!attendance[selectedPerson]) {
        attendance[selectedPerson] = {};
    }
    
    const currentStatus = attendance[selectedPerson][dateKey];
    
    if (!currentStatus) {
        attendance[selectedPerson][dateKey] = 'present';
    } else if (currentStatus === 'present') {
        attendance[selectedPerson][dateKey] = 'absent';
    } else {
        delete attendance[selectedPerson][dateKey];
    }
    
    saveDataToStorage();
    renderCalendar();
    renderSummary();
}

// Calculate attendance summary for a person
function calculateSummary(personId) {
    const daysInMonth = getDaysInMonth(currentYear, currentMonth);
    let present = 0;
    let absent = 0;
    
    if (attendance[personId]) {
        for (let day = 1; day <= daysInMonth; day++) {
            const dateKey = `${currentYear}-${currentMonth}-${day}`;
            const status = attendance[personId][dateKey];
            
            if (status === 'present') present++;
            else if (status === 'absent') absent++;
        }
    }
    
    const percentage = daysInMonth > 0 ? ((present / daysInMonth) * 100).toFixed(1) : 0;
    
    return {
        totalDays: daysInMonth,
        present: present,
        absent: absent,
        percentage: percentage
    };
}

// Render summary
function renderSummary() {
    const summaryContainer = document.getElementById('summary');
    
    if (!selectedPerson) {
        summaryContainer.innerHTML = '<div class="no-data">Select a person to view attendance summary</div>';
        return;
    }
    
    const person = people.find(p => p.id === selectedPerson);
    const summary = calculateSummary(selectedPerson);
    
    summaryContainer.innerHTML = `
        <div class="summary-card total">
            <h3>Total Working Days</h3>
            <div class="value">${summary.totalDays}</div>
        </div>
        <div class="summary-card present">
            <h3>Total Present</h3>
            <div class="value">${summary.present}</div>
        </div>
        <div class="summary-card absent">
            <h3>Total Absent</h3>
            <div class="value">${summary.absent}</div>
        </div>
        <div class="summary-card percentage">
            <h3>Attendance %</h3>
            <div class="value">${summary.percentage}%</div>
        </div>
    `;
}

// Save data to localStorage
function saveDataToStorage() {
    localStorage.setItem('attendanceApp_people', JSON.stringify(people));
    localStorage.setItem('attendanceApp_attendance', JSON.stringify(attendance));
}

// Load data from localStorage
function loadDataFromStorage() {
    const storedPeople = localStorage.getItem('attendanceApp_people');
    const storedAttendance = localStorage.getItem('attendanceApp_attendance');
    
    if (storedPeople) {
        people = JSON.parse(storedPeople);
    }
    
    if (storedAttendance) {
        attendance = JSON.parse(storedAttendance);
    }
    
    // Auto-select first person if available
    if (people.length > 0 && !selectedPerson) {
        selectedPerson = people[0].id;
    }
}
