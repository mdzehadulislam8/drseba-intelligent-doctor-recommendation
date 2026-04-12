// API Configuration
// Use the same host as the opened frontend (works for localhost and LAN IP like 192.168.x.x)
const apiHost = window.location.hostname || 'localhost';
const API_BASE_URL = `${window.location.protocol}//${apiHost}:5000/api`;

// DOM Elements - will be set after DOM is ready
let districtSelect;
let thanaSelect;
let specializationSelect;
let maxFeeInput;
let onlineCheckbox;
let emergencyCheckbox;
let topNInput;
let searchBtn;
let loadingDiv;
let resultsSection;
let resultsContainer;
let errorMessage;

// Store data for dynamic filtering
let allOptions = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Get all DOM elements
    districtSelect = document.getElementById('district');
    thanaSelect = document.getElementById('thana');
    specializationSelect = document.getElementById('specialization');
    maxFeeInput = document.getElementById('maxFee');
    onlineCheckbox = document.getElementById('online');
    emergencyCheckbox = document.getElementById('emergency');
    topNInput = document.getElementById('topN');
    searchBtn = document.getElementById('searchBtn');
    loadingDiv = document.getElementById('loading');
    resultsSection = document.getElementById('resultsSection');
    resultsContainer = document.getElementById('results');
    errorMessage = document.getElementById('errorMessage');
    
    // Verify all elements exist
    if (!districtSelect) console.error('Element "district" not found');
    if (!specializationSelect) console.error('Element "specialization" not found');
    
    // Load options and attach listeners
    loadOptions();
    attachEventListeners();
});

// Attach event listeners
function attachEventListeners() {
    if (searchBtn) {
        searchBtn.addEventListener('click', searchDoctors);
    }
    if (districtSelect) {
        districtSelect.addEventListener('change', onDistrictChange);
    }
    
    // Allow Enter key to search
    document.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchDoctors();
        }
    });
}

// Load all options from API
async function loadOptions() {
    try {
        console.log('Loading options from API...');
        const response = await fetch(`${API_BASE_URL}/options`);
        const data = await response.json();
        
        console.log('API Response:', data);
        
        if (data.success) {
            allOptions = data.options;
            console.log('Districts loaded:', allOptions.districts);
            console.log('Specializations loaded:', allOptions.specializations);
            
            // Populate districts
            if (districtSelect) {
                districtSelect.innerHTML = '<option value="">-- Select District --</option>';
                allOptions.districts.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district;
                    option.textContent = district;
                    districtSelect.appendChild(option);
                });
                console.log('Districts populated in dropdown');
            }
            
            // Populate specializations
            if (specializationSelect) {
                specializationSelect.innerHTML = '<option value="">-- Select Specialization --</option>';
                allOptions.specializations.forEach(spec => {
                    const option = document.createElement('option');
                    option.value = spec;
                    option.textContent = spec;
                    specializationSelect.appendChild(option);
                });
                console.log('Specializations populated in dropdown');
            }
            
            // Set first district as default
            if (allOptions.districts.length > 0 && districtSelect) {
                districtSelect.value = allOptions.districts[0];
                console.log('Selected first district:', allOptions.districts[0]);
                onDistrictChange();
            }
        } else {
            showError('API returned success: false');
        }
    } catch (error) {
        console.error('Error loading options:', error);
        showError('Failed to load options. Make sure the API is running on localhost:5000');
    }
}

// Handle district change
async function onDistrictChange() {
    const selectedDistrict = districtSelect.value;
    console.log('District changed to:', selectedDistrict);
    
    if (!selectedDistrict) {
        if (thanaSelect) {
            thanaSelect.innerHTML = '<option value="">-- Select Thana --</option>';
        }
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/thanas/${selectedDistrict}`);
        const data = await response.json();
        
        console.log('Thanas for', selectedDistrict, ':', data);
        
        // Populate thanas
        if (thanaSelect) {
            thanaSelect.innerHTML = '<option value="">-- Select Thana --</option>';
            if (data.thanas) {
                data.thanas.forEach(thana => {
                    const option = document.createElement('option');
                    option.value = thana;
                    option.textContent = thana;
                    thanaSelect.appendChild(option);
                });
                
                // Set first thana as default
                if (data.thanas.length > 0) {
                    thanaSelect.value = data.thanas[0];
                }
            }
        }
    } catch (error) {
        console.error('Error loading thanas:', error);
    }
}

// Search doctors
async function searchDoctors() {
    // Validate inputs
    if (!districtSelect.value || !thanaSelect.value || !specializationSelect.value) {
        showError('Please fill all required fields');
        return;
    }
    
    // Show loading
    hideError();
    showLoading();
    
    try {
        const payload = {
            district: districtSelect.value,
            thana: thanaSelect.value,
            specialization: specializationSelect.value,
            max_fee: parseInt(maxFeeInput.value) || 2000,
            online: onlineCheckbox.checked ? 1 : 0,
            emergency: emergencyCheckbox.checked ? 1 : 0,
            top_n: parseInt(topNInput.value) || 5
        };
        
        console.log('Sending search request:', payload);
        
        const response = await fetch(`${API_BASE_URL}/recommendations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        console.log('Search response:', data);
        
        hideLoading();
        
        if (data.success && data.doctors && data.doctors.length > 0) {
            displayResults(data.doctors);
        } else if (data.message) {
            showError(data.message);
        } else if (data.error) {
            showError(data.error);
        } else {
            showError('No doctors found with the given criteria');
        }
    } catch (error) {
        hideLoading();
        console.error('Error:', error);
        showError(`Error: ${error.message}. Make sure the API is running on http://localhost:5000`);
    }
}

