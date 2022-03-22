//
//  Nordic Uart Service
//
var service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'.toLowerCase();
var tx_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'.toLowerCase();
var rx_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'.toLowerCase();

class Nus {
  constructor(on_connected, on_rx, on_disconnected) {
    this.on_connected = on_connected;
    this.on_rx = on_rx;
    this.on_disconnected = on_disconnected;

    this.device =null;
    this.uart_service = null;
  }

  // The tramperline to convert the 'self' into 'this' context.
  // This function is called from the Bluetooth stack context while GATT is disconnected.
  _disconnected(self) {
    self.on_disconnected();
  }

  log(msg) {
    console.log(msg);
  }

  // Public function for client to send data to the server.
  //
  // Args:
  //   data: Uint8Array (or other array-like types).
  //
  send_data(data) {
    if (this.uart_service) {
      this.uart_service.getCharacteristic(tx_uuid)
      .then(characteristic => {
          return characteristic.writeValue(new Uint8Array(data));
      })
      .then(_ => {
        this.log('Sent: ' + data);
      })
      .catch(error => {
        this.log('send_data() error: ' + error);
      });
    } else {
      this.log('Ignored sending data because UART is not connected.');
    }
  }

  // The context when this function is called, it is in BluetoothRemoteGATTCharacteristic().
  handleCharacteristicValueChanged(self, event) {
    var value = event.target.value;
    value = String.fromCharCode.apply(null, new Uint8Array(value.buffer));
    self.log(`handleCharacteristicValueChanged(${value})`);
    self.on_rx(value);
  }

  scan() {
    var options = {
        optionalServices: [service_uuid],
        acceptAllDevices: true
    };

    this.log('------------------------------');
    this.log('Requesting Bluetooth Device...');
    navigator.bluetooth.requestDevice(options)
    .then(device => {
      this.log(`Connecting [${device.name}] ...`)
      this.device = device;
      device.addEventListener('gattserverdisconnected', make_func(this._disconnected, this));
      return device.gatt.connect();
    })
    .then(server => {
      this.log(`Connected server: [${server}].`);
      return server.getPrimaryService(service_uuid);
    })
    .then(service => {
      this.log(`Connected service: [${service}].`);
      this.uart_service = service;
      return service.getCharacteristic(rx_uuid);
    })
    .then(characteristic => {
      characteristic.addEventListener('characteristicvaluechanged',
          make_func(this.handleCharacteristicValueChanged, this));
      this.log('Added event listener.');
      return characteristic;
    })
    .then(characteristic => {
      characteristic.startNotifications();
      this.log('Notifications have been started.');
      this.on_connected();
    })
    .catch(error => {
      this.log('Argh! ' + error);
      this._disconnected(this);
    });
  }

  disconnect() {
    if (this.device) {
      this.device.gatt.disconnect();
    }
  }
}
