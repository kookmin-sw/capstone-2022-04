import 'dart:async';
import 'package:beacon_broadcast/beacon_broadcast.dart';
import 'package:beacon_simulator/Model/FireStore.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

class BeaconScreen extends StatefulWidget {
  final Map<dynamic, dynamic> data;

  const BeaconScreen({required this.data});
  @override
  _BeaconScreenState createState() => _BeaconScreenState();
}

class _BeaconScreenState extends State<BeaconScreen> {
  late String uuid;
  static const int majorId = 0;
  static const int minorId = 0;
  static const int transmissionPower = -59;
  static const String identifier = 'com.example.beacon-simulator';
  static const AdvertiseMode advertiseMode = AdvertiseMode.lowLatency;
  static const String layout = BeaconBroadcast.ALTBEACON_LAYOUT;
  static const int manufacturerId = 0x0118;

  BeaconBroadcast beaconBroadcast = BeaconBroadcast();

  late BeaconStatus _isTransmissionSupported;
  bool _isAdvertising = false;
  late StreamSubscription<bool> _isAdvertisingSubscription;
  int idx = 0;

  late FireStore fireStore;

  @override
  void initState() {
    super.initState();

    fireStore = new FireStore();

    beaconBroadcast
        .checkTransmissionSupported()
        .then((isTransmissionSupported) {
      setState(() {
        _isTransmissionSupported = isTransmissionSupported;
      });
    });

    _isAdvertisingSubscription =
        beaconBroadcast.getAdvertisingStateChange().listen((isAdvertising) {
      setState(() {
        _isAdvertising = isAdvertising;
      });
    });

    uuid = widget.data['uuid'];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('Beacon'),
          centerTitle: true,
        ),
        body: SingleChildScrollView(
          child: StreamBuilder(
              stream: FirebaseFirestore.instance
                  .collection('flag')
                  .doc('data')
                  .snapshots(),
              builder: (BuildContext context, AsyncSnapshot snapshot) {
                if (snapshot.hasData) {
                  if (snapshot.data['flag']) startNonPromise();
                }

                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      SizedBox(
                        width: MediaQuery.of(context).size.width * 1,
                        height: MediaQuery.of(context).size.height * 0.03,
                      ),
                      Text(
                        'UUID',
                        style: TextStyle(
                          fontFamily: 'NotoSans-Regular',
                          fontSize: 28,
                          color: Colors.black87,
                        ),
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.02,
                      ),
                      Container(
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(15),
                            color: Colors.grey[300]),
                        child: Padding(
                          padding: const EdgeInsets.all(10.0),
                          child: Text(
                            '$uuid',
                            style:
                                TextStyle(color: Colors.black87, fontSize: 17),
                          ),
                        ),
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.04,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          Column(
                            children: [
                              Text(
                                'Major',
                                style: TextStyle(
                                  fontFamily: 'NotoSans-Regular',
                                  fontSize: 28,
                                  color: Colors.black87,
                                ),
                              ),
                              SizedBox(
                                height:
                                    MediaQuery.of(context).size.height * 0.02,
                              ),
                              Text(
                                '$majorId',
                                style: TextStyle(
                                  fontSize: 22,
                                  color: Colors.black87,
                                ),
                              )
                            ],
                          ),
                          Column(
                            children: [
                              Text(
                                'Minor',
                                style: TextStyle(
                                  fontFamily: 'NotoSans-Regular',
                                  fontSize: 28,
                                  color: Colors.black87,
                                ),
                              ),
                              SizedBox(
                                height:
                                    MediaQuery.of(context).size.height * 0.02,
                              ),
                              Text(
                                '$minorId',
                                style: TextStyle(
                                  fontSize: 22,
                                  color: Colors.black87,
                                ),
                              )
                            ],
                          ),
                        ],
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.04,
                      ),
                      Text(
                        'Beacon Status',
                        style: TextStyle(
                          fontFamily: 'NotoSans-Regular',
                          fontSize: 28,
                          color: Colors.black87,
                        ),
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.02,
                      ),
                      Text(
                        _isAdvertising ? 'ON' : 'OFF',
                        style: TextStyle(
                          fontSize: 22,
                          color: Colors.black87,
                        ),
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.06,
                      ),
                      Container(
                        width: MediaQuery.of(context).size.width * 0.5,
                        height: MediaQuery.of(context).size.height * 0.06,
                        decoration: BoxDecoration(
                          color: Colors.blueAccent,
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: MaterialButton(
                          onPressed: () {
                            beaconBroadcast
                                .setUUID(uuid)
                                .setMajorId(majorId)
                                .setMinorId(minorId)
                                .setTransmissionPower(transmissionPower)
                                .setAdvertiseMode(advertiseMode)
                                .setIdentifier(identifier)
                                .setLayout(
                                    'm:2-3=0215,i:4-19,i:20-21,i:22-23,p:24-24')
                                .setManufacturerId(manufacturerId)
                                .start();
                          },
                          child: Text('START',
                              style:
                                  TextStyle(color: Colors.white, fontSize: 16)),
                        ),
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.02,
                      ),
                      Container(
                        width: MediaQuery.of(context).size.width * 0.5,
                        height: MediaQuery.of(context).size.height * 0.06,
                        decoration: BoxDecoration(
                          color: Colors.blueAccent,
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: MaterialButton(
                          onPressed: () {
                            beaconBroadcast.stop();
                          },
                          child: Text('STOP',
                              style:
                                  TextStyle(color: Colors.white, fontSize: 16)),
                        ),
                      ),
                    ],
                  ),
                );
              }),
        ));
  }

  startNonPromise() async {
    await fireStore.setFlag();

    for (int i = 0; i < 2; i++) {
      if (i == 1) {
        _isAdvertising = !_isAdvertising;
        print('change: ' + _isAdvertising.toString());

        beaconBroadcast.stop();
      }

      await Future.delayed(
          Duration(microseconds: widget.data['data'][idx] * 1000000));

      idx += 1;

      if (i == 1) {
        _isAdvertising = !_isAdvertising;
        print('change: ' + _isAdvertising.toString());

        beaconBroadcast
            .setUUID(uuid)
            .setMajorId(majorId)
            .setMinorId(minorId)
            .setTransmissionPower(transmissionPower)
            .setAdvertiseMode(advertiseMode)
            .setIdentifier(identifier)
            .setLayout('m:2-3=0215,i:4-19,i:20-21,i:22-23,p:24-24')
            .setManufacturerId(manufacturerId)
            .start();
      }
    }
  }
}