// Display search results
function displayResults(doctors) {
    console.log('Displaying', doctors.length, 'doctors');
    
    // Hide empty state and ensure results section is visible
    const emptyState = document.getElementById('emptyState');
    if (emptyState) {
        emptyState.classList.add('hidden');
    }
    
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
    }
    
    if (doctors.length === 0) {
        const noResults = document.getElementById('noResults');
        if (noResults) {
            noResults.classList.remove('hidden');
        }
        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }
        return;
    }
    
    // Hide no results message
    const noResults = document.getElementById('noResults');
    if (noResults) {
        noResults.classList.add('hidden');
    }
    
    // Update result count
    const resultCount = document.getElementById('resultCount');
    if (resultCount) {
        resultCount.textContent = doctors.length;
    }
    
    doctors.forEach((doctor, index) => {
        if (resultsContainer) {
            const card = createDoctorCard(doctor, index + 1);
            resultsContainer.appendChild(card);
        }
    });
    
    if (resultsSection) {
        resultsSection.classList.remove('hidden');
    }
}

// Create doctor card
function createDoctorCard(doctor, rank) {
    const card = document.createElement('div');
    card.className = 'doctor-card';
    
    // Determine score badge class based on predicted score
    let scoreBadgeClass = 'score-badge score-fair';
    if (doctor.predicted_score > 1.5) {
        scoreBadgeClass = 'score-badge score-excellent';
    } else if (doctor.predicted_score > 1.0) {
        scoreBadgeClass = 'score-badge score-good';
    }
    
    // Determine score level text
    let scoreLevel = 'Fair';
    if (doctor.predicted_score > 1.5) {
        scoreLevel = 'Excellent';
    } else if (doctor.predicted_score > 1.0) {
        scoreLevel = 'Good';
    }
    
    card.innerHTML = `
        <div class="doctor-rank">
            <div class="rank-badge">#${rank}</div>
            <div class="doctor-name">
                <h3>${doctor.doctor_name}</h3>
                <div class="doctor-spec">${doctor.specialization || 'General Practice'}</div>
            </div>
        </div>
        
        <div class="doctor-info">
            <div class="info-item">
                <div class="info-label">Rating</div>
                <div class="info-value rating">⭐ ${doctor.rating_avg.toFixed(1)}/5.0</div>
            </div>
            <div class="info-item">
                <div class="info-label">Experience</div>
                <div class="info-value">${doctor.experience_years} years</div>
            </div>
            <div class="info-item">
                <div class="info-label">Consultation Fee</div>
                <div class="info-value">৳${doctor.consultation_fees.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Quality Score</div>
                <div class="info-value">${doctor.predicted_score.toFixed(4)}</div>
            </div>
        </div>
        
        <div class="${scoreBadgeClass}">
            Quality: ${scoreLevel} (${doctor.predicted_score.toFixed(4)})
        </div>
        
        <div class="hospital-info">
            <div class="hospital-name">🏥 ${doctor.hospital_name}</div>
            <div class="full-address">📍 ${doctor.full_address}</div>
        </div>
    `;
    
    return card;
}

// Show loading indicator
function showLoading() {
    if (loadingDiv) {
        loadingDiv.classList.remove('hidden');
    }
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }
}

// Hide loading indicator
function hideLoading() {
    if (loadingDiv) {
        loadingDiv.classList.add('hidden');
    }
}

// Show error message
function showError(message) {
    console.error('Showing error:', message);
    const errorText = document.getElementById('errorText');
    if (errorText) {
        errorText.textContent = message;
    }
    if (errorMessage) {
        errorMessage.classList.remove('hidden');
    }
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }
}

// Hide error message
function hideError() {
    if (errorMessage) {
        errorMessage.classList.add('hidden');
    }
}

// Export functions for external use
window.searchDoctors = searchDoctors;
