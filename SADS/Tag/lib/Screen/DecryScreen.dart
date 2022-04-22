import 'dart:convert';

import 'package:beacon_simulator/Model/ElGamal.dart';
import 'package:beacon_simulator/Screen/BeaconScreen.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:http/http.dart' as http;

class DecryScreen extends StatefulWidget {
  const DecryScreen({Key? key}) : super(key: key);

  @override
  _DecryScreenState createState() => _DecryScreenState();
}

class _DecryScreenState extends State<DecryScreen> {
  TextEditingController _key = TextEditingController();
  Map<dynamic, dynamic> beaconData = Map();

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection('encry').snapshots(),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (!snapshot.hasData || snapshot.data.docs.isEmpty) {
          return Column(
            children: [
              SizedBox(
                width: MediaQuery.of(context).size.width * 1,
                height: MediaQuery.of(context).size.height * 0.04,
              ),
              Text(
                'Encryption value does not exist',
                style: TextStyle(fontSize: 22, color: Colors.black87),
              ),
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.02,
              ),
              Text(
                'Please run the server and encrypt the data...',
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.1,
              ),
              Container(
                height: MediaQuery.of(context).size.height * 0.1,
                width: MediaQuery.of(context).size.height * 0.1,
                child: CircularProgressIndicator(),
              ),
            ],
          );
        } else {
          var en = snapshot.data.docs[0].data();
          beaconData['uuid'] = en['uuid'];
          return Column(
            children: [
              SizedBox(
                width: MediaQuery.of(context).size.width * 1,
                height: MediaQuery.of(context).size.height * 0.04,
              ),
              Text(
                'Encrypted Value',
                style: TextStyle(
                  fontFamily: 'NotoSans-Regular',
                  fontSize: 28,
                  color: Colors.black87,
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
                        'y1',
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
                        en['y1'].toString(),
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
                        'y2',
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
                        en['y2'].toString(),
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
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Text(
                'Set your private key',
                style: TextStyle(color: Colors.black87, fontSize: 20),
              ),
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.03,
              ),
              Container(
                width: MediaQuery.of(context).size.width * 0.35,
                child: TextFormField(
                  controller: _key,
                  validator: (value) {
                    if (value!.isEmpty) {
                      return '입력해주세요..';
                    } else {
                      return null;
                    }
                  },
                  keyboardType: TextInputType.number,
                  textAlign: TextAlign.center,
                  decoration: InputDecoration(
                    contentPadding:
                        EdgeInsets.symmetric(vertical: 0, horizontal: 10),
                    enabledBorder: OutlineInputBorder(
                      borderSide:
                          BorderSide(color: Color.fromRGBO(224, 224, 224, 1)),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    border: OutlineInputBorder(
                      borderSide:
                          BorderSide(color: Color.fromRGBO(224, 224, 224, 1)),
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                ),
              ),
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Container(
                width: MediaQuery.of(context).size.width * 0.5,
                height: MediaQuery.of(context).size.height * 0.06,
                decoration: BoxDecoration(
                  color: Colors.blueAccent,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: MaterialButton(
                  onPressed: () async {
                    var e = ElGamal(32653, 1, 0, 32978);
                    List en2 = [en['y1'], en['y2']];

                    beaconData['decry'] = e.decrypt(en2, int.parse(_key.text));
                    print(beaconData['decry'][0].toString());

                    Uri url = Uri.parse(
                        'https://asia-northeast3-beacon-330502.cloudfunctions.net/createRandList?seed=' +
                            beaconData['decry'][0].toString());

                    http.Response response = await http.get(url);
                    try {
                      if (response.statusCode == 200) {
                        String data = response.body;
                        var decodedData = jsonDecode(data);
                        beaconData['data'] = decodedData['data'];
                        print(decodedData);
                        Get.to(BeaconScreen(data: beaconData));
                      }
                    } catch (e) {
                      print(e);
                    }
                  },
                  child: Text('Create Beacon',
                      style: TextStyle(color: Colors.white, fontSize: 16)),
                ),
              ),
            ],
          );
        }
      },
    );
  }
}
