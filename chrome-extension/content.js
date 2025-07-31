// ShadowLens Content Script - Enhanced with Dashboard Integration
let currentAnalysis = null;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔒 ShadowLens Content Script: Initializing...');
    
    // Get current URL from address bar and analyze
    const currentUrl = window.location.href;
    console.log('🌐 Current URL from address bar:', currentUrl);
    
    // Analyze immediately for faster response
    analyzeCurrentPage();
});

// Simple URL change detection
let lastUrl = window.location.href;
new MutationObserver(() => {
    const url = window.location.href;
    if (url !== lastUrl) {
        lastUrl = url;
        analyzeCurrentPage();
    }
}).observe(document, {subtree: true, childList: true});

// Removed unused functions for cleaner code

function analyzeCurrentPage() {
    try {
        console.log('🔍 Starting page analysis...');
        
        // Get URL directly from address bar with error handling
        let currentUrl = '';
        try {
            currentUrl = window.location.href;
            console.log('🌐 Analyzing URL from address bar:', currentUrl);
        } catch (urlError) {
            console.error('Error getting URL:', urlError);
            currentUrl = 'unknown';
        }
        
        // Quick analysis for immediate response with error handling
        let pageText = '';
        try {
            pageText = document.body ? document.body.innerText : '';
        } catch (textError) {
            console.error('Error getting page text:', textError);
            pageText = '';
        }
        
        // Collect analysis data with individual error handling
        const analysisData = {
            url: currentUrl,
            text: '',
            forms: [],
            riskIndicators: [],
            websiteType: 'general'
        };
        
        // Extract text with error handling
        try {
            analysisData.text = extractPageText();
        } catch (textError) {
            console.error('Error extracting page text:', textError);
            analysisData.text = '';
        }
        
        // Extract forms with error handling
        try {
            analysisData.forms = extractForms();
        } catch (formsError) {
            console.error('Error extracting forms:', formsError);
            analysisData.forms = [];
        }
        
        // Detect risk indicators with error handling
        try {
            analysisData.riskIndicators = detectRiskIndicators();
        } catch (riskError) {
            console.error('Error detecting risk indicators:', riskError);
            analysisData.riskIndicators = [];
        }
        
        // Detect website type with error handling
        try {
            analysisData.websiteType = detectWebsiteType(currentUrl, pageText);
        } catch (typeError) {
            console.error('Error detecting website type:', typeError);
            analysisData.websiteType = 'general';
        }
        
        console.log('📊 Analysis data collected:', analysisData);
        
        // Perform immediate local analysis with error handling
        let analysis = null;
        try {
            analysis = performLocalAnalysis(analysisData);
            console.log('✅ Local analysis complete:', analysis);
        } catch (analysisError) {
            console.error('Error in local analysis:', analysisError);
            // Create fallback analysis
            analysis = {
                risk_score: 0,
                recommendation: 'Safe',
                recommendation_reason: 'Analysis failed due to error',
                privacy_threats: [],
                websiteType: 'general',
                forms: [],
                detailed_metrics: {},
                total_threats: 0,
                critical_threats: 0,
                features_used: ['Error Recovery'],
                summary: 'Analysis failed due to error',
                student_summary: 'Unable to analyze this website',
                detailed_analysis: {}
            };
        }
        
        currentAnalysis = analysis;
        
        // Save to Chrome storage with error handling
        try {
            saveAnalysisToStorage(analysis);
        } catch (storageError) {
            console.error('Error saving to storage:', storageError);
        }
        
        // Notify popup with error handling
        try {
            chrome.runtime.sendMessage({
                action: 'analysisComplete',
                analysis: analysis
            }, function(response) {
                if (chrome.runtime.lastError) {
                    console.error('Error sending analysis to popup:', chrome.runtime.lastError);
                }
            });
        } catch (messageError) {
            console.error('Error sending message to popup:', messageError);
        }
    } catch (error) {
        console.error('Critical error in analyzeCurrentPage:', error);
        // Send error to popup with error handling
        try {
            chrome.runtime.sendMessage({
                action: 'analysisError',
                error: error.message || 'Unknown error occurred'
            }, function(response) {
                if (chrome.runtime.lastError) {
                    console.error('Error sending error to popup:', chrome.runtime.lastError);
                }
            });
        } catch (sendError) {
            console.error('Error sending error message:', sendError);
        }
    }
}

