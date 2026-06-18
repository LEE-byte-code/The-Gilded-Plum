document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initScrollReveal();
    initMenuFilter();
    initReservationModal();
    initGalleryLightbox();
    initSoundscape();
    initIngredientDrawer();
    initChefTableAvailability();
    initCustomCursor();
    initPageSkeleton();
    initImageSkeleton();
});

/**
 * Custom Gilded Cursor Logic
 */
function initCustomCursor() {
    const cursor = document.querySelector('.custom-cursor');
    const follower = document.querySelector('.custom-cursor-follower');
    const interactives = document.querySelectorAll('a, button, .menu-card, .zone-card, .svg-zone');

    if (!cursor || !follower) return;

    let mouseX = 0;
    let mouseY = 0;
    let followerX = 0;
    let followerY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursor.style.left = `${mouseX}px`;
        cursor.style.top = `${mouseY}px`;
    });

    const animate = () => {
        followerX += (mouseX - followerX) * 0.1;
        followerY += (mouseY - followerY) * 0.1;
        follower.style.left = `${followerX}px`;
        follower.style.top = `${followerY}px`;
        requestAnimationFrame(animate);
    };
    animate();

    interactives.forEach(el => {
        el.addEventListener('mouseenter', () => {
            document.body.classList.add('cursor-active');
        });
        el.addEventListener('mouseleave', () => {
            document.body.classList.remove('cursor-active');
        });
    });
}

/**
 * Mobile Navigation Menu
 */
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger-menu');
    const navLinks = document.querySelector('nav ul');
    const header = document.querySelector('header');
    
    const logo = document.querySelector('.logo');
    
    if (!hamburger || !navLinks) return;

    const closeMenu = () => {
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
    };

    hamburger.addEventListener('click', () => {
        const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
        hamburger.setAttribute('aria-expanded', !isExpanded);
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Close menu when clicking the logo
    if (logo) {
        logo.addEventListener('click', closeMenu);
    }

    // Focus trap for mobile nav accessibility
    navLinks.addEventListener('keydown', (e) => {
        if (!navLinks.classList.contains('active') || e.key !== 'Tab') return;
        const focusable = navLinks.querySelectorAll('a, button');
        if (!focusable.length) return;

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
        }
    });

    // Header scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

/**
 * Scroll Reveal Animation (Intersection Observer)
 */
function initScrollReveal() {
    // Respect user's motion preferences
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.querySelectorAll('.reveal').forEach(el => {
            el.classList.add('revealed');
        });
        return;
    }

    const revealElements = document.querySelectorAll('.reveal');
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -20px 0px', // Trigger just as it enters for a "reveal" feel
        threshold: 0.05 
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                obs.unobserve(entry.target); // Animates only once
            }
        });
    }, observerOptions);

    revealElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Chef's Selection Menu Filtering
 */
function initMenuFilter() {
    const filterTabs = document.querySelectorAll('.menu-tab');
    const menuGrid = document.querySelector('.menu-grid');
    const menuItems = document.querySelectorAll('.menu-card');
    const categoryHeadings = document.querySelectorAll('.menu-category-heading');

    if (!filterTabs.length || !menuGrid || !menuItems.length) return;

    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const category = tab.getAttribute('data-category');

            menuGrid.classList.add('filtering-active');

            setTimeout(() => {
                menuItems.forEach(item => {
                    const itemCategory = item.getAttribute('data-category');
                    if (category === 'all' || itemCategory === category) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                });

                categoryHeadings.forEach(heading => {
                    const headingCategory = heading.getAttribute('data-category');
                    if (category === 'all') {
                        heading.classList.remove('hidden');
                    } else if (headingCategory === category) {
                        heading.classList.remove('hidden');
                    } else {
                        heading.classList.add('hidden');
                    }
                });

                menuGrid.classList.remove('filtering-active');
            }, 300);
        });
    });
}

/**
 * Table Reservation Modal System
 */
