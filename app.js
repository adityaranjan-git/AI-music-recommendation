document.addEventListener('DOMContentLoaded', () => {
    // --- Auth DOM Elements ---
    const authSection = document.getElementById('auth-section');
    const appSection = document.getElementById('app-section');
    const tabLogin = document.getElementById('tab-login');
    const tabSignup = document.getElementById('tab-signup');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const welcomeMessage = document.getElementById('welcome-message');
    const logoutBtn = document.getElementById('logout-btn');
    const loginError = document.getElementById('login-error');
    const signupError = document.getElementById('signup-error');

    // --- App DOM Elements ---
    const form = document.getElementById('search-form');
    const categorySelect = document.getElementById('category');
    const moodInput = document.getElementById('mood');
    const moodChips = document.querySelectorAll('.chip');
    const recentSearchesEl = document.getElementById('recent-searches');
    const aiSuggestionEl = document.getElementById('ai-suggestion');
    const loaderEl = document.getElementById('loader');
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const errorEl = document.getElementById('error-message');

    // Setup Local Storage display on load
    function displayRecentSearches() {
        const searches = JSON.parse(localStorage.getItem('aiSongFinder_recentSearches')) || [];
        if (searches.length > 0) {
            recentSearchesEl.querySelector('span').textContent = searches.join(', ');
            recentSearchesEl.classList.remove('hidden');
        } else {
            recentSearchesEl.classList.add('hidden');
        }
    }
    displayRecentSearches();

    // --- Auth Logic ---
    function getUsers() {
        return JSON.parse(localStorage.getItem('aiSongFinder_users')) || [];
    }

    function saveUser(user) {
        const users = getUsers();
        users.push(user);
        localStorage.setItem('aiSongFinder_users', JSON.stringify(users));
    }

    function checkSession() {
        const currentUser = localStorage.getItem('aiSongFinder_currentUser');
        if (currentUser) {
            authSection.classList.add('hidden');
            appSection.classList.remove('hidden');
            welcomeMessage.textContent = `Welcome, ${currentUser}`;
        } else {
            authSection.classList.remove('hidden');
            appSection.classList.add('hidden');
        }
    }

    // Tab Switching
    tabLogin.addEventListener('click', () => {
        tabLogin.classList.add('active');
        tabSignup.classList.remove('active');
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        loginError.classList.add('hidden');
        signupError.classList.add('hidden');
    });

    tabSignup.addEventListener('click', () => {
        tabSignup.classList.add('active');
        tabLogin.classList.remove('active');
        signupForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        loginError.classList.add('hidden');
        signupError.classList.add('hidden');
    });

    // Signup Logic
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('signup-username').value.trim();
        const email = document.getElementById('signup-email').value.trim();
        const password = document.getElementById('signup-password').value;

        const users = getUsers();
        const existingUser = users.find(u => u.username.toLowerCase() === username.toLowerCase() || u.email.toLowerCase() === email.toLowerCase());

        if (existingUser) {
            signupError.textContent = 'Username or email already exists.';
            signupError.classList.remove('hidden');
            return;
        }

        saveUser({ username, email, password });
        localStorage.setItem('aiSongFinder_currentUser', username);
        signupForm.reset();
        checkSession();
    });

    // Login Logic
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const usernameOrEmail = document.getElementById('login-username').value.trim().toLowerCase();
        const password = document.getElementById('login-password').value;

        const users = getUsers();
        const user = users.find(u => 
            (u.username.toLowerCase() === usernameOrEmail || u.email.toLowerCase() === usernameOrEmail) && 
            u.password === password
        );

        if (user) {
            localStorage.setItem('aiSongFinder_currentUser', user.username);
            loginForm.reset();
            checkSession();
        } else {
            loginError.textContent = 'Invalid username or password.';
            loginError.classList.remove('hidden');
        }
    });

    // Logout Logic
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('aiSongFinder_currentUser');
        checkSession();
    });

    // Initial check
    checkSession();

    // Handle Chip clicks
    moodChips.forEach(chip => {
        chip.addEventListener('click', () => {
            moodInput.value = chip.dataset.mood;
        });
    });

    // AI Suggestion Logic Mapping
    const aiSuggestions = {
        'happy': "Keep the good vibes going! Here are some upbeat tracks to match your energy.",
        'sad': "It's okay to feel down. Try listening to these comforting and uplifting songs.",
        'romantic': "Love is in the air. Enjoy these beautiful romantic melodies.",
        'energetic': "Time to get moving! These high-energy tracks are perfect for your workout.",
        'calm': "Take a deep breath and relax with these soothing, mellow tunes.",
        'angry': "Let it out. Here are some intense tracks to help you process your feelings.",
        'chill': "Kick back and relax with these smooth, easy-listening tracks."
    };

    function getSmartSuggestion(mood) {
        const lowerMood = mood.toLowerCase().trim();
        let baseSuggestion = `Here is a curated playlist tailored perfectly for your "${mood}" mood.`;
        
        // Exact match
        if (aiSuggestions[lowerMood]) {
            baseSuggestion = aiSuggestions[lowerMood];
        } else {
            // Partial match
            for (const [key, value] of Object.entries(aiSuggestions)) {
                if (lowerMood.includes(key)) {
                    baseSuggestion = value;
                    break;
                }
            }
        }

        // Dynamic addition based on conditions
        let dynamicMsg = "";
        if (lowerMood.includes('sad')) {
            dynamicMsg = " We recommend some uplifting songs to brighten your day!";
        } else if (lowerMood.includes('happy')) {
            dynamicMsg = " Time to play some party songs!";
        } else if (lowerMood.includes('energetic')) {
            dynamicMsg = " A great time for some workout songs!";
        }

        return baseSuggestion + dynamicMsg;
    }

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const category = categorySelect.value.trim();
        const mood = moodInput.value.trim();

        if (!mood) return;

        // 1. Update Personalization (Recent Searches)
        let recentSearches = JSON.parse(localStorage.getItem('aiSongFinder_recentSearches')) || [];
        recentSearches = recentSearches.filter(s => s.toLowerCase() !== mood.toLowerCase());
        recentSearches.unshift(mood);
        if (recentSearches.length > 3) recentSearches.pop();
        localStorage.setItem('aiSongFinder_recentSearches', JSON.stringify(recentSearches));
        displayRecentSearches();

        // 2. Update AI Suggestion
        aiSuggestionEl.textContent = getSmartSuggestion(mood);
        aiSuggestionEl.classList.remove('hidden');

        // 3. UI State transitions
        resultsSection.classList.add('hidden');
        errorEl.classList.add('hidden');
        loaderEl.classList.remove('hidden');
        resultsGrid.innerHTML = '';

        try {
            // 4. Fetch Data from iTunes Search API
            // Combine category and mood for a better query. If no category, just use mood.
            const query = category ? `${mood} ${category}` : mood;
            
            // Note: iTunes API returns JSONP traditionally, but modern browsers can use CORS for certain endpoints
            // However, the standard search endpoint usually supports direct fetch now.
            // limit to 10 results
            const url = `https://itunes.apple.com/search?term=${encodeURIComponent(query)}&media=music&entity=song&limit=10`;
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();

            // 5. Display Results
            loaderEl.classList.add('hidden');

            if (data.results && data.results.length > 0) {
                renderSongs(data.results);
                resultsSection.classList.remove('hidden');
            } else {
                showError(`We couldn't find any songs for "${mood}"${category ? ` in ${category}` : ''}. Try another mood!`);
            }

        } catch (error) {
            console.error('Error fetching songs:', error);
            loaderEl.classList.add('hidden');
            showError("Oops! Something went wrong while fetching songs. Please try again later.");
        }
    });

    function renderSongs(songs) {
        // Take up to 6 songs for a nice grid
        const songsToRender = songs.slice(0, 6);

        songsToRender.forEach((song, index) => {
            // iTunes returns 100x100 artwork, we can hack the URL to get a larger version
            const artworkUrl = song.artworkUrl100 ? song.artworkUrl100.replace('100x100bb', '600x600bb') : 'https://via.placeholder.com/600?text=No+Cover';
            
            const card = document.createElement('div');
            card.className = 'song-card';
            card.style.animationDelay = `${index * 0.1}s`;

            card.innerHTML = `
                <img src="${artworkUrl}" alt="${song.trackName} cover" class="card-image" loading="lazy">
                <div class="card-content">
                    <h3 class="song-title" title="${song.trackName}">${song.trackName}</h3>
                    <p class="song-artist" title="${song.artistName}">${song.artistName}</p>
                    ${song.previewUrl ? `
                        <audio controls preload="none">
                            <source src="${song.previewUrl}" type="audio/mp4">
                            Your browser does not support the audio element.
                        </audio>
                    ` : '<p style="color:var(--text-secondary);font-size:0.8rem;margin-top:auto;">No preview available</p>'}
                    <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(song.trackName + ' ' + song.artistName)}" target="_blank" class="btn-youtube">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                        Watch on YouTube
                    </a>
                </div>
            `;
            resultsGrid.appendChild(card);
        });

        // Add event listener to stop other audios when one is played
        const audios = resultsGrid.querySelectorAll('audio');
        audios.forEach(audio => {
            audio.addEventListener('play', (e) => {
                audios.forEach(otherAudio => {
                    if (otherAudio !== e.target) {
                        otherAudio.pause();
                    }
                });
            });
        });
    }

    function showError(message) {
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
    }
});
