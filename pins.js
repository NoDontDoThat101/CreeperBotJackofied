for (var pins = [], i = 100000; i < 1000000; ++i) a[i] = i;


function shuffle(array) {
    var tmp, current, top = array.length;
    if (top)
        while (--top) {
            current = Math.floor(Math.random() * (top + 1));
            tmp = array[current];
            array[current] = array[top];
            array[top] = tmp;
        }
    return array;
}

pins = shuffle(pins);
var pin = pins[Math.floor(Math.random() * pins.length)];