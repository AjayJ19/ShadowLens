// ShadowLens Popup JavaScript - Enhanced Features
let currentAnalysis = null;
let privacyLinks = [];

// Initialize popup when opened
document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('🔒 ShadowLens Popup: Initializing Enhanced Features...');
        
        // Show loading state with null checks
        const loadingElement = document.getElementById('loading');
        const analysisElement = document.getElementById('analysis');
        const errorElement = document.getElementById('error');
        
        if (loadingElement) {
            try {
                loadingElement.style.display = 'block';
            } catch (displayError) {
                console.error('Error setting loading display:', displayError);
            }
        }
        
        if (analysisElement) {
            try {
                analysisElement.style.display = 'none';
            } catch (displayError) {
                console.error('Error setting analysis display:', displayError);
            }
        }
        
        if (errorElement) {
            try {
                errorElement.style.display = 'none';
            } catch (displayError) {
                console.error('Error setting error display:', displayError);
            }
        }
        
        // Get current tab and trigger analysis with error handling
        try {
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                try {
                    if (tabs && tabs[0]) {
                        const currentTab = tabs[0];
                        console.log('🌐 Current tab URL from address bar:', currentTab.url);
                        
                        // Show the URL immediately with error handling
                        try {
                            const urlElement = document.getElementById('current-url');
                            if (urlElement) {
                                urlElement.textContent = currentTab.url || 'Unknown URL';
                            }
                        } catch (urlError) {
                            console.error('Error setting URL display:', urlError);
                        }
                        
                        // Always trigger fresh analysis with error handling
                        try {
                            triggerAnalysis(currentTab.id);
                        } catch (triggerError) {
                            console.error('Error triggering analysis:', triggerError);
                            showError('Unable to start analysis');
                        }
                    } else {
                        console.error('No active tab found');
                        showError('No active tab found');
                    }
                } catch (tabError) {
                    console.error('Error processing tabs:', tabError);
                    showError('Unable to access current tab');
                }
            });
        } catch (queryError) {
            console.error('Error querying tabs:', queryError);
            showError('Unable to access browser tabs');
        }
        
        // Listen for messages from content script with enhanced error handling
        try {
            chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
                try {
                    if (message && message.action) {
                        if (message.action === 'analysisComplete') {
                            console.log('Analysis complete received:', message.analysis);
                            currentAnalysis = message.analysis;
                            try {
                                displayAnalysis(currentAnalysis);
                            } catch (displayError) {
                                console.error('Error displaying analysis:', displayError);
                                showError('Error displaying analysis results');
                            }
                        } else if (message.action === 'analysisError') {
                            console.error('Analysis error received:', message.error);
                            try {
                                showError(`Analysis failed: ${message.error}`);
                            } catch (showError) {
                                console.error('Error showing error message:', showError);
                            }
                        } else if (message.action === 'privacyLinksFound') {
                            console.log('Privacy links found:', message.links);
                            privacyLinks = message.links || [];
                            try {
                                displayPrivacyLinks(privacyLinks);
                            } catch (displayError) {
                                console.error('Error displaying privacy links:', displayError);
                            }
                        }
                    }
                } catch (messageError) {
                    console.error('Error in popup message listener:', messageError);
                    try {
                        showError('Error processing analysis results');
                    } catch (showError) {
                        console.error('Error showing error message:', showError);
                    }
                }
            });
        } catch (listenerError) {
            console.error('Error setting up message listener:', listenerError);
        }
        
        // Add timeout for analysis with error handling
        try {
            setTimeout(() => {
                try {
                    const loadingElement = document.getElementById('loading');
                    if (loadingElement && loadingElement.style.display !== 'none') {
                        console.log('Analysis timeout, showing error');
                        showError('Analysis timed out. Please try again.');
                    }
                } catch (timeoutError) {
                    console.error('Error in timeout handler:', timeoutError);
                }
            }, 10000); // 10 second timeout
        } catch (timeoutError) {
            console.error('Error setting timeout:', timeoutError);
        }
    } catch (initError) {
        console.error('Critical error in popup initialization:', initError);
        // Try to show error message
        try {
            const errorElement = document.getElementById('error');
            const errorMessageElement = document.getElementById('error-message');
            if (errorElement) errorElement.style.display = 'block';
            if (errorMessageElement) errorMessageElement.textContent = 'Extension initialization failed';
        } catch (fallbackError) {
            console.error('Error in fallback error display:', fallbackError);
        }
    }
});

