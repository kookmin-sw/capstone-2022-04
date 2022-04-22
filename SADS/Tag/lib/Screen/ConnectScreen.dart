import 'package:beacon_simulator/Model/ElGamal.dart';
import 'package:beacon_simulator/Model/FirebaseMassage.dart';
import 'package:beacon_simulator/Screen/CheckScreen.dart';
import 'package:beacon_simulator/Screen/DecryScreen.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class ConnectScreen extends StatefulWidget {
  const ConnectScreen({Key? key}) : super(key: key);

  @override
  _ConnectScreenState createState() => _ConnectScreenState();
}

class _ConnectScreenState extends State<ConnectScreen> {
  late FireMassage fm;
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    fm = FireMassage(context);
    fm.getToken();

    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage event) async {
      String? title = event.notification!.title;
      String? body = event.notification!.body;

      if (body == "5") {
        await createPubKey();
        Get.back();
      }
    });

    FirebaseMessaging.onMessage.listen((RemoteMessage event) async {
      String? title = event.notification!.title;
      String? body = event.notification!.body;

      showDialog(
        context: context,
        builder: (BuildContext context) {
          return new AlertDialog(
            content: new Text(title! + ' ' + body!),
            actions: <Widget>[
              new FlatButton(
                child: new Text(
                  '확인',
                  style: TextStyle(
                    color: Color.fromRGBO(0, 110, 119, 1),
                  ),
                ),
                onPressed: () {
                  Navigator.of(context).pop(true);
                },
              )
            ],
          );
        },
      );

      if (body == "5") {
        await createPubKey();
        Get.back();
      }
    });
  }

  createPubKey() async {
    var e = ElGamal(32653, 1, 0, 32978);
    e.keygen();

    await showDialog(
      context: context,
      builder: (BuildContext context) {
        return new AlertDialog(
          content: Text("Create Private Key: ${e.a}"),
          actions: <Widget>[
            new FlatButton(
              child: new Text(
                '확인',
                style: TextStyle(
                  color: Color.fromRGBO(0, 110, 119, 1),
                ),
              ),
              onPressed: () {
                Navigator.of(context).pop(true);
              },
            )
          ],
        );
      },
    );

    await FirebaseFirestore.instance
        .collection('public')
        .doc('data')
        .set({'g': e.g, 'h': e.h});

    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: Text('Beacon'),
        centerTitle: true,
        actions: [
          IconButton(
              onPressed: () => Get.to(CheckScreen()),
              icon: Icon(Icons.notifications))
        ],
      ),
      body: StreamBuilder(
        stream: FirebaseFirestore.instance.collection('public').snapshots(),
        builder: (BuildContext context, AsyncSnapshot snapshot) {
          if (!snapshot.hasData || snapshot.data.docs.isEmpty) {
            return Column(
              children: [
                SizedBox(
                  width: MediaQuery.of(context).size.width * 1,
                  height: MediaQuery.of(context).size.height * 0.04,
                ),
                Text(
                  'Public Key does not exist',
                  style: TextStyle(fontSize: 22, color: Colors.black87),
                ),
                SizedBox(
                  height: MediaQuery.of(context).size.height * 0.02,
                ),
                Text(
                  'Press the button below to set the public key.',
                  style: TextStyle(fontSize: 18, color: Colors.black87),
                ),
                SizedBox(
                  height: MediaQuery.of(context).size.height * 0.04,
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
                      await createPubKey();
                    },
                    child: Text('Click',
                        style: TextStyle(color: Colors.white, fontSize: 16)),
                  ),
                ),
              ],
            );
          } else {
            return DecryScreen();
          }
        },
      ),
    );
  }
}