function initReservationModal() {
    const openButtons = document.querySelectorAll('[data-open-modal="reservation"]');
    const modal = document.getElementById('reservation-modal');
    if (!modal) return;

    const closeButton = modal.querySelector('[data-close-modal]');
    const form = document.getElementById('reservation-form');
    const successState = modal.querySelector('.reservation-success');
    const formState = modal.querySelector('.reservation-form-container');
    const dateInput = document.getElementById('res-date');
    const zoneInput = document.getElementById('res-zone');
    const zoneCards = modal.querySelectorAll('.zone-card');
    const svgZones = modal.querySelectorAll('.svg-zone');

    // Helper: Sync Zone Selection (Card + SVG + Hidden Input)
    const selectZone = (zoneCode) => {
        // Update hidden input
        if (zoneInput) zoneInput.value = zoneCode;

        // Update cards
        zoneCards.forEach(card => {
            if (card.getAttribute('data-zone') === zoneCode) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });

        // Update SVG
        svgZones.forEach(svgZone => {
            if (svgZone.getAttribute('data-zone') === zoneCode) {
                svgZone.classList.add('active');
            } else {
                svgZone.classList.remove('active');
            }
        });
    };

    // Set minimum date to today
    if (dateInput) {
        const today = getLocalDateString();
        dateInput.min = today;
        dateInput.value = today;
    }

    // Zone selection grid interactivity
    zoneCards.forEach(card => {
        card.addEventListener('click', () => {
            selectZone(card.getAttribute('data-zone'));
        });
    });

    // SVG Map interactivity
    svgZones.forEach(svgZone => {
        svgZone.addEventListener('click', () => {
            selectZone(svgZone.getAttribute('data-zone'));
        });
    });

    // Helper: Lock scroll when modal is open
    const setScrollLock = (lock) => {
        document.body.style.overflow = lock ? 'hidden' : '';
    };

    const openModal = (e) => {
        if (e) e.preventDefault();
        modal.classList.add('active');
        setScrollLock(true);
        
        // Handle preselected zones (e.g. Chef's Table card)
        const triggerBtn = e ? e.currentTarget : null;
        if (triggerBtn && triggerBtn.getAttribute('data-preselect-zone') === 'chef') {
            selectZone('chef');
            // Pre-fill guests selector to 2 for Chef's Table typically
            const guestsSelect = document.getElementById('res-guests');
            if (guestsSelect) guestsSelect.value = "2";
        } else {
            selectZone('hall');
        }

        // Focus first input
        setTimeout(() => {
            const firstInput = form ? form.querySelector('input, select') : null;
            if (firstInput) firstInput.focus();
        }, 100);
    };

    const closeModal = () => {
        modal.classList.remove('active');
        setScrollLock(false);
        // Reset form and success state after animation completes
        setTimeout(() => {
            if (form) {
                form.reset();
                form.querySelectorAll('.form-group').forEach(g => g.classList.remove('has-error'));
                form.querySelectorAll('.error-message').forEach(el => { el.textContent = ''; });
            }
            if (successState) successState.classList.add('hidden');
            if (formState) formState.classList.remove('hidden');
            if (dateInput) {
                const today = getLocalDateString();
                dateInput.value = today;
            }
            // Reset active zone card
            selectZone('hall');
        }, 400);
    };

    // Attach listeners to open buttons
    openButtons.forEach(btn => {
        btn.addEventListener('click', openModal);
    });

    // Close button
    if (closeButton) {
        closeButton.addEventListener('click', closeModal);
    }

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close on ESC key
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Handle form submit
    if (form) {
        // Inline validation helpers
        const addErrorSpan = (input) => {
            if (input.parentElement.querySelector('.error-message')) return;
            const span = document.createElement('span');
            span.className = 'error-message';
            input.parentElement.appendChild(span);
        };

        const validateField = (input) => {
            const group = input.closest('.form-group');
            if (!group) return true;

            addErrorSpan(input);
            const errorSpan = group.querySelector('.error-message');

            if (!input.checkValidity()) {
                group.classList.add('has-error');
                if (input.validity.valueMissing) {
                    errorSpan.textContent = 'This field is required';
                } else if (input.validity.typeMismatch) {
                    errorSpan.textContent = input.type === 'email' ? 'Please enter a valid email address' : 'Invalid format';
                } else {
                    errorSpan.textContent = 'Please check this field';
                }
                return false;
            } else {
                group.classList.remove('has-error');
                errorSpan.textContent = '';
                return true;
            }
        };

        // Validate on blur and clear errors on input
        const formInputs = form.querySelectorAll('input[required], select[required]');
        formInputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => {
                if (input.closest('.form-group')?.classList.contains('has-error')) {
                    validateField(input);
                }
            });
        });

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            // Inline validation
            let isValid = true;
            formInputs.forEach(input => {
                if (!validateField(input)) isValid = false;
            });
            if (!isValid) return;

            // Retrieve form values
            const name = document.getElementById('res-name').value;
            const date = document.getElementById('res-date').value;
            const time = document.getElementById('res-time').value;
            const guests = document.getElementById('res-guests').value;
            const zoneCode = zoneInput ? zoneInput.value : 'hall';

            const zoneNameMap = {
                hall: 'Grand Hall',
                window: 'Window Seating',
                booth: 'Saffron Booths',
                bar: 'Sommelier Bar',
                chef: "The Chef's Table"
            };
            const zoneName = zoneNameMap[zoneCode] || 'Grand Hall';

            // Show loading spinner state on button
            const submitBtn = form.querySelector('.submit-btn');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Confirming...';

            // Simulate API Request
            setTimeout(() => {
                // Populate success details
                const summaryText = modal.querySelector('.success-summary');
                if (summaryText) {
                    const [year, month, day] = date.split('-');
                    const dateObj = new Date(year, month - 1, day);
                    const formattedDate = dateObj.toLocaleDateString(undefined, { 
                        weekday: 'long', 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                    });
                    summaryText.innerHTML = `
                        <strong>Guest:</strong> ${name}<br>
                        <strong>Table for:</strong> ${guests} ${guests === '1' ? 'Person' : 'Guests'}<br>
                        <strong>Dining Zone:</strong> ${zoneName}<br>
                        <strong>Date & Time:</strong> ${formattedDate} at ${time}<br>
                        <strong>Status:</strong> <span class="badge">Confirmed</span>
                    `;
                }

                // Show success view
                formState.classList.add('hidden');
                successState.classList.remove('hidden');
                
                // Reset submit button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 1200);
        });
    }

    // Bind success close button
    const successCloseBtn = modal.querySelector('.success-close-btn');
    if (successCloseBtn) {
        successCloseBtn.addEventListener('click', closeModal);
    }
}

