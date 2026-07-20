const CACHE_NAME = "workout-tracker-v1";

const APP_SHELL = [
    "/",
    "/main",
    "/graphs",
    "/scores",
    "/settings",

    "/static/style.css",
    "/static/app.js"
];


self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)
            .then(cache => {

                return cache.addAll(APP_SHELL);

            })

    );

    self.skipWaiting();

});


self.addEventListener("activate", event => {

    event.waitUntil(

        Promise.all([

            clients.claim(),

            caches.keys().then(keys => {

                return Promise.all(

                    keys.map(key => {

                        if (key !== CACHE_NAME) {
                            return caches.delete(key);
                        }

                    })

                );

            })

        ])

    );

});

self.addEventListener("fetch", event => {

    const url = new URL(event.request.url);


    // Never cache APIs or auth actions
    if (
        url.pathname.startsWith("/api/") ||
        url.pathname === "/logout" ||
        url.pathname === "/register" ||
        url.pathname === "/"
    ) {
        return;
    }


    // Pages: try server first
    if (event.request.mode === "navigate") {

        event.respondWith(

            fetch(event.request)
                .catch(() => caches.match(event.request))

        );

        return;
    }


    // Static files: cache first
    event.respondWith(

        caches.match(event.request)
            .then(cached => {

                return cached || fetch(event.request);

            })

    );

});