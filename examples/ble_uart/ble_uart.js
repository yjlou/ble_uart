var service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'.toLowerCase();
var tx_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'.toLowerCase();
var rx_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'.toLowerCase();
var uart_service = null;

function send_line() {
  var local_input = document.getElementById('local_input');
  var chars = [];
  for (var i = 0; i < local_input.value.length; ++i){
    chars.push(local_input.value.charCodeAt(i));
  }
  chars.push(13);  // CR (Carriage Return)
  // chars.push(10);  // LF (Line Feed)

  if (uart_service) {
    disable_send_btn();
    uart_service.getCharacteristic(tx_uuid)
    .then(characteristic => {
        return characteristic.writeValue(new Uint8Array(chars));
    })
    .then(_ => {
      console.log('Sent: ' + local_input.value);
      local_input.value = '';
      enable_send_btn();
    })
    .catch(error => { console.error(error); on_disconnected(); });
  }
}

function handleCharacteristicValueChanged(event) {
  // TODO: handle the terminal control code.
  var remote_output = document.getElementById('remote_output');
  var value = event.target.value;
  var a = [];
  for (var i = 0; i < value.byteLength; i++) {
    a.push(String.fromCharCode(value.getUint8(i)));
  }
  remote_output.value += a.join('');
  remote_output.scrollTop = remote_output.scrollHeight;
}

function ble_scan() {
  var options = {
      optionalServices: [service_uuid],
      acceptAllDevices: true
  };
  var logs = document.getElementById('logs');

  if (!navigator.bluetooth) {
    log('navigator.bluetooth is undefined!');
    var remote_output = document.getElementById('remote_output');
    disable_scan_btn();
    remote_output.value = "
      The browser doesn't support Bluetooth feature (navigator.bluetooth).
      If you are using Chrome, try to enable
      <a href='chrome://flags/#enable-experimental-web-platform-features' target='_blank'>
        this flag
      </a>.
    ";
    return;
  }

  log('------------------------------');
  log('Requesting Bluetooth Device...');
  navigator.bluetooth.requestDevice(options)
  .then(device => {
    log(`Connecting [${device.name}] ...`)
    device.addEventListener('gattserverdisconnected', on_disconnected);
    return device.gatt.connect();
  })
  .then(server => server.getPrimaryService(service_uuid))
  .then(service => {
    log('Connected.');
    uart_service = service;
    return service.getCharacteristic(rx_uuid);
  })
  .then(characteristic => characteristic.startNotifications())
  .then(characteristic => {
    characteristic.addEventListener('characteristicvaluechanged',
                                    handleCharacteristicValueChanged);
    log('Notifications have been started.');
    var remote_output = document.getElementById('remote_output');
    remote_output.value = '';
    enable_send_btn();
  })
  .catch(error => {
    log('Argh! ' + error);
    on_disconnected();
  });
}

function on_disconnected(event) {
  if (event) {
    var device_name = event.target.name;
  } else {
    var device_name = '';
  }
  log(`Device [${device_name}] is disconnected.`);
  disable_send_btn();
}

function disable_scan_btn() {
  var scan_btn = document.getElementById('scan_btn');
  scan_btn.disabled = true;
}

function disable_send_btn() {
  var send_line_btn = document.getElementById('send_line_btn');
  send_line_btn.disabled = true;
}

function enable_send_btn() {
  var send_line_btn = document.getElementById('send_line_btn');
  send_line_btn.disabled = false;
}

function log(msg) {
  var logs = document.getElementById('logs');
  logs.insertAdjacentHTML('beforeend', msg + '\n');
}