/**
 * Helper: Get timezone-safe local YYYY-MM-DD date string
 */
function getLocalDateString() {
    const localDate = new Date();
    const offset = localDate.getTimezoneOffset();
    const adjustedDate = new Date(localDate.getTime() - (offset * 60 * 1000));
    return adjustedDate.toISOString().split('T')[0];
}

/**
 * Gallery Image Lightbox Viewer
 */
function initGalleryLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox-modal');
    if (!lightbox || !galleryItems.length) return;

    const lightboxImg = lightbox.querySelector('.lightbox-img');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeBtn = lightbox.querySelector('[data-close-lightbox]');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');

    let currentIndex = 0;
    const images = Array.from(galleryItems).map(item => {
        const img = item.querySelector('img');
        return {
            src: img.getAttribute('src'),
            alt: img.getAttribute('alt') || 'Fine Dining Masterpiece'
        };
    });

    const setScrollLock = (lock) => {
        document.body.style.overflow = lock ? 'hidden' : '';
    };

    const openLightbox = (index) => {
        currentIndex = index;
        updateLightboxContent();
        lightbox.classList.add('active');
        setScrollLock(true);
        lightbox.focus();
    };

    const closeLightbox = () => {
        lightbox.classList.remove('active');
        setScrollLock(false);
    };

    const updateLightboxContent = () => {
        const { src, alt } = images[currentIndex];
        // Fade effect for image switch
        lightboxImg.style.opacity = 0;
        
        setTimeout(() => {
            lightboxImg.setAttribute('src', src);
            lightboxImg.setAttribute('alt', alt);
            lightboxCaption.textContent = alt;
            lightboxImg.style.opacity = 1;
        }, 150);
    };

    const showPrev = (e) => {
        if (e) e.stopPropagation();
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateLightboxContent();
    };

    const showNext = (e) => {
        if (e) e.stopPropagation();
        currentIndex = (currentIndex + 1) % images.length;
        updateLightboxContent();
    };

    // Attach click listeners to gallery elements
    galleryItems.forEach((item, index) => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            openLightbox(index);
        });
    });

    // Control buttons
    if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
    if (prevBtn) prevBtn.addEventListener('click', showPrev);
    if (nextBtn) nextBtn.addEventListener('click', showNext);

    // Backdrop click
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.classList.contains('lightbox-content-wrapper')) {
            closeLightbox();
        }
    });

    // Key events
    window.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        
        if (e.key === 'Escape') {
            closeLightbox();
        } else if (e.key === 'ArrowLeft') {
            showPrev();
        } else if (e.key === 'ArrowRight') {
            showNext();
        }
    });

    // Touch events for mobile swipe gesture
    let startX = 0;
    let endX = 0;
    
    lightbox.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        const diffX = startX - endX;
        
        if (Math.abs(diffX) > 50) {
            if (diffX > 0) showNext();
            else showPrev();
        }
    }, { passive: true });
}

