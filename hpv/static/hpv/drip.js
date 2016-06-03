var $dripRate = $('#dripRate');
var $startDrip = $('#startDrip');
var $stopDrip = $('#stopDrip');
var $hook = $('#truckHook');
var $div = $('<div id="lastTruck">');
var dripInterval = setInterval(console.log('You gonna start this puppy?'), 100000000)

function getDripRate() {
    if ($dripRate.val() < 5){
        return 5000;
    } else if ($dripRate.val() == "") {
        return 5000;
    } else {
        return ($dripRate.val() * 1000)
    }
}

$startDrip.click(function() {
    data = {'dripRate': getDripRate()};

    dripInterval = setInterval(function () {
        $.get('', data);
        console.log('DRIP!');
    }, getDripRate());

    return false;
});

$stopDrip.click(function() {
    clearInterval(dripInterval);
    console.log('Drip plugged')
});
