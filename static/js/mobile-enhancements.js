// ==================== ADVANCED MOBILE ENHANCEMENTS ====================

/**
 * This file adds advanced mobile and touch features to enhance the user experience
 * Features include: swipe navigation, gesture support, improved touch feedback, 
 * and advanced mobile optimizations
 */

// ==================== SWIPE DETECTION ====================
class SwipeDetector {
    constructor(element, callbacks = {}) {
        this.element = element;
        this.startX = 0;
        this.startY = 0;
        this.endX = 0;
        this.endY = 0;
        this.minSwipeDistance = 50;
        
        this.callbacks = {
            onSwipeLeft: callbacks.onSwipeLeft || (() => {}),
            onSwipeRight: callbacks.onSwipeRight || (() => {}),
            onSwipeUp: callbacks.onSwipeUp || (() => {}),
            onSwipeDown: callbacks.onSwipeDown || (() => {})
        };
        
        this.init();
    }
    
    init() {
        this.element.addEventListener('touchstart', (e) => this.handleTouchStart(e), false);
        this.element.addEventListener('touchend', (e) => this.handleTouchEnd(e), false);
    }
    
    handleTouchStart(e) {
        this.startX = e.changedTouches[0].screenX;
        this.startY = e.changedTouches[0].screenY;
    }
    
    handleTouchEnd(e) {
        this.endX = e.changedTouches[0].screenX;
        this.endY = e.changedTouches[0].screenY;
        this.detectSwipe();
    }
    
    detectSwipe() {
        const diffX = this.startX - this.endX;
        const diffY = this.startY - this.endY;
        
        if (Math.abs(diffX) > Math.abs(diffY)) {
            // Horizontal swipe
            if (diffX > this.minSwipeDistance) {
                this.callbacks.onSwipeLeft();
            } else if (diffX < -this.minSwipeDistance) {
                this.callbacks.onSwipeRight();
            }
        } else {
            // Vertical swipe
            if (diffY > this.minSwipeDistance) {
                this.callbacks.onSwipeUp();
            } else if (diffY < -this.minSwipeDistance) {
                this.callbacks.onSwipeDown();
            }
        }
    }
}

// ==================== VIEWPORT HEIGHT OPTIMIZATION ====================
/**
 * Fixes the 100vh issue on mobile browsers that hide/show address bar
 * Mobile browsers calculate vh based on full viewport, causing overflow
 */
document.addEventListener('DOMContentLoaded', function() {
    // Set custom property for actual viewport height
    const setVH = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    };
    
    setVH();
    window.addEventListener('resize', setVH);
    window.addEventListener('orientationchange', setVH);
});

// ==================== PASSIVE EVENT LISTENERS ====================
/**
 * Improves scroll performance by using passive event listeners
 * Tells browser it can optimize scroll performance
 */
document.addEventListener('DOMContentLoaded', function() {
    let lastScrollY = 0;
    
    document.addEventListener('scroll', () => {
        lastScrollY = window.scrollY;
    }, { passive: true });
    
    // Add passive listeners to touch events
    document.addEventListener('touchstart', () => {}, { passive: true });
    document.addEventListener('touchmove', () => {}, { passive: true });
    document.addEventListener('wheel', () => {}, { passive: true });
});

// ==================== INTELLIGENT TOUCH FEEDBACK ====================
class TouchFeedback {
    constructor() {
        this.setupTouchFeedback();
    }
    
    setupTouchFeedback() {
        const buttons = document.querySelectorAll('button, a.btn, .btn, [role="button"]');
        
        buttons.forEach(button => {
            // Touch start effect
            button.addEventListener('touchstart', (e) => {
                this.addTouchEffect(button);
            }, { passive: true });
            
            // Touch end effect
            button.addEventListener('touchend', (e) => {
                this.removeTouchEffect(button);
            }, { passive: true });
            
            // Touch cancel (user cancels touch)
            button.addEventListener('touchcancel', (e) => {
                this.removeTouchEffect(button);
            }, { passive: true });
        });
    }
    
    addTouchEffect(element) {
        element.style.opacity = '0.7';
        element.style.transform = 'scale(0.98)';
    }
    
    removeTouchEffect(element) {
        element.style.opacity = '1';
        element.style.transform = 'scale(1)';
    }
}

// ==================== DOUBLE TAP DETECTION ====================
class DoubleTapDetector {
    constructor(element, callback) {
        this.element = element;
        this.callback = callback;
        this.lastTap = 0;
        this.touchTimeout;
        
        this.element.addEventListener('touchend', (e) => this.handleTap(e), false);
    }
    
    handleTap(e) {
        const currentTime = new Date().getTime();
        const tapLength = currentTime - this.lastTap;
        
        if (tapLength < 300 && tapLength > 0) {
            // Double tap detected
            e.preventDefault();
            this.callback();
        }
        
        this.lastTap = currentTime;
    }
}

// ==================== KEYBOARD VIEWPORT FIX ====================
/**
 * Prevents layout shift when mobile keyboard appears/disappears
 */
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            // Scroll input into view when keyboard appears
            setTimeout(() => {
                input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        });
    });
});

// ==================== ORIENTATION CHANGE HANDLER ====================
/**
 * Handles layout adjustments when device orientation changes
 */