/**
 * Background Soundscape Controller
 */
function initSoundscape() {
    const audio = document.getElementById('ambient-audio');
    const select = document.getElementById('soundscape-select');
    const btn = document.getElementById('music-toggle-btn');
    if (!audio || !select || !btn) return;

    const playIcon = btn.querySelector('.icon-play');
    const pauseIcon = btn.querySelector('.icon-pause');

    let isPlaying = false;

    const updateControls = () => {
        if (isPlaying) {
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
            btn.classList.add('playing');
        } else {
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
            btn.classList.remove('playing');
        }
    };

    const playAudio = () => {
        audio.play().then(() => {
            isPlaying = true;
            updateControls();
        }).catch(err => {
            console.log("Autoplay blocked by browser. User interaction required.");
            isPlaying = false;
            updateControls();
        });
    };

    const pauseAudio = () => {
        audio.pause();
        isPlaying = false;
        updateControls();
    };

    select.addEventListener('change', () => {
        const val = select.value;
        if (val === 'off') {
            pauseAudio();
        } else {
            audio.src = val;
            playAudio();
        }
    });

    btn.addEventListener('click', () => {
        if (select.value === 'off') {
            // Default to first song if music was off
            select.selectedIndex = 1;
            audio.src = select.value;
            playAudio();
        } else {
            if (isPlaying) {
                pauseAudio();
            } else {
                playAudio();
            }
        }
    });

    // Handle network/source errors with user-facing feedback
    audio.addEventListener('error', () => {
        isPlaying = false;
        updateControls();
        const controller = document.getElementById('soundscape-player');
        if (controller) {
            controller.classList.add('audio-error');
            setTimeout(() => controller.classList.remove('audio-error'), 3000);
        }
    });
}

/**
 * Ingredient details sliding drawer panel
 */
