// ShadowLens Background Script
console.log('🔒 ShadowLens: Background script loaded');

// Handle extension installation with comprehensive error handling
chrome.runtime.onInstalled.addListener(() => {
    try {
        console.log('🔒 ShadowLens: Extension installed');
        
        // Set default badge with error handling
        try {
            chrome.action.setBadgeText({ text: '🔒' }, function() {
                if (chrome.runtime.lastError) {
                    console.error('Error setting default badge text:', chrome.runtime.lastError);
                }
            });
        } catch (badgeTextError) {
            console.error('Error setting badge text:', badgeTextError);
        }
        
        try {
            chrome.action.setBadgeBackgroundColor({ color: '#667eea' }, function() {
                if (chrome.runtime.lastError) {
                    console.error('Error setting default badge color:', chrome.runtime.lastError);
                }
            });
        } catch (badgeColorError) {
            console.error('Error setting badge color:', badgeColorError);
        }
    } catch (error) {
        console.error('Error in installation handler:', error);
    }
});

// Handle messages from popup and content scripts with comprehensive error handling
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    try {
        if (!request) {
            console.error('Received null or undefined request');
            sendResponse({ error: 'Invalid request' });
            return true;
        }
        
        console.log('Background received message:', request);
        
        if (request.action === 'updateBadge') {
            try {
                updateBadge(request.riskScore);
                sendResponse({ success: true });
            } catch (badgeError) {
                console.error('Error updating badge:', badgeError);
                sendResponse({ error: 'Failed to update badge' });
            }
            return true; // Keep message channel open
        } else if (request.action === 'getAnalysis') {
            try {
                // Forward to content script with error handling
                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    try {
                        if (tabs && tabs[0]) {
                            chrome.tabs.sendMessage(tabs[0].id, request, (response) => {
                                try {
                                    if (chrome.runtime.lastError) {
                                        console.error('Error forwarding message:', chrome.runtime.lastError);
                                        sendResponse({ error: 'Content script not available' });
                                    } else {
                                        sendResponse(response || { error: 'No response from content script' });
                                    }
                                } catch (responseError) {
                                    console.error('Error handling response:', responseError);
                                    sendResponse({ error: 'Error processing response' });
                                }
                            });
                        } else {
                            sendResponse({ error: 'No active tab found' });
                        }
                    } catch (queryError) {
                        console.error('Error querying tabs:', queryError);
                        sendResponse({ error: 'Error accessing tabs' });
                    }
                });
            } catch (forwardError) {
                console.error('Error forwarding message:', forwardError);
                sendResponse({ error: 'Error forwarding message' });
            }
            return true; // Keep message channel open
        } else {
            console.log('Unknown action:', request.action);
            sendResponse({ error: 'Unknown action' });
            return true;
        }
    } catch (error) {
        console.error('Error in background message listener:', error);
        try {
            sendResponse({ error: error.message || 'Unknown error' });
        } catch (sendError) {
            console.error('Error sending error response:', sendError);
        }
        return true; // Keep message channel open
    }
});

function updateBadge(riskScore) {
    try {
        if (typeof riskScore !== 'number' || isNaN(riskScore)) {
            console.warn('Invalid risk score:', riskScore);
            riskScore = 0;
        }
        
        let badgeText = '🔒';
        let badgeColor = '#667eea';
        
        if (riskScore >= 8) {
            badgeText = '🔴';
            badgeColor = '#f44336';
        } else if (riskScore >= 6) {
            badgeText = '🟠';
            badgeColor = '#FF9800';
        } else if (riskScore >= 4) {
            badgeText = '🟡';
            badgeColor = '#FFC107';
        } else {
            badgeText = '🟢';
            badgeColor = '#4CAF50';
        }
        
        try {
            chrome.action.setBadgeText({ text: badgeText }, function() {
                if (chrome.runtime.lastError) {
                    console.error('Error setting badge text:', chrome.runtime.lastError);
                }
            });
        } catch (badgeTextError) {
            console.error('Error setting badge text:', badgeTextError);
        }
        
        try {
            chrome.action.setBadgeBackgroundColor({ color: badgeColor }, function() {
                if (chrome.runtime.lastError) {
                    console.error('Error setting badge color:', chrome.runtime.lastError);
                }
            });
        } catch (badgeColorError) {
            console.error('Error setting badge color:', badgeColorError);
        }
    } catch (error) {
        console.error('Error in updateBadge:', error);
    }
}

// Handle tab updates to trigger analysis with comprehensive error handling
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    try {
        if (!changeInfo || !tab) {
            console.warn('Invalid tab update event');
            return;
        }
        
        if (changeInfo.status === 'complete' && tab.url) {
            try {
                // Check if this is a supported website
                const supportedPatterns = [
                    /.*\.edu.*/,
                    /.*\.school.*/,
                    /.*\.education.*/,
                    /.*khanacademy\.org.*/,
                    /.*duolingo\.com.*/,
                    /.*coursera\.org.*/,
                    /.*edx\.org.*/,
                    /.*privacy.*/,
                    /.*terms.*/,
                    /.*policy.*/
                ];
                
                const isSupported = supportedPatterns.some(pattern => {
                    try {
                        return pattern.test(tab.url);
                    } catch (patternError) {
                        console.error('Error testing pattern:', patternError);
                        return false;
                    }
                });
                
                if (isSupported) {
                    console.log('🔒 ShadowLens: Supported website detected, ready for analysis');
                    // The content script will automatically detect and analyze
                }
            } catch (patternError) {
                console.error('Error checking supported patterns:', patternError);
            }
        }
    } catch (error) {
        console.error('Error in tab update listener:', error);
    }
});

// Handle extension icon click with comprehensive error handling
chrome.action.onClicked.addListener((tab) => {
    try {
        console.log('🔒 ShadowLens: Extension icon clicked');
        
        if (tab && tab.url) {
            try {
                chrome.tabs.sendMessage(tab.id, { action: 'analyzeCurrentPage' }, function(response) {
                    try {
                        if (chrome.runtime.lastError) {
                            console.error('Error sending message to tab:', chrome.runtime.lastError);
                        }
                    } catch (responseError) {
                        console.error('Error handling response:', responseError);
                    }
                });
            } catch (sendError) {
                console.error('Error sending message to tab:', sendError);
            }
        } else {
            console.warn('No valid tab or URL for analysis');
        }
    } catch (error) {
        console.error('Error in extension icon click handler:', error);
    }
});

// Handle storage changes with comprehensive error handling
chrome.storage.onChanged.addListener((changes, namespace) => {
    try {
        if (namespace === 'local' && changes) {
            console.log('🔒 ShadowLens: Storage changed:', changes);
        }
    } catch (error) {
        console.error('Error in storage change listener:', error);
    }
}); 