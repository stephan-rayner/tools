const dimensions = [
    { name: 'Communicating', left: 'Low-Context', right: 'High-Context' },
    { name: 'Evaluating', left: 'Direct Neg. Feedback', right: 'Indirect Neg. Feedback' },
    { name: 'Persuading', left: 'Principles-First', right: 'Applications-First/Holistic' },
    { name: 'Leading', left: 'Egalitarian', right: 'Hierarchical' },
    { name: 'Deciding', left: 'Consensual', right: 'Top-Down' },
    { name: 'Trusting', left: 'Task-Based', right: 'Relationship-Based' },
    { name: 'Disagreeing', left: 'Confrontational', right: 'Avoids Confrontation' },
    { name: 'Scheduling', left: 'Linear-Time', right: 'Flexible-Time' }
];

const countryData = {
    'USA': [1, 6, 9, 4, 8, 2, 4, 2],
    'Canada': [2, 5, 8, 3, 5, 3, 6, 3],
    'UK': [3, 4, 9, 4, 6, 3, 5, 2],
    'Australia': [2, 3, 8, 2, 4, 2, 3, 2],
    'Germany': [1, 1, 2, 5, 2, 2, 1, 1],
    'Greece': [8, 8, 3, 6, 8, 8, 2, 8],
    'Portugal': [8, 8, 3, 6, 8, 8, 7, 8],
    'Spain': [7, 4, 3, 6, 8, 6, 2, 8],
    'Argentina': [8, 7, 3, 8, 9, 9, 8, 9],
    'Brazil': [9, 8, 3, 8, 9, 9, 8, 10],
    'Peru': [9, 8, 3, 8, 9, 9, 8, 10],
    'Singapore': [9, 7, 5, 9, 8, 8, 9, 4],
    'Netherlands': [1, 1, 4, 2, 2, 1, 1, 1],
    'Sweden': [3, 4, 5, 1, 1, 2, 8, 1],
    'Ukraine': [7, 5, 2, 8, 8, 7, 5, 5],
    'Ethiopia': [10, 9, 5, 10, 9, 10, 9, 10],
    'Russia': [8, 1, 2, 9, 9, 8, 1, 5],
    'Israel': [8, 1, 5, 2, 8, 5, 1, 5],
    'Finland': [2, 3, 5, 2, 2, 2, 7, 1],
    'India': [8, 8, 5, 8, 8, 9, 8, 9],
    'China': [10, 9, 10, 10, 9, 10, 10, 7],
    'Thailand': [9, 9, 8, 8, 8, 9, 10, 7],
    'Philippines': [9, 9, 8, 8, 8, 9, 10, 8],
    'Japan': [10, 9, 10, 7, 1, 9, 10, 1],
    'South Korea': [10, 9, 10, 9, 8, 9, 10, 3],
    'Turkey': [8, 8, 3, 8, 7, 8, 8, 8],
    'Syria': [10, 9, 2, 10, 9, 10, 9, 10],
    'Austria': [1, 2, 3, 2, 2, 2, 1, 1],
    'Belgium': [5, 5, 3, 6, 4, 6, 5, 3],
    'France': [8, 2, 2, 8, 9, 7, 2, 6],
    'Iran': [9, 8, 3, 9, 8, 10, 8, 9],
    'Iraq': [10, 9, 2, 10, 9, 10, 9, 10],
    'Afghanistan': [10, 9, 2, 10, 9, 10, 9, 10]
};

const colors = [
    '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
    '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', 
    '#469990', '#dcbeff', '#9a6324', '#fffac8', '#800000', 
    '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9',
    '#000000', '#f9a825', '#ad1457', '#6a1b9a', '#283593',
    '#2e7d32', '#ef6c00', '#4e342e', '#37474f'
];

let selectedCountries = ['USA', 'Singapore', 'Australia', 'Canada'];
const countryColors = {};
Object.keys(countryData).forEach((country, index) => {
    countryColors[country] = colors[index % colors.length];
});

const svg = document.getElementById('culture-map-svg');
const countryListEl = document.getElementById('country-list');
const legendEl = document.getElementById('chart-legend');
const toggleBtn = document.getElementById('toggle-selection');

function init() {
    renderCountryList();
    renderChart();
    
    toggleBtn.addEventListener('click', () => {
        if (selectedCountries.length > 0) {
            selectedCountries = [];
        } else {
            selectedCountries = Object.keys(countryData);
        }
        updateUI();
    });
}