function initIngredientDrawer() {
    const drawer = document.getElementById('details-drawer');
    const backdrop = document.getElementById('drawer-backdrop');
    const closeBtn = document.getElementById('drawer-close-btn');
    const cards = document.querySelectorAll('.menu-card');
    if (!drawer || !backdrop || !closeBtn || !cards.length) return;

    // Rich database containing ingredient profiles, pairings, and allergens
    const dishDetails = {
        "Artisanal Plum Crostini": {
            category: "Starters",
            ingredients: "Roasted organic black plums, whipped French goat cheese, wild rosemary honey, fresh thyme, hand-pulled toasted sourdough.",
            nutrition: { cal: 240, protein: "8g", carbs: "28g", fat: "12g" },
            allergens: ["Gluten", "Dairy"],
            pairing: "Sommelier-selected Prosecco Extra Dry",
            chefsNote: "The plum is the heart of this restaurant. I source these from a small orchard in Sonoma — they're roasted until they just begin to caramelize, bringing out a jammy richness that cuts through the creamy goat cheese beautifully."
        },
        "Burrata & Heirloom Beets": {
            category: "Starters",
            ingredients: "Fresh pugliese burrata, roasted baby beets, salted Sicilian pistachios, organic micro-herbs, 25-year aged Modena white balsamic glaze.",
            nutrition: { cal: 310, protein: "12g", carbs: "14g", fat: "22g" },
            allergens: ["Dairy", "Nuts"],
            pairing: "Crisp Sauvignon Blanc",
            chefsNote: "This dish was born from a trip to Puglia where I watched a nonna pull burrata by hand. The beets are roasted with sea salt and thyme until candy-sweet — a simple tribute to that beautiful memory."
        },
        "Plum Glazed Duck": {
            category: "Mains",
            ingredients: "Slow-roasted free-range duck breast, spiced red plum and port reduction, organic parsnip purée, heirloom rainbow carrots, micro-herbs.",
            nutrition: { cal: 580, protein: "42g", carbs: "18g", fat: "38g" },
            allergens: [],
            pairing: "Reserve Cabernet Sauvignon",
            chefsNote: "Our signature for a reason. The glaze takes three days — we reduce the plums with star anise, cinnamon, and a splash of port until it coats the back of a spoon. The skin is basted every few minutes for that glass-like finish."
        },
        "Gilded Saffron Risotto": {
            category: "Mains",
            ingredients: "Aged Carnaroli rice, premium Iranian saffron filaments, wild chanterelles, Parmigiano-Reggiano, edible 24k gold leaf flakes.",
            nutrition: { cal: 450, protein: "14g", carbs: "62g", fat: "16g" },
            allergens: ["Dairy"],
            pairing: "Dry oaky Chardonnay or Pinot Noir",
            chefsNote: "I insist on Persian saffron from a single family farm in Khorasan. A pinch goes into the stock, another into the finish. The 24k gold is whimsical, but it's the earthiness of the chanterelles that truly gilds this dish."
        },
        "Truffle Butter Filet Mignon": {
            category: "Mains",
            ingredients: "Prime dry-aged beef tenderloin, black winter truffle butter, charred baby asparagus spears, gold potato fondant.",
            nutrition: { cal: 620, protein: "48g", carbs: "12g", fat: "42g" },
            allergens: ["Dairy"],
            pairing: "Reserve Cabernet Sauvignon (Vintage 2021)",
            chefsNote: "We dry-age our beef for a minimum of 28 days. The truffle butter is made fresh each morning — black winter truffles from Provence whipped into French butter with a touch of sea salt. Decadence, pure and simple."
        },
        "Wild Berry Soufflé": {
            category: "Desserts",
            ingredients: "Organic local red raspberries, light egg-white soufflé base, hot vanilla bean crème anglaise pour-over.",
            nutrition: { cal: 320, protein: "6g", carbs: "44g", fat: "14g" },
            allergens: ["Dairy", "Eggs"],
            pairing: "Sauternes Sweet Dessert Wine",
            chefsNote: "A soufflé is a test of patience and timing. We pick the berries at their peak in July and freeze them immediately. The crème anglaise is my grandmother's recipe — it has never let me down."
        },
        "Deconstructed Plum Tart": {
            category: "Desserts",
            ingredients: "70% dark Belgian chocolate ganache, spiced plum compote, toasted hazelnut praline, edible gold dust, shortbread shards.",
            nutrition: { cal: 480, protein: "7g", carbs: "52g", fat: "28g" },
            allergens: ["Gluten", "Dairy", "Nuts"],
            pairing: "10-Year Tawny Port",
            chefsNote: "I wanted to capture the nostalgia of the rustic plum tart my mother made, but deconstruct it into something modern. Each element is made from scratch — familiar yet entirely new."
        },
        "Gilded Old Fashioned": {
            category: "Wines & Cocktails",
            ingredients: "Aged Kentucky bourbon, house-infused plum bitters, demerara sugar syrup, flame-orange peel expression, edible gold flakes.",
            nutrition: { cal: 180, protein: "0g", carbs: "12g", fat: "0g" },
            allergens: [],
            pairing: "Pairs perfectly alongside our Truffle Butter Filet Mignon",
            chefsNote: "Our plum bitters are steeped for six weeks with dried plums, cardamom, and clove. The gold flakes catch the candlelight in a way that just feels right for this room."
        },
        "Plum & Lavender Spritz": {
            category: "Starters",
            ingredients: "House-made plum liqueur, organic lavender flowers, premium Italian Prosecco, sparkling mineral water, fresh mint sprig.",
            nutrition: { cal: 150, protein: "0g", carbs: "14g", fat: "0g" },
            allergens: [],
            pairing: "Excellent pairing with the Artisanal Plum Crostini",
            chefsNote: "We grow the lavender ourselves on the restaurant's rooftop garden. The plum liqueur is macerated for a full lunar cycle — it turns a deep ruby color and smells like summer in a glass."
        },
        "Reserve Cabernet Sauvignon": {
            category: "Wines & Cocktails",
            ingredients: "A rich red wine vintage from Napa Valley, oak-barrel aged for 24 months, with notes of dark blackberry, leather, and vanilla.",
            nutrition: { cal: 125, protein: "0g", carbs: "4g", fat: "0g" },
            allergens: ["Sulfites"],
            pairing: "Specially curated for beef and game main courses",
            chefsNote: "Our sommelier travels to Napa personally each year to select our reserve barrels. This vintage spent 24 months in French oak — it has the structure to stand up to our heartiest dishes."
        }
    };

    const openDrawer = (dishName, imgUrl) => {
        const detail = dishDetails[dishName];
        if (!detail) return;

        // Set drawer image, title and category
        const img = document.getElementById('drawer-img');
        const title = document.getElementById('drawer-title');
        const category = document.getElementById('drawer-category');
        const descText = document.getElementById('drawer-desc');
        const ingredientsText = document.getElementById('drawer-ingredients');
        const pairingText = document.getElementById('drawer-pairing');
        const allergensContainer = document.getElementById('drawer-allergens');
        
        // Nutrition elements
        const nutCal = document.getElementById('nut-cal');
        const nutProtein = document.getElementById('nut-protein');
        const nutCarbs = document.getElementById('nut-carbs');
        const nutFat = document.getElementById('nut-fat');

        if (img) {
            img.src = imgUrl;
            img.alt = dishName;
        }
        if (title) title.textContent = dishName;
        if (category) category.textContent = detail.category;

        // Fetch description from the original card
        let desc = "An exquisite house recipe prepared with premium, locally sourced ingredients.";
        cards.forEach(card => {
            const cardTitle = card.querySelector('h3').textContent.trim();
            if (cardTitle === dishName) {
                const descEl = card.querySelector('.description');
                if (descEl) desc = descEl.textContent.trim();
            }
        });
        if (descText) descText.textContent = desc;

        // Set chef's note
        const chefsNoteText = document.getElementById('drawer-chefs-note');
        if (chefsNoteText) chefsNoteText.textContent = detail.chefsNote || 'Every dish at The Gilded Plum is crafted with passion and precision.';

        // Set ingredients & pairing
        if (ingredientsText) ingredientsText.textContent = detail.ingredients;
        if (pairingText) pairingText.textContent = detail.pairing;

        // Set nutrition
        if (nutCal) nutCal.textContent = detail.nutrition.cal;
        if (nutProtein) nutProtein.textContent = detail.nutrition.protein;
        if (nutCarbs) nutCarbs.textContent = detail.nutrition.carbs;
        if (nutFat) nutFat.textContent = detail.nutrition.fat;

        // Load allergens
        if (allergensContainer) {
            allergensContainer.innerHTML = '';
            if (detail.allergens.length === 0) {
                allergensContainer.innerHTML = '<span class="tag">Allergen Free</span>';
            } else {
                const allergenClassMap = {
                    'Gluten': 'tag-gf',
                    'Dairy': 'tag-dairy',
                    'Nuts': 'tag-nuts',
                    'Eggs': 'tag-eggs',
                    'Sulfites': 'tag-sulfites'
                };
                detail.allergens.forEach(allergen => {
                    const span = document.createElement('span');
                    const tagClass = allergenClassMap[allergen] || '';
                    span.className = `tag ${tagClass}`.trim();
                    span.textContent = allergen;
                    allergensContainer.appendChild(span);
                });
            }
        }

        // Reset accordion: collapse all, expand only first
        const accordionSections = drawer.querySelectorAll('.accordion-section');
        accordionSections.forEach((section, i) => {
            const toggle = section.querySelector('.accordion-toggle');
            const content = section.querySelector('.accordion-content');
            if (i === 0) {
                toggle.setAttribute('aria-expanded', 'true');
                content.style.display = 'block';
            } else {
                toggle.setAttribute('aria-expanded', 'false');
                content.style.display = 'none';
            }
            section.classList.remove('stagger-enter');
        });

        // Scroll drawer body to top
        const drawerBody = drawer.querySelector('.drawer-body');
        if (drawerBody) drawerBody.scrollTop = 0;

        // Animate Drawer open
        drawer.classList.add('active');
        document.body.style.overflow = 'hidden'; // Lock scroll
        drawer.focus();

        // Stagger entrance animation on next frame
        requestAnimationFrame(() => {
            accordionSections.forEach((section, i) => {
                setTimeout(() => {
                    section.classList.add('stagger-enter');
                }, i * 80);
            });
        });
    };

    // Accordion toggle behavior
    const initAccordion = () => {
        const toggles = drawer.querySelectorAll('.accordion-toggle');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                const section = toggle.closest('.accordion-section');
                const content = section.querySelector('.accordion-content');
                const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

                if (isExpanded) {
                    toggle.setAttribute('aria-expanded', 'false');
                    content.style.display = 'none';
                } else {
                    toggle.setAttribute('aria-expanded', 'true');
                    content.style.display = 'block';
                    // Trigger reflow for entrance animation
                    requestAnimationFrame(() => {
                        content.classList.remove('accordion-enter');
                        content.offsetHeight;
                        content.classList.add('accordion-enter');
                    });
                }
            });
        });
    };
    initAccordion();

    const closeDrawer = () => {
        drawer.classList.remove('active');
        document.body.style.overflow = ''; // Release scroll
    };

    // Attach click listeners to all menu cards
    cards.forEach(card => {
        card.style.cursor = 'pointer'; // Ensure pointer cursor is visible
        card.addEventListener('click', (e) => {
            // Prevent drawer if clicking tab buttons or action buttons
            if (e.target.closest('.btn') || e.target.closest('.menu-tabs')) return;

            const dishName = card.querySelector('h3').textContent.trim();
            const imgUrl = card.querySelector('img').getAttribute('src');
            openDrawer(dishName, imgUrl);
        });
    });

    // Close listeners
    closeBtn.addEventListener('click', closeDrawer);
    backdrop.addEventListener('click', closeDrawer);
    drawer.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDrawer();
    });
}