function checkForAnalysis(tabId) {
    try {
        // Send message to content script to get current analysis
        chrome.tabs.sendMessage(tabId, {action: 'getAnalysis'}, function(response) {
            if (chrome.runtime.lastError) {
                console.error('Error checking analysis:', chrome.runtime.lastError);
                showError('Unable to get analysis results');
            } else if (response && response.analysis) {
                console.log('Found existing analysis:', response.analysis);
                currentAnalysis = response.analysis;
                displayAnalysis(currentAnalysis);
            } else if (response && response.error) {
                console.error('Analysis error:', response.error);
                showError(response.error);
            } else {
                // No analysis found, show error
                console.log('No analysis found');
                showError('Analysis not available for this page');
            }
        });
    } catch (error) {
        console.error('Error in checkForAnalysis:', error);
        showError('Unable to check analysis');
    }
}

function triggerAnalysis(tabId) {
    try {
        // Check if content script is available first
        chrome.tabs.sendMessage(tabId, {action: 'ping'}, function(response) {
            if (chrome.runtime.lastError) {
                console.log('Content script not ready, injecting...');
                // Inject content script if not available
                chrome.scripting.executeScript({
                    target: {tabId: tabId},
                    files: ['content.js']
                }, function() {
                    if (chrome.runtime.lastError) {
                        console.error('Failed to inject content script:', chrome.runtime.lastError);
                        showError('Unable to analyze this page');
                    } else {
                        // Try analysis again after injection
                        setTimeout(() => {
                            performAnalysis(tabId);
                        }, 500);
                    }
                });
            } else {
                // Content script is ready, perform analysis
                performAnalysis(tabId);
            }
        });
    } catch (error) {
        console.error('Error in triggerAnalysis:', error);
        showError('Unable to trigger analysis');
    }
}

function performAnalysis(tabId) {
    try {
        chrome.tabs.sendMessage(tabId, {action: 'analyzeCurrentPage'}, function(response) {
            if (chrome.runtime.lastError) {
                console.error('Analysis error:', chrome.runtime.lastError);
                showError('Unable to analyze this page');
            } else if (response && response.error) {
                console.error('Analysis error:', response.error);
                showError(response.error);
            } else if (response) {
                console.log('Analysis triggered:', response);
                
                // Check for results immediately
                setTimeout(() => {
                    checkForAnalysis(tabId);
                }, 1000);
            } else {
                console.log('No response from content script');
                showError('Unable to analyze this page');
            }
        });
    } catch (error) {
        console.error('Error in performAnalysis:', error);
        showError('Analysis failed');
    }
}

