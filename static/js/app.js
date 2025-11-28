// Student Performance Prediction App JavaScript

class StudentPerformanceApp {
    constructor() {
        this.resultsData = [];
        this.performanceChart = null;
        this.resultsTable = null;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initializeDataTable();
    }
    
    bindEvents() {
        // Single prediction form
        $('#singlePredictionForm').on('submit', (e) => {
            e.preventDefault();
            this.handleSinglePrediction();
        });
        
        // Batch prediction form
        $('#batchPredictionForm').on('submit', (e) => {
            e.preventDefault();
            this.handleBatchPrediction();
        });
        
        // Tab switching
        $('button[data-bs-toggle="tab"]').on('shown.bs.tab', (e) => {
            if (e.target.id === 'results-tab') {
                this.updateResultsView();
            }
        });
        
        // Toggle suggestions - use event delegation for dynamically created elements
        $(document).on('click', '.toggle-suggestions', (e) => {
            e.preventDefault();
            const link = $(e.currentTarget);
            const uniqueId = link.data('id');
            const isExpanded = link.data('expanded');
            
            if (isExpanded) {
                // Collapse - show short list, hide full list
                $(`#${uniqueId}-short`).removeClass('d-none');
                $(`#${uniqueId}-full`).addClass('d-none');
                const moreCount = $(`#${uniqueId}-full li`).length - 3;
                link.text(`+${moreCount} more suggestions`);
                link.data('expanded', false);
            } else {
                // Expand - hide short list, show full list
                $(`#${uniqueId}-short`).addClass('d-none');
                $(`#${uniqueId}-full`).removeClass('d-none');
                link.text('Show less');
                link.data('expanded', true);
            }
        });
    }
    
    initializeDataTable() {
        this.resultsTable = $('#resultsTable').DataTable({
            pageLength: 10,
            order: [[1, 'desc']], // Sort by performance prediction
            columnDefs: [
                {
                    targets: 2, // Confidence column
                    render: function(data, type, row) {
                        if (type === 'display') {
                            const percentage = (data * 100).toFixed(1);
                            return `<span class="badge bg-info">${percentage}%</span>`;
                        }
                        return data;
                    }
                },
                {
                    targets: 1, // Performance column
                    render: function(data, type, row) {
                        if (type === 'display') {
                            const badgeClass = {
                                'Excellent': 'bg-success',
                                'Good': 'bg-primary',
                                'Average': 'bg-warning',
                                'Poor': 'bg-danger',
                                'Error': 'bg-secondary'
                            };
                            return `<span class="badge ${badgeClass[data] || 'bg-secondary'}">${data}</span>`;
                        }
                        return data;
                    }
                },
                {
                    targets: 3, // Suggestions column
                    render: function(data, type, row) {
                        if (type === 'display' && Array.isArray(data)) {
                            const topSuggestions = data.slice(0, 3);
                            const uniqueId = 'suggestions-' + Math.random().toString(36).substr(2, 9);
                            let html = '<ul class="mb-0 small suggestions-list" id="' + uniqueId + '-short">';
                            topSuggestions.forEach(suggestion => {
                                html += `<li>${suggestion}</li>`;
                            });
                            html += '</ul>';
                            if (data.length > 3) {
                                html += '<ul class="mb-0 small suggestions-list d-none" id="' + uniqueId + '-full">';
                                data.forEach(suggestion => {
                                    html += `<li>${suggestion}</li>`;
                                });
                                html += '</ul>';
                                html += `<a href="#" class="text-info small toggle-suggestions" data-id="${uniqueId}" data-expanded="false">+${data.length - 3} more suggestions</a>`;
                            }
                            return html;
                        }
                        return data;
                    }
                }
            ],
            responsive: true,
            language: {
                emptyTable: "No student predictions available"
            }
        });
    }
    