/**
 * Chef's Table Live Availability Simulator
 */
function initChefTableAvailability() {
    const seatCounter = document.getElementById('chef-seat-counter');
    const dotsContainer = document.getElementById('chef-seating-dots');
    if (!seatCounter || !dotsContainer) return;

    const totalSeats = 6;
    let availableSeats = 4;

    const updateUI = () => {
        // Update text
        seatCounter.textContent = `Only ${availableSeats} seat${availableSeats !== 1 ? 's' : ''} remaining for tonight`;
        
        // Update dots
        dotsContainer.innerHTML = '';
        for (let i = 0; i < totalSeats; i++) {
            const dot = document.createElement('div');
            dot.className = 'seat-dot';
            if (i < (totalSeats - availableSeats)) {
                dot.classList.add('occupied');
            }
            dotsContainer.appendChild(dot);
        }
    };

    // Initial render
    updateUI();

    // Simulate occasional seat booking for urgency
    setTimeout(() => {
        if (availableSeats > 2) {
            availableSeats--;
            updateUI();
        }
    }, 15000);
}

/**
 * Initial page loading skeleton overlay
 */
function initPageSkeleton() {
    const skeleton = document.getElementById('page-skeleton');
    if (!skeleton) return;

    const hide = () => skeleton.classList.add('hidden');

    // Hide once everything (fonts, CSS, images) is fully loaded
    window.addEventListener('load', hide);

    // Fallback timeout so skeleton never stays longer than necessary
    setTimeout(hide, 2500);
}

/**
 * Image skeleton shimmer — removes placeholder once image loads
 */
function initImageSkeleton() {
    const wrappers = document.querySelectorAll('.img-skeleton');
    wrappers.forEach(wrapper => {
        const img = wrapper.querySelector('img');
        if (!img) return;

        const reveal = () => wrapper.classList.remove('img-skeleton');

        // Already cached
        if (img.complete && img.naturalWidth > 0) {
            reveal();
        } else {
            img.addEventListener('load', reveal);
            img.addEventListener('error', reveal);
        }
    });
}
