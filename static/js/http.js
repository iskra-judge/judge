(function (scope) {
    const httpRequest = (url, method, body, headers = {}) => {
        return fetch(url, {
            method,
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
                ...headers,
            },
            body: body && JSON.stringify(body),
        })
            .then(response => response.json());
    };

    scope.http = {
        get: (url, headers = {}) => httpRequest(url, 'get', null, headers),
        post: (url, body, headers = {}) => httpRequest(url, 'post', body, headers),
    }
}(window));