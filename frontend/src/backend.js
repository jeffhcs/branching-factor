const serverAddress = "http://127.0.0.1:5000"

export class EndpointCaller {
    constructor(endpoint) {
        this.xhr = new XMLHttpRequest();
        this.endpoint = serverAddress + "/" + endpoint;
        this.xhr.withCredentials = true;
        this.onProgress = null;
        this.onDone = null;
    }

    abort() {
        this.xhr.abort();
    }

    call(queryStrings) {
        this.xhr.abort();
        this.xhr = new XMLHttpRequest();
        this.xhr.open("GET", this.endpoint + this.stringifyQueryStrings(queryStrings), true);

        if (this.onProgress) {
            this.xhr.onprogress = () => {
                this.onProgress(this.xhr.responseText);
            };
        }

        if (this.onDone) {
            this.xhr.onreadystatechange = () => {
                if (this.xhr.readyState === XMLHttpRequest.DONE) {
                    if (this.xhr.status === 200) {
                        this.onDone(this.xhr.responseText);
                    } else {
                        console.error("There was a problem with the request.");
                    }
                }
            }
        }

        this.xhr.send();
    }

    stringifyQueryStrings(queryStringsObject) {
        if (queryStringsObject == null) {
            return "";
        }
        let queryStrings = "?";
        for (let key in queryStringsObject) {
            queryStrings += key + "=" + encodeURIComponent(queryStringsObject[key]) + "&";
        }
        return queryStrings;
    }


}