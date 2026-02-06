// ==================== FLASH MESSAGES ====================
document.addEventListener('DOMContentLoaded', function() {
    // Auto-close flash messages
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// ==================== PRICE FILTER ====================
function applyPriceFilter() {
    const minPrice = document.getElementById('min_price').value;
    const maxPrice = document.getElementById('max_price').value;
    const urlParams = new URLSearchParams(window.location.search);
    
    // Update or remove price parameters
    if (minPrice) {
        urlParams.set('price_min', minPrice);
    } else {
        urlParams.delete('price_min');
    }
    
    if (maxPrice) {
        urlParams.set('price_max', maxPrice);
    } else {
        urlParams.delete('price_max');
    }
    
    // Redirect with updated parameters
    window.location.href = window.location.pathname + '?' + urlParams.toString();
}

// Allow Enter key to apply filter
document.addEventListener('DOMContentLoaded', function() {
    const priceInputs = document.querySelectorAll('.price-input');
    priceInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyPriceFilter();
            }
        });
    });
});

// ==================== WISHLIST HEART TOGGLE ==================== 
document.addEventListener('DOMContentLoaded', function() {
    const wishlistButtons = document.querySelectorAll('.add-to-wishlist');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = this.getAttribute('data-product-id');
            const icon = this.querySelector('i');
            
            fetch(`/wishlist/add/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update wishlist badge
                    updateWishlistBadge(data.wishlist_count);
                    
                    if (data.action === 'added') {
                        showNotification('Added to wishlist!', 'success');
                        // Toggle heart icon color
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        button.style.color = 'var(--danger)';
                    } else if (data.action === 'removed') {
                        showNotification('Removed from wishlist!', 'success');
                        icon.classList.add('far');
                        icon.classList.remove('fas');
                        button.style.color = 'inherit';
                    }
                }
            })
            .catch(error => {
                showNotification('Please login to add to wishlist', 'warning');
            });
            
            return false;
        });
    });
});


// ==================== MOBILE MENU ====================
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileMenuToggle && navMenu) {
        const toggleIcon = () => {
            const icon = mobileMenuToggle.querySelector('i');
            if (!icon) return;
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        };

        mobileMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            navMenu.classList.toggle('active');
            toggleIcon();
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.navbar')) {
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    toggleIcon();
                }
            }
        });

        // Close menu when a link is clicked (mobile) - except dropdown toggles
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function(e) {
                // Don't close if it's a dropdown button
                if (this.classList.contains('dropbtn')) {
                    return;
                }
                if (window.innerWidth <= 768) {
                    navMenu.classList.remove('active');
                    toggleIcon();
                }
            });
        });

        // Handle dropdown clicks on mobile - one click shows all categories
        const dropdowns = document.querySelectorAll('.nav-menu .dropdown');
        dropdowns.forEach(dropdown => {
            const dropbtn = dropdown.querySelector('.dropbtn');
            const dropdownContent = dropdown.querySelector('.dropdown-content');
            
            if (dropbtn && dropdownContent) {
                dropbtn.addEventListener('click', function(e) {
                    if (window.innerWidth <= 768) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Toggle this dropdown
                        dropdown.classList.toggle('active');
                        
                        // Close other dropdowns
                        dropdowns.forEach(otherDropdown => {
                            if (otherDropdown !== dropdown) {
                                otherDropdown.classList.remove('active');
                            }
                        });
                    }
                });
            }
        });

        // Handle window resize - close menu if resizing to desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                toggleIcon();
                // Also close all dropdowns
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            }
        });
    }
});

// ==================== NOTIFICATION SYSTEM ====================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `${message}<button class="close-alert">&times;</button>`;
    
    let flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) {
        flashContainer = document.createElement('div');
        flashContainer.className = 'flash-messages';
        document.body.insertBefore(flashContainer, document.body.firstChild);
    }
    
    flashContainer.appendChild(notification);
    
    notification.querySelector('.close-alert').addEventListener('click', () => notification.remove());
    setTimeout(() => notification.remove(), 5000);
}

// ==================== SMOOTH SCROLL ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
});

// ==================== FORM VALIDATION ENHANCEMENT ====================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                
                // Re-enable after 3 seconds in case of error
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = submitButton.getAttribute('data-original-text') || 'Submit';
                }, 3000);
            }
        });
    });
});

// ==================== IMAGE LAZY LOADING ====================
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// ==================== CART COUNT UPDATE ====================
function updateCartCount() {
    fetch('/api/cart/count')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.textContent = data.count;
                if (data.count === 0) {
                    cartBadge.style.display = 'none';
                } else {
                    cartBadge.style.display = 'flex';
                }
            }
        })
        .catch(error => console.error('Error updating cart count:', error));
}

// ==================== CATEGORY CARD CART CONTROLS ====================
function updateCartBadge(count) {
    const cartBadges = document.querySelectorAll('.cart-icon .cart-badge');
    cartBadges.forEach(badge => {
        if (typeof count === 'number') {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }
    });
}

function updateWishlistBadge(count) {
    const wishlistIcons = document.querySelectorAll('.wishlist-icon');
    wishlistIcons.forEach(icon => {
        let badge = icon.querySelector('.cart-badge');
        
        if (count > 0) {
            if (!badge) {
                badge = document.createElement('span');
                badge.className = 'cart-badge';
                icon.appendChild(badge);
            }
            badge.textContent = count;
            badge.style.display = 'flex';
            icon.classList.add('has-items');
        } else {
            if (badge) {
                badge.style.display = 'none';
            }
            icon.classList.remove('has-items');
        }
    });
}

function createQuickAddButton(productId) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn-add-cart quick-add';
    button.dataset.productId = productId;
    button.title = 'Add to Cart';
    button.innerHTML = '<i class="fas fa-shopping-bag"></i><span>Add to Cart</span>';
    button.addEventListener('click', handleQuickAddClick);
    return button;
}

function createQtyControl(productId, quantity) {
    const control = document.createElement('div');
    control.className = 'qty-control';
    control.dataset.productId = productId;
    control.innerHTML = `
        <button type="button" class="qty-btn" data-action="decrement" aria-label="Decrease quantity">-</button>
        <span class="qty-value">${quantity}</span>
        <button type="button" class="qty-btn" data-action="increment" aria-label="Increase quantity">+</button>
    `;
    attachQtyEvents(control);
    return control;
}

function attachQtyEvents(control) {
    const buttons = control.querySelectorAll('.qty-btn');
    buttons.forEach(btn => btn.addEventListener('click', handleQtyButtonClick));
}

function handleQuickAddClick(e) {
    e.preventDefault();
    const button = e.currentTarget;
    const productId = button.dataset.productId;
    const actionContainer = button.closest('.cart-action');

    fetch(`/cart/add/${productId}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({ quantity: 1 })
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;
        if (!data.success) {
            showNotification(data.message || 'Unable to add to cart', 'warning');
            return;
        }

        const control = createQtyControl(productId, data.quantity || 1);
        if (actionContainer) {
            actionContainer.innerHTML = '';
            actionContainer.appendChild(control);
        }

        updateCartBadge(data.cart_count);
        showNotification('Added to cart', 'success');
    })
    .catch(() => showNotification('Please login to add to cart', 'warning'));
}

