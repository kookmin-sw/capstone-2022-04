import 'package:flutter/material.dart';

SnackBar withAlertBar(String text) {
  return SnackBar(
    backgroundColor: Colors.red[400],
    duration: Duration(seconds: 3),
    content: Text(text),
    action: SnackBarAction(
      label: "Done",
      textColor: Colors.white,
      onPressed: () {},
    ),
  );
}

SnackBar withCirclerBar(String text) {
  return SnackBar(
    duration: Duration(seconds: 1),
    content: Row(
      children: <Widget>[CircularProgressIndicator(), Text(text)],
    ),
  );
}

SnackBar withShowMessage(String text) {
  return SnackBar(
    duration: Duration(seconds: 3),
    content: Text(text),
    action: SnackBarAction(
      label: "Done",
      onPressed: () {},
    ),
  );
}
