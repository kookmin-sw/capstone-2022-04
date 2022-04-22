import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

class CheckScreen extends StatefulWidget {
  const CheckScreen({Key? key}) : super(key: key);

  @override
  _CheckScreenState createState() => _CheckScreenState();
}

class _CheckScreenState extends State<CheckScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Alarm'),
          centerTitle: true,
        ),
        body: StreamBuilder(
          stream: FirebaseFirestore.instance.collection('spoofing').snapshots(),
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            if (!snapshot.hasData || snapshot.data.docs.isEmpty) {
              return Column(
                children: [
                  SizedBox(
                    width: MediaQuery.of(context).size.width * 1,
                    height: MediaQuery.of(context).size.height * 0.04,
                  ),
                  Text('No Data')
                ],
              );
            } else {
              List<Widget> Item = snapshot.data.docs
                  .map((item) => ItemBox(item))
                  .toList()
                  .cast<Widget>();

              return ListView(padding: EdgeInsets.all(8), children: Item);
            }
          },
        ));
  }

  Container ItemBox(item) {
    return Container(
      child: Column(
        children: [
          SizedBox(height: 10),
          TextBox('Time', item['time'].toDate().toString()),
          SizedBox(height: 5),
          TextBox('UUID', item['uuid']),
          SizedBox(height: 5),
          TextBox('MacAddr', item['mac']),
          SizedBox(height: 5),
          Row(
            children: [
              TextBox('Major', item['major'].toString()),
              SizedBox(width: MediaQuery.of(context).size.width * 0.1),
              TextBox('Minor', item['minor'].toString())
            ],
          ),
          SizedBox(height: 5),
          TextBox('RSSI', item['rssi'].toString()),
          SizedBox(height: 10),
          Container(
            width: MediaQuery.of(context).size.width * 1,
            height: 2,
            color: Colors.blueAccent,
          )
        ],
      ),
    );
  }

  Row TextBox(String title, String content) {
    return Row(
      children: [
        Text(
          title + ':',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        SizedBox(width: 10),
        Text(
          content,
          style: TextStyle(
            fontSize: 16,
          ),
        )
      ],
    );
  }
}
