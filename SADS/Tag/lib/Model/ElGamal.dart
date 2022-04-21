import 'dart:math';
import 'package:beacon_simulator/Model/ECC.dart';
import 'package:beacon_simulator/Model/UseData.dart';

class ElGamal {
  late int numpoints;
  late ECC e;
  late UseData useData;
  late int a;
  late List g;
  late var h;

  ElGamal(int p, int a, int b, int numpoints) {
    this.numpoints = numpoints;
    this.e = ECC(p, a, b);
    this.useData = UseData();
  }

  List<dynamic> randomBase() {
    return this.useData.data[Random().nextInt(this.numpoints) + 0];
  }

  int createPrivateKey() {
    a = Random().nextInt(this.numpoints) + 0;
    return a;
  }

  multiply(x, y) {
    return e.addPoints(x, y);
  }

  exponentiate(x, n) {
    if (n > 0) {
      var temp = e.inversePoint(x);
      return e.multiplumOfPoint(temp, n);
    }
  }

  void keygen() {
    List<dynamic> base = randomBase();
    this.a = createPrivateKey();
    this.g = base;
    this.h = e.multiplumOfPoint(base, this.a);
  }

  decrypt(c, pk) {
    return multiply(c[1], exponentiate(c[0], pk));
  }
}