document.addEventListener('DOMContentLoaded', function() {
    function handleOrientationChange() {
        // Close mobile menu on orientation change
        const navMenu = document.getElementById('navMenu');
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            const icon = document.querySelector('.mobile-menu-toggle i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
        
        // Reset scroll position
        window.scrollTo(0, 0);
    }
    
    window.addEventListener('orientationchange', handleOrientationChange);
});

// ==================== HAPTIC FEEDBACK (VIBRATION) ====================
/**
 * Provides vibration feedback on supported devices
 * Great for button clicks and interactions
 */
class HapticFeedback {
    static trigger(duration = 10) {
        if ('vibrate' in navigator) {
            navigator.vibrate(duration);
        }
    }
    
    static pattern(pattern = [50, 30, 50]) {
        if ('vibrate' in navigator) {
            navigator.vibrate(pattern);
        }
    }
}

// ==================== PREVENT ZOOM ON DOUBLE TAP ====================
/**
 * On newer devices, prevents accidental zoom while maintaining accessibility
 */
document.addEventListener('DOMContentLoaded', function() {
    let lastTouchEnd = 0;
    
    document.addEventListener('touchend', function(e) {
        const now = new Date().getTime();
        if (now - lastTouchEnd <= 300) {
            e.preventDefault();
        }
        lastTouchEnd = now;
    }, { passive: false });
});

// ==================== MOBILE BROWSER DETECTION ====================
class MobileDetect {
    static isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    static isTablet() {
        const ua = navigator.userAgent;
        return /(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua);
    }
    
    static isPhone() {
        return this.isMobile() && !this.isTablet();
    }
    
    static isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent);
    }
    
    static isAndroid() {
        return /Android/.test(navigator.userAgent);
    }
    
    static getViewportWidth() {
        return Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    }
    
    static getViewportHeight() {
        return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    }
}

// ==================== SAFE AREA DETECTION ====================
/**
 * Detects safe areas for notched devices (iPhone X+)
 */
document.addEventListener('DOMContentLoaded', function() {
    // CSS custom properties are already set in mobile-touch.css
    // This JS just logs for debugging if needed
    
    if (typeof CSS !== 'undefined' && CSS.supports('padding-top: env(safe-area-inset-top)')) {
        console.log('Device has safe area support (notched device)');
    }
});

// ==================== NETWORK STATUS DETECTION ====================
/**
 * Detects network connectivity and type
 */
class NetworkStatus {
    static isOnline() {
        return navigator.onLine;
    }
    
    static getConnectionType() {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        return connection ? connection.effectiveType : 'unknown';
    }
    
    static isFastConnection() {
        const type = this.getConnectionType();
        return ['4g'].includes(type);
    }
    
    static isSlowConnection() {
        const type = this.getConnectionType();
        return ['slow-2g', '2g', '3g'].includes(type);
    }
    
    static setupOnlineOfflineHandlers() {
        window.addEventListener('online', () => {
            console.log('Back online');
            // Show notification
            if (window.showNotification) {
                window.showNotification('Back online', 'success');
            }
        });
        
        window.addEventListener('offline', () => {
            console.log('Gone offline');
            // Show notification
            if (window.showNotification) {
                window.showNotification('You are offline', 'warning');
            }
        });
    }
}

// ==================== PERFORMANCE MONITORING ====================
/**
 * Monitors and logs performance metrics for mobile optimization
 */
class PerformanceMonitor {
    static logMetrics() {
        if (performance && performance.timing) {
            const timing = performance.timing;
            const metrics = {
                navigationStart: timing.navigationStart,
                firstPaint: timing.responseEnd - timing.navigationStart,
                DOMLoad: timing.domLoading - timing.navigationStart,
                pageLoad: timing.loadEventEnd - timing.navigationStart
            };
            
            console.log('Performance Metrics:', metrics);
        }
    }
    
    static getFirstContentfulPaint() {
        return new Promise((resolve) => {
            if ('PerformanceObserver' in window) {
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        console.log('FCP:', entry.startTime);
                        observer.disconnect();
                        resolve(entry.startTime);
                    }
                });
                observer.observe({ entryTypes: ['paint'] });
            }
        });
    }
}

// ==================== INITIALIZE MOBILE ENHANCEMENTS ====================
document.addEventListener('DOMContentLoaded', function() {
    // Initialize touch feedback
    const touchFeedback = new TouchFeedback();
    
    // Initialize network status monitoring
    NetworkStatus.setupOnlineOfflineHandlers();
    
    // Log performance metrics
    PerformanceMonitor.logMetrics();
    
    // Add mobile class to body if on mobile device
    if (MobileDetect.isMobile()) {
        document.body.classList.add('is-mobile');
    }
    
    if (MobileDetect.isTablet()) {
        document.body.classList.add('is-tablet');
    }
    
    if (MobileDetect.isIOS()) {
        document.body.classList.add('is-ios');
    }
    
    if (MobileDetect.isAndroid()) {
        document.body.classList.add('is-android');
    }
    
    console.log('Mobile Enhancements Initialized');
    console.log('Device:', {
        isMobile: MobileDetect.isMobile(),
        isTablet: MobileDetect.isTablet(),
        isIOS: MobileDetect.isIOS(),
        isAndroid: MobileDetect.isAndroid(),
        viewportWidth: MobileDetect.getViewportWidth(),
        connectionType: NetworkStatus.getConnectionType()
    });
});

// ==================== UTILITY FUNCTIONS ====================

/**
 * Triggers haptic feedback for button clicks
 */
function triggerHapticFeedback() {
    if (MobileDetect.isMobile()) {
        HapticFeedback.trigger(20);
    }
}

/**
 * Get safe viewport dimensions considering mobile browsers
 */
function getSafeViewportDimensions() {
    return {
        width: MobileDetect.getViewportWidth(),
        height: MobileDetect.getViewportHeight(),
        isMobile: MobileDetect.isMobile()
    };
}

/**
 * Check if user prefers reduced motion
 */
function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Check if user prefers dark mode
 */
function prefersDarkMode() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
}

console.log('Mobile Enhancement Library Loaded');