function extractPageText() {
    try {
        // Faster text extraction - only key elements
        const textElements = document.querySelectorAll('p, h1, h2, h3, title, meta[name="description"]');
        let text = '';
        
        textElements.forEach(element => {
            if (element && element.textContent && element.textContent.trim()) {
                text += element.textContent.trim() + ' ';
            }
        });
        
        return text.substring(0, 2000); // Shorter text for faster processing
    } catch (error) {
        console.error('Error extracting page text:', error);
        return '';
    }
}

function extractForms() {
    try {
        const forms = [];
        const formElements = document.querySelectorAll('form');
        
        formElements.forEach((form, index) => {
            if (form) {
                const fields = [];
                const inputs = form.querySelectorAll('input, select, textarea');
                
                inputs.forEach(input => {
                    if (input) {
                        const field = {
                            name: input.name || input.id || `field_${index}`,
                            type: input.type || input.tagName.toLowerCase(),
                            sensitive: isSensitiveField(input)
                        };
                        fields.push(field);
                    }
                });
                
                forms.push({
                    action: form.action || '',
                    method: form.method || 'get',
                    fields: fields
                });
            }
        });
        
        return forms;
    } catch (error) {
        console.error('Error extracting forms:', error);
        return [];
    }
}

function isSensitiveField(input) {
        const sensitivePatterns = [
        'password', 'passwd', 'pwd', 'secret', 'key',
        'ssn', 'social', 'security', 'id', 'passport',
        'card', 'credit', 'payment', 'paypal', 'stripe',
        'account', 'login', 'email', 'phone', 'mobile'
    ];
    
    const fieldName = (input.name || input.id || '').toLowerCase();
    const fieldType = (input.type || '').toLowerCase();
    
    return sensitivePatterns.some(pattern => 
        fieldName.includes(pattern) || fieldType.includes(pattern)
    );
}

function extractImages() {
        const images = [];
        const imgElements = document.querySelectorAll('img');
        
        imgElements.forEach(img => {
        if (img.src) {
                images.push({
                src: img.src,
                    alt: img.alt || '',
                width: img.width || 0,
                height: img.height || 0
                });
            }
        });
        
        return images;
    }

