console.log("Helo")

if (!sessionStorage.getItem('siteConnection'))
{
    const socket = new WebSocket('ws://' + window.location.host + '/ws/auctions/');

    sessionStorage.setItem('siteConnection', socket);
    console.log("First connect")

}
else
{
    const socket = sessionStorage.getItem('siteConnection')
    console.log("Repeating connect")
}

console.log(socket)

socket.onmessage = function (e) {
    console.log('data: ' + e.data);
    const data = JSON.parse(e.data)
    const price = data.bidPrice;
    const time = data.timeLeft;

    console.log(price);
    console.log(time);
};