function handleQtyButtonClick(e) {
    e.preventDefault();
    const btn = e.currentTarget;
    const control = btn.closest('.qty-control');
    if (!control) return;

    const productId = control.dataset.productId;
    const valueEl = control.querySelector('.qty-value');
    const actionContainer = control.closest('.cart-action');

    let quantity = parseInt(valueEl.textContent, 10) || 1;
    quantity = btn.dataset.action === 'increment' ? quantity + 1 : quantity - 1;
    quantity = Math.max(quantity, 0);

    setCartQuantity(productId, quantity, actionContainer, valueEl);
}

function setCartQuantity(productId, quantity, actionContainer, valueEl) {
    fetch(`/cart/set/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ quantity })
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;
        if (!data.success) {
            showNotification(data.message || 'Could not update cart', 'warning');
            return;
        }

        if (data.quantity === 0) {
            const quickAdd = createQuickAddButton(productId);
            if (actionContainer) {
                actionContainer.innerHTML = '';
                actionContainer.appendChild(quickAdd);
            }
        } else if (valueEl) {
            valueEl.textContent = data.quantity;
        }

        updateCartBadge(data.cart_count);
        showNotification(data.message || 'Cart updated', 'success');
    })
    .catch(() => showNotification('Could not update cart', 'warning'));
}

document.addEventListener('DOMContentLoaded', function() {
    // Only attach handlers to quick-add buttons on categories/shop pages
    document.querySelectorAll('.quick-add:not(.home-add-cart)').forEach(btn => {
        if (btn.type === 'button') {
            btn.addEventListener('click', handleQuickAddClick);
        }
    });
    document.querySelectorAll('.qty-control').forEach(control => attachQtyEvents(control));
});

// ==================== PRODUCT SEARCH (Future Enhancement) ====================
// Add this when search functionality is implemented
/*
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#search-input');
    
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = this.value.trim();
                if (query.length > 2) {
                    // Perform search
                    console.log('Searching for:', query);
                }
            }, 500);
        });
    }
});
*/

// ==================== SCROLL TO TOP BUTTON ====================
document.addEventListener('DOMContentLoaded', function() {
    // Create scroll to top button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        transition: all 0.3s;
    `;
    document.body.appendChild(scrollBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'flex';
        } else {
            scrollBtn.style.display = 'none';
        }
    });
    
    // Scroll to top when clicked
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    scrollBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
    });
    
    scrollBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});

// (Removed duplicate mobile menu toggle block to prevent conflicting handlers)