function detectRiskIndicators() {
    try {
        const indicators = [];
        const text = document.body ? document.body.innerText.toLowerCase() : '';
        const url = window.location.href.toLowerCase();
    
    // Advanced Privacy Risk Categories
    
    // 1. Data Monetization Indicators
    const dataMonetizationTerms = [
        'sell your data', 'data brokers', 'third party advertising',
        'advertising partners', 'marketing partners', 'data sharing',
        'revenue sharing', 'data licensing', 'user profiling',
        'behavioral tracking', 'cross-site tracking', 'fingerprinting'
    ];
    
    dataMonetizationTerms.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'data_monetization',
                term: term,
                risk: 'high',
                category: 'Data Monetization',
                description: 'Website may sell or share your personal data with third parties'
            });
        }
    });
    
    // 2. Sensitive Data Collection
    const sensitiveDataTerms = [
        'social security number', 'ssn', 'government id', 'passport',
        'credit card', 'debit card', 'bank account', 'routing number',
        'medical information', 'health records', 'biometric data',
        'location tracking', 'gps coordinates', 'precise location'
    ];
    
    sensitiveDataTerms.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'sensitive_data',
                term: term,
                risk: 'critical',
                category: 'Sensitive Data Collection',
                description: 'Website collects highly sensitive personal information'
            });
        }
    });
    
    // 3. Behavioral Tracking
    const trackingTerms = [
        'cookies', 'tracking pixels', 'web beacons', 'analytics',
        'user behavior', 'click tracking', 'mouse movements',
        'keystroke logging', 'session recording', 'heat mapping'
    ];
    
    trackingTerms.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'behavioral_tracking',
                term: term,
                risk: 'medium',
                category: 'Behavioral Tracking',
                description: 'Website tracks your behavior and interactions'
            });
        }
    });
    
    // 4. Legal Red Flags
    const legalRedFlags = [
        'disclaim all liability', 'not responsible', 'use at your own risk',
        'no warranty', 'as is', 'without limitation', 'broad rights',
        'irrevocable license', 'perpetual rights', 'sub-license'
    ];
    
    legalRedFlags.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'legal_red_flags',
                term: term,
                risk: 'high',
                category: 'Legal Concerns',
                description: 'Concerning legal terms that limit your rights'
            });
        }
    });
    
    // 5. Data Retention Issues
    const retentionTerms = [
        'indefinite retention', 'permanent storage', 'data retention',
        'archived data', 'backup storage', 'long-term storage'
    ];
    
    retentionTerms.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'data_retention',
                term: term,
                risk: 'medium',
                category: 'Data Retention',
                description: 'Website may retain your data indefinitely'
            });
        }
    });
    
    // 6. Third-Party Access
    const thirdPartyTerms = [
        'third party access', 'service providers', 'partners',
        'affiliates', 'subcontractors', 'data processors'
    ];
    
    thirdPartyTerms.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'third_party_access',
                term: term,
                risk: 'medium',
                category: 'Third-Party Access',
                description: 'Third parties may access your data'
            });
        }
    });
    
    // 7. International Data Transfer
    const internationalTerms = [
        'international transfer', 'cross-border', 'global processing',
        'eu data', 'gdpr compliance', 'international servers'
    ];
    
    internationalTerms.forEach(term => {
        if (text.includes(term)) {
            indicators.push({
                type: 'international_transfer',
                term: term,
                risk: 'medium',
                category: 'International Data Transfer',
                description: 'Data may be transferred internationally'
            });
        }
    });
    
    return indicators;
    } catch (error) {
        console.error('Error in detectRiskIndicators:', error);
        return [];
    }
}

function detectWebsiteType(url, text) {
    try {
        const urlLower = (url || '').toLowerCase();
        const textLower = (text || '').toLowerCase();
        
        // Social media detection
        if (urlLower.includes('facebook') || urlLower.includes('instagram') || 
            urlLower.includes('twitter') || urlLower.includes('linkedin')) {
            return 'social_media';
        }
        
        // Educational detection
        if (urlLower.includes('coursera') || urlLower.includes('edx') || 
            urlLower.includes('khanacademy') || urlLower.includes('udemy') ||
            textLower.includes('course') || textLower.includes('learn') || 
            textLower.includes('education')) {
            return 'educational';
        }
        
        // Financial detection
        if (urlLower.includes('bank') || urlLower.includes('paypal') || 
            urlLower.includes('stripe') || textLower.includes('payment') ||
            textLower.includes('credit') || textLower.includes('financial')) {
            return 'financial';
        }

        // E-commerce detection
        if (urlLower.includes('amazon') || urlLower.includes('ebay') || 
            urlLower.includes('shop') || textLower.includes('buy') ||
            textLower.includes('purchase') || textLower.includes('cart')) {
            return 'ecommerce';
        }
        
        return 'general';
    } catch (error) {
        console.error('Error in detectWebsiteType:', error);
        return 'general';
    }
}

function detectDocumentType(url, text) {
    try {
        const urlLower = (url || '').toLowerCase();
        const textLower = (text || '').toLowerCase();
        
        if (urlLower.includes('privacy') || textLower.includes('privacy policy')) {
            return 'privacy_policy';
        }
        
        if (urlLower.includes('terms') || textLower.includes('terms of service')) {
            return 'terms_of_service';
        }
        
        if (urlLower.includes('policy') || textLower.includes('policy')) {
            return 'policy';
        }
        
        return 'general';
    } catch (error) {
        console.error('Error in detectDocumentType:', error);
        return 'general';
    }
}

// Removed sendToBackend function - using direct local analysis

