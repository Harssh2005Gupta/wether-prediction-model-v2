const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, 'stitch_agriweather_intelligence_system', 'krishimitra_agriweather_intelligence_system');

const views = {
    login: extractContent(path.join(baseDir, 'login', 'code.html'), true),
    'ai_control_center': extractContent(path.join(baseDir, 'ai_control_center', 'code.html'), false),
    'crop_doctor': extractContent(path.join(baseDir, 'crop_doctor_analysis_result', 'code.html'), false),
    'irrigation': extractContent(path.join(baseDir, 'irrigation_dashboard_desktop', 'code.html'), false),
    'soil_analysis': extractContent(path.join(baseDir, 'soil_intelligence_hub', 'code.html'), false),
};

function extractContent(filePath, isLogin) {
    if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${filePath}`);
        return '';
    }
    const html = fs.readFileSync(filePath, 'utf8');
    
    if (isLogin) {
        const match = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
        return match ? match[1].trim() : '';
    } else {
        const mainMatch = html.match(/<main([^>]*)>([\s\S]*?)<\/main>/);
        if (!mainMatch) return '';
        let mainAttrs = mainMatch[1];
        let mainContent = mainMatch[2];
        
        mainContent = mainContent.replace(/<header[^>]*>([\s\S]*?)<\/header>/, '');
        
        // Remove layout classes that are already handled by index.html's wrapper
        mainAttrs = mainAttrs.replace(/ml-64|lg:ml-64|min-h-screen/g, '');
        // Make paddings responsive
        mainAttrs = mainAttrs.replace(/p-8|px-8|px-6/g, 'p-4 md:p-8');
        mainAttrs = mainAttrs.replace(/pt-24/g, 'pt-6 md:pt-12');
        mainAttrs = mainAttrs.replace(/\s{2,}/g, ' ');
        
        return `<div${mainAttrs}>\n${mainContent.trim()}\n</div>`;
    }
}

const sanitize = (str) => str.replace(/`/g, '\\`').replace(/\$/g, '\\$');

const appJsContent = `
const views = {
    login: \`${sanitize(views.login)}\`,
    communication: \`${sanitize(views['ai_control_center'])}\`,
    'crop-doctor': \`${sanitize(views['crop_doctor'])}\`,
    irrigation: \`${sanitize(views['irrigation'])}\`,
    'soil-analysis': \`${sanitize(views['soil_analysis'])}\`,
    dashboard: \`
        <div class="p-4 md:p-8 max-w-screen-2xl mx-auto space-y-6 md:space-y-8">
            <div class="flex justify-between items-center">
                <h2 class="font-headline-lg text-primary">Dashboard Overview</h2>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
                <!-- Weather Forecast Section -->
                <div class="col-span-12 lg:col-span-8 space-y-6">
                    <div class="bg-white rounded-xl p-lg card-shadow border border-[#8B5E3C]/15 ai-glow relative overflow-hidden">
                        <div class="absolute top-0 right-0 p-4">
                            <span class="px-3 py-1 bg-secondary-container/10 text-secondary text-caption rounded-full font-bold flex items-center gap-1">
                                <span class="material-symbols-outlined text-xs" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                                AI Weather Insight
                            </span>
                        </div>
                        <div class="flex items-center gap-4 mb-6">
                            <div class="w-16 h-16 bg-secondary-fixed rounded-full flex items-center justify-center">
                                <span class="material-symbols-outlined text-4xl text-secondary" style="font-variation-settings: 'FILL' 1;">partly_cloudy_day</span>
                            </div>
                            <div>
                                <h3 class="font-headline-xl text-primary">24°C</h3>
                                <p class="font-body-md text-on-surface-variant">Partly Cloudy, 15% precipitation</p>
                            </div>
                        </div>
                        <p class="font-body-md text-on-surface leading-relaxed max-w-2xl">
                            Optimal conditions for spraying in the afternoon. Wind speeds are expected to drop below 10km/h after 2 PM.
                        </p>
                    </div>

                    <!-- 7 Day Forecast -->
                    <div class="bg-white rounded-xl p-lg card-shadow border border-[#8B5E3C]/15">
                        <h3 class="font-headline-md mb-6">7-Day Forecast</h3>
                        <div class="flex flex-wrap gap-4 justify-between">
                            \${['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, i) => \`
                                <div class="flex flex-col items-center bg-surface-container-low p-4 rounded-xl flex-1 min-w-[80px]">
                                    <span class="font-label-bold text-on-surface-variant mb-2">\${day}</span>
                                    <span class="material-symbols-outlined text-secondary mb-2" style="font-variation-settings: 'FILL' 1;">\${i % 3 === 0 ? 'rainy' : i % 2 === 0 ? 'sunny' : 'partly_cloudy_day'}</span>
                                    <span class="font-headline-md text-primary">\${22 + (i % 4)}°</span>
                                </div>
                            \`).join('')}
                        </div>
                    </div>
                </div>

                <!-- Right Column: News & Ads -->
                <div class="col-span-12 lg:col-span-4 space-y-6">
                    <!-- Crop Doctor Summary -->
                    <div class="bg-white rounded-xl p-lg card-shadow border border-[#8B5E3C]/15">
                        <h3 class="font-headline-md mb-4 flex items-center gap-2">
                            <span class="material-symbols-outlined text-tertiary">bug_report</span>
                            Crop Doctor
                        </h3>
                        <div class="space-y-4">
                            <div class="border-b border-outline-variant pb-4">
                                <div class="flex items-start justify-between">
                                    <div class="flex items-center gap-3">
                                        <div class="p-2 bg-tertiary-fixed rounded-lg text-tertiary flex items-center justify-center">
                                            <span class="material-symbols-outlined">coronavirus</span>
                                        </div>
                                        <div>
                                            <p class="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">Sector 4G</p>
                                            <h4 class="font-label-bold text-on-surface mt-0.5">Early Blight</h4>
                                        </div>
                                    </div>
                                    <span class="bg-tertiary-fixed-dim text-tertiary px-2 py-0.5 rounded text-[10px] font-label-bold">Medium Risk</span>
                                </div>
                                <p class="text-caption text-on-surface-variant mt-3">AI Confidence: <span class="font-bold text-primary">94%</span></p>
                                <p class="text-caption text-on-surface-variant mt-1">Action recommended within 48h</p>
                            </div>
                        </div>
                        <button onclick="window.location.hash='crop-doctor'" class="w-full mt-4 py-2 bg-primary-container text-on-primary font-label-bold hover:opacity-90 transition-colors rounded-lg flex items-center justify-center gap-2">
                            <span class="material-symbols-outlined text-sm">analytics</span>
                            Open Crop Doctor
                        </button>
                    </div>

                    <!-- Ads / Sponsored Content -->
                    <div class="bg-surface-container-low rounded-xl p-lg border border-outline-variant/50 relative overflow-hidden group cursor-pointer">
                        <div class="absolute top-2 right-2 text-[10px] uppercase text-outline bg-white px-2 py-1 rounded shadow-sm">Ad</div>
                        <h4 class="font-headline-md text-primary mb-2">Upgrade Your Tractor</h4>
                        <p class="font-body-md text-on-surface-variant mb-4">Discover the new John Deere 8R Series with advanced autonomous capabilities.</p>
                        <img src="https://images.unsplash.com/photo-1592982537447-6f296d0bb43c?auto=format&fit=crop&q=80&w=800" alt="Tractor Ad" class="w-full h-32 object-cover rounded-lg group-hover:scale-105 transition-transform duration-300">
                    </div>
                </div>
            </div>
        </div>
    \`
};
`;

