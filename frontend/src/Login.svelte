<script>
    let currentUser = "";

    var YOUR_CLIENT_ID =
        "184710267585-lmu0vjd0rkaa6sqqc6eq86vcit3nev0i.apps.googleusercontent.com";
    var YOUR_REDIRECT_URI = "http://localhost:8080";
    var fragmentString = location.hash.substring(1);

    // Parse query string to see if page request is coming from OAuth 2.0 server.
    var params = {};
    var regex = /([^&=]+)=([^&]*)/g,
        m;
    while ((m = regex.exec(fragmentString))) {
        params[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
    }
    if (Object.keys(params).length > 0) {
        localStorage.setItem("oauth2-test-params", JSON.stringify(params));
        document.cookie = "access_token=" + params["access_token"] + ";path=/";
        history.replaceState(null, null, " "); // Clear URI
        trySampleRequest();
    }

    // If there's an access token, try an API request.
    // Otherwise, start OAuth 2.0 flow.
    function trySampleRequest() {
        var params = JSON.parse(localStorage.getItem("oauth2-test-params"));
        if (params && params["access_token"]) {
            var xhr = new XMLHttpRequest();
            xhr.open(
                "GET",
                "https://www.googleapis.com/userinfo/v2/me?" +
                    "access_token=" +
                    params["access_token"],
            );
            xhr.onreadystatechange = function (e) {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const user = JSON.parse(xhr.response);
                    currentUser = user.email
                } else if (xhr.readyState === 4 && xhr.status === 401) {
                    // Token invalid, so prompt for user permission.
                    oauth2SignIn();
                }
            };
            xhr.send(null);
        } else {
            oauth2SignIn();
        }
    }

    /*
     * Create form to request access token from Google's OAuth 2.0 server.
     */
    function oauth2SignIn() {
        // Google's OAuth 2.0 endpoint for requesting an access token
        var oauth2Endpoint = "https://accounts.google.com/o/oauth2/v2/auth";

        // Create element to open OAuth 2.0 endpoint in new window.
        var form = document.createElement("form");
        form.setAttribute("method", "GET"); // Send as a GET request.
        form.setAttribute("action", oauth2Endpoint);

        // Parameters to pass to OAuth 2.0 endpoint.
        var params = {
            client_id: YOUR_CLIENT_ID,
            redirect_uri: YOUR_REDIRECT_URI,
            scope: "https://www.googleapis.com/auth/userinfo.email",
            // state: "try_sample_request",
            include_granted_scopes: "true",
            response_type: "token",
            prompt: "select_account",
        };

        // Add form parameters as hidden input values.
        for (var p in params) {
            var input = document.createElement("input");
            input.setAttribute("type", "hidden");
            input.setAttribute("name", p);
            input.setAttribute("value", params[p]);
            form.appendChild(input);
        }

        // Add form to page and submit it to open the OAuth 2.0 endpoint.
        document.body.appendChild(form);
        form.submit();
    }
    function logOut() {
        localStorage.removeItem("oauth2-test-params");
        currentUser = "";
    }

    $: if (!currentUser) trySampleRequest();
</script>

<main>
    {#if currentUser}
        <div class="login">{ currentUser }</div>
    {:else}
        <div class="login" on:click={oauth2SignIn}>Login</div>
    {/if}
</main>

<style>
    .login {
        position: absolute;
        top: 0;
        right: 0;
        margin: 10px;
        font-family: sans-serif;
        font-size: 20px;
        font-weight: bold;
        padding: 20px;
        cursor: pointer;
    }
    .login:hover {
        text-decoration: underline;
    }
</style>
