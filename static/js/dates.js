// Convert all dates into local timezone
document.addEventListener("DOMContentLoaded", function() {
    console.log("[dates.js] Converting dates to local timezone");

    const dateElements = document.querySelectorAll('time');
    dateElements.forEach(function(timeElement) {
        console.log("[dates.js] Found time element:", timeElement);
        const utcDate = new Date(timeElement.getAttribute('datetime'));
            const now = new Date();
            const diffMs = utcDate - now;
            let diffText = "";
            if (diffMs > 0) {
                const diffSec = Math.floor(diffMs / 1000);
                const diffMin = Math.floor(diffSec / 60);
                const diffHr = Math.floor(diffMin / 60);
                const diffDay = Math.floor(diffHr / 24);
                if (diffDay > 0) {
                    diffText = `in ${diffDay} day${diffDay !== 1 ? 's' : ''}`;
                } else if (diffHr > 0) {
                    diffText = `in ${diffHr} hour${diffHr !== 1 ? 's' : ''}`;
                } else if (diffMin > 0) {
                    diffText = `in ${diffMin} minute${diffMin !== 1 ? 's' : ''}`;
                } else {
                    diffText = `in ${diffSec} second${diffSec !== 1 ? 's' : ''}`;
                }
            } else {
                const diffSec = Math.floor(-diffMs / 1000);
                const diffMin = Math.floor(diffSec / 60);
                const diffHr = Math.floor(diffMin / 60);
                const diffDay = Math.floor(diffHr / 24);
                if (diffDay > 0) {
                    diffText = `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`;
                } else if (diffHr > 0) {
                    diffText = `${diffHr} hour${diffHr !== 1 ? 's' : ''} ago`;
                } else if (diffMin > 0) {
                    diffText = `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`;
                } else {
                    diffText = `${diffSec} second${diffSec !== 1 ? 's' : ''} ago`;
                }
            }
            timeElement.textContent = diffText + ` (on ${utcDate.toDateString()})`;
            console.log("[dates.js] Converted date:", timeElement.textContent);
    });
    console.log("[dates.js] Date conversion complete");
});