function displayAnalysis(analysis) {
    try {
        // Hide loading and error states
        const loadingElement = document.getElementById('loading');
        const errorElement = document.getElementById('error');
        const analysisElement = document.getElementById('analysis');
        
        if (loadingElement) loadingElement.style.display = 'none';
        if (errorElement) errorElement.style.display = 'none';
        if (analysisElement) analysisElement.style.display = 'block';
        
        // Display current URL from address bar
        const currentUrl = analysis.url || 'Unknown URL';
        console.log('🌐 Displaying analysis for URL from address bar:', currentUrl);
        
        // Show the URL in the popup
        const urlElement = document.getElementById('current-url');
        if (urlElement) {
            urlElement.textContent = currentUrl;
        }
        
        // Display risk score
        const riskScore = analysis.risk_score || 0;
        const recommendation = analysis.recommendation || 'Unknown';
        
        const riskNumberElement = document.getElementById('risk-number');
        const riskLabelElement = document.getElementById('risk-label');
        const riskDescriptionElement = document.getElementById('risk-description');
        
        if (riskNumberElement) riskNumberElement.textContent = riskScore;
        if (riskLabelElement) riskLabelElement.textContent = recommendation;
        
        // Set risk color
        if (riskLabelElement) {
            riskLabelElement.className = 'risk-label';
            
            if (riskScore >= 8) {
                riskLabelElement.classList.add('risk-dangerous');
                if (riskDescriptionElement) riskDescriptionElement.textContent = 'Critical privacy concerns detected';
            } else if (riskScore >= 6) {
                riskLabelElement.classList.add('risk-caution');
                if (riskDescriptionElement) riskDescriptionElement.textContent = 'Significant privacy concerns';
            } else if (riskScore >= 4) {
                riskLabelElement.classList.add('risk-moderate');
                if (riskDescriptionElement) riskDescriptionElement.textContent = 'Some privacy concerns';
            } else {
                riskLabelElement.classList.add('risk-safe');
                if (riskDescriptionElement) riskDescriptionElement.textContent = 'Good privacy practices';
            }
        }
        
        // Display recommendation reason
        const recommendationReason = analysis.recommendation_reason || 'Analysis complete';
        const reasonElement = document.getElementById('recommendation-reason');
        if (reasonElement) {
            reasonElement.textContent = recommendationReason;
        }
        
        // Display features used
        if (analysis.features_used) {
            const featuresContainer = document.getElementById('features-list');
            const featuresUsedElement = document.getElementById('features-used');
            
            if (featuresContainer) {
                featuresContainer.innerHTML = '';
                
                analysis.features_used.forEach(feature => {
                    const featureTag = document.createElement('span');
                    featureTag.className = 'feature-tag';
                    featureTag.textContent = feature;
                    featuresContainer.appendChild(featureTag);
                });
            }
            
            if (featuresUsedElement) {
                featuresUsedElement.style.display = 'block';
            }
        }
        
        // Display analysis summary
        const summary = analysis.summary || 'Analysis completed';
        const summaryElement = document.getElementById('analysis-summary');
        if (summaryElement) {
            summaryElement.textContent = summary;
        }
        
        // Display student-friendly summary
        const studentSummary = analysis.student_summary || 'Student summary not available';
        const studentSummaryElement = document.getElementById('student-summary');
        if (studentSummaryElement) {
            studentSummaryElement.textContent = studentSummary;
        }
        
        // Display privacy threats
        const privacyThreats = analysis.privacy_threats || [];
        const threatsContainer = document.getElementById('privacy-threats');
        
        if (threatsContainer) {
            if (privacyThreats.length > 0) {
                threatsContainer.innerHTML = '';
                privacyThreats.forEach(threat => {
                    const threatElement = document.createElement('div');
                    threatElement.className = 'threat-item';
                    threatElement.textContent = threat;
                    threatsContainer.appendChild(threatElement);
                });
            } else {
                threatsContainer.innerHTML = '<div class="detail-item">No privacy threats detected</div>';
            }
        }
        
        // Display detailed risk metrics
        if (analysis.detailed_metrics) {
            const metrics = analysis.detailed_metrics;
            const detailedAnalysis = analysis.detailed_analysis || {};
            
            // Update metric values
            const metricElements = {
                'data-monetization': detailedAnalysis.data_monetization_risk || 'Low',
                'sensitive-data': detailedAnalysis.sensitive_data_risk || 'Low',
                'behavioral-tracking': detailedAnalysis.tracking_risk || 'Low',
                'legal-concerns': detailedAnalysis.legal_risk || 'Low',
                'data-retention': detailedAnalysis.retention_risk || 'Low',
                'third-party': detailedAnalysis.third_party_risk || 'Low',
                'international': detailedAnalysis.international_risk || 'Low',
                'form-risks': detailedAnalysis.form_risk || 'Low'
            };
            
            Object.keys(metricElements).forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    element.textContent = metricElements[id];
                    element.className = 'metric-value';
                    
                    // Add risk color class
                    const riskLevel = metricElements[id].toLowerCase();
                    if (riskLevel === 'critical') {
                        element.classList.add('risk-critical');
                    } else if (riskLevel === 'high') {
                        element.classList.add('risk-high');
                    } else if (riskLevel === 'medium') {
                        element.classList.add('risk-medium');
                    } else {
                        element.classList.add('risk-low');
                    }
                }
            });
        }
        
        // Display form analysis
        const forms = analysis.forms || [];
        const totalFields = forms.reduce((count, form) => count + (form.fields ? form.fields.length : 0), 0);
        const sensitiveFields = forms.reduce((count, form) => {
            return count + (form.fields ? form.fields.filter(f => f.sensitive).length : 0);
        }, 0);
        
        const formAnalysis = `Found ${forms.length} forms with ${totalFields} fields (${sensitiveFields} sensitive)`;
        const formAnalysisElement = document.getElementById('form-analysis');
        if (formAnalysisElement) {
            formAnalysisElement.textContent = formAnalysis;
        }
        
        // Update badge
        updateBadge(riskScore);
    } catch (error) {
        console.error('Error in displayAnalysis:', error);
        showError('Error displaying analysis results');
    }
}

