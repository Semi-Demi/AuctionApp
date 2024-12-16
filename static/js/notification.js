console.log("Hello")


    const mySocket = new WebSocket('ws://' + window.location.host + '/ws/auctions/');

    mySocket.onmessage = function (e) {
        const data = JSON.parse(e.data)
        console.log(data)
        window.alert(data.message_sent)
    };

    mySocket.onclose = function (e) {
        console.error("Closed unexpectedly")
    };


    document.querySelector('#form-submit').onclick = function (e) {
        const user = "test"
        const message = user.value + " clicked button";
        mySocket.send(JSON.stringify({
            'message': message
        }));
    };