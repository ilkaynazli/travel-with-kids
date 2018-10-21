function postData(url='', data={}) {
            console.log('this is postData: ' + JSON.stringify(data));
            return fetch(url, {
                method: 'POST',
                headers: {
                "Content-Type": "application/json; charset=utf-8",
                },
                body: JSON.stringify(data)               
            })
            .then((response) => response.json());
        }