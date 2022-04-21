import 'package:cloud_firestore/cloud_firestore.dart';

class FireStore {
  FirebaseFirestore firestore = FirebaseFirestore.instance;

  setFlag() async {
    await firestore.collection('flag').doc('data').update({
      'flag': false,
    });
  }
}