function renderCountryList() {
    countryListEl.innerHTML = '';
    const allCountries = Object.keys(countryData).sort();
    
    // Split into selected and unselected
    const selected = allCountries.filter(c => selectedCountries.includes(c));
    const unselected = allCountries.filter(c => !selectedCountries.includes(c));
    
    // Combine: selected first, then unselected (both internally alphabetical)
    const sortedToDisplay = [...selected, ...unselected];

    // Update toggle button text
    toggleBtn.textContent = selectedCountries.length > 0 ? 'Clear All' : 'Select All';

    sortedToDisplay.forEach(country => {
        const isSelected = selectedCountries.includes(country);
        const div = document.createElement('div');
        div.className = `country-item ${isSelected ? 'active' : ''}`;
        div.innerHTML = `
            <input type="checkbox" ${isSelected ? 'checked' : ''}>
            <span>${country}</span>
        `;
        div.addEventListener('click', (e) => {
            if (e.target.tagName !== 'INPUT') {
                const cb = div.querySelector('input');
                cb.checked = !cb.checked;
            }
            toggleCountry(country);
        });
        countryListEl.appendChild(div);
    });
}

function toggleCountry(country) {
    const index = selectedCountries.indexOf(country);
    if (index > -1) {
        selectedCountries.splice(index, 1);
    } else {
        selectedCountries.push(country);
    }
    updateUI();
}

function updateUI() {
    renderCountryList();
    renderChart();
}

function renderChart() {
    const svg = document.getElementById('culture-map-svg');
    svg.innerHTML = '';
    
    const margin = { top: 60, right: 150, bottom: 40, left: 150 };
    const width = svg.width.baseVal.value;
    const height = svg.height.baseVal.value;
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    
    const yStep = innerHeight / (dimensions.length - 1);
    
    // Draw background scales
    dimensions.forEach((dim, i) => {
        const y = margin.top + i * yStep;
        
        // Horizontal line
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', margin.left);
        line.setAttribute('y1', y);
        line.setAttribute('x2', margin.left + innerWidth);
        line.setAttribute('y2', y);
        line.setAttribute('stroke', '#e0e0e0');
        line.setAttribute('stroke-dasharray', '4');
        svg.appendChild(line);
        
        // Axis label (center)
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', width / 2);
        text.setAttribute('y', y - 15);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('class', 'axis-label');
        text.textContent = dim.name;
        svg.appendChild(text);
        
        // Left label
        const leftText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        leftText.setAttribute('x', margin.left - 10);
        leftText.setAttribute('y', y + 5);
        leftText.setAttribute('text-anchor', 'end');
        leftText.setAttribute('class', 'scale-label');
        leftText.textContent = dim.left;
        svg.appendChild(leftText);
        
        // Right label
        const rightText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        rightText.setAttribute('x', margin.left + innerWidth + 10);
        rightText.setAttribute('y', y + 5);
        rightText.setAttribute('text-anchor', 'start');
        rightText.setAttribute('class', 'scale-label');
        rightText.textContent = dim.right;
        svg.appendChild(rightText);
    });
    
    // Draw country lines
    selectedCountries.forEach(country => {
        const scores = countryData[country];
        const color = countryColors[country];
        let pathData = '';
        
        scores.forEach((score, i) => {
            const x = margin.left + (score / 10) * innerWidth;
            const y = margin.top + i * yStep;
            
            pathData += (i === 0 ? 'M' : 'L') + x + ',' + y;
            
            // Draw dot
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', y);
            circle.setAttribute('r', '5');
            circle.setAttribute('fill', color);
            circle.setAttribute('class', 'country-dot');
            svg.appendChild(circle);
        });
        
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathData);
        path.setAttribute('stroke', color);
        path.setAttribute('class', 'country-line');
        svg.appendChild(path);
    });
    
    renderLegend();
}

function renderLegend() {
    legendEl.innerHTML = '';
    selectedCountries.forEach(country => {
        const div = document.createElement('div');
        div.className = 'legend-item';
        div.innerHTML = `
            <div class="legend-color" style="background-color: ${countryColors[country]}"></div>
            <span>${country}</span>
        `;
        legendEl.appendChild(div);
    });
}

init();