const routerLogic = `
document.addEventListener('DOMContentLoaded', () => {
    const appRoot = document.getElementById('app-root');
    const sidebar = document.getElementById('app-sidebar');
    const header = document.getElementById('app-header');
    const mainContainer = document.getElementById('main-container');
    const navLinks = document.querySelectorAll('.nav-link');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileOverlay = document.getElementById('mobile-overlay');

    function toggleMobileMenu(forceClose = false) {
        if (!sidebar || !mobileOverlay) return;
        
        const isClosed = sidebar.classList.contains('-translate-x-full');
        if (forceClose || !isClosed) {
            sidebar.classList.add('-translate-x-full');
            mobileOverlay.classList.add('opacity-0', 'pointer-events-none');
        } else {
            sidebar.classList.remove('-translate-x-full');
            mobileOverlay.classList.remove('opacity-0', 'pointer-events-none');
        }
    }

    if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', () => toggleMobileMenu());
    if (mobileOverlay) mobileOverlay.addEventListener('click', () => toggleMobileMenu(true));

    function render() {
        const hash = window.location.hash.substring(1) || 'login';
        
        if (views[hash]) {
            appRoot.innerHTML = views[hash];
        } else {
            appRoot.innerHTML = '<div class="p-8 text-center text-error font-headline-md">404 - Page Not Found</div>';
        }

        if (hash === 'login') {
            sidebar.classList.add('hidden-layout');
            header.classList.add('hidden-layout');
            mainContainer.classList.add('main-expanded');
            mainContainer.classList.remove('min-h-screen');
        } else {
            sidebar.classList.remove('hidden-layout');
            header.classList.remove('hidden-layout');
            mainContainer.classList.remove('main-expanded');
            mainContainer.classList.add('min-h-screen');
            window.scrollTo(0, 0);
        }

        navLinks.forEach(link => {
            const linkRoute = link.getAttribute('data-route');
            if (linkRoute === hash) {
                link.classList.add('bg-[#2D5A27]/5', 'text-[#2D5A27]', 'border-r-4', 'border-[#2D5A27]', 'font-bold');
                link.classList.remove('text-zinc-500');
            } else {
                link.classList.remove('bg-[#2D5A27]/5', 'text-[#2D5A27]', 'border-r-4', 'border-[#2D5A27]', 'font-bold');
                link.classList.add('text-zinc-500');
            }
        });
        
        // Close menu on navigation
        toggleMobileMenu(true);
        
        setupInternalLinks();
    }

    function setupInternalLinks() {
        const loginBtn = document.querySelector('button:has(span.text-on-primary-fixed)');
        if (loginBtn && (window.location.hash === '' || window.location.hash === '#login')) {
            loginBtn.addEventListener('click', (e) => {
                e.preventDefault();
                window.location.hash = 'dashboard';
            });
        }
    }

    window.addEventListener('hashchange', render);
    
    render();
});
`;

fs.writeFileSync(path.join(__dirname, 'app.js'), appJsContent + routerLogic);
console.log('Successfully built app.js');