    async handleSinglePrediction() {
        try {
            // Collect form data
            const formData = {
                student_name: $('#studentName').val(),
                previous_grades: parseFloat($('#previousGrades').val()),
                attendance: parseFloat($('#attendance').val()),
                study_hours: parseFloat($('#studyHours').val()),
                extracurricular_activities: parseInt($('#extracurricular').val()),
                interactiveness: $('#interactiveness').val(),
                practical_knowledge: $('#practicalKnowledge').val(),
                communication_skill: $('#communicationSkill').val(),
                projects_handled: parseInt($('#projectsHandled').val()),
                assignments_completed: parseInt($('#assignmentsCompleted').val())
            };
            
            // Validate form data
            if (!this.validateSinglePredictionData(formData)) {
                return;
            }
            
            this.showLoading();
            
            // Make API call
            const response = await fetch('/api/predict_single', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Prediction failed');
            }
            
            // Add to results
            this.resultsData = [result];
            
            // Show success message
            this.showSuccessAlert('Prediction completed successfully!');
            
            // Switch to results tab
            $('#results-tab').tab('show');
            
        } catch (error) {
            console.error('Single prediction error:', error);
            this.showErrorAlert(error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    async handleBatchPrediction() {
        try {
            const fileInput = $('#excelFile')[0];
            const file = fileInput.files[0];
            
            if (!file) {
                this.showErrorAlert('Please select an Excel file');
                return;
            }
            
            // Validate file type
            const allowedTypes = [
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-excel'
            ];
            
            if (!allowedTypes.includes(file.type)) {
                this.showErrorAlert('Please upload a valid Excel file (.xlsx or .xls)');
                return;
            }
            
            this.showLoading();
            
            // Prepare form data
            const formData = new FormData();
            formData.append('file', file);
            
            // Make API call
            const response = await fetch('/api/predict_batch', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Batch prediction failed');
            }
            
            // Store results
            this.resultsData = result.results;
            this.performanceStats = result.performance_stats;
            
            // Show success message
            this.showSuccessAlert(`Batch prediction completed! Processed ${result.total_students} students.`);
            
            // Switch to results tab
            $('#results-tab').tab('show');
            
        } catch (error) {
            console.error('Batch prediction error:', error);
            this.showErrorAlert(error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    validateSinglePredictionData(data) {
        // Check for required fields
        for (const [key, value] of Object.entries(data)) {
            if (value === '' || value === null || value === undefined) {
                this.showErrorAlert(`Please fill in the ${key.replace('_', ' ')} field`);
                return false;
            }
        }
        
        // Validate ranges
        if (data.previous_grades < 0 || data.previous_grades > 100) {
            this.showErrorAlert('Previous grades must be between 0 and 100');
            return false;
        }
        
        if (data.attendance < 0 || data.attendance > 100) {
            this.showErrorAlert('Attendance percentage must be between 0 and 100');
            return false;
        }
        
        if (data.study_hours < 0 || data.study_hours > 24) {
            this.showErrorAlert('Study hours must be between 0 and 24');
            return false;
        }
        
        return true;
    }
    
    updateResultsView() {
        if (this.resultsData.length === 0) {
            $('#resultsContainer').addClass('d-none');
            $('#noResultsMessage').removeClass('d-none');
            return;
        }
        
        $('#noResultsMessage').addClass('d-none');
        $('#resultsContainer').removeClass('d-none');
        
        // Update chart
        this.updatePerformanceChart();
        
        // Update summary statistics
        this.updateSummaryStats();
        
        // Update results table
        this.updateResultsTable();
    }
    
    updatePerformanceChart() {
        // Calculate performance distribution
        const stats = this.performanceStats || this.calculatePerformanceStats();
        
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.performanceChart) {
            this.performanceChart.destroy();
        }
        
        this.performanceChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Excellent', 'Good', 'Average', 'Poor'],
                datasets: [{
                    data: [
                        stats.Excellent || 0,
                        stats.Good || 0,
                        stats.Average || 0,
                        stats.Poor || 0
                    ],
                    backgroundColor: [
                        '#198754', // Success green
                        '#0d6efd', // Primary blue
                        '#ffc107', // Warning yellow
                        '#dc3545'  // Danger red
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    calculatePerformanceStats() {
        const stats = { Poor: 0, Average: 0, Good: 0, Excellent: 0 };
        
        this.resultsData.forEach(result => {
            if (stats.hasOwnProperty(result.predicted_performance)) {
                stats[result.predicted_performance]++;
            }
        });
        
        return stats;
    }
    
    updateSummaryStats() {
        const stats = this.performanceStats || this.calculatePerformanceStats();
        const total = this.resultsData.length;
        
        // Calculate average confidence
        const avgConfidence = this.resultsData.reduce((sum, result) => {
            return sum + (result.confidence || 0);
        }, 0) / total;
        
        const html = `
            <div class="row g-3">
                <div class="col-6">
                    <div class="text-center">
                        <h4 class="text-success">${stats.Excellent || 0}</h4>
                        <small class="text-muted">Excellent</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="text-center">
                        <h4 class="text-primary">${stats.Good || 0}</h4>
                        <small class="text-muted">Good</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="text-center">
                        <h4 class="text-warning">${stats.Average || 0}</h4>
                        <small class="text-muted">Average</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="text-center">
                        <h4 class="text-danger">${stats.Poor || 0}</h4>
                        <small class="text-muted">Poor</small>
                    </div>
                </div>
                <div class="col-12">
                    <hr>
                    <div class="text-center">
                        <h5>${total}</h5>
                        <small class="text-muted">Total Students</small>
                    </div>
                    <div class="text-center mt-2">
                        <h6>${(avgConfidence * 100).toFixed(1)}%</h6>
                        <small class="text-muted">Avg. Confidence</small>
                    </div>
                </div>
            </div>
        `;
        
        $('#summaryStats').html(html);
    }
    
    updateResultsTable() {
        // Clear existing data
        this.resultsTable.clear();
        
        // Add new data
        this.resultsData.forEach(result => {
            this.resultsTable.row.add([
                result.student_name,
                result.predicted_performance,
                result.confidence || 0,
                result.suggestions || []
            ]);
        });
        
        // Redraw table
        this.resultsTable.draw();
    }
    
    showLoading() {
        $('#loadingModal').modal('show');
    }
    
    hideLoading() {
        $('#loadingModal').modal('hide');
    }
    
    showSuccessAlert(message) {
        this.showAlert(message, 'success');
    }
    
    showErrorAlert(message) {
        this.showAlert(message, 'danger');
    }
    
    showAlert(message, type) {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Remove existing alerts
        $('.alert').remove();
        
        // Add new alert to the top of the container
        $('.container').prepend(alertHtml);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            $('.alert').fadeOut();
        }, 5000);
    }
}

// Initialize app when document is ready
$(document).ready(() => {
    new StudentPerformanceApp();
});
