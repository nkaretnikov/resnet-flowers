function appendResponse(form, text, success) {
    const responseId = "response";

    // Remove previous responses if they exist.
    var response = document.getElementById(responseId);
    if (response) {
        // Find the right form.
        response.parentElement.removeChild(response);
    }

    // Append a response to the current form.
    var response = document.createElement("div");
    response.id = responseId;

    // Requires Bootstrap.
    response.setAttribute("role", "alert");
    if (success && !text.startsWith("{{ error_prefix }}")) {
        response.setAttribute("class", "alert alert-primary alert-dismissible fade show");
    } else {
        response.setAttribute("class", "alert alert-danger alert-dismissible fade show");
    }

    var button = document.createElement("button");
    button.type = "button";
    button.setAttribute("class", "close");
    button.setAttribute("data-dismiss", "alert");
    response.appendChild(button);

    var closeText = document.createTextNode("\xD7");  // times symbol
    button.appendChild(closeText);

    var responseText = document.createTextNode(text);
    response.appendChild(responseText);
    form.appendChild(response);
}

// Perform a request without redirection and update the page.
function uploadImage(form) {
    var request = new XMLHttpRequest();

    request.open(form.method, form.action, true);

    request.onload = function() {  // success
        appendResponse(form, request.responseText, true);
    };

    request.onerror = function() {  // failure
        appendResponse(form, "{{ error_prefix }} failed to get image", false);
    };

    request.send(new FormData(form));

    return false;
}
