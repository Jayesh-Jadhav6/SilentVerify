console.log("script loaded");

const startTime = Date.now(); // When user lands on page


// Track mouse movement (position + timestamp)
let mouseMoves = []; // To store mouse movements
document.addEventListener("mousemove", function (e) {
    mouseMoves.push({
        x: e.clientX,
        y: e.clientY,
        t: Date.now() // capture time of movement
    });
});

let clicks = []; // To store click events
document.addEventListener("click", function(e) {
    clicks.push({
        x: e.clientX,
        y: e.clientY,
        t: Date.now()
    });
});

let scrolls = []; // To store scroll events
document.addEventListener("scroll", function () {
    scrolls.push({
        scrollY: window.scrollY,
        t: Date.now()
    });
});



// When user closes or refreshes page
window.addEventListener("beforeunload", function () {
    const endTime = Date.now();
    const timeOnPage = (endTime - startTime) / 1000; // seconds

    const data = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        screenWidth: screen.width,
        screenHeight: screen.height,
        timeOnPage: timeOnPage,
        mouseMoves: mouseMoves,
        clicks: clicks,
        scrolls: scrolls
    };

    navigator.sendBeacon("/submit-data", JSON.stringify(data));
});