function displayPrivacyLinks(links) {
    try {
        if (links && links.length > 0) {
            const linksContainer = document.getElementById('links-list');
            const privacyLinksElement = document.getElementById('privacy-links');
            
            if (linksContainer) {
                linksContainer.innerHTML = '';
                
                links.forEach(link => {
                    if (link && link.href) {
                        const linkElement = document.createElement('a');
                        linkElement.className = 'link-item';
                        linkElement.href = link.href;
                        linkElement.textContent = `${link.text || 'Link'} (${link.type || 'unknown'})`;
                        linkElement.target = '_blank';
                        linksContainer.appendChild(linkElement);
                    }
                });
            }
            
            if (privacyLinksElement) {
                privacyLinksElement.style.display = 'block';
            }
        }
    } catch (error) {
        console.error('Error in displayPrivacyLinks:', error);
    }
}

function showError(message) {
    try {
        const loadingElement = document.getElementById('loading');
        const analysisElement = document.getElementById('analysis');
        const errorElement = document.getElementById('error');
        const errorMessageElement = document.getElementById('error-message');
        
        if (loadingElement) loadingElement.style.display = 'none';
        if (analysisElement) analysisElement.style.display = 'none';
        if (errorElement) errorElement.style.display = 'block';
        if (errorMessageElement) errorMessageElement.textContent = message;
        
        // Auto-retry after 5 seconds
        setTimeout(() => {
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                if (tabs[0]) {
                    triggerAnalysis(tabs[0].id);
                }
            });
        }, 5000);
    } catch (error) {
        console.error('Error in showError:', error);
    }
}

function retryAnalysis() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        if (tabs[0]) {
            const loadingElement = document.getElementById('loading');
            const errorElement = document.getElementById('error');
            const analysisElement = document.getElementById('analysis');
            
            if (loadingElement) loadingElement.style.display = 'block';
            if (errorElement) errorElement.style.display = 'none';
            if (analysisElement) analysisElement.style.display = 'none';
            
            triggerAnalysis(tabs[0].id);
        }
    });
}

function refreshAnalysis() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        if (tabs[0]) {
            const loadingElement = document.getElementById('loading');
            const analysisElement = document.getElementById('analysis');
            
            if (loadingElement) loadingElement.style.display = 'block';
            if (analysisElement) analysisElement.style.display = 'none';
            
            triggerAnalysis(tabs[0].id);
        }
    });
}

function openCurrentPage() {
    try {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs[0]) {
                chrome.tabs.update(tabs[0].id, {active: true});
                window.close();
            } else {
                console.error('No active tab found');
            }
        });
    } catch (error) {
        console.error('Error in openCurrentPage:', error);
    }
}

function updateBadge(riskScore) {
    try {
        // Send message to background script to update badge
        chrome.runtime.sendMessage({
            action: 'updateBadge',
            riskScore: riskScore || 0
        }, function(response) {
            if (chrome.runtime.lastError) {
                console.error('Error updating badge:', chrome.runtime.lastError);
            }
        });
    } catch (error) {
        console.error('Error in updateBadge:', error);
    }
}

// Handle window focus to refresh analysis
window.addEventListener('focus', function() {
    try {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs[0]) {
                checkForAnalysis(tabs[0].id);
            }
        });
    } catch (error) {
        console.error('Error in window focus handler:', error);
    }
}); 