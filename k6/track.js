import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 1000 }, // Ramp up to x users in 30 seconds
        { duration: '3m', target: 1000 }, // Stay at x users for 3 minutes
        { duration: '30s', target: 0 },   // Ramp down to 0 users in 30 seconds
    ],
    thresholds: {
        http_req_duration: ["p(99) < 5000"],
    },
};

// URLs list
const urls = [
    "https://test-k6-1.fr/tracking-test-v2",
    "https://test-k6-2.fr/tracking-test-v2",
    "https://test-k6-3.fr/tracking-test-v2"
];

export default function () {
    let url = 'http://polymetrie-service.orch-team-a.pns-projects.fr.eu.org/track';

    let randomIndex = Math.floor(Math.random() * urls.length);
    let randomUrl = urls[randomIndex];

    let payload = {
        tracker: { 
            WINDOW_LOCATION_HREF: randomUrl, 
            USER_AGENT: "Mozilla/5.0", 
            PLATFORM: "Windows 11 Pro x64", 
            TIMEZONE: "UTC+01:00" 
        } 
    }

    let headers = { 'Content-Type': 'application/json' };

    let response = http.post(url, JSON.stringify(payload), { headers: headers });
    
    check(response, {
        'Track successful': (r) => r.status === 200,
    });

    sleep(1); // Sleep 1 second
}