function performLocalAnalysis(data) {
    try {
        const riskIndicators = data.riskIndicators || [];
        const forms = data.forms || [];
        const websiteType = data.websiteType || 'general';
    
    // Advanced risk calculation with detailed metrics
    let riskScore = 0;
    let privacyThreats = [];
    let detailedMetrics = {
        dataMonetization: 0,
        sensitiveData: 0,
        behavioralTracking: 0,
        legalRedFlags: 0,
        dataRetention: 0,
        thirdPartyAccess: 0,
        internationalTransfer: 0,
        formRisks: 0
    };
    
    // Base score by website type
    switch(websiteType) {
        case 'social_media': riskScore = 4; break;
        case 'financial': riskScore = 5; break;
        case 'ecommerce': riskScore = 3; break;
        case 'educational': riskScore = 2; break;
        default: riskScore = 1;
    }
    
    // Advanced risk indicator analysis
    riskIndicators.forEach(indicator => {
        let points = 0;
        let threatDescription = '';
        
        switch(indicator.type) {
            case 'data_monetization':
                points = 3;
                detailedMetrics.dataMonetization++;
                threatDescription = `Data Monetization: ${indicator.description}`;
                break;
            case 'sensitive_data':
                points = 4;
                detailedMetrics.sensitiveData++;
                threatDescription = `Sensitive Data: ${indicator.description}`;
                break;
            case 'behavioral_tracking':
                points = 2;
                detailedMetrics.behavioralTracking++;
                threatDescription = `Behavioral Tracking: ${indicator.description}`;
                break;
            case 'legal_red_flags':
                points = 3;
                detailedMetrics.legalRedFlags++;
                threatDescription = `Legal Concerns: ${indicator.description}`;
                break;
            case 'data_retention':
                points = 2;
                detailedMetrics.dataRetention++;
                threatDescription = `Data Retention: ${indicator.description}`;
                break;
            case 'third_party_access':
                points = 2;
                detailedMetrics.thirdPartyAccess++;
                threatDescription = `Third-Party Access: ${indicator.description}`;
                break;
            case 'international_transfer':
                points = 2;
                detailedMetrics.internationalTransfer++;
                threatDescription = `International Transfer: ${indicator.description}`;
                break;
        }
        
        riskScore += points;
        privacyThreats.push(threatDescription);
    });
    
    // Form analysis with detailed metrics
    const sensitiveFields = forms.reduce((sum, form) => 
        sum + (form.fields ? form.fields.filter(f => f.sensitive).length : 0), 0);
    if (sensitiveFields > 0) {
        riskScore += Math.min(sensitiveFields, 3);
        detailedMetrics.formRisks = sensitiveFields;
    }
    
    // Cap risk score
    riskScore = Math.min(riskScore, 10);
    
    // Determine recommendation with detailed reasoning
    let recommendation = 'Safe';
    let recommendationReason = 'No significant privacy concerns detected';
    
    if (riskScore >= 8) {
        recommendation = 'Dangerous';
        recommendationReason = 'Multiple critical privacy risks detected';
    } else if (riskScore >= 6) {
        recommendation = 'Caution';
        recommendationReason = 'Several privacy concerns that require attention';
    } else if (riskScore >= 4) {
        recommendation = 'Moderate';
        recommendationReason = 'Some privacy concerns to be aware of';
    }
    
    // Generate detailed analysis summary
    const totalThreats = Object.values(detailedMetrics).reduce((sum, val) => sum + val, 0);
    const criticalThreats = detailedMetrics.sensitiveData + detailedMetrics.dataMonetization;
    
    return {
        risk_score: riskScore,
        recommendation: recommendation,
        recommendation_reason: recommendationReason,
        privacy_threats: privacyThreats,
        websiteType: websiteType,
        forms: forms,
        detailed_metrics: detailedMetrics,
        total_threats: totalThreats,
        critical_threats: criticalThreats,
        features_used: ['Advanced Privacy Analysis', 'Detailed Risk Metrics', 'Comprehensive Threat Detection'],
        summary: `Analysis of ${websiteType} website with ${totalThreats} privacy threats (${criticalThreats} critical)`,
        student_summary: riskScore <= 3 ? 'This website appears to have good privacy practices' : 
                        riskScore <= 5 ? 'This website has some privacy concerns to be aware of' :
                        'This website has significant privacy concerns - proceed with caution',
        detailed_analysis: {
            data_monetization_risk: detailedMetrics.dataMonetization > 0 ? 'High' : 'Low',
            sensitive_data_risk: detailedMetrics.sensitiveData > 0 ? 'Critical' : 'Low',
            tracking_risk: detailedMetrics.behavioralTracking > 0 ? 'Medium' : 'Low',
            legal_risk: detailedMetrics.legalRedFlags > 0 ? 'High' : 'Low',
            retention_risk: detailedMetrics.dataRetention > 0 ? 'Medium' : 'Low',
            third_party_risk: detailedMetrics.thirdPartyAccess > 0 ? 'Medium' : 'Low',
            international_risk: detailedMetrics.internationalTransfer > 0 ? 'Medium' : 'Low',
            form_risk: detailedMetrics.formRisks > 0 ? 'Medium' : 'Low'
        }
    };
    } catch (error) {
        console.error('Error in performLocalAnalysis:', error);
        return {
            risk_score: 0,
            recommendation: 'Safe',
            recommendation_reason: 'Analysis failed',
            privacy_threats: [],
            websiteType: 'general',
            forms: [],
            detailed_metrics: {},
            total_threats: 0,
            critical_threats: 0,
            features_used: ['Error Recovery'],
            summary: 'Analysis failed due to error',
            student_summary: 'Unable to analyze this website',
            detailed_analysis: {}
        };
    }
}

function saveAnalysisToStorage(analysis) {
    try {
        if (!analysis) {
            console.error('No analysis data to save');
            return;
        }
        
        // Get existing history
        chrome.storage.local.get(['websiteHistory'], function(result) {
            if (chrome.runtime.lastError) {
                console.error('Error getting storage:', chrome.runtime.lastError);
                return;
            }
            
            let history = result.websiteHistory || [];
            
            // Add new analysis
            const newEntry = {
                url: window.location.href,
                timestamp: new Date().toISOString(),
                riskScore: analysis.risk_score || 0,
                recommendation: analysis.recommendation || 'Unknown',
                privacyThreats: analysis.privacy_threats || [],
                forms: analysis.forms ? analysis.forms.length : 0,
                sensitiveFields: analysis.forms ? analysis.forms.reduce((sum, form) => 
                    sum + (form.fields ? form.fields.filter(f => f.sensitive).length : 0), 0) : 0,
                websiteType: analysis.websiteType || 'general',
                analysis: analysis
            };
            
            // Add to beginning of history
            history.unshift(newEntry);
                
            // Keep only last 100 entries
            if (history.length > 100) {
                history = history.slice(0, 100);
            }
                
            // Save to storage
            chrome.storage.local.set({ websiteHistory: history }, function() {
                if (chrome.runtime.lastError) {
                    console.error('Error saving to storage:', chrome.runtime.lastError);
                } else {
                    console.log('💾 Analysis saved to storage');
                }
            });
        });
    } catch (error) {
        console.error('Error in saveAnalysisToStorage:', error);
    }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    try {
        if (message.action === 'ping') {
            // Respond to ping to confirm content script is ready
            sendResponse({ status: 'ready' });
            return true; // Keep message channel open
        } else if (message.action === 'getAnalysis') {
            sendResponse({ analysis: currentAnalysis });
            return true; // Keep message channel open
        } else if (message.action === 'analyzeCurrentPage') {
            analyzeCurrentPage();
            sendResponse({ status: 'analysis_started' });
            return true; // Keep message channel open
        } else if (message.action === 'getCurrentUrl') {
            // Get URL directly from address bar
            const currentUrl = window.location.href;
            console.log('🌐 Getting URL from address bar:', currentUrl);
            sendResponse({ url: currentUrl });
            return true; // Keep message channel open
        }
    } catch (error) {
        console.error('Error in message listener:', error);
        sendResponse({ error: error.message });
        return true; // Keep message channel open
    }
});

console.log('🔒 ShadowLens Content Script: Ready!'); 