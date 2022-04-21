import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';

class FireMassage {
  BuildContext context;
  FirebaseMessaging fireMessage = FirebaseMessaging.instance;
  FireMassage(this.context);

  getToken() async {
    String? token = await fireMessage.getToken();
    print(token);
  }
}
