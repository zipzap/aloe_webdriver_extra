/* Miscellaneous functions. */

/*
    Update the value of a specific <p> element.

    @param value: String. Value to display.
 */
function result(value) {
    document.getElementById('result').innerHTML = value;
}

function reset() {
    document.getElementById('result').innerHTML = 'No results yet.';
}

function onReady(){
    reset();
    setTimeout(function () {
        var delayed_link = '<a href="javascript:result(\'delayed_link\')"> Delayed Link </a>'
        document.getElementById('wait_for').innerHTML = delayed_link;
    }, 5000);
}

/**
 * Delete and re-create a HTML element.
 */
function recreateElement(elementId) {
    var elem = document.getElementById(elementId);
    var parent = elem.parentNode;

    // Delete the element.
    parent.removeChild(elem);

    // Create the element again.
    parent.appendChild(elem);
}

/**
 * Delete and re-create a HTML element.
 *
 * This help to trigger StaleElementReferenceException.
 */
function makeElementStale(elementId, timeout, start_callback, end_callback) {
    if (!timeout) {
        timeout = 500;
    }

    setTimeout(function () {
        // Call start callback function if any was given.
        if (start_callback) {
            start_callback();
        }

        recreateElement(elementId);

        // Call end callback function if any was given.
        if (end_callback) {
            end_callback();
        }
    }, timeout);
